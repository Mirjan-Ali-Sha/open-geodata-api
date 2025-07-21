API Reference
=============

Complete reference documentation for all classes, functions, and modules.

.. toctree::
   :maxdepth: 2

   core-classes
   client-classes
   utility-functions
   factory-functions
   usage-patterns


Quick Navigation
----------------

**Core Classes**

- :class:`STACItem` - Individual satellite scenes
- :class:`STACItemCollection` - Collections of scenes
- :class:`STACAsset` - Individual data files
- :class:`STACSearch` - Search result containers

**Client Classes**  

- :class:`PlanetaryComputerCollections` - Microsoft PC client
- :class:`EarthSearchCollections` - Element84 ES client

**Utility Functions**

- :func:`filter_by_cloud_cover` - Quality filtering
- :func:`download_datasets` - Intelligent downloading
- :func:`create_download_summary` - Progress reporting

**Factory Functions**

- :func:`planetary_computer` - Create PC client
- :func:`earth_search` - Create ES client
- :func:`get_clients` - Get both clients

Class Hierarchy
---------------

.. code-block:: text

   BaseAPIClient
   ├── PlanetaryComputerCollections
   └── EarthSearchCollections

   STACAsset
   STACItem
   STACItemCollection
   STACSearch

Usage Patterns
--------------

**Basic Usage Pattern**:

.. code-block:: python

   import open_geodata_api as ogapi
   
   # Create client
   client = ogapi.planetary_computer()
   
   # Search for data
   results = client.search(collections=['sentinel-2-l2a'])
   
   # Work with results
   items = results.get_all_items()
   item = items[0]
   urls = item.get_all_asset_urls()

**Advanced Usage Pattern**:

.. code-block:: python

   from open_geodata_api.utils import filter_by_cloud_cover, download_datasets
   
   # Search and filter
   results = client.search(collections=['sentinel-2-l2a'], limit=20)
   items = results.get_all_items()
   clear_items = filter_by_cloud_cover(items, max_cloud_cover=20)
   
   # Download
   download_results = download_datasets(clear_items, destination="./data/")

Downloadable Notebook of API References Testing:
-----------------------------------------------

You can download the full Jupyter notebook of API examples here:

- `Download Test Open GeoData API References.ipynb <https://github.com/Mirjan-Ali-Sha/open-geodata-api/raw/main/Test_Open_GeoData_API_References.ipynb>`_

- `Open in Google Colab <https://colab.research.google.com/github/Mirjan-Ali-Sha/open-geodata-api/blob/main/Test_Open_GeoData_API_References.ipynb>`_

- `Launch Binder <https://mybinder.org/v2/gh/Mirjan-Ali-Sha/open-geodata-api/main?filepath=Test_Open_GeoData_API_References.ipynb>`_

