import requests
import yaml


class OpenAPI:
    """ A simple class representing an openAPI specification"""

    def __init__(self, url: str):
        resp = None
        try:
            resp = requests.get(url)
        except requests.exceptions.ConnectionError:
            raise Error("ConnectionError")
        if not resp:
            raise RequestError(resp.status_code)
        spec = yaml.safe_load(resp.text)
        if spec is None:
            raise Error("Spec is not yaml")
        self._version = spec['openapi']

    @property
    def version(self):
        return self._version


class Error(Exception):
    """Base class for exceptins in this module"""
    pass


class RequestError(Error):
    """The url is not found on server

    Attributes:
        message -- explanation of the error
    """

    def __init__(self, message):
        self.message = message
