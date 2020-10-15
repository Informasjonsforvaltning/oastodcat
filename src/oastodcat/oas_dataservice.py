"""oas_dataservice module for mapping a openapi-specification to dcat rdf.

This module contains methods for mapping an openAPI specification to rdf
dcat:DataService according to the
`dcat-ap-no v.2 standard <https://doc.difi.no/review/dcat-ap-no/#klasse-dataset>`__

Example:
    >>> import yaml
    >>> import requests
    >>> from datacatalogtordf import Catalog
    >>> from oastodcat import OASDataService
    >>>
    >>> # Create catalog object
    >>> catalog = Catalog()
    >>> catalog.identifier = "http://example.com/catalogs/1"
    >>> catalog.title = {"en": "A dataset catalog"}
    >>> catalog.publisher = "https://example.com/publishers/1"
    >>>
    >>> # Create a dataservice based on an openAPI-specification:
    >>> url = ("https://raw.githubusercontent.com/"
    >>>        "OAI/OpenAPI-Specification/master/examples/v3.0/petstore.yaml"
    >>>       )
    >>> oas = yaml.safe_load(requests.get(url).text)
    >>> identifier = "http://example.com/dataservices/{uuid}"
    >>> oas_spec = OASDataService(url, oas, identifier)
    >>> #
    >>> # Add dataservices to catalog:
    >>> for dataservice in oas_spec.dataservices:
    >>>    catalog.services.append(dataservice)
    >>>
    >>> # get dcat representation in turtle (default)
    >>> dcat = catalog.to_rdf()
    >>> print(dcat.decode())
    >>> bool(dcat)
    True
"""
from typing import List, Optional
import uuid

from concepttordf import Contact
from datacatalogtordf import DataService, URI


class OASDataService:
    """A simple class representing an openAPI specification.

    Attributes:
    specification (dict): an openAPI spec as a dict
    dataservices (List[DataService]): a list of dataservices created
    endpointdescription (str): The url of the openAPI specification
    identifier (str): the identifier template, should contain {uuid}
    """

    __slots__ = (
        "specification",
        "dataservices",
        "_identifier",
        "endpointdescription",
        "_media_types",
        "_dataservice",
    )

    # Types:
    specification: dict
    dataservices: List[DataService]
    _identifier: str
    endpointdescription: URI
    _media_types: List[str]

    def __init__(self, url: str, specification: dict, identifier: str) -> None:
        """Inits an object with default values and parses the specification.

        Args:
            url (str): the url of the openAPI specification
            specification (dict): an openAPI specification as a dict
            identifier (str): the identifier template, containing {uuid}

        Raises:
            NotSupportedOASError: We do not support this version of the specification
            NotValidOASError: The specification is not valid
            RequiredFieldMissingError: a required property is missing
        """
        super().__init__()
        if not (specification):
            raise NotValidOASError("Empty specification object")

        if not specification["openapi"].startswith("3.0."):
            raise NotSupportedOASError(
                f'Version {specification["openapi"]}" is not supported'
            )
        if len(identifier) == 0:
            raise RequiredFieldMissingError("Empty indentification attribute")

        self.endpointdescription = URI(url)
        self.specification = specification
        self.identifier = identifier
        self.dataservices = []
        self._media_types = []

        # endpointURL
        if "servers" in specification:
            for server in specification["servers"]:
                if "url" in server:
                    self._create_dataservice(url=server["url"])
        else:
            self._create_dataservice()

    @property
    def identifier(self) -> str:
        """Get/set for identifier."""
        return self._identifier

    @identifier.setter
    def identifier(self, identifier: str) -> None:
        self._identifier = identifier

    # --
    def _create_dataservice(self, url: Optional[str] = None) -> None:
        self._dataservice = DataService()
        # We may be given an identifier "template" ending with {uuid}.
        # We create the uuid and complete the identifer:
        self._dataservice.identifier = URI(
            self.identifier.format(uuid=self._create_uuid())
        )

        if url:
            self._dataservice.endpointURL = url
        self._dataservice.endpointDescription = self.endpointdescription

        self._parse_specification()
        self.dataservices.append(self._dataservice)

    def _parse_specification(self) -> None:
        # title
        self._parse_title()
        # description
        self._parse_description()
        # contactpoint
        self._parse_contacpoint()
        # license
        self._parse_license()
        # mediaType
        self._parse_media_type()
        # externalDocs
        self._parse_external_docs()

    def _parse_title(self) -> None:
        """Parses the title object."""
        if "title" in self.specification["info"]:
            # Assuming English
            # title
            self._dataservice.title = {"en": self.specification["info"]["title"]}

    def _parse_description(self) -> None:
        """Parses the description object."""
        if "description" in self.specification["info"]:
            self._dataservice.description = {
                "en": self.specification["info"]["description"]
            }

    def _parse_contacpoint(self) -> None:
        """Parses the contact object."""
        if "contact" in self.specification["info"]:
            contact = Contact()
            if "name" in self.specification["info"]["contact"]:
                contact.name = {"en": self.specification["info"]["contact"]["name"]}
            if "email" in self.specification["info"]["contact"]:
                contact.email = self.specification["info"]["contact"]["email"]
            if "url" in self.specification["info"]["contact"]:
                contact.url = self.specification["info"]["contact"]["url"]
            self._dataservice.contactpoint = contact

    def _parse_license(self) -> None:
        """Parses the license object."""
        if "license" in self.specification["info"]:
            if "url" in self.specification["info"]["license"]:
                self._dataservice.license = self.specification["info"]["license"]["url"]

    def _parse_media_type(self) -> None:
        """Parses the media type objects."""
        self._seek_media_types(self.specification, ["content"])
        # Need to remove duplicates:
        self._dataservice.media_types = list(set(self._media_types))

    def _parse_external_docs(self) -> None:
        """Parses the externalDocs objects."""
        if "externalDocs" in self.specification:
            if "url" in self.specification["externalDocs"]:
                self._dataservice.landing_page.append(
                    self.specification["externalDocs"]["url"]
                )

    # --
    def _create_uuid(self) -> str:
        return str(uuid.uuid4())

    def _seek_media_types(self, d: dict, key_list: List[str]) -> None:
        """Helper method.

        Seeks for keys matching any of keys in key_list.
        Adds matching keys to self._media_types.

        Args:
            d (dict): the dict in which to searc
            key_list (List[str]): list of keys to search for
        """
        _url = "https://www.iana.org/assignments/media-types/"
        for k, v in d.items():
            if k in key_list:
                for key in v.keys():
                    self._media_types.append(_url + str(key))
            if isinstance(v, dict):
                self._seek_media_types(v, key_list)


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
    """We do not support this version of the specification.

    Attributes:
        message -- explanation of the error
    """

    def __init__(self, message: str) -> None:
        """Inits an object with default values."""
        self.message = message


class RequiredFieldMissingError(Error):
    """A required filed is missing.

    Attributes:
        message -- explanation of the error
    """

    def __init__(self, message: str) -> None:
        """Inits an object with default values."""
        self.message = message
