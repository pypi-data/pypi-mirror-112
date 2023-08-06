class StudyGovernorError(Exception):
    pass


class StudyGovernorValueError(StudyGovernorError):
    pass


class StudyGovernorResponseError(StudyGovernorError):
    def __init__(self, uri, status_code, acceptable_status_codes):
        self.uri = uri
        self.status_code = status_code
        self.acceptable_status_codes = acceptable_status_codes

    def __str__(self):
        return 'Invalid response from StudyClient for url {}, got status {}, expected status {}'.format(
            self.uri,
            self.status_code,
            self.acceptable_status_codes,
        )


class StudyGovernorNotFoundError(StudyGovernorResponseError):
    def __init__(self, cls, uri, status_code, acceptable_status_codes):
        super().__init__(uri, status_code, acceptable_status_codes)
        self.cls = cls

    def __str__(self):
        return f'Could not find {self.cls.__name__} using {self.uri}, encountered {self.status_code} status code!'


class StudyGovernorConnectionError(StudyGovernorError):
    pass


class StudyGovernorNoAuthError(StudyGovernorConnectionError):
    def __init__(self, payload, message):
        super(StudyGovernorNoAuthError, self).__init__(message)
        self.payload = payload


class StudyGovernorSSLError(StudyGovernorConnectionError):
    pass


class SubjectExistsError(StudyGovernorValueError):
    pass


class ExperimentExistsError(StudyGovernorValueError):
    pass

