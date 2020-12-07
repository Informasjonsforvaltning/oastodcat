![Tests](https://github.com/Informasjonsforvaltning/oastodcat/workflows/Tests/badge.svg)
[![codecov](https://codecov.io/gh/Informasjonsforvaltning/oastodcat/branch/master/graph/badge.svg)](https://codecov.io/gh/Informasjonsforvaltning/oastodcat)
[![PyPI](https://img.shields.io/pypi/v/oastodcat.svg)](https://pypi.org/project/oastodcat/)
[![Read the Docs](https://readthedocs.org/projects/oastodcat/badge/)](https://oastodcat.readthedocs.io/)
# oastodcat

A small Python library to transform an openAPI file to a dcat:DataService

At this moment we support all 3.0.x versions of (The OpenAPI specification)[https://github.com/OAI/OpenAPI-Specification]

## Usage
### Install
```
% pip install oastodcat
```
### Getting started
Example usage:
```
import yaml
import requests
from datacatalogtordf import Catalog
from oastodcat import OASDataService

# Create catalog object
catalog = Catalog()
catalog.identifier = "http://example.com/catalogs/1"
catalog.title = {"en": "A dataset catalog"}
catalog.publisher = "https://example.com/publishers/1"

# Create a dataservice based on an openAPI-specification:
url = ("https://raw.githubusercontent.com/"
      "OAI/OpenAPI-Specification/master/examples/v3.0/petstore.yaml"
     )
oas = yaml.safe_load(requests.get(url).text)
identifier = "http://example.com/dataservices/{id}"
oas_spec = OASDataService(url, oas, identifier)
#
# Add dataservices to catalog:
for dataservice in oas_spec.dataservices:
  catalog.services.append(dataservice)

get dcat representation in turtle (default)
dcat = catalog.to_rdf()
# Get dcat representation in turtle (default)
dcat = catalog.to_rdf()
print(dcat.decode())
```

## Mapping
The following table shows how an openAPI specification is mapped to a dcat:DataService:  
(Only dcat:DataService properties are shown.)

| dcat:DataService         | RDF property             | openAPI v 3.0.x      | Note |
| ------------------------ | ------------------------ | -------------------- | ---- |
| endpoint description     | dcat:endpointDescription | <url to description> |      |
| endpoint URL             | dcat:endpointURL         | servers.url          | [1]  |
| serves dataset           |                          | _n/a_                |      |
| access rights            |                          |                      |      |
| conforms to              | dct:conformsTo           |                      |      |
| contact point            | dcat:contactPoint        | info.contact         |      |
| creator                  |                          |                      |      |
| description              | dct:description          | info.description     |      |
| has policy               |                          |                      |      |
| identifier               |                          | _n/a_                |      |
| is referenced by         |                          |                      |      |
| keyword/tag              |                          |                      |      |
| landing page             | dcat:landingPage         | externalDocs         |      |
| license                  | dct:license              | info.license.url     |      |
| resource language        |                          |                      |      |
| relation                 |                          |                      |      |
| rights                   |                          |                      |      |
| qualified relation       |                          |                      |      |
| publisher                | dct:publisher            |                      |      |
| release date             |                          |                      |      |
| theme/category           |                          |                      |      |
| title                    | dct:title                | info.title           |      |
| type/genre               |                          |                      |      |
| update/modification date |                          |                      |      |
| qualified attribution    |                          |                      |      |
| _media type_             | dcat:mediaType           | <it's complicated>   |      |

[1] For each url in the servers object array, an instance of dcat:DataService will be created.

## Development
### Requirements
- python3
- [pyenv](https://github.com/pyenv/pyenv) (recommended)
- [pipx](https://github.com/pipxproject/pipx) (recommended)
- [poetry](https://python-poetry.org/)
- [nox](https://nox.thea.codes/en/stable/)
- [nox-poetry](https://pypi.org/project/nox-poetry/)
```
% pipx install poetry==1.0.5
% pipx install nox==2019.11.9
% pipx inject nox nox-poetry
```

### Install
```
% git clone https://github.com/Informasjonsforvaltning/oastodcat.git
% cd oastodcat
% pyenv install 3.8.6
% pyenv install 3.7.9
% pyenv install 3.9.0
% pyenv local 3.9.0 3.8.3 3.7.7
% poetry install
```
### Run all sessions
```
% nox
```
### Run all tests with coverage reporting
```
% nox -rs tests
```
### Debugging
You can enter into [Pdb](https://docs.python.org/3/library/pdb.html) by passing `--pdb` to pytest:
```
nox -rs tests -- --pdb
```
You can set breakpoints directly in code by using the function `breakpoint()`.
