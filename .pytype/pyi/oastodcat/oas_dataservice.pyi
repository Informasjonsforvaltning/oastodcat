# (generated with --quick)

from typing import Any, Dict

DataService: Any

class Error(Exception):
    __doc__: str

class NotValidOASError(Error):
    __doc__: str
    message: str
    def __init__(self, message: str) -> None: ...

class OASDataService(Any):
    __doc__: str
    title: Dict[str, Any]
    def __init__(self, specification: dict) -> None: ...
