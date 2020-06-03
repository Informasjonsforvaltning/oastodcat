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
