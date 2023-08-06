import hashlib
import logging
import time
from typing import Optional, Union
from .connection import StudyClient, Experiment, Subject, State, Workflow, Action, Transition, ExternalSystem
from . import exceptions

__version__ = '0.4.0'
__all__ = ['StudyClient', 'Experiment', 'Subject', 'State', 'Workflow', 'Action', 'Transition', 'ExternalSystem', 'connect']


def connect(uri: str,
            user: Optional[str]=None,
            password: Optional[str]=None,
            logger: Optional[logging.Logger]=None,
            loglevel: Optional[Union[str, int]]=None,
            debug: bool=False,
            user_agent_prefix: Optional[str]=None) -> StudyClient:
    # Generate a hash for the connection
    hasher = hashlib.md5()
    hasher.update(uri.encode('utf-8'))
    hasher.update(str(time.time()).encode('utf-8'))
    connection_id = hasher.hexdigest()

    # Setup the logger for this connection
    if logger is None:
        logger = logging.getLogger(f'task-client-{connection_id}')
        handler = logging.StreamHandler()
        handler.setLevel(logging.DEBUG)
        logger.addHandler(handler)

        # create formatter
        if debug:
            formatter = logging.Formatter('[%(asctime)s] %(levelname)s: %(module)s:%(lineno)d >> %(message)s')
        else:
            formatter = logging.Formatter('[%(levelname)s] %(message)s')
        handler.setFormatter(formatter)

        if loglevel is not None:
            logger.setLevel(loglevel)
        elif debug:
            logger.setLevel('DEBUG')
        else:
            logger.setLevel('WARNING')

    client = StudyClient(uri, user=user, password=password, logger=logger,
                         user_agent_prefix=user_agent_prefix, debug=debug)
    return client
