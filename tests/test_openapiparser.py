import pytest
from openapiparser.openapi import OpenAPI, Error, RequestError


def test_read_spec_from_wrong_url_should_raise_error():
    with pytest.raises(Error):
        OpenAPI("http://wrong_url")


def test_read_empty_spec_shold_raise_error():
    with pytest.raises(Error):
        OpenAPI(
                (
                 "https://raw.githubusercontent.com/Informasjonsforvaltning"
                 "/openapiparser/master/tests/empty_spec.yaml"
                )
                )


def test_read_spec_shold_raise_RequestError():
    with pytest.raises(RequestError):
        OpenAPI("https://raw.githubusercontent.com/Informasjonsforvaltning")


def test_get_version_should_return_valid_version_string():
    url = (
          "https://raw.githubusercontent.com/Informasjonsforvaltning/"
          "dataservice-publisher/master/dataservice-catalog.yaml"
          )
    api = OpenAPI(url)

    assert api.version[:4] == "3.0."  # We support all 3.0.x versions
