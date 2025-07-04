Quick Start Guide
=================

30-Second Example
-----------------

.. code-block:: python

   import open_geodata_api as ogapi

   # Get clients for both APIs
   clients = ogapi.get_clients(pc_auto_sign=True)
   pc = clients['planetary_computer']
   es = clients['earth_search']

   # Search for Sentinel-2 data
   results = pc.search(
       collections=["sentinel-2-l2a"],
       bbox=[-122.5, 47.5, -122.0, 48.0],
       datetime="2024-01-01/2024-03-31"
   )

   # Get items and URLs
   items = results.get_all_items()
   item = items[0]

   # Get ready-to-use URLs
   blue_url = item.get_asset_url('B02')  # Automatically signed!
   all_urls = item.get_all_asset_urls()  # All assets

   # Use with ANY raster package
   import rioxarray
   data = rioxarray.open_rasterio(blue_url)

   # Or use with rasterio
   import rasterio
   with rasterio.open(blue_url) as src:
       data = src.read(1)

5-Minute Tutorial
-----------------

Step 1: Import and Setup
~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   # 1. Import and setup
   import open_geodata_api as ogapi

   # 2. Create clients
   pc = ogapi.planetary_computer(auto_sign=True)
   es = ogapi.earth_search()

   print(f"PC Collections: {pc.list_collections()}")
   print(f"ES Collections: {es.list_collections()}")

Step 2: Search for Data
~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   # 3. Search for data
   search_params = {
       'collections': ['sentinel-2-l2a'],
       'bbox': [-122.5, 47.5, -122.0, 48.0],
       'datetime': '2024-01-01/2024-03-31',
       'query': {'eo:cloud_cover': {'lt': 30}}
   }

   pc_results = pc.search(**search_params, limit=10)
   es_results = es.search(**search_params, limit=10)

Step 3: Work with Results
~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   # 4. Work with results
   pc_items = pc_results.get_all_items()
   es_items = es_results.get_all_items()

   print(f"Found: PC={len(pc_items)}, ES={len(es_items)} items")

   # 5. Get URLs and use with your preferred package
   item = pc_items[0]
   item.print_assets_info()

   # Get specific bands
   rgb_urls = item.get_band_urls(['B04', 'B03', 'B02'])  # Red, Green, Blue
   print(f"RGB URLs: {rgb_urls}")

Compare Providers
-----------------

Both Planetary Computer and EarthSearch offer unique advantages depending on your use case.

Planetary Computer (PC) provides a comprehensive collection catalog with automatic URL signing, while EarthSearch (ES) offers open access without authentication, making it easier for quick data retrieval.

.. code-block:: python

   import open_geodata_api as ogapi

   # Compare last 500 days
   result = ogapi.compare_providers(
    collections=["sentinel-2-l2a"],
    bbox=[-122.5, 47.5, -122.0, 48.0],
    datetime=500,
    cloud_cover=100
    )
    
   # Compare specific date range
   result = ogapi.compare_providers(
    collections=["sentinel-2-l2a"],
    bbox=[-122.5, 47.5, -122.0, 48.0],
    datetime="2023-01-01/2023-12-31",
    cloud_cover=30
    )

   print(result)
   print(f"PC Results: {len(result['planetary_computer'])} items")
   print(f"ES Results: {len(result['earth_search'])} items")

Key Concepts
------------

**Providers**
  - Planetary Computer (Microsoft) - requires signing
  - EarthSearch (Element84/AWS) - no authentication needed

**Collections**
  - Groups of related datasets (e.g., "sentinel-2-l2a")

**Items**
  - Individual products/scenes with metadata

**Assets**
  - Individual files (bands, thumbnails, metadata)

**URL Management**
  - Package automatically handles signing/validation
  - URLs work with any raster reading package

Command Line Interface
----------------------

The package also provides a comprehensive CLI:

.. code-block:: bash

   # Show package info
   ogapi info

   # List collections
   ogapi collections list --provider pc

   # Search for data
   ogapi search items --collections sentinel-2-l2a \
     --bbox "-122.5,47.5,-122.0,48.0" \
     --datetime "2024-06-01/2024-08-31" \
     --output search_results.json

   # Download data
   ogapi download search-results search_results.json \
     --assets "B04,B03,B02" --destination "./rgb_data/"

Next Steps
----------

- Read the :doc:`core-concepts` for detailed understanding
- Check out :doc:`usage-examples` for real-world examples
- Browse the :doc:`api-reference` for complete reference
- Explore :doc:`cli-usage` for command-line operations
