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
    >>> dataservice = OASDataService(oas)
    >>> dataservice.identifier = "http://example.com/dataservices/1"
    >>> dataservice.endpointDescription = url
    >>> #
    >>> # Add dataservice to catalog:
    >>> catalog.services.append(dataservice)
    >>>
    >>> # get dcat representation in turtle (default)
    >>> dcat = catalog.to_rdf()
    >>> print(dcat.decode())
    >>> bool(dcat)
    True
"""
import logging
from typing import List

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
        logging.debug(specification)
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
            if "url" in specification["servers"][0]:
                self.endpointURL = specification["servers"][0]["url"]
        # license
        self._parse_license()
        # mediaType
        self._parse_media_type()
        # externalDocs
        self._parse_external_docs()

    def _parse_license(self) -> None:
        """Parses the license object."""
        if "license" in self.specification["info"]:
            if "url" in self.specification["info"]["license"]:
                self.license = self.specification["info"]["license"]["url"]

    def _parse_media_type(self) -> None:
        """Parses the media type objects."""
        self._media_types: List[str] = list()
        self._seek_media_types(self.specification, ["content"])
        # Need to remove duplicates:
        self.media_types = list(set(self._media_types))

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
                    logging.debug(k + ": " + str(key))
                    self._media_types.append(_url + str(key))
            if isinstance(v, dict):
                self._seek_media_types(v, key_list)

    def _parse_external_docs(self) -> None:
        """Parses the externalDocs objects."""
        if "externalDocs" in self.specification:
            if "url" in self.specification["externalDocs"]:
                self.landing_page.append(self.specification["externalDocs"]["url"])


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
