Universal Catalog Quick Start
==============================

The Universal Catalog Client allows you to connect to any STAC-compliant API endpoint with optional authentication.

Installation
------------

The Universal Catalog Client is included in the core package:

.. code-block:: bash

   pip install open-geodata-api

Basic Usage
-----------

**Without Authentication** (Public APIs)

.. code-block:: python

   import open_geodata_api as ogapi

   # Connect to a public STAC API
   client = ogapi.catalog("https://earth-search.aws.element84.com/v1")

   # List available collections
   collections = client.list_collections()
   print(f"Available collections: {collections}")

   # Search for data
   results = client.search(
       collections=["sentinel-2-l2a"],
       bbox=[-122.5, 47.5, -122.0, 48.0],
       datetime="2024-01-01/2024-03-31",
       limit=10
   )

   # Get items
   items = results.get_all_items()
   print(f"Found {len(items)} items")

**With Authentication** (Private/Protected APIs)

.. code-block:: python

   # Connect to an API requiring authentication
   client = ogapi.catalog(
       "https://geoservice.dlr.de/eoc/ogc/stac/v1/",
       auth_token="your-access-token-here"
   )

   # Use the same interface
   results = client.search(
       collections=["collection-name"],
       bbox=[-10, 40, 10, 50],
       datetime="2024-06-01/2024-06-30"
   )

Supported STAC APIs
-------------------

The Universal Catalog Client works with any STAC-compliant API, including:

- AWS Element84 Earth Search
- DLR EOC STAC Catalog
- OpenEO Earth Engine
- Copernicus Data Space
- Custom STAC implementations
- Any other STAC v1.0+ compliant API

Next Steps
----------

- :doc:`catalog-usage-examples` - More detailed usage examples
- :doc:`catalog-authentication` - Authentication configuration
- :doc:`catalog-api-reference` - Complete API reference
