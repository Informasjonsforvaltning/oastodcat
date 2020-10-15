"""Test cases for the oas_dataservice module."""
from datacatalogtordf import Catalog
import pytest
from pytest_mock import MockFixture
from rdflib import Graph
from rdflib.compare import graph_diff, isomorphic
import yaml

from oastodcat import (
    NotSupportedOASError,
    NotValidOASError,
    OASDataService,
    RequiredFieldMissingError,
)


@pytest.fixture(scope="session")
def minimal_spec() -> str:
    """Helper for creating a minimal specification object."""
    _minimal_spec = """
                    openapi: 3.0.3
                    info:
                      title: Swagger Petstore
                      version: 1.0.0
                    paths: {}
                    """
    return _minimal_spec


@pytest.fixture(scope="session")
def spec_with_servers() -> str:
    """Helper for creating a minimal specification object."""
    _spec = """
            openapi: 3.0.3
            info:
              title: Swagger Petstore
              version: 1.0.0
            servers:
              - url: http://petstore.swagger.io/v1
            paths: {}
            """
    return _spec


@pytest.fixture(scope="session")
def spec_with_multiple_servers() -> str:
    """Helper for creating a minimal specification object."""
    _spec = """
            openapi: 3.0.3
            info:
              title: Swagger Petstore
              version: 1.0.0
            servers:
              - url: 'http://test.petstore.swagger.io/v1'
                description: test
              - url: 'http://petstore.swagger.io/v1'
                description: production
            paths: {}
            """
    return _spec


@pytest.fixture(scope="session")
def spec_with_media_types() -> str:
    """Helper for creating a specification object with a path item."""
    _spec = """
            openapi: "3.0.3"
            info:
              title: Swagger Petstore
              version: 1.0.0
            paths:
              /pets:
                get:
                  summary: List all pets
                  responses:
                    '200':
                      description: A paged array of pets
                      content:
                        application/xml:
                          schema:
                            $ref: "#/components/schemas/Pets"
                        application/json:
                          schema:
                            $ref: "#/components/schemas/Pets"
              /pets/{petId}:
                get:
                  parameters:
                    - name: petId
                      in: path
                      required: true
                      description: The id of the pet to retrieve
                      schema:
                        type: string
                  responses:
                    '200':
                      description: Expected response to a valid request
                      content:
                        application/json:
                          schema:
                            $ref: "#/components/schemas/Pet"
            components:
              schemas:
                Pet:
                  type: object
                  required:
                    - id
                    - name
                  properties:
                    id:
                      type: integer
                      format: int64
                    name:
                      type: string
                Pets:
                  type: array
                  items:
                    $ref: "#/components/schemas/Pet"
            """
    return _spec


@pytest.fixture(scope="session")
def spec_with_external_docs() -> str:
    """Helper for creating a specification object with externalDocs."""
    _spec = """
            openapi: 3.0.3
            info:
              title: Swagger Petstore
              version: 1.0.0
            paths: {}
            externalDocs:
              description: Find more info here
              url: https://example.com
            """
    return _spec


def test_parse_empty_spec_should_raise_error() -> None:
    """It raises a NotValidOASError."""
    with pytest.raises(NotValidOASError):
        specification = "{}"
        url = "http://example.com/specificatons/1"
        identifier = "http://example.com/identifiers/1"
        oas = yaml.safe_load(specification)
        OASDataService(url, oas, identifier)


def test_parse_other_than_v3_spec_should_raise_error() -> None:
    """It raises a NotValidOASError."""
    with pytest.raises(NotSupportedOASError):
        v2_spec = """
                    openapi: '2.0'
                    info:
                      title: Swagger Petstore
                      version: 1.0.0
                    paths: {}
                    """
        url = "http://example.com/specificatons/1"
        identifier = "http://example.com/identifiers/1"
        oas = yaml.safe_load(v2_spec)
        OASDataService(url, oas, identifier)


def test_parse_minimal_spec(minimal_spec: str, mocker: MockFixture) -> None:
    """It returns a valid dataservice in a catalog."""
    catalog = Catalog()
    catalog.identifier = "http://example.com/catalogs/1"

    url = "http://example.com/specifications/1"
    oas = yaml.safe_load(minimal_spec)
    identifier = "http://example.com/dataservices/1"
    oas_spec = OASDataService(url, oas, identifier)
    for dataservice in oas_spec.dataservices:
        catalog.services.append(dataservice)

    src = """
        @prefix dct: <http://purl.org/dc/terms/> .
        @prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
        @prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
        @prefix dcat: <http://www.w3.org/ns/dcat#> .

        <http://example.com/catalogs/1> a dcat:Catalog ;
            dcat:service <http://example.com/dataservices/1> .

        <http://example.com/dataservices/1> a dcat:DataService ;
            dct:title   "Swagger Petstore"@en ;
            dcat:endpointDescription <http://example.com/specifications/1> ;
        .
        """
    g1 = Graph().parse(data=catalog.to_rdf(), format="turtle")
    g2 = Graph().parse(data=src, format="turtle")

    _isomorphic = isomorphic(g1, g2)
    if not _isomorphic:
        _dump_diff(g1, g2)
        pass
    assert _isomorphic


def test_parse_spec_with_servers_url(spec_with_servers: str) -> None:
    """It returns a valid dataservice with endpoint URL."""
    catalog = Catalog()
    catalog.identifier = "http://example.com/catalogs/1"

    url = "http://example.com/specifications/1"
    oas = yaml.safe_load(spec_with_servers)
    identifier = "http://example.com/dataservices/1"
    oas_spec = OASDataService(url, oas, identifier)
    for dataservice in oas_spec.dataservices:
        catalog.services.append(dataservice)

    src = """
        @prefix dct: <http://purl.org/dc/terms/> .
        @prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
        @prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
        @prefix dcat: <http://www.w3.org/ns/dcat#> .

        <http://example.com/catalogs/1> a dcat:Catalog ;
            dcat:service <http://example.com/dataservices/1> .

        <http://example.com/dataservices/1> a dcat:DataService ;
            dct:title   "Swagger Petstore"@en ;
            dcat:endpointURL   <http://petstore.swagger.io/v1> ;
            dcat:endpointDescription <http://example.com/specifications/1> ;
        .
        """

    g1 = Graph().parse(data=catalog.to_rdf(), format="turtle")
    g2 = Graph().parse(data=src, format="turtle")

    _isomorphic = isomorphic(g1, g2)
    if not _isomorphic:
        _dump_diff(g1, g2)
        pass
    assert _isomorphic


def _get_mock_uuid() -> int:
    uuid = 0
    uuid += 1
    print("uuid", uuid)
    return uuid


def test_parse_spec_with_multiple_servers_url(
    spec_with_multiple_servers: str, mocker: MockFixture
) -> None:
    """It returns multiple valid dataservices with one endpoint URL."""
    catalog = Catalog()
    catalog.identifier = "http://example.com/catalogs/1"
    ids = [1, 2]
    mocker.patch("oastodcat.OASDataService._create_uuid", side_effect=ids)
    url = "http://example.com/specifications/1"
    oas = yaml.safe_load(spec_with_multiple_servers)
    identifier = "http://example.com/dataservices/{uuid}"
    oas_spec = OASDataService(url, oas, identifier)
    for dataservice in oas_spec.dataservices:
        catalog.services.append(dataservice)

    src = """
        @prefix dct: <http://purl.org/dc/terms/> .
        @prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
        @prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
        @prefix dcat: <http://www.w3.org/ns/dcat#> .

        <http://example.com/catalogs/1> a dcat:Catalog ;
            dcat:service <http://example.com/dataservices/1> ,
                         <http://example.com/dataservices/2>
        .

        <http://example.com/dataservices/1> a dcat:DataService ;
            dct:title   "Swagger Petstore"@en ;
            dcat:endpointURL   <http://test.petstore.swagger.io/v1> ;
            dcat:endpointDescription <http://example.com/specifications/1> ;
        .
        <http://example.com/dataservices/2> a dcat:DataService ;
            dct:title   "Swagger Petstore"@en ;
            dcat:endpointURL   <http://petstore.swagger.io/v1> ;
            dcat:endpointDescription <http://example.com/specifications/1> ;
        .
        """

    g1 = Graph().parse(data=catalog.to_rdf(), format="turtle")
    g2 = Graph().parse(data=src, format="turtle")

    _isomorphic = isomorphic(g1, g2)
    if not _isomorphic:
        _dump_diff(g1, g2)
        pass
    assert _isomorphic


def test_parse_spec_with_description(minimal_spec: str) -> None:
    """It returns a valid dataservice with description."""
    catalog = Catalog()
    catalog.identifier = "http://example.com/catalogs/1"

    oas = yaml.safe_load(minimal_spec)
    url = "http://example.com/specifications/1"
    oas["info"]["description"] = "A description of the Swagger Petstore"
    identifier = "http://example.com/dataservices/1"
    oas_spec = OASDataService(url, oas, identifier)
    for dataservice in oas_spec.dataservices:
        catalog.services.append(dataservice)

    src = """
        @prefix dct: <http://purl.org/dc/terms/> .
        @prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
        @prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
        @prefix dcat: <http://www.w3.org/ns/dcat#> .

        <http://example.com/catalogs/1> a dcat:Catalog ;
            dcat:service <http://example.com/dataservices/1>
        .

        <http://example.com/dataservices/1> a dcat:DataService ;
            dct:title   "Swagger Petstore"@en ;
            dct:description "A description of the Swagger Petstore"@en ;
            dcat:endpointDescription <http://example.com/specifications/1> ;
        .
        """

    g1 = Graph().parse(data=catalog.to_rdf(), format="turtle")
    g2 = Graph().parse(data=src, format="turtle")

    _isomorphic = isomorphic(g1, g2)
    if not _isomorphic:
        _dump_diff(g1, g2)
        pass
    assert _isomorphic


def test_parse_spec_with_contact(minimal_spec: str) -> None:
    """It returns a valid dataservice with contactPoint."""
    catalog = Catalog()
    catalog.identifier = "http://example.com/catalogs/1"

    oas = yaml.safe_load(minimal_spec)
    oas["info"]["contact"] = {}
    oas["info"]["contact"]["name"] = "Example Inc"
    oas["info"]["contact"]["email"] = "email@example.com"
    oas["info"]["contact"]["url"] = "http://example.com"
    url = "http://example.com/specifications/1"
    identifier = "http://example.com/dataservices/1"
    oas_spec = OASDataService(url, oas, identifier)
    for dataservice in oas_spec.dataservices:
        catalog.services.append(dataservice)

    src = """
        @prefix dct: <http://purl.org/dc/terms/> .
        @prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
        @prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
        @prefix dcat: <http://www.w3.org/ns/dcat#> .
        @prefix vcard: <http://www.w3.org/2006/vcard/ns#> .

        <http://example.com/catalogs/1> a dcat:Catalog ;
            dcat:service <http://example.com/dataservices/1>
        .

        <http://example.com/dataservices/1> a dcat:DataService ;
            dct:title   "Swagger Petstore"@en ;
            dcat:contactPoint [ a               vcard:Organization ;
                                vcard:hasEmail  <mailto:email@example.com> ;
                                vcard:hasOrganizationName
                                        "Example Inc"@en ;
                                vcard:hasURL <http://example.com> ;
                              ] ;
            dcat:endpointDescription <http://example.com/specifications/1> ;
        .
        """

    g1 = Graph().parse(data=catalog.to_rdf(), format="turtle")
    g2 = Graph().parse(data=src, format="turtle")

    _isomorphic = isomorphic(g1, g2)
    if not _isomorphic:
        _dump_diff(g1, g2)
        pass
    assert _isomorphic


def test_parse_spec_with_license(minimal_spec: str) -> None:
    """It returns a valid dataservice with license."""
    catalog = Catalog()
    catalog.identifier = "http://example.com/catalogs/1"

    oas = yaml.safe_load(minimal_spec)
    oas["info"]["license"] = {}
    oas["info"]["license"]["name"] = "Apache 2.0"
    oas["info"]["license"]["url"] = "https://www.apache.org/licenses/LICENSE-2.0.html"
    url = "http://example.com/specifications/1"
    identifier = "http://example.com/dataservices/1"
    oas_spec = OASDataService(url, oas, identifier)
    for dataservice in oas_spec.dataservices:
        catalog.services.append(dataservice)

    src = """
        @prefix dct: <http://purl.org/dc/terms/> .
        @prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
        @prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
        @prefix dcat: <http://www.w3.org/ns/dcat#> .

        <http://example.com/catalogs/1> a dcat:Catalog ;
            dcat:service <http://example.com/dataservices/1>
        .

        <http://example.com/dataservices/1> a dcat:DataService ;
            dct:title   "Swagger Petstore"@en ;
            dct:license <https://www.apache.org/licenses/LICENSE-2.0.html> ;
            dcat:endpointDescription <http://example.com/specifications/1> ;
        .
        """

    g1 = Graph().parse(data=catalog.to_rdf(), format="turtle")
    g2 = Graph().parse(data=src, format="turtle")

    _isomorphic = isomorphic(g1, g2)
    if not _isomorphic:
        _dump_diff(g1, g2)
        pass
    assert _isomorphic


def test_parse_spec_with_media_types(spec_with_media_types: str) -> None:
    """It returns a valid dataservice with media types."""
    catalog = Catalog()
    catalog.identifier = "http://example.com/catalogs/1"

    oas = yaml.safe_load(spec_with_media_types)
    url = "http://example.com/specifications/1"
    identifier = "http://example.com/dataservices/1"
    oas_spec = OASDataService(url, oas, identifier)
    for dataservice in oas_spec.dataservices:
        catalog.services.append(dataservice)

    src = """
        @prefix dct: <http://purl.org/dc/terms/> .
        @prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
        @prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
        @prefix dcat: <http://www.w3.org/ns/dcat#> .

        <http://example.com/catalogs/1> a dcat:Catalog ;
            dcat:service <http://example.com/dataservices/1>
        .

        <http://example.com/dataservices/1> a dcat:DataService ;
            dct:title   "Swagger Petstore"@en ;
            dcat:mediaType \
            <https://www.iana.org/assignments/media-types/application/json> ,
            <https://www.iana.org/assignments/media-types/application/xml> ;
            dcat:endpointDescription <http://example.com/specifications/1> ;
        .
        """

    g1 = Graph().parse(data=catalog.to_rdf(), format="turtle")
    g2 = Graph().parse(data=src, format="turtle")

    _isomorphic = isomorphic(g1, g2)

    if not _isomorphic:
        _dump_diff(g1, g2)
        pass
    assert _isomorphic


def test_service_to_rdf_without_identifier_should_raise_error(
    minimal_spec: str,
) -> None:
    """It raises a RequiredFieldMissingError."""
    with pytest.raises(RequiredFieldMissingError):
        catalog = Catalog()
        catalog.identifier = "http://example.com/catalogs/1"

        url = "http://example.com/specifications/1"
        oas = yaml.safe_load(minimal_spec)
        oas_spec = OASDataService(url, oas, "")
        for dataservice in oas_spec.dataservices:
            catalog.services.append(dataservice)
        catalog.to_rdf()


def test_parse_spec_with_external_docs(spec_with_external_docs: str) -> None:
    """It returns a valid dataservice with dcat:landingPage."""
    catalog = Catalog()
    catalog.identifier = "http://example.com/catalogs/1"

    oas = yaml.safe_load(spec_with_external_docs)
    url = "http://example.com/specifications/1"
    identifier = "http://example.com/dataservices/1"
    oas_spec = OASDataService(url, oas, identifier)
    for dataservice in oas_spec.dataservices:
        catalog.services.append(dataservice)

    src = """
        @prefix dct: <http://purl.org/dc/terms/> .
        @prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
        @prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
        @prefix dcat: <http://www.w3.org/ns/dcat#> .

        <http://example.com/catalogs/1> a dcat:Catalog ;
            dcat:service <http://example.com/dataservices/1>
        .

        <http://example.com/dataservices/1> a dcat:DataService ;
            dct:title   "Swagger Petstore"@en ;
            dcat:landingPage   <https://example.com> ;
            dcat:endpointDescription <http://example.com/specifications/1> ;
        .
        """

    g1 = Graph().parse(data=catalog.to_rdf(), format="turtle")
    g2 = Graph().parse(data=src, format="turtle")

    _isomorphic = isomorphic(g1, g2)
    if not _isomorphic:
        _dump_diff(g1, g2)
        pass
    assert _isomorphic


# ---------------------------------------------------------------------- #
# Utils for displaying debug information


def _dump_diff(g1: Graph, g2: Graph) -> None:
    in_both, in_first, in_second = graph_diff(g1, g2)
    print("\nin both:")
    _dump_turtle(in_both)
    print("\nin first:")
    _dump_turtle(in_first)
    print("\nin second:")
    _dump_turtle(in_second)


def _dump_turtle(g: Graph) -> None:
    for _l in g.serialize(format="turtle").splitlines():
        if _l:
            print(_l.decode())
