Universal Catalog Usage Examples
=================================

This guide provides comprehensive examples for using the Universal Catalog Client.

Example 1: Basic Connection and Search
--------------------------------------

**Public API (No Authentication)**

.. code-block:: python

   import open_geodata_api as ogapi

   # Connect to Earth Search
   client = ogapi.catalog("https://earth-search.aws.element84.com/v1")

   # List collections
   collections = client.list_collections()
   print(f"Available collections: {collections}")

   # Search for Sentinel-2 data
   results = client.search(
       collections=["sentinel-2-l2a"],
       bbox=[-122.5, 47.5, -122.0, 48.0],
       datetime="2024-06-01/2024-08-31",
       query={"eo:cloud_cover": {"lt": 20}},
       limit=10
   )

   # Process results
   items = results.get_all_items()
   print(f"Found {len(items)} items")

   for item in items:
       print(f"Item ID: {item.id}")
       print(f"Date: {item.datetime}")
       print(f"Cloud cover: {item.properties.get('eo:cloud_cover')}%")

Example 2: Authenticated Access
--------------------------------

**DLR EOC STAC Catalog**

.. code-block:: python

   # Connect with authentication
   dlr_client = ogapi.catalog(
       "https://geoservice.dlr.de/eoc/ogc/stac/v1/",
       auth_token="your-dlr-access-token"
   )

   # Get collection information
   collections = dlr_client.get_collections()
   for col in collections:
       print(f"Collection: {col['id']}")
       print(f"  Title: {col['title']}")
       print(f"  Description: {col['description'][:100]}...")

   # Search specific collection
   results = dlr_client.search(
       collections=["collection-id"],
       bbox=[10, 50, 15, 55],
       datetime="2024-01-01/2024-12-31",
       limit=20
   )

Example 3: Multi-Provider Comparison
-------------------------------------

**Compare Data from Different STAC APIs**

.. code-block:: python

   # Connect to multiple STAC APIs
   earth_search = ogapi.catalog("https://earth-search.aws.element84.com/v1")
   
   custom_api = ogapi.catalog(
       "https://your-custom-stac.com/api/",
       auth_token="your-token"
   )

   # Search parameters
   search_params = {
       "collections": ["sentinel-2-l2a"],
       "bbox": [-120, 35, -119, 36],
       "datetime": "2024-07-01/2024-07-31",
       "limit": 10
   }

   # Search both providers
   es_results = earth_search.search(**search_params)
   custom_results = custom_api.search(**search_params)

   es_items = es_results.get_all_items()
   custom_items = custom_results.get_all_items()

   print(f"Earth Search: {len(es_items)} items")
   print(f"Custom API: {len(custom_items)} items")

   # Compare assets
   if es_items and custom_items:
       print("\nEarth Search assets:", es_items[0].list_assets()[:5])
       print("Custom API assets:", custom_items[0].list_assets()[:5])

Example 4: Custom Headers and Configuration
--------------------------------------------

**Advanced Configuration**

.. code-block:: python

   # Connect with custom configuration
   client = ogapi.catalog(
       "https://custom-stac-api.com/v2/",
       auth_token="bearer-token-123",
       headers={
           "X-API-Key": "additional-api-key",
           "User-Agent": "MyApp/1.0",
           "Accept": "application/geo+json"
       },
       timeout=60,
       verify_ssl=True
   )

   # Get detailed client information
   info = client.get_info()
   print(f"""
   Client Configuration:
   - Type: {info['client_type']}
   - API URL: {info['api_url']}
   - STAC Version: {info['stac_version']}
   - Search Available: {info['search_available']}
   - Authenticated: {info['authenticated']}
   - Collections: {info['collections_count']}
   """)

Example 5: Band Name Mapping
-----------------------------

**Automatic Band Name Translation**

.. code-block:: python

   # Search for data
   results = client.search(
       collections=["sentinel-2-l2a"],
       bbox=[-122, 47, -121, 48],
       datetime="2024-05-01/2024-05-07",
       limit=5
   )

   items = results.get_all_items()
   item = items[0]

   # Get band URLs using different naming conventions
   # Standard Sentinel-2 band names
   b02_url = client.get_asset_url(item, 'B02')  # Blue
   b03_url = client.get_asset_url(item, 'B03')  # Green
   b04_url = client.get_asset_url(item, 'B04')  # Red
   b08_url = client.get_asset_url(item, 'B08')  # NIR

   # Common band names (automatically mapped)
   blue_url = client.get_asset_url(item, 'blue')
   green_url = client.get_asset_url(item, 'green')
   red_url = client.get_asset_url(item, 'red')
   nir_url = client.get_asset_url(item, 'nir')

   # Get multiple bands at once
   rgb_urls = item.get_band_urls(['B04', 'B03', 'B02'])  # Red, Green, Blue
   
   print("RGB URLs:", rgb_urls)

Example 6: Error Handling
--------------------------

**Robust Connection Handling**

.. code-block:: python

   def connect_to_stac_safely(api_url, token=None):
       """
       Safely connect to a STAC API with error handling.
       """
       try:
           # Try connecting
           client = ogapi.catalog(api_url, auth_token=token)
           
           # Test connection by listing collections
           collections = client.list_collections()
           
           print(f"✓ Successfully connected to {api_url}")
           print(f"  Found {len(collections)} collections")
           
           return client
           
       except ConnectionError as e:
           print(f"✗ Connection failed: {e}")
           return None
       except Exception as e:
           print(f"✗ Unexpected error: {e}")
           return None

   # Usage
   client = connect_to_stac_safely(
       "https://your-api.com/stac",
       token="optional-token"
   )

   if client:
       # Proceed with searches
       results = client.search(...)

Example 7: Export and Download Workflow
----------------------------------------

**Complete Data Pipeline**

.. code-block:: python

   import open_geodata_api as ogapi
   from open_geodata_api.utils import filter_by_cloud_cover, download_items

   # Connect to API
   client = ogapi.catalog("https://earth-search.aws.element84.com/v1")

   # Search for data
   results = client.search(
       collections=["sentinel-2-l2a"],
       bbox=[-120.5, 38.0, -120.0, 38.5],
       datetime="2024-06-01/2024-08-31",
       limit=50
   )

   items = results.get_all_items()
   print(f"Found {len(items)} items")

   # Filter by cloud cover
   clear_items = filter_by_cloud_cover(items, max_cloud_cover=15)
   print(f"After filtering: {len(clear_items)} clear items")

   # Export URLs to JSON
   clear_items.export_urls_json(
       "sentinel2_urls.json",
       asset_keys=['B04', 'B03', 'B02', 'B08']
   )

   # Download specific bands
   downloads = download_items(
       clear_items[:5],  # First 5 items
       base_destination="./satellite_data",
       asset_keys=['B04', 'B03', 'B02'],  # RGB bands
       create_product_folders=True
   )

   print(f"Downloaded {len(downloads)} items")

Example 8: OpenEO Integration
------------------------------

**Connect to OpenEO Earth Engine**

.. code-block:: python

   # Connect to OpenEO
   openeo_client = ogapi.catalog(
       "https://earthengine.openeo.org/v1.0/",
       auth_token="your-openeo-token",
       headers={"User-Agent": "MyApp/1.0"}
   )

   # List available collections
   collections = openeo_client.list_collections()
   print(f"OpenEO collections: {len(collections)}")

   # Get collection details
   for col_id in collections[:5]:
       info = openeo_client.get_collection_info(col_id)
       print(f"\nCollection: {info['id']}")
       print(f"  Title: {info.get('title', 'N/A')}")
       print(f"  License: {info.get('license', 'N/A')}")

   # Search for data
   results = openeo_client.search(
       collections=["COPERNICUS/S2"],
       bbox=[10, 50, 11, 51],
       datetime="2024-06-01/2024-06-30",
       limit=10
   )
