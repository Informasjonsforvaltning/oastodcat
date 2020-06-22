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
from concepttordf import Contact
from datacatalogtordf import DataService


class OASDataService(DataService):
    """A simple class representing an openAPI specification."""

    __slots__ = "specification"

    # Types:
    specification: dict

    def __init__(self, specification: dict) -> None:
        """Inits an object with default values."""
        super().__init__()
        if not (specification):
            raise NotValidOASError("Empty specification object")

        if not specification["openapi"].startswith("3.0."):
            raise NotSupportedOASError(
                f'Version {specification["openapi"]}" is not supported'
            )
        self.specification = specification
        # Assuming English
        # title
        self.title = {"en": specification["info"]["title"]}
        # description
        if "description" in specification["info"]:
            self.description = {"en": specification["info"]["description"]}
        # contactPoint
        if "contact" in specification["info"]:
            contact = Contact()
            if "name" in specification["info"]["contact"]:
                contact.name = {"en": specification["info"]["contact"]["name"]}
            if "email" in specification["info"]["contact"]:
                contact.email = specification["info"]["contact"]["email"]
            if "url" in specification["info"]["contact"]:
                contact.url = specification["info"]["contact"]["url"]
            self.contactpoint = contact
        # endpointURL
        if "servers" in specification:
            if "url" in specification["servers"]:
                self.endpointURL = specification["servers"]["url"]
        # license
        self._parse_license()

    def _parse_license(self) -> None:
        if "license" in self.specification["info"]:
            if "url" in self.specification["info"]["license"]:
                self.license = self.specification["info"]["license"]["url"]


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


class NotSupportedOASError(Error):
    """The specification object is not valid.

    Attributes:
        message -- explanation of the error
    """

    def __init__(self, message: str) -> None:
        """Inits an object with default values."""
        self.message = message
