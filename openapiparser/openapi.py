import requests
import yaml


class Error(Exception):
    """Base class for exceptins in this module"""
    pass


class OpenAPI:
    """ A simple class representing an openAPI specification"""

    def __init__(self, url: str):
        resp = None
        try:
            resp = requests.get(url)
        except requests.exceptions.ConnectionError:
            raise Error("ConnectionError")
        spec = yaml.safe_load(resp.text)
        if spec is None:
            raise Error("Spec is not yaml")
