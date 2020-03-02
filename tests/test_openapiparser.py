import pytest
from openapiparser.openapi import (
                OpenAPI, Info, NotValidYamlError, RequestError
                )


def test_read_spec_from_wrong_url_should_raise_error():
    with pytest.raises(RequestError):
        OpenAPI("http://wrong_url")


def test_read_empty_spec_shold_raise_error():
    with pytest.raises(NotValidYamlError):
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


def test_get_info_should_return_required_info_object():
    url = (
          "https://raw.githubusercontent.com/Informasjonsforvaltning/"
          "dataservice-publisher/master/dataservice-catalog.yaml"
          )
    api = OpenAPI(url)

    info = api.info
    assert isinstance(info, Info)
    assert type(info.title) is str
    assert len(info.title) > 0
    assert type(info.version) is str
    assert len(info.version) > 0
