# (generated with --quick)

import oastodcat.oas_dataservice
from typing import Any, Type

Graph: Any
NotValidOASError: Type[oastodcat.oas_dataservice.NotValidOASError]
OASDataService: Type[oastodcat.oas_dataservice.OASDataService]
graph_diff: Any
isomorphic: Any
json: module
minimal_spec: Any
pytest: Any

def _dump_diff(g1, g2) -> None: ...
def _dump_turtle(g) -> None: ...
def test_read_empty_spec_should_raise_error() -> None: ...
def test_read_minimal_spec(minimal_spec: str) -> None: ...
def test_service_to_rdf_without_identifier_should_raise_error(minimal_spec: str) -> None: ...
