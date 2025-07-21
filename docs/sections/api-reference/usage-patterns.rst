Usage Patterns (Full API Testing)
=================================

The core classes provide STAC-compliant data models for working with satellite imagery metadata and assets.

Install The Module
------------------

.. code-block:: python

   pip install open-geodata-api['complete']

Initialize Module
-----------------

.. code-block:: python

   import open_geodata_api as ogapi
   
   ogapi.info()

Define Clients
--------------

.. code-block:: python

   import open_geodata_api as ogapi

   # Create client with auto-signing
   pc = ogapi.planetary_computer(auto_sign=True)

   # Search for data
   pc_results = pc.search(
       collections=["sentinel-2-l2a"],
       bbox=[-122.5, 47.5, -122.0, 48.0],
       datetime="2024-01-01/2024-03-31"
   )

   # Get ready-to-use URLs
   pc_items = pc_results.get_all_items()
   print(f"PC Items: {len(pc_items)}")

   es = ogapi.earth_search()

   # Search for data
   es_results = es.search(
       collections=["sentinel-2-l2a"],
       bbox=[-122.5, 47.5, -122.0, 48.0],
       days=200,  # added to 0.2.9 version
       limit=150
   )

   # Get ready-to-use URLs
   es_items = es_results.get_all_items()
   print(f"ES Items: {len(es_items)}")

Get Available Collections
-------------------------

.. code-block:: python

   # Get available collections
   pc_collections = pc.list_collections()
   print(f"Available Collections in Planetary Computer: {pc_collections}")

   # Get collection details
   es_collection = es.list_collections()
   print(f"Available Collections in Earth Search: {es_collection}")

STACSearch API Reference
------------------------

Get all items from search results:
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   len(pc_results.get_all_items())

.. code-block:: python

   len(es_results.get_all_items())

Get item collection from search results:
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   pc_results.item_collection()

.. code-block:: python

   es_results.item_collection()

Get items from search results (Generator):
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   pc_results.items()

.. code-block:: python

   es_results.items()

Extracting Items from Generator:
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   gen = pc_results.items()
   pc_all_items = list(gen)
   pc_all_items

.. code-block:: python

   es_gen = es_results.items()
   es_all_items = list(es_gen)
   es_all_items

Get Matched Items:
~~~~~~~~~~~~~~~~~~

.. code-block:: python

   pc_results.matched()

.. code-block:: python

   es_results.matched()

Get Total Number of items:
~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   pc_results.total_items()

.. code-block:: python

   es_results.total_items()

Get Search Parameters:
~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   pc_results.search_params()

.. code-block:: python

   es_results.search_params()

Get all Available keys:
~~~~~~~~~~~~~~~~~~~~~~~
.. code-block:: python

   pc_results.all_keys()

.. code-block:: python

   es_results.all_keys()

Get List of all Product IDs:
~~~~~~~~~~~~~~~~~~~~~~~~~~~~
.. code-block:: python

   pc_results.list_product_ids()

.. code-block:: python

   es_results.list_product_ids()

Get your Search Fallback Methods (used for pagination):
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   pc_results.get_fallback_status()

.. code-block:: python

   es_results.get_fallback_status()


STACItemCollection API Reference
--------------------------------

Get a Collection:
~~~~~~~~~~~~~~~~~

.. code-block:: python

   pc_items = pc_results.get_all_items()

.. code-block:: python

   es_items = es_results.get_all_items()

Get all Items as List:
~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   pc_items.to_list()

.. code-block:: python

   es_items.to_list()

Get all Items as Dictionary/JSON:
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   pc_items.to_dict()

.. code-block:: python

   es_items.to_dict()

Get all Items as geojson (geojson module required):
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   pc_items.to_geojson()

.. code-block:: python

   es_items.to_geojson()

Get all Items as DataFrame (pandas module required):
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   pc_items.to_dataframe()

.. code-block:: python

   es_items.to_dataframe(include_geometry=True)

Filter Items by Property (date, datetime, days):
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   start_date = "2024-01-01"
   end_date = "2024-02-31"
   pc_filtered_items = pc_items.filter_by_date_range(start_date, end_date) # "2024-01-01/2024-03-31"
   print(f"Filtered PC Items: {len(pc_filtered_items)}")

.. code-block:: python

   es_filtered_items = es_items.filter_by_date_range(days_back=150) #("2024-01-01", "2024-03-31")
   print(f"Filtered ES Items: {len(es_filtered_items)}")

Get all unique collection types:
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   pc_items.get_unique_collections()

.. code-block:: python

   es_items.get_unique_collections()

Get the date range of the collection:
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   pc_items.get_date_range()

.. code-block:: python

   es_filtered_items.get_date_range()

Get all unique item IDs/assets:
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   pc_items.get_all_assets()

.. code-block:: python

   es_items.get_all_assets()

Get all unique asset keys:
~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   pc_items.get_all_assets().keys()

.. code-block:: python

   es_items.get_all_assets().keys()

Get asset by pattern/Extensions (e.g., ".xml", ".jp2"):
~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   pc_items.get_assets_by_pattern(".xml")

.. code-block:: python

   es_items.get_assets_by_pattern(".jp2")

Get all unique asset keys by collection types:
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   pc_items.get_assets_by_collection()
   es_items.get_assets_by_collection()

Get all products/items in dictionary/json format with assets keys (without links):
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   pc_items.to_products_dict()

.. code-block:: python

   es_items.to_products_dict()

Get all products/items in list format with/without links:
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   pc_items.to_simple_products_list(include_urls=False)

.. code-block:: python

   es_items.to_simple_products_list(include_urls=True, url_bands=['red', 'green', 'blue'])

Get all unique asset keys by collection types:
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   pc_items.get_available_bands()

... code-block:: python

   es_items.get_available_bands()

Get all common asset keys:
~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   pc_items.get_common_bands()
   es_items.get_common_bands()

Get all products/items in dictionary/json format with all assets keys and urls:
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   pc_items.get_all_urls()

.. code-block:: python

   es_items.get_all_urls()

Get all products/items in list format with specific assets keys and urls:
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   pc_items.get_band_urls(['B04', 'B03', 'B02'])

.. code-block:: python

   es_items.get_band_urls(['nir', 'red', 'green'])

Get only image/tiff assets urls:
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   pc_items.get_band_urls(asset_type='image')

.. code-block:: python

   es_items.get_band_urls(asset_type='image')

Get only spectral bands urls:
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   pc_items.get_band_urls(asset_type='bands')

Get only visual assets:
~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   pc_items.get_band_urls(asset_type='visual')

Save the collection to a file (JSON):
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   pc_items.export_urls_json("pc_export_urls.json")

.. code-block:: python

   es_items.export_urls_json("es_items.json")

Get collection Summary:
~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   pc_items.print_collection_summary()

.. code-block:: python

   es_items.print_collection_summary()


STACItem API Reference
----------------------

Choose an Item from Search Results:
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   pc_item = pc_items[0]

.. code-block:: python

   es_item = es_items[0]

Get Item Details in Dictionary/JSON Format:
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   pc_item.to_dict()

.. code-block:: python

   es_item.to_dict()

Get Item All Item Keys:
~~~~~~~~~~~~~~~~

.. code-block:: python

   print(pc_item.to_dict().keys())

.. code-block:: python

   print(es_item.to_dict().keys())

Get Item Properties:
~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   pc_item.properties

.. code-block:: python

   es_item.properties

Get Item Id:
~~~~~~~~~~~~

.. code-block:: python

   pc_item.get("id")

.. code-block:: python

   es_item.get("id")

Get Assets List of an Item :
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   pc_item.list_assets()

.. code-block:: python

   es_item.list_assets()

Fetch Band URLs:
~~~~~~~~~~~~~~~~

.. code-block:: python

   pc_item.get_asset_url("B01")

.. code-block:: python

   es_item.get_asset_url("blue")

Get All Asset URLs:
~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   pc_item.get_all_asset_urls()

.. code-block:: python

   es_item.get_all_asset_urls()

Get Asset List all available asset types:
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   pc_item.list_asset_types()

.. code-block:: python

   es_item.list_asset_types()

Get Assets with URLs by Type defaulting to "image/tiff":
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   pc_item.get_assets_by_type("image/tiff")

.. code-block:: python

   es_item.get_assets_by_type()

Get All Raster Assets and URLs:
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   pc_item.get_raster_assets()

.. code-block:: python

   es_item.get_raster_assets()

Get All Metadata Assets and URLs:
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   pc_item.get_metadata_assets()

.. code-block:: python

   es_item.get_metadata_assets()

Get Specific Band URLs:
~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   pc_item.get_band_urls(["B01", "B02", "B03"])

.. code-block:: python

   es_item.get_band_urls(["blue"])

Check if Item has Specific Asset:
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   pc_item.has_asset("B10") # It will return False if the asset is not present

.. code-block:: python

   es_item.has_asset("blue")

Get RGB Bands URLs:
~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   pc_item.get_rgb_urls()

.. code-block:: python

   es_item.get_rgb_urls()

Get all Sentinel-2 Bands URLs:
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   pc_item.get_sentinel2_urls()

.. code-block:: python

   es_item.get_sentinel2_urls()

Get Asset Informations
~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   pc_item.print_assets_info()

.. code-block:: python

   es_item.print_assets_info()

STACAsset API Reference
------------------------

Get Asset Details:
~~~~~~~~~~~~~~~~~

.. code-block:: python

   # Access asset directly
   pc_item = pc_items[0]
   asset = pc_item.assets['B04']

   print(f"Asset URL: {asset.href}")
   print(f"Asset type: {asset.type}")
   print(f"Asset title: {asset.title}")

.. code-block:: python

   # Access asset directly
   es_item = es_items[0]
   asset = es_item.assets['red']

   print(f"Asset URL: {asset.href}")
   print(f"Asset type: {asset.type}")
   print(f"Asset title: {asset.title}")
