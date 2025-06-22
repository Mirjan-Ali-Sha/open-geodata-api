First Steps
===========

Master the fundamental concepts and workflows of Open Geodata API with hands-on examples.

Understanding Core Concepts
---------------------------

STAC (SpatioTemporal Asset Catalog)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Open Geodata API is built around the STAC specification, which provides a common language for describing geospatial data:

.. code-block:: python

   import open_geodata_api as ogapi
   
   # Create client
   pc = ogapi.planetary_computer(auto_sign=True)
   
   # Search returns STAC-compliant results
   results = pc.search(collections=['sentinel-2-l2a'], limit=1)
   
   # Results contain STAC Items
   items = results.get_all_items()
   item = items[0]
   
   # Each item has STAC properties
   print(f"Item ID: {item.id}")
   print(f"Collection: {item.collection}")
   print(f"Date: {item.properties['datetime']}")
   print(f"Cloud Cover: {item.properties['eo:cloud_cover']}%")

**STAC Hierarchy**:
- **Collection**: A group of related items (e.g., "sentinel-2-l2a")
- **Item**: A single acquisition/scene (e.g., one Sentinel-2 image)
- **Asset**: Individual files within an item (e.g., B04.tif for red band)

Providers and Collections
~~~~~~~~~~~~~~~~~~~~~~~~~

Understanding data providers and their collections:

.. code-block:: python

   # List available collections
   pc = ogapi.planetary_computer()
   pc_collections = pc.list_collections()
   print(f"Planetary Computer: {len(pc_collections)} collections")
   
   es = ogapi.earth_search()
   es_collections = es.list_collections()
   print(f"EarthSearch: {len(es_collections)} collections")
   
   # Find specific collections
   sentinel_collections = [c for c in pc_collections if 'sentinel' in c.lower()]
   print(f"Sentinel collections: {sentinel_collections}")

**Common Collections**:
- ``sentinel-2-l2a``: Sentinel-2 atmospherically corrected imagery
- ``landsat-c2-l2``: Landsat Collection 2 surface reflectance
- ``sentinel-1-grd``: Sentinel-1 ground range detected SAR

Your First Search
-----------------

Basic Search Parameters
~~~~~~~~~~~~~~~~~~~~~~~

Learn the essential search parameters:

.. code-block:: python

   # Essential search parameters
   search_params = {
       'collections': ['sentinel-2-l2a'],           # What: Data type
       'bbox': [-122.5, 47.5, -122.0, 48.0],       # Where: Geographic area
       'datetime': '2024-06-01/2024-08-31',         # When: Time period
       'limit': 10                                  # How many: Number of results
   }
   
   results = pc.search(**search_params)
   items = results.get_all_items()
   
   print(f"Found {len(items)} Sentinel-2 scenes over Seattle in summer 2024")

Understanding Bounding Boxes
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Bounding boxes define your area of interest:

.. code-block:: python

   # Bbox format: [west, south, east, north] in degrees
   # Also known as: [min_lon, min_lat, max_lon, max_lat]
   
   # Small area (faster search)
   small_bbox = [-122.35, 47.55, -122.25, 47.65]  # Downtown Seattle
   
   # Large area (more data, slower search)  
   large_bbox = [-125.0, 45.0, -120.0, 49.0]      # Pacific Northwest
   
   # Tips for bbox creation:
   # 1. Use online tools like bbox-finder.com
   # 2. Start small for testing
   # 3. Remember: west < east, south < north

Working with Search Results
~~~~~~~~~~~~~~~~~~~~~~~~~~~

Explore and understand your search results:

.. code-block:: python

   # Perform search
   results = pc.search(
       collections=['sentinel-2-l2a'],
       bbox=[-122.5, 47.5, -122.0, 48.0],
       datetime='2024-06-01/2024-08-31',
       limit=20
   )
   
   items = results.get_all_items()
   
   # Basic information
   print(f"Search returned {len(items)} items")
   
   # Examine first item
   if items:
       item = items[0]
       print(f"\nFirst item details:")
       print(f"  ID: {item.id}")
       print(f"  Date: {item.properties['datetime']}")
       print(f"  Cloud cover: {item.properties.get('eo:cloud_cover', 'N/A')}%")
       print(f"  Platform: {item.properties.get('platform', 'N/A')}")
       
       # Available assets (bands/files)
       assets = item.list_assets()
       print(f"  Available assets: {len(assets)}")
       print(f"  Asset names: {assets[:5]}...")  # Show first 5

Understanding Assets
--------------------

Asset Naming Conventions
~~~~~~~~~~~~~~~~~~~~~~~~

Different providers use different naming conventions:

.. code-block:: python

   # Get an item from each provider
   pc_results = pc.search(collections=['sentinel-2-l2a'], limit=1)
   es_results = es.search(collections=['sentinel-2-l2a'], limit=1)
   
   if pc_results.get_all_items():
       pc_item = pc_results.get_all_items()[0]
       pc_assets = pc_item.list_assets()
       print(f"Planetary Computer assets: {pc_assets[:8]}")
       # Output: ['B01', 'B02', 'B03', 'B04', 'B05', 'B06', 'B07', 'B08']
   
   if es_results.get_all_items():
       es_item = es_results.get_all_items()[0]
       es_assets = es_item.list_assets()
       print(f"EarthSearch assets: {es_assets[:8]}")
       # Output: ['coastal', 'blue', 'green', 'red', 'rededge1', 'rededge2', ...]

**Asset Mapping for Sentinel-2**:

.. list-table::
   :header-rows: 1
   :widths: 25 25 25 25

   * - Band
     - Planetary Computer
     - EarthSearch
     - Description
   * - Coastal
     - B01
     - coastal
     - 443 nm, 60m
   * - Blue
     - B02
     - blue
     - 490 nm, 10m
   * - Green
     - B03
     - green
     - 560 nm, 10m
   * - Red
     - B04
     - red
     - 665 nm, 10m
   * - NIR
     - B08
     - nir
     - 842 nm, 10m

Working with Assets
~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   # Provider-agnostic asset access
   def get_rgb_assets(item):
       """Get RGB assets regardless of provider."""
       assets = item.list_assets()
       
       # Try Planetary Computer naming first
       if all(band in assets for band in ['B04', 'B03', 'B02']):
           return ['B04', 'B03', 'B02']  # Red, Green, Blue
       
       # Try EarthSearch naming
       elif all(band in assets for band in ['red', 'green', 'blue']):
           return ['red', 'green', 'blue']
       
       else:
           print(f"Unknown asset naming. Available: {assets}")
           return None
   
   # Use the function
   rgb_assets = get_rgb_assets(item)
   if rgb_assets:
       rgb_urls = item.get_band_urls(rgb_assets)
       print(f"RGB URLs obtained: {len(rgb_urls)} bands")

Getting URLs and Reading Data
-----------------------------

URL Generation
~~~~~~~~~~~~~~

Get ready-to-use URLs from items:

.. code-block:: python

   # Get URL for a specific asset
   item = items[0]
   red_url = item.get_asset_url('B04')  # or 'red' for EarthSearch
   print(f"Red band URL: {red_url[:60]}...")
   
   # Get URLs for multiple assets
   rgb_urls = item.get_band_urls(['B04', 'B03', 'B02'])
   print(f"RGB URLs: {len(rgb_urls)} bands")
   
   # Get all available URLs
   all_urls = item.get_all_asset_urls()
   print(f"All URLs: {len(all_urls)} assets")

Reading Data with Different Libraries
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The URLs work with any raster reading library:

.. code-block:: python

   # Option 1: rioxarray (recommended)
   try:
       import rioxarray as rxr
       
       red_data = rxr.open_rasterio(red_url)
       print(f"rioxarray - Shape: {red_data.shape}, CRS: {red_data.rio.crs}")
       
   except ImportError:
       print("rioxarray not available. Install with: pip install rioxarray")
   
   # Option 2: rasterio
   try:
       import rasterio
       
       with rasterio.open(red_url) as src:
           red_array = src.read(1)  # Read first band
           print(f"rasterio - Shape: {red_array.shape}, CRS: {src.crs}")
           
   except ImportError:
       print("rasterio not available. Install with: pip install rasterio")
   
   # Option 3: GDAL
   try:
       from osgeo import gdal
       
       dataset = gdal.Open(red_url)
       red_gdal = dataset.ReadAsArray()
       print(f"GDAL - Shape: {red_gdal.shape}")
       
   except ImportError:
       print("GDAL not available")

Basic Analysis Example
~~~~~~~~~~~~~~~~~~~~~~

Calculate NDVI (Normalized Difference Vegetation Index):

.. code-block:: python

   import rioxarray as rxr
   import numpy as np
   
   # Get NIR and Red band URLs
   nir_url = item.get_asset_url('B08')  # NIR
   red_url = item.get_asset_url('B04')  # Red
   
   # Load the data
   nir = rxr.open_rasterio(nir_url)
   red = rxr.open_rasterio(red_url)
   
   # Calculate NDVI
   ndvi = (nir - red) / (nir + red)
   
   # Basic statistics
   print(f"NDVI Statistics:")
   print(f"  Mean: {ndvi.mean().values:.3f}")
   print(f"  Min: {ndvi.min().values:.3f}")
   print(f"  Max: {ndvi.max().values:.3f}")
   
   # Save result (optional)
   ndvi.rio.to_raster('ndvi_result.tif')
   print("NDVI saved to ndvi_result.tif")

Quality Filtering
-----------------

Cloud Cover Filtering
~~~~~~~~~~~~~~~~~~~~~

Filter data by quality metrics:

.. code-block:: python

   from open_geodata_api.utils import filter_by_cloud_cover
   
   # Search for data
   results = pc.search(
       collections=['sentinel-2-l2a'],
       bbox=[-122.5, 47.5, -122.0, 48.0],
       datetime='2024-06-01/2024-08-31',
       limit=50
   )
   
   items = results.get_all_items()
   print(f"Initial results: {len(items)} items")
   
   # Filter by cloud cover
   clear_items = filter_by_cloud_cover(items, max_cloud_cover=20)
   print(f"Clear items (< 20% clouds): {len(clear_items)} items")
   
   # Show cloud cover distribution
   cloud_covers = [item.properties.get('eo:cloud_cover', 0) for item in items]
   print(f"Cloud cover range: {min(cloud_covers):.1f}% to {max(cloud_covers):.1f}%")

Advanced Search Filters
~~~~~~~~~~~~~~~~~~~~~~~

Use query parameters for advanced filtering:

.. code-block:: python

   # Search with quality filters in the query
   results = pc.search(
       collections=['sentinel-2-l2a'],
       bbox=[-122.5, 47.5, -122.0, 48.0],
       datetime='2024-06-01/2024-08-31',
       query={
           'eo:cloud_cover': {'lt': 25},          # Less than 25% clouds
           'platform': {'eq': 'sentinel-2a'},     # Only Sentinel-2A
           's2:processing_baseline': {'gte': '04.00'}  # Recent processing
       },
       limit=20
   )
   
   items = results.get_all_items()
   print(f"Filtered search: {len(items)} high-quality items")

Data Organization and Download
------------------------------

Understanding Download Options
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Open Geodata API provides multiple download approaches:

.. code-block:: python

   from open_geodata_api.utils import download_datasets
   
   # Option 1: Download specific assets only
   download_results = download_datasets(
       clear_items[:5],                    # First 5 clear items
       destination="./rgb_data/",
       asset_keys=['B04', 'B03', 'B02'],  # RGB bands only
       create_folders=True                 # Organize in folders
   )
   
   print(f"Downloaded {len(download_results)} items to ./rgb_data/")

Folder Organization
~~~~~~~~~~~~~~~~~~~

Understand how downloads are organized:

.. code-block:: text

   ./rgb_data/
   ├── S2A_MSIL2A_20240615T180921_N0510_R027_T11ULA_20240616T000511/
   │   ├── B04.tif
   │   ├── B03.tif
   │   └── B02.tif
   ├── S2B_MSIL2A_20240618T180919_N0510_R027_T11ULA_20240618T213456/
   │   ├── B04.tif
   │   ├── B03.tif
   │   └── B02.tif
   └── ...

Progress Tracking
~~~~~~~~~~~~~~~~~

Monitor download progress:

.. code-block:: python

   # Downloads show progress automatically
   download_results = download_datasets(
       clear_items,
       destination="./monitored_download/",
       asset_keys=['B08', 'B04'],  # For NDVI analysis
       show_progress=True,         # Show progress bars
       max_workers=4              # Parallel downloads
   )

Common Workflow Patterns
------------------------

Pattern 1: Data Discovery
~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   def discover_data(area_bbox, time_period, max_cloud_cover=30):
       """Discover available satellite data for an area and time."""
       
       # Search both providers
       pc = ogapi.planetary_computer(auto_sign=True)
       es = ogapi.earth_search()
       
       providers_data = {}
       
       for name, client in [('PC', pc), ('ES', es)]:
           try:
               results = client.search(
                   collections=['sentinel-2-l2a'],
                   bbox=area_bbox,
                   datetime=time_period,
                   query={'eo:cloud_cover': {'lt': max_cloud_cover}},
                   limit=50
               )
               
               items = results.get_all_items()
               providers_data[name] = {
                   'count': len(items),
                   'cloud_cover_range': [
                       min([i.properties.get('eo:cloud_cover', 0) for i in items]),
                       max([i.properties.get('eo:cloud_cover', 0) for i in items])
                   ] if items else [0, 0],
                   'date_range': [
                       min([i.properties['datetime'] for i in items])[:10],
                       max([i.properties['datetime'] for i in items])[:10]
                   ] if items else ['N/A', 'N/A']
               }
               
           except Exception as e:
               providers_data[name] = {'error': str(e)}
       
       return providers_data
   
   # Use the discovery function
   data_availability = discover_data(
       area_bbox=[-122.5, 47.5, -122.0, 48.0],
       time_period='2024-06-01/2024-08-31'
   )
   
   for provider, data in data_availability.items():
       print(f"{provider}: {data}")

Pattern 2: Quality Assessment
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   def assess_data_quality(items):
       """Assess the quality of a collection of items."""
       
       if not items:
           return {"error": "No items to assess"}
       
       # Extract quality metrics
       cloud_covers = [item.properties.get('eo:cloud_cover', 0) for item in items]
       dates = [item.properties['datetime'][:10] for item in items]
       platforms = [item.properties.get('platform', 'unknown') for item in items]
       
       # Calculate statistics
       assessment = {
           'total_items': len(items),
           'cloud_cover': {
               'mean': sum(cloud_covers) / len(cloud_covers),
               'min': min(cloud_covers),
               'max': max(cloud_covers),
               'excellent': len([cc for cc in cloud_covers if cc < 10]),
               'good': len([cc for cc in cloud_covers if 10 <= cc < 25]),
               'fair': len([cc for cc in cloud_covers if 25 <= cc < 50]),
               'poor': len([cc for cc in cloud_covers if cc >= 50])
           },
           'temporal': {
               'start_date': min(dates),
               'end_date': max(dates),
               'date_range_days': (
                   pd.to_datetime(max(dates)) - pd.to_datetime(min(dates))
               ).days
           },
           'platforms': dict(pd.Series(platforms).value_counts())
       }
       
       return assessment
   
   # Assess your data
   quality_report = assess_data_quality(items)
   print(f"Quality Assessment:")
   print(f"  Total items: {quality_report['total_items']}")
   print(f"  Excellent quality: {quality_report['cloud_cover']['excellent']} items")
   print(f"  Date range: {quality_report['temporal']['date_range_days']} days")

Pattern 3: Progressive Download
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   def progressive_download(items, destination, batch_size=5):
       """Download data progressively in small batches."""
       
       total_batches = (len(items) + batch_size - 1) // batch_size
       all_results = {}
       
       for i in range(0, len(items), batch_size):
           batch_num = i // batch_size + 1
           batch = items[i:i + batch_size]
           
           print(f"Downloading batch {batch_num}/{total_batches} ({len(batch)} items)")
           
           try:
               batch_results = download_datasets(
                   batch,
                   destination=f"{destination}/batch_{batch_num}/",
                   asset_keys=['B04', 'B03', 'B02'],
                   create_folders=True
               )
               
               all_results.update(batch_results)
               print(f"✅ Batch {batch_num} completed")
               
           except Exception as e:
               print(f"❌ Batch {batch_num} failed: {e}")
               continue
       
       return all_results
   
   # Use progressive download for large datasets
   download_results = progressive_download(
       clear_items, 
       destination="./progressive_download/",
       batch_size=3
   )

Command Line Basics
-------------------

Essential CLI Commands
~~~~~~~~~~~~~~~~~~~~~~

Get started with the command-line interface:

.. code-block:: bash

   # Check installation
   ogapi --version
   
   # List available collections
   ogapi collections list --provider pc
   
   # Search for data
   ogapi search items \
     --collections sentinel-2-l2a \
     --bbox "-122.5,47.5,-122.0,48.0" \
     --datetime "2024-06-01/2024-08-31" \
     --cloud-cover 25 \
     --output my_search.json
   
   # Filter results
   ogapi utils filter-clouds my_search.json \
     --max-cloud-cover 15 \
     --output clear_results.json
   
   # Download data
   ogapi download search-results clear_results.json \
     --assets "B04,B03,B02" \
     --destination "./cli_downloads/"

Getting Help
~~~~~~~~~~~~

.. code-block:: bash

   # General help
   ogapi --help
   
   # Command-specific help
   ogapi search --help
   ogapi download --help
   
   # Subcommand help
   ogapi search items --help
   ogapi utils filter-clouds --help

Next Steps and Best Practices
-----------------------------

Best Practices for Beginners
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

1. **Start Small**: Begin with small areas and short time periods
2. **Filter Early**: Use cloud cover filters to get quality data
3. **Check Provider Differences**: Understand asset naming conventions
4. **Monitor Progress**: Use progress bars for downloads
5. **Organize Data**: Use consistent folder structures

Performance Tips
~~~~~~~~~~~~~~~~

1. **Use Appropriate Limits**: Don't request more data than you need
2. **Cache Results**: Save search results to avoid repeated API calls
3. **Parallel Processing**: Use multiple workers for downloads
4. **Preview First**: Use overview levels for initial data exploration

Common Mistakes to Avoid
~~~~~~~~~~~~~~~~~~~~~~~~

1. **Wrong Bbox Order**: Remember [west, south, east, north]
2. **Large Initial Searches**: Start small, then scale up
3. **Ignoring Cloud Cover**: Always filter by quality
4. **Mixed Asset Names**: Be consistent with provider naming conventions
5. **No Progress Monitoring**: Always monitor long-running operations

Ready for More?
~~~~~~~~~~~~~~~

You've completed the first steps! Continue your journey:

- :doc:`../examples/index` - Real-world examples and advanced workflows
- :doc:`../cli-reference/index` - Complete CLI documentation
- :doc:`../api-reference/index` - Detailed API reference
- :doc:`../faq/index` - Frequently asked questions and troubleshooting

**Congratulations!** 🎉 You now understand the fundamentals of Open Geodata API and are ready to explore satellite data with confidence!
