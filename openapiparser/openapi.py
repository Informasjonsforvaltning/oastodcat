import requests
import yaml


class OpenAPI:
    """A simple class representing an openAPI specification"""

    def __init__(self, url: str):
        resp = None
        try:
            resp = requests.get(url)
        except requests.exceptions.ConnectionError:
            raise RequestError("ConnectionError")
        if not resp:
            raise RequestError(resp.status_code)
        spec = yaml.safe_load(resp.text)
        if spec is None:
            raise NotValidYamlError("Spec is not valid yaml")
        if 'openapi' not in spec:
            raise RequiredFieldMissingError('openapi')
        self._version = spec['openapi']
        if 'info' not in spec:
            raise RequiredFieldMissingError('info')
        self._info = Info(spec['info'])

    @property
    def version(self):
        return self._version

    @property
    def info(self):
        return self._info


class Info:
    """A class representing the Info Object of the openAPI specification"""

    def __init__(self, info: dict):
        if 'title' not in info:
            raise RequiredFieldMissingError('title')
        self._title = info['title']
        if 'version' not in info:
            raise RequiredFieldMissingError('version')
        self._version = info['version']

    @property
    def title(self):
        return self._title

    @property
    def version(self):
        return self._version


class Error(Exception):
    """Base class for exceptins in this module"""
    pass


class NotValidYamlError(Error):
    """The url is not found on server

    Attributes:
        message -- explanation of the error
    """

    def __init__(self, message):
        self.message = message


class RequestError(Error):
    """The url is not found on server

    Attributes:
        message -- explanation of the error
    """

    def __init__(self, message):
        self.message = message


class RequiredFieldMissingError(Error):
    """The url is not found on server

    Attributes:
        message -- explanation of the error
    """

    def __init__(self, message):
        self.message = message
