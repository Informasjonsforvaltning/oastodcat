# (generated with --quick)

from typing import Any

DataService: Any

class Error(Exception):
    __doc__: str

class NotValidOASError(Error):
    __doc__: str
    message: Any
    def __init__(self, message) -> None: ...

class OASDataservice(Any):
    __doc__: str

class RequestError(Error):
    __doc__: str
    message: Any
    def __init__(self, message) -> None: ...

class RequiredFieldMissingError(Error):
    __doc__: str
    message: Any
    def __init__(self, message) -> None: ...
