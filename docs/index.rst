oastodcat library
==============================

.. toctree::
   :hidden:
   :maxdepth: 1

   license
   reference

A small Python library to transform an openAPI file to one or more instances of dcat:DataService
For each server object, an instance of DataService object will be created.


Installation
------------

To install the oastodcat package,
run this command in your terminal:

.. code-block:: console

   $ pip install oastodcat


Usage
-----

This package can be used like this:

.. code-block::

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

    # get dcat representation in turtle (default)
    dcat = catalog.to_rdf()
    print(dcat)
