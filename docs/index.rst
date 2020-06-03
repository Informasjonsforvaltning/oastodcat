oastodcat library
==============================

.. toctree::
   :hidden:
   :maxdepth: 1

   license
   reference

A small Python library to transform an openAPI file to a dcat:DataService


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
