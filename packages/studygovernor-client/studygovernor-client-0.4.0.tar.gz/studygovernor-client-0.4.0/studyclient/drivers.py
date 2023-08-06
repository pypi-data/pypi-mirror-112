import weakref
from .exceptions import StudyGovernorError

__all__ = ['DRIVERS']


class BaseDriver(object):
    def __init__(self, parent):
        self.parent = weakref.ref(parent)

    @property
    def session(self):
        return self.parent()

    @property
    def logger(self):
        return self.parent().logger


class DriverV1(BaseDriver):
    pass


DRIVERS = {
    1: DriverV1,
}
