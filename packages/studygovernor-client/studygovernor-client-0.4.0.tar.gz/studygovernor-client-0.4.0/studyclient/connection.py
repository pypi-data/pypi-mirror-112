from __future__ import absolute_import
from __future__ import unicode_literals

import os
import netrc
import platform
import requests
from urllib import parse

from typing import List, Mapping, Optional, Tuple, Type, TypeVar, Union, Dict

from .core import StudyClientBaseObject, Experiment, Subject, State, Workflow, Action, Transition, ExternalSystem
from .drivers import DRIVERS
from .exceptions import StudyGovernorValueError
from .exceptions import StudyGovernorNoAuthError
from .exceptions import StudyGovernorResponseError
from .exceptions import StudyGovernorNotFoundError
from .exceptions import StudyGovernorSSLError
from .exceptions import StudyGovernorConnectionError
from .exceptions import SubjectExistsError
from .exceptions import ExperimentExistsError


JSONType = Union[str, int, float, bool, None, Mapping[str, 'JSON'], List['JSON']]


class StudyClient(object):
    CACHE_NAMES = {
        Experiment: '__experiments__',
        Subject: '__subjects__',
        State: '__states__',
        Workflow: '__workflows__',
        Action: '__actions__',
        Transition: '__transitions__',
        ExternalSystem: '__external_systems__'
    }

    def __init__(self, server, user=None, password=None, session=None, logger=None,
                 user_agent=None, user_agent_prefix=None, debug=False, application_name=None):
        self._server = parse.urlparse(server)
        self.original_uri = server.rstrip()
        self._url_prefix = self.original_uri
        self._version_prefix = None
        self.application_name = application_name

        # Pre-set some variables
        self.api_version = None
        self.driver = None

        # Caching settings
        self._cache = {}
        self.clearcache()
        self.caching = True

        self.logger = logger

        # Requests session
        if session:
            self.interface = session
        else:
            self.interface = requests.Session()

        if user_agent is None:
            user_agent = "({platform}/{release}; python/{python}; requests/{requests})".format(
                platform=platform.system(),
                release=platform.release(),
                python=platform.python_version(),
                requests=requests.__version__
            )

            # Add user agent prefix if needed
            if not user_agent_prefix:
                user_agent_prefix = 'studygovernor-client'

            user_agent = "{user_agent_prefix} {user_agent}".format(
                user_agent_prefix=user_agent_prefix,
                user_agent=user_agent
            )

        # Set user agent and accept content type headers
        self.interface.headers.update({
            'User-Agent': user_agent,
            'Accept': 'application/json'
        })

        # Get auth
        if user is None and password is None:
            netrc_file = '~/_netrc' if os.name == 'nt' else '~/.netrc'
            netrc_file = os.path.abspath(os.path.expanduser(netrc_file))
            self.logger.info(f'Retrieving login info for {self._server.netloc}')
            try:
                user, _, password = netrc.netrc(netrc_file).authenticators(self._server.netloc)
            except IOError:
                self.logger.info(f'Could not load the netrc file ({netrc_file}), it does not exist!')
            except TypeError:
                self.logger.info(f'Could not retrieve login info for "{server}" from the .netrc file!')

        self.interface.auth = (user, password)

        # Set some connection properties
        self.debug = debug
        self.request_timeout = 20  # 10 seconds default
        self.accepted_status_get = [200]
        self.accepted_status_post = [200, 201]
        self.accepted_status_put = [200, 201]
        self.accepted_status_delete = [200]
        self.skip_response_check = False

        # Detect API version and load appropriate driver
        self.detect_api_version()

        # Check whether login was successful
        self._test_login()

        try:
            response = self.get('/workflows', accepted_status=[200, 401], timeout=2)
        except Exception as exception:
            self.logger.error(f'Error in test workflows request {self.original_uri}: {exception}')
            raise

        self.logger.info(f'Response code on test workflows request: {response.status_code}')
        if response.status_code == 401:
            payload = response.headers['www-authenticate'].split("=")[1].strip("\"")
            raise StudyGovernorNoAuthError(payload, f'Could not authenticate for {self.original_uri}')

    def __del__(self):
        self.disconnect()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.disconnect()

    def disconnect(self):
        """
        Placeholder in case we ever need cleanup later
        """
        pass

    def _test_login(self):
        try:
            response = self.get('/subjects', accepted_status=[200, 401, 404], timeout=2)
        except Exception as exception:
            message = f'Cannot create connection to {self.original_uri}'
            if self.debug:
                message = '{}: {}'.format(message, exception)
            self.logger.error(message)
            raise StudyGovernorConnectionError(message)

        self.logger.info(f'Response code on initial try: {response.status_code}')
        if response.status_code == 401:
            payload = response.headers['www-authenticate'].split("=")[1].strip("\"")
            raise StudyGovernorNoAuthError(payload, f'Could not authenticate for {self.original_uri}')

        if b'<div class="login-form">' in response.content:
            payload = response.headers['www-authenticate'].split("=")[1].strip("\"")
            raise StudyGovernorNoAuthError(payload, f'Could not authenticate for {self.original_uri}')

    def detect_api_version(self):
        # Detect API version
        try:
            response = self.get('/-/versions', accepted_status=[200, 401, 404], timeout=2)
        except Exception as exception:
            message = f'Cannot create connection to {self.original_uri}'
            if self.debug:
                message = '{}: {}'.format(message, exception)
            self.logger.error(message)
            raise StudyGovernorConnectionError(message)

        self.logger.info(f'Response code on initial try: {response.status_code}')
        if response.status_code == 401:
            payload = response.headers['www-authenticate'].split("=")[1].strip("\"")
            raise StudyGovernorNoAuthError(payload, f'Could not authenticate for {self.original_uri}')

        if response.status_code == 200:
            versions = response.json().get('api_versions')
            if not versions:
                raise StudyGovernorValueError('Could not get version from /-/versions endpoint data, found {}'.format(
                    response.json())
                )

            api_version = max(float(x) for x in versions)
            version_uri = versions[str(api_version)]
            server_uri = response.url[:-11]
        else:
            response = self.get('/data')
            self.logger.info(f'Response code on secondary try: {response.status_code}')
            server_data = response.json()
            api_version = server_data.get('api_version', 0)
            if api_version == 2:
                api_version = 0.5
            version_uri = '/data'
            server_uri = response.url[:-5]

        self._url_prefix = server_uri

        if self._url_prefix != self.original_uri:
            self.logger.warning('Detected a redirect from {0} to {1}, using {1} from now on'.format(
                self.original_uri, self._url_prefix
            ))

        self.logger.info('Found StudyGovernor server with API version {} at {}{}'.format(
            api_version,
            self._url_prefix.rstrip('/'),
            version_uri
        ))

        # Change server uri to be inside the server path
        self._server = parse.urlparse(self._url_prefix.rstrip('/') + version_uri)
        self._version_prefix = version_uri
        self.api_version = api_version

        # Select API Driver
        self.driver = DRIVERS[self.api_version](self)

    def _format_uri(self,
                    path: str,
                    query: Optional[Mapping[str, str]]=None) -> str:
        if path[0] != '/':

            if self._url_prefix is not None and path.startswith(self._url_prefix):
                path = path[len(self._url_prefix):]  # Strip original uri

            if self.original_uri is not None and path.startswith(self.original_uri):
                path = path[len(self.original_uri):]  # Strip original uri

            if path[0] != '/':
                raise StudyGovernorValueError(f'The requested URI path should start with a /, found {path}')

        if self._version_prefix is not None and path.startswith(self._version_prefix):
            path = path[len(self._version_prefix.rstrip('/')):]  # Strip version prefix

        if query is None:
            query = {}

        # Sanitize unicode in query
        query = {k: v.encode('utf-8', 'xmlcharrefreplace') if isinstance(v, str) else v for k, v in query.items()}

        # Create the query string
        if len(query) > 0:
            query_string = parse.urlencode(query, doseq=True)
        else:
            query_string = ''

        data = (self._server.scheme,
                self._server.netloc,
                self._server.path.rstrip('/') + path,
                '',
                query_string,
                '')

        result = parse.urlunparse(data)

        # Make sure we work with strings
        if isinstance(result,  bytes):
            result = result.decode('utf-8')

        return result

    def url_for(self,
                obj: StudyClientBaseObject,
                query: Optional[Mapping[str, str]]=None,
                scheme: Optional[str]=None) -> str:
        """
        Return the (external) url for a given XNAT object
        :param XNATBaseObject obj: object to get url for
        :param query: extra query string parameters
        :return: external url for the object
        """
        return self._format_uri(obj.uri, query=query)

    def _check_response(self,
                        response: requests.Response,
                        accepted_status: Optional[List[int]]=None,
                        uri: Optional[str]=None):

        if self.debug:
            self.logger.debug(f'Received response with status code: {response.status_code}')

        if not self.skip_response_check:
            if accepted_status is None:
                accepted_status = [200, 201, 202, 203, 204, 205, 206]  # All successful responses of HTTP

            if response.status_code not in accepted_status:
                raise StudyGovernorResponseError(uri, response.status_code, accepted_status)

    def get(self,
            path: str,
            query: Optional[Mapping[str, str]]=None,
            accepted_status: Optional[List[int]]=None,
            timeout: Union[float, Tuple[float, float]]=None,
            headers: Optional[Mapping[str, str]]=None) -> requests.Response:
        """
        Retrieve the content of a given REST directory.

        :param str path: the path of the uri to retrieve (e.g. "/data/archive/projects")
                         the remained for the uri is constructed automatically
        :param dict query: the values to be added to the query string in the uri
        :param list accepted_status: a list of the valid values for the return code, default [200]
        :param timeout: timeout in seconds, float or (connection timeout, read timeout)
        :type timeout: float or tuple
        :param dict headers: the HTTP headers to include
        :returns: the requests response
        :rtype: requests.Response
        """
        accepted_status = accepted_status or self.accepted_status_get
        uri = self._format_uri(path, query=query)
        timeout = timeout or self.request_timeout

        self.logger.debug('GET URI {}'.format(uri))

        try:
            response = self.interface.get(uri, timeout=timeout, headers=headers)
        except requests.exceptions.SSLError:
            raise StudyGovernorSSLError('Encountered a problem with the SSL connection, are you sure the server is offering https?')
        except requests.ConnectionError:
            raise StudyGovernorConnectionError(f'Could not connect to server for {uri}')
        self._check_response(response, accepted_status=accepted_status, uri=uri)  # Allow OK, as we want to get data
        return response

    def get_json(self,
                 path: str,
                 query: Optional[Mapping[str, str]]=None,
                 accepted_status: Optional[List[int]]=None) -> JSONType:
        """
        Helper function that perform a GET, but sets the format to JSON and
        parses the result as JSON

        :param str path: the path of the uri to retrieve (e.g. "/data/archive/projects")
                         the remained for the uri is constructed automatically
        :param list accepted_status: a list of the valid values for the return code, default [200]
        :param dict query: the values to be added to the query string in the uri
        """
        response = self.get(path, query=query, accepted_status=accepted_status)
        return response.json()

    def head(self,
             path: str,
             accepted_status: Optional[List[int]]=None,
             allow_redirects: bool=False,
             timeout: Union[float, Tuple[float, float]]=None,
             headers: Optional[Mapping[str, str]]=None):
        """
        Retrieve the header for a http request of a given REST directory.

        :param str path: the path of the uri to retrieve (e.g. "/data/archive/projects")
                         the remained for the uri is constructed automatically
        :param list accepted_status: a list of the valid values for the return code, default [200]
        :param bool allow_redirects: allow you request to be redirected
        :param timeout: timeout in seconds, float or (connection timeout, read timeout)
        :type timeout: float or tuple
        :param dict headers: the HTTP headers to include
        :returns: the requests response
        :rtype: requests.Response
        """
        accepted_status = accepted_status or self.accepted_status_get
        uri = self._format_uri(path)
        timeout = timeout or self.request_timeout

        self.logger.debug('GET URI {}'.format(uri))

        try:
            response = self.interface.head(uri, allow_redirects=allow_redirects, timeout=timeout, headers=headers)
        except requests.exceptions.SSLError:
            raise StudyGovernorSSLError('Encountered a problem with the SSL connection, are you sure the server is offering https?')
        except requests.ConnectionError:
            raise StudyGovernorConnectionError(f'Could not connect to server for {uri}')
        self._check_response(response, accepted_status=accepted_status, uri=uri)  # Allow OK, as we want to get data
        return response

    def post(self,
             path: str,
             data=None,
             json=None,
             query: Optional[Mapping[str, str]]=None,
             accepted_status: Optional[List[int]]=None,
             timeout: Union[float, Tuple[float, float]]=None,
             headers: Optional[Mapping[str, str]]=None):
        """
        Post data to a given REST directory.

        :param str path: the path of the uri to retrieve (e.g. "/data/archive/projects")
                         the remained for the uri is constructed automatically
        :param data: Dictionary, bytes, or file-like object to send in the body of the :class:`Request`.
        :param json: json data to send in the body of the :class:`Request`.
        :param dict query: the values to be added to the query string in the uri
        :param list accepted_status: a list of the valid values for the return code, default [200, 201]
        :param timeout: timeout in seconds, float or (connection timeout, read timeout)
        :type timeout: float or tuple
        :param dict headers: the HTTP headers to include
        :returns: the requests response
        :rtype: requests.Response
        """
        accepted_status = accepted_status or self.accepted_status_post
        uri = self._format_uri(path, query=query)
        timeout = timeout or self.request_timeout

        self.logger.debug(f'POST URI {uri}')
        if self.debug:
            self.logger.debug(f'POST DATA {data}')

        try:
            response = self.interface.post(uri, data=data, json=json, timeout=timeout, headers=headers)
        except requests.exceptions.SSLError:
            raise StudyGovernorSSLError('Encountered a problem with the SSL connection, are you sure the server is offering https?')
        except requests.ConnectionError:
            raise StudyGovernorConnectionError(f'Could not connect to server for {uri}')
        self._check_response(response, accepted_status=accepted_status, uri=uri)
        return response

    def put(self,
            path: str,
            data=None,
            files=None,
            json=Mapping,
            query: Optional[Mapping[str, str]]=None,
            accepted_status: Optional[List[int]]=None,
            timeout: Union[float, Tuple[float, float]]=None,
            headers: Optional[Mapping[str, str]]=None):
        """
        Put the content of a given REST directory.

        :param str path: the path of the uri to retrieve (e.g. "/data/archive/projects")
                         the remained for the uri is constructed automatically
        :param data: Dictionary, bytes, or file-like object to send in the body of the :class:`Request`.
        :param json: json data to send in the body of the :class:`Request`.
        :param files: Dictionary of ``'name': file-like-objects`` (or ``{'name': file-tuple}``) for multipart encoding upload.
                      ``file-tuple`` can be a 2-tuple ``('filename', fileobj)``, 3-tuple ``('filename', fileobj, 'content_type')``
                      or a 4-tuple ``('filename', fileobj, 'content_type', custom_headers)``, where ``'content-type'`` is a string
                      defining the content type of the given file and ``custom_headers`` a dict-like object containing additional headers
                      to add for the file.
        :param dict query: the values to be added to the query string in the uri
        :param list accepted_status: a list of the valid values for the return code, default [200, 201]
        :param timeout: timeout in seconds, float or (connection timeout, read timeout)
        :type timeout: float or tuple
        :param dict headers: the HTTP headers to include
        :returns: the requests response
        :rtype: requests.Response
        """
        self.logger.info('PUT {} WITH JSON: {}'.format(path, json))
        accepted_status = accepted_status or self.accepted_status_put
        uri = self._format_uri(path, query=query)
        timeout = timeout or self.request_timeout

        self.logger.debug(f'PUT URI {uri}')
        if self.debug:
            self.logger.debug(f'PUT DATA {data}')
            self.logger.debug(f'PUT FILES {files}')

        try:
            self.logger.info(f'CALL REQUESTS.PUT {uri} WITH DATA: {data}  JSON: {json}')
            response = self.interface.put(uri, data=data, files=files, json=json, timeout=timeout, headers=headers)
        except requests.exceptions.SSLError:
            raise StudyGovernorSSLError('Encountered a problem with the SSL connection, are you sure the server is offering https?')
        except requests.ConnectionError:
            raise StudyGovernorConnectionError(f'Could not connect to server for {uri}')
        self._check_response(response, accepted_status=accepted_status, uri=uri)  # Allow created OK or Create status (OK if already exists)
        return response

    def delete(self,
               path: str,
               headers: Optional[Mapping[str, str]]=None,
               accepted_status: Optional[List[int]]=None,
               query: Optional[Mapping[str, str]]=None,
               timeout: Union[float, Tuple[float, float]]=None):
        """
        Delete the content of a given REST directory.

        :param str path: the path of the uri to retrieve (e.g. "/data/archive/projects")
                         the remained for the uri is constructed automatically
        :param dict headers: the HTTP headers to include
        :param dict query: the values to be added to the query string in the uri
        :param list accepted_status: a list of the valid values for the return code, default [200]
        :param timeout: timeout in seconds, float or (connection timeout, read timeout)
        :type timeout: float or tuple
        :returns: the requests response
        :rtype: requests.Response
        """
        accepted_status = accepted_status or self.accepted_status_delete
        uri = self._format_uri(path, query=query)
        timeout = timeout or self.request_timeout

        self.logger.debug(f'DELETE URI {uri}')
        if self.debug:
            self.logger.debug(f'DELETE HEADERS {headers}')

        try:
            response = self.interface.delete(uri, headers=headers, timeout=timeout)
        except requests.exceptions.SSLError:
            raise StudyGovernorSSLError('Encountered a problem with the SSL connection, are you sure the server is offering https?')
        except requests.ConnectionError:
            raise StudyGovernorConnectionError(f'Could not connect to server for {uri}')
        self._check_response(response, accepted_status=accepted_status, uri=uri)
        return response

    def clearcache(self):
        """
        Clear the cache of the listings in the Session object
        """
        self._cache.clear()
        self._cache = {x: {} for x in self.CACHE_NAMES.values()}

    # Define a type variable to get the create-object hinting correctly
    T = TypeVar('T')

    def create_object(self, cls: Type[T], data: Union[Mapping, str]) -> T:
        if isinstance(data, str):
            uri = data
            data = {}
        else:
            # TODO: hack due to inconsistency in study-governor, needs to be fixed
            data = dict(data)
            if 'uri' not in data and 'url' in data:
                data['uri'] = data.pop('url')

            uri = data['uri']

        type_name = self.CACHE_NAMES[cls]

        try:
            return self._cache[type_name][uri]
        except KeyError:
            task = cls(self, uri, data)
            self._cache[type_name][uri] = task
            return task

    def get_subject(self, label: str) -> Subject:
        try:
            data = self.get_json(f'/subjects/{label}')
        except StudyGovernorResponseError as exception:
            if exception.status_code == 404:
                raise StudyGovernorNotFoundError(
                    Subject,
                    exception.uri,
                    exception.status_code,
                    exception.acceptable_status_codes
                )
            else:
                raise

        return self.create_object(Subject, data)

    def get_subjects(self) -> List[Subject]:
        data = self.get_json('/subjects')
        return [self.create_object(Subject, x) for x in data['subjects']]

    def create_subject(self,
                       subject_label: str,
                       date_of_birth: Optional[str]=None,
                       external_ids: Optional[Mapping[str, str]]=None,
                       exist_ok: bool=False):
        try:
            # Check if subject exists and handle accordingly
            subject = self.get_subject(subject_label)

            if not exist_ok:
                raise SubjectExistsError(f'Cannot create subject {subject_label}, it already exists!')

            if date_of_birth:
                subject.date_of_birth = date_of_birth
        except StudyGovernorNotFoundError:
            # Could not find subject, safely create it
            subject = Subject(self, label=subject_label, date_of_birth=date_of_birth)

        if external_ids:
            for key, value in external_ids.items():
                subject.external_ids[key] = value

        return subject

    def get_experiment(self, label: str) -> Experiment:
        try:
            data = self.get_json(f'/experiments/{label}')
        except StudyGovernorResponseError as exception:
            if exception.status_code == 404:
                raise StudyGovernorNotFoundError(
                    Experiment,
                    exception.uri,
                    exception.status_code,
                    exception.acceptable_status_codes
                )
            else:
                raise

        return self.create_object(Experiment, data)

    def create_experiment(self,
                          subject: Union[Subject, str],
                          label: str,
                          scandate: Optional[str]=None,
                          workflow: Optional[Union[Workflow, str]]=None,
                          external_ids: Optional[Mapping[str, str]]=None,
                          exist_ok: bool=False):
        try:
            # Check if experiment exists and handle accordingly
            experiment = self.get_experiment(label)

            if not exist_ok:
                raise ExperimentExistsError(f'Cannot create experiment {label}, it already exists!')

        except StudyGovernorNotFoundError:
            # Could not find experiment, safely create it
            experiment = Experiment(self,
                                    label=label,
                                    subject=subject,
                                    scandate=scandate,
                                    workflow=workflow)

        if external_ids:
            for key, value in external_ids.items():
                experiment.external_ids[key] = value

        return experiment

    @property
    def external_systems(self) -> Dict[str, ExternalSystem]:
        data = self.get_json('/external_systems')
        data = [self.create_object(ExternalSystem, x) for x in data['external_systems']]
        return {x.system_name: x for x in data}
