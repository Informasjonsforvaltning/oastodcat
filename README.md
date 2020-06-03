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
```
from datacatalogtordf import Catalog
from oastodcat import OASDataService

# Create catalog object
catalog = Catalog()
catalog.identifier = "http://example.com/catalogs/1"
catalog.title = {"en": "A dataset catalog"}
catalog.publisher = "https://example.com/publishers/1"

# Create a dataservice based on an openAPI-specification:
oas = json.load(<url_to_specification>)
dataservice = OASDataService(oas)
dataservice.identifier = "http://example.com/dataservices/1"
#
# Add dataservice to catalog:
catalog.services.append(dataservice)

# get dcat representation in turtle (default)
dcat = catalog.to_rdf()
print(dcat.decode())
```

## Mapping
The following table shows how an openAPI specification is mapped to a dcat:DataService:  
(Only dcat:DataService properties are shown.)

| dcat:DataService         | openAPI v 3.0.x |
| ------------------------ | --------------- |
| endpoint description     |                 |
| endpoint URL             | servers.url     |
| serves dataset           | _n/a_           |
| access rights            |                 |
| conforms to              |                 |
| contact point            |                 |
| creator                  |                 |
| description              |                 |
| has policy               |                 |
| identifier               | _n/a_           |
| is referenced by         |                 |
| keyword/tag              |                 |
| landing page             |                 |
| license                  |                 |
| resource language        |                 |
| relation                 |                 |
| rights                   |                 |
| qualified relation       |                 |
| publisher                |                 |
| release date             |                 |
| theme/category           |                 |
| title                    | info.title      |
| type/genre               |                 |
| update/modification date |                 |
| qualified attribution    |                 |

## Development
### Requirements
- python3
- [pyenv](https://github.com/pyenv/pyenv) (recommended)
- [poetry](https://python-poetry.org/)
- [nox](https://nox.thea.codes/en/stable/)

### Install
```
% git clone https://github.com/Informasjonsforvaltning/oastodcat.git
% cd oastodcat
% pyenv install 3.8.3
% pyenv install 3.7.7
% pyenv local 3.8.3 3.7.7
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
