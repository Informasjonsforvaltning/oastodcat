"""oas_dataservice module for mapping a openapi-specification to dcat rdf.

This module contains methods for mapping an openAPI specification to rdf
dcat:DataService according to the
`dcat-ap-no v.2 standard <https://doc.difi.no/review/dcat-ap-no/#klasse-dataset>`__

Example:
    >>> from oastodcat import OASDataService
    >>>
    >>> oas = json.loads(minimal_spec)
    >>> dataservice = OASDataService(oas)
    >>> dataservice.identifier = "http://example.com/dataservices/1"
    >>>
    >>> bool(dataservice.to_rdf())
    True
"""
from datacatalogtordf import DataService


class OASDataService(DataService):
    """A simple class representing an openAPI specification."""

    def __init__(self, specification: dict) -> None:
        """Inits an object with default values."""
        super().__init__()
        if not (specification):
            raise NotValidOASError("Empty specification object")
        # Assuming English
        self.title = {"en": specification["info"]["title"]}


class Error(Exception):
    """Base class for exceptins in this module."""

    pass


class NotValidOASError(Error):
    """The specification object is not valid.

    Attributes:
        message -- explanation of the error
    """

    def __init__(self, message: str) -> None:
        """Inits an object with default values."""
        self.message = message
