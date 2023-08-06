import datetime
import isodate

from types import MappingProxyType
from typing import Mapping as MappingType
from typing import List, Optional, Union
from collections.abc import Mapping

import studyclient


def format_datetime(value: Union[str, datetime.datetime]) -> str:
    if isinstance(value, str):
        value = value.replace(' ', 'T')
        value = isodate.parse_datetime(value)

    if isinstance(value, datetime.datetime):
        return value.isoformat()
    else:
        raise ValueError('To create a proper string representation for a'
                         ' datetime, either a datetime.datetime or str has'
                         ' to be supplied!')


def format_date(value: Union[str, datetime.datetime, datetime.date]) -> str:
    if isinstance(value, str):
        value = isodate.parse_date(value)

    if isinstance(value, datetime.datetime):
        value = value.date()

    if isinstance(value, datetime.date):
        return value.isoformat()
    else:
        raise ValueError('To create a proper string representation for a'
                         ' datetime, either a datetime.datetime or str has'
                         ' to be supplied!')


class StudyClientBaseObject:
    def __init__(self, session: 'studyclient.StudyClient', uri: str, data: MappingType):
        self.uri = uri
        self.session = session
        self._data = dict(**data)  # Copy initial data in cache to avoid fetching when only summary is required
        self.caching = True

    def __repr__(self):
        return str(self)

    def __str__(self):
        return f'<{type(self).__name__} {self.uri}>'

    def external_uri(self, query: MappingType[str, str] = None) -> str:
        """
        Return the external url for this object, not just a REST path

        :param query: extra query string parameters
        :return: external url for this object
        """
        return self.session.url_for(self, query=query)

    @property
    def logger(self):
        return self.session.logger

    # Function for getting data in a lazy/cached way when possible
    def _update_data(self):
        object_data = self.session.get_json(self.uri)
        self._data = object_data

    def _get_data_field(self, name: str):
        if not self.caching or name not in self._data:
            self._update_data()

        return self._data[name]

    def _set_data_field(self, name: str, value):
        data = {
            name: value
        }

        self.session.put(self.uri, json=data)
        self.clearcache()

    def set_fields(self, **kwargs):
        """
        Set multiple fields in one go

        :param kwargs: keywords arguments are used as the fields to set
        """
        self.session.put(self.uri, json=kwargs)
        self.clearcache()

    # Some cache management methods
    def clearcache(self):
        self._data.clear()

    @property
    def caching(self):
        if self._caching is not None:
            return self._caching
        else:
            return self.session.caching

    @caching.setter
    def caching(self, value):
        self._caching = value

    @caching.deleter
    def caching(self):
        self._caching = None


class ExternalIdMap(Mapping):
    def __init__(self, parent: 'HasExternalIds'):
        self._parent = parent

    def __str__(self):
        return str(self._parent.raw_external_ids)

    def __repr__(self):
        return f'<ExternalIdMap {self}>'

    def __getitem__(self, item) -> str:
        return self._parent.raw_external_ids[item]

    def __setitem__(self, key: str, value: str):
        typename = type(self._parent).__name__.lower()

        data = {
            typename: self._parent.uri,
            'external_system': key,
            'external_id': value,
        }

        response = self._parent.session.post(f'/external_{typename}_links', json=data)
        self._parent.clearcache()

    def __iter__(self) -> str:
        for item in iter(self._parent.raw_external_ids):
            yield item

    def __len__(self) -> int:
        return len(self._parent.raw_external_ids)


class HasExternalIds(StudyClientBaseObject):
    @property
    def external_ids(self) -> ExternalIdMap:
        return ExternalIdMap(self)

    @property
    def raw_external_ids(self) -> MappingType[str, str]:
        return MappingProxyType(self._get_data_field('external_ids'))


class Subject(HasExternalIds):
    def __init__(self,
                 session,
                 uri: Optional[str]=None,
                 data: Optional[MappingType]=None,
                 label: Optional[str]=None,
                 date_of_birth: Optional[Union[str, datetime.date, datetime.datetime]]=None):
        if uri is not None:
            if data is None:
                data = {}

            super().__init__(session, uri=uri, data=data)
        else:
            if not label:
                raise ValueError("Cannot create a subject without a label")

            if date_of_birth:
                date_of_birth = format_date(date_of_birth)

            data = {
                "label": label,
                "date_of_birth": date_of_birth,
            }

            response = session.post('/subjects', json=data)
            data = response.json()

            uri = data.get('uri')
            super().__init__(session, uri=uri, data=data)

    def __str__(self) -> str:
        return f'<Subject {self.label}>'

    @property
    def id(self) -> int:
        return int(self.uri.rsplit('/', 1)[1])

    @property
    def label(self) -> str:
        return self._get_data_field('label')

    @label.setter
    def label(self, value: str):
        self._set_data_field('label', value)

    @property
    def date_of_birth(self) -> str:
        return self._get_data_field('date_of_birth')

    @date_of_birth.setter
    def date_of_birth(self, value: Union[str, datetime.date, datetime.datetime]):
        value = format_date(value)
        self._set_data_field('date_of_birth', value)

    @property
    def experiments(self) -> 'List[Experiment]':
        return [self.session.create_object(Experiment, x) for x in self._get_data_field('experiments')]


class Experiment(HasExternalIds):
    def __init__(self,
                 session,
                 uri: Optional[str]=None,
                 data: Optional[MappingType]=None,
                 label: Optional[str]=None,
                 subject: Union[str, Subject]=None,
                 scandate: Optional[Union[str, datetime.datetime]]=None,
                 workflow: Optional[Union[str, 'Workflow']]=None):
        if uri is not None:
            if data is None:
                data = {}

            super().__init__(session, uri=uri, data=data)
        else:
            if not subject:
                raise ValueError('Need to specify a subject to create an Experiment')

            if not label:
                raise ValueError('Need to specify a label to create an Experiment')

            if isinstance(subject, Subject):
                subject = subject.id

            if isinstance(workflow, Workflow):
                workflow = workflow.label

            if scandate:
                scandate = format_datetime(scandate)

            data = {
                "label": label,
                "subject": subject,
                "scandate": scandate,
                "workflow": workflow,
            }

            response = session.post('/experiments', json=data)
            data = response.json()

            uri = data['uri']
            super().__init__(session, uri=uri, data=data)

    def __str__(self) -> str:
        return f'<Experiment {self.label}>'

    @property
    def label(self) -> str:
        return self._get_data_field('label')

    @property
    def scandate(self) -> str:
        return self._get_data_field('scandate')

    @property
    def subject(self) -> Subject:
        return self.session.create_object(Subject, self._get_data_field('subject'))

    @property
    def actions(self) -> 'List[Action]':
        actions = self.session.get_json(f"{self.uri}/actions")['actions']
        return [self.session.create_object(Action, x) for x in actions]

    @property
    def state(self) -> 'State':
        data = self.session.get_json(self._get_data_field('state'))
        return self.session.create_object(State, data['state'])

    @state.setter
    def state(self, value: 'Union[str, State]'):
        self.set_state(value)

    def set_state(self,
                  value: 'Union[str, State]',
                  freetext: Optional[str]=None):
        if isinstance(value, State):
            value = value.label

        data = {
            'state': value
        }

        if freetext:
            data['freetext'] = freetext

        response = self.session.put(self._get_data_field('state'), json=data)

        result = response.json()

        if not result['success']:
            self.logger.warning(f'Server could not change state: {result["error"]}')


class State(StudyClientBaseObject):
    def __str__(self) -> str:
        return f'<State {self.label}>'

    @property
    def label(self) -> str:
        return self._get_data_field('label')

    @property
    def callback(self) -> str:
        return self._get_data_field('callback')

    @property
    def lifespan(self):
        return self._get_data_field('lifespan')

    @property
    def freetext(self) -> str:
        return self._get_data_field('freetext')

    @property
    def workflow(self) -> 'Workflow':
        return self.session.create_object(Workflow, self._get_data_field('workflow'))

    @property
    def experiments(self) -> List[Experiment]:
        data = self.session.get_json(self._get_data_field('experiments'))
        return [self.session.create_object(Experiment, x) for x in data['experiments']]


class Workflow(StudyClientBaseObject):
    def __str__(self) -> str:
        return f'<Workflow {self.label}>'

    @property
    def label(self) -> str:
        return self._get_data_field('label')

    @property
    def states(self) -> List[State]:
        data = self.session.get_json(f'{self.uri}/states')
        return [self.session.create_object(State, x) for x in data['states']]


class Transition(StudyClientBaseObject):
    def __str__(self) -> str:
        return f'<Transition {self.uri}>'

    @property
    def source_state(self) -> State:
        return self.session.create_object(State, self._get_data_field('source_state'))

    @property
    def destination_state(self) -> State:
        return self.session.create_object(State, self._get_data_field('destination_state'))

    @property
    def conditions(self):
        return self._get_data_field('conditions')


class Action(StudyClientBaseObject):
    def __str__(self) -> str:
        return f'<Action {self.uri}>'

    @property
    def experiment(self) -> Experiment:
        return self.session.create_object(Experiment, self._get_data_field('experiment'))

    @property
    def transition(self) -> Transition:
        return self.session.create_object(Transition, self._get_data_field('transition'))

    @property
    def success(self) -> bool:
        return self._get_data_field('success')

    @success.setter
    def success(self, value: bool):
        self._set_data_field('success', value)

    @property
    def return_value(self) -> str:
        return self._get_data_field('return_value')

    @return_value.setter
    def return_value(self, value: str):
        self._set_data_field('return_value', value)

    @property
    def freetext(self) -> str:
        return self._get_data_field('freetext')

    @property
    def start_time(self) -> str:
        return self._get_data_field('start_time')

    @property
    def end_time(self) -> str:
        return self._get_data_field('end_time')

    @end_time.setter
    def end_time(self, value: Union[str, datetime.datetime]):
        value = format_datetime(value)
        self._set_data_field('end_time', value)


class ExternalSystem(StudyClientBaseObject):
    @property
    def system_name(self) -> str:
        return self._get_data_field('system_name')

    @property
    def url(self) -> str:
        return self._get_data_field('url')

