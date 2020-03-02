import pytest
from openapiparser.openapi import OpenAPI


def test_read_valid_spec_from_url():
    url = "https://raw.githubusercontent.com/Informasjonsforvaltning/"
    "dataservice-publisher/master/dataservice-catalog.yaml"
    api = OpenAPI(url)

    assert api is not None


def test_read_spec_from_wrong_url_should_raise_error():
    with pytest.raises(Exception):
        OpenAPI("http://wrong_url")


def test_read_empty_spec_shold_raise_error():
    with pytest.raises(Exception):
        OpenAPI(
               "https://raw.githubusercontent.com/Informasjonsforvaltning"
               "/openapiparser/master/tests/empty_spec.yaml"
                )
