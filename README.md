# openapiparser

A small Python library to work with an openAPI specification.

Roadmap:
- a method for validating the specification  
- properties for most useful attributes of spec such as:
  - content types in responses
  - server urls
  - schema objects

## Run all tests
```
pytest -rA
```

With coverage:
```
pytest -rA --cov-report term-missing --cov=openapiparser tests/
```
