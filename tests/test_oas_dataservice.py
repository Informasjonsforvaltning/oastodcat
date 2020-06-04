"""Test cases for the oas_dataservice module."""
import json

import pytest
from rdflib import Graph
from rdflib.compare import graph_diff, isomorphic

from oastodcat import NotSupportedOASError, NotValidOASError, OASDataService


@pytest.fixture(scope="session")  # one server to rule'em all
def minimal_spec() -> str:
    """Helper for creating a minimal specification object."""
    minimal_spec = """
        {
          "openapi": "3.0.3",
          "info": {
            "title": "fdk-reports-bff",
            "version": "1.0"
          },
          "paths": {}
        }
    """
    return minimal_spec


def test_read_empty_spec_should_raise_error() -> None:
    """It raises a NotValidOASError."""
    with pytest.raises(NotValidOASError):
        specification = "{}"
        oas = json.loads(specification)
        OASDataService(oas)


def test_read_other_than_v3_spec_should_raise_error() -> None:
    """It raises a NotValidOASError."""
    with pytest.raises(NotSupportedOASError):
        v2_spec = """
            {
              "openapi": "2.0",
              "info": {
                "title": "fdk-reports-bff",
                "version": "1.0"
              },
              "paths": {}
            }
        """
        oas = json.loads(v2_spec)
        OASDataService(oas)


def test_read_minimal_spec(minimal_spec: str) -> None:
    """It returns a valid dataservice."""
    # Create a dataservice based on an openAPI-specification:
    # 1. Get the specification
    # 2. Convert the specification to a json-object if needed
    # 3. Parse the json
    # 4. Instantiate a dataservice object with the parsed json
    # 5. Set the identifer
    # 6. Create the dcat-representation

    oas = json.loads(minimal_spec)
    dataservice = OASDataService(oas)
    dataservice.identifier = "http://example.com/dataservices/1"

    src = """
        @prefix dct: <http://purl.org/dc/terms/> .
        @prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
        @prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
        @prefix dcat: <http://www.w3.org/ns/dcat#> .

        <http://example.com/dataservices/1> a dcat:DataService ;
            dct:title   "fdk-reports-bff"@en ;
        .
        """

    g1 = Graph().parse(data=dataservice.to_rdf(), format="turtle")
    g2 = Graph().parse(data=src, format="turtle")

    _isomorphic = isomorphic(g1, g2)
    if not _isomorphic:
        _dump_diff(g1, g2)
        pass
    assert _isomorphic


def test_read_spec_with_servers_url(minimal_spec: str) -> None:
    """It returns a valid dataservice with endpoint URL."""
    oas = json.loads(minimal_spec)
    oas["servers"] = {}
    oas["servers"]["url"] = "http://example.com/server/url"
    dataservice = OASDataService(oas)
    dataservice.identifier = "http://example.com/dataservices/1"

    src = """
        @prefix dct: <http://purl.org/dc/terms/> .
        @prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
        @prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
        @prefix dcat: <http://www.w3.org/ns/dcat#> .

        <http://example.com/dataservices/1> a dcat:DataService ;
            dct:title   "fdk-reports-bff"@en ;
            dcat:endpointURL   <http://example.com/server/url>
        .
        """

    g1 = Graph().parse(data=dataservice.to_rdf(), format="turtle")
    g2 = Graph().parse(data=src, format="turtle")

    _isomorphic = isomorphic(g1, g2)
    if not _isomorphic:
        _dump_diff(g1, g2)
        pass
    assert _isomorphic


def test_read_spec_with_description(minimal_spec: str) -> None:
    """It returns a valid dataservice with description."""
    oas = json.loads(minimal_spec)
    oas["info"]["description"] = "A description of the fdk-reports-bff"
    dataservice = OASDataService(oas)
    dataservice.identifier = "http://example.com/dataservices/1"

    src = """
        @prefix dct: <http://purl.org/dc/terms/> .
        @prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
        @prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
        @prefix dcat: <http://www.w3.org/ns/dcat#> .

        <http://example.com/dataservices/1> a dcat:DataService ;
            dct:title   "fdk-reports-bff"@en ;
            dct:description "A description of the fdk-reports-bff"@en ;
        .
        """

    g1 = Graph().parse(data=dataservice.to_rdf(), format="turtle")
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
    with pytest.raises(AttributeError):
        oas = json.loads(minimal_spec)
        dataservice = OASDataService(oas)
        dataservice.to_rdf()


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
