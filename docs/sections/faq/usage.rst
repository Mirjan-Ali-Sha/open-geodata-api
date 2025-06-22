Usage FAQ
=========

Basic Usage Questions
---------------------

How do I get started with the API?
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Q**: I've installed the package, now what?

**A**: Follow this basic workflow:

.. code-block:: python

   # 1. Import and create clients
   import open_geodata_api as ogapi
   
   pc = ogapi.planetary_computer(auto_sign=True)
   es = ogapi.earth_search()
   
   # 2. Explore available data
   collections = pc.list_collections()
   print(f"Available collections: {len(collections)}")
   
   # 3. Search for data
   results = pc.search(
       collections=['sentinel-2-l2a'],
       bbox=[-122.5, 47.5, -122.0, 48.0],  # Your area
       datetime='2024-06-01/2024-08-31',
       limit=5
   )
   
   # 4. Get items and URLs
   items = results.get_all_items()
   item = items[0]
   urls = item.get_all_asset_urls()
   
   # 5. Use URLs with your preferred library
   import rioxarray
   data = rioxarray.open_rasterio(urls['B04'])

Which provider should I use?
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Q**: When should I use Planetary Computer vs EarthSearch?

**A**: Choose based on your needs:

**Use Planetary Computer when:**
- You need comprehensive data coverage
- Performance is important (faster with auto-signing)
- You're okay with authentication requirements
- You want the latest datasets and processing levels

**Use EarthSearch when:**
- You prefer no authentication
- You're doing quick exploration or testing
- You need specific open datasets
- You want to avoid API quotas/limits

**Example comparison:**

.. code-block:: python

   # Quick comparison
   pc_results = pc.search(collections=['sentinel-2-l2a'], limit=10)
   es_results = es.search(collections=['sentinel-2-l2a'], limit=10)
   
   print(f"PC found: {len(pc_results.get_all_items())} items")
   print(f"ES found: {len(es_results.get_all_items())} items")

How do I handle different asset names?
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Q**: Asset names are different between providers. How do I write portable code?

**A**: Use these patterns for provider-agnostic code:

.. code-block:: python

   def get_rgb_assets(item):
       """Get RGB assets regardless of provider."""
       assets = item.list_assets()
       
       # Planetary Computer naming
       if all(band in assets for band in ['B04', 'B03', 'B02']):
           return ['B04', 'B03', 'B02']  # Red, Green, Blue
       
       # EarthSearch naming
       elif all(band in assets for band in ['red', 'green', 'blue']):
           return ['red', 'green', 'blue']
       
       else:
           # Show available options
           print(f"Available assets: {assets}")
           return None
   
   # Usage
   rgb_bands = get_rgb_assets(item)
   if rgb_bands:
       urls = item.get_band_urls(rgb_bands)

Search and Discovery
--------------------

Why is my search returning no results?
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Q**: My search returns empty results even though I expect data

**A**: Check these common issues:

**1. Bbox format:**

.. code-block:: python

   # Correct: [west, south, east, north]
   bbox = [-122.5, 47.5, -122.0, 48.0]  # ✓ Correct
   
   # Common mistakes:
   bbox = [47.5, -122.5, 48.0, -122.0]  # ✗ lat/lon swapped
   bbox = [-122.0, 47.5, -122.5, 48.0]  # ✗ west > east

**2. Date format:**

.. code-block:: python

   # Correct formats:
   datetime = "2024-06-01/2024-08-31"     # ✓ Date range
   datetime = "2024-06-15"                # ✓ Single date
   
   # Common mistakes:
   datetime = "06/01/2024"                # ✗ Wrong format
   datetime = "2024-06-01 to 2024-08-31"  # ✗ Wrong separator

**3. Collection names:**

.. code-block:: python

   # Check available collections first
   collections = pc.list_collections()
   sentinel_collections = [c for c in collections if 'sentinel' in c.lower()]
   print(f"Sentinel collections: {sentinel_collections}")

**4. Too restrictive filters:**

.. code-block:: python

   # Start broad, then narrow down
   results = pc.search(
       collections=['sentinel-2-l2a'],
       bbox=your_bbox,
       datetime='2024-01-01/2024-12-31',  # Full year
       query={'eo:cloud_cover': {'lt': 80}},  # Relaxed cloud filter
       limit=50
   )

How do I find data for my specific location?
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Q**: How do I determine the right bounding box for my area of interest?

**A**: Use these methods:

**1. Online tools:**

.. code-block:: text

   # Use bboxfinder.com or geojson.io
   # 1. Navigate to your area
   # 2. Draw a rectangle
   # 3. Copy the bbox coordinates

**2. From place names:**

.. code-block:: python

   # Using geocoding (requires geopy)
   from geopy.geocoders import Nominatim
   
   geolocator = Nominatim(user_agent="my_app")
   location = geolocator.geocode("Seattle, WA")
   
   # Create small bbox around point
   lat, lon = location.latitude, location.longitude
   buffer = 0.05  # degrees
   bbox = [lon - buffer, lat - buffer, lon + buffer, lat + buffer]

**3. From existing data:**

.. code-block:: python

   # If you have a shapefile or geojson
   import geopandas as gpd
   
   gdf = gpd.read_file("my_study_area.shp")
   bbox = gdf.total_bounds  # [minx, miny, maxx, maxy]

How do I filter by data quality?
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Q**: How do I ensure I get high-quality satellite imagery?

**A**: Use these filtering strategies:

**1. Cloud cover filtering:**

.. code-block:: python

   # Built-in cloud filter
   results = pc.search(
       collections=['sentinel-2-l2a'],
       bbox=your_bbox,
       query={'eo:cloud_cover': {'lt': 20}},  # Less than 20%
       limit=20
   )
   
   # Post-search filtering
   from open_geodata_api.utils import filter_by_cloud_cover
   
   all_items = results.get_all_items()
   clear_items = filter_by_cloud_cover(all_items, max_cloud_cover=15)

**2. Date-based quality:**

.. code-block:: python

   # Prefer recent data
   results = pc.search(
       collections=['sentinel-2-l2a'],
       bbox=your_bbox,
       datetime='2024-01-01/2024-12-31',  # Recent year
       limit=50
   )
   
   # Sort by date (most recent first)
   items = results.get_all_items()
   df = items.to_dataframe()
   df = df.sort_values('datetime', ascending=False)

**3. Multi-criteria filtering:**

.. code-block:: python

   # Combine multiple quality criteria
   def quality_filter(items, max_cloud=20, min_date='2024-01-01'):
       """Filter items by multiple quality criteria."""
       filtered = []
       
       for item in items:
           cloud_cover = item.properties.get('eo:cloud_cover', 100)
           date = item.properties.get('datetime', '')
           
           if cloud_cover <= max_cloud and date >= min_date:
               filtered.append(item)
       
       return filtered

Data Reading and Processing
---------------------------

How do I actually read the satellite data?
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Q**: I have URLs, but how do I load the actual raster data?

**A**: Use any raster reading library:

**1. With rioxarray (recommended):**

.. code-block:: python

   import rioxarray as rxr
   
   # Get URL from item
   url = item.get_asset_url('B04')  # Red band
   
   # Load data
   data = rxr.open_rasterio(url)
   
   # Basic operations
   print(f"Shape: {data.shape}")
   print(f"CRS: {data.rio.crs}")
   print(f"Bounds: {data.rio.bounds()}")
   
   # Calculate statistics
   mean_value = data.mean()
   print(f"Mean reflectance: {mean_value.values}")

**2. With rasterio:**

.. code-block:: python

   import rasterio
   
   with rasterio.open(url) as src:
       # Read full array
       data = src.read(1)  # First band
       
       # Read a subset
       window = rasterio.windows.Window(0, 0, 1000, 1000)
       subset = src.read(1, window=window)
       
       # Get metadata
       print(f"CRS: {src.crs}")
       print(f"Transform: {src.transform}")

**3. With GDAL:**

.. code-block:: python

   from osgeo import gdal
   
   # Open dataset
   ds = gdal.Open(url)
   
   # Read as array
   band = ds.GetRasterBand(1)
   data = band.ReadAsArray()
   
   # Get georeference info
   transform = ds.GetGeoTransform()
   projection = ds.GetProjection()

How do I calculate vegetation indices?
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Q**: How do I calculate NDVI and other indices?

**A**: Here's a complete example:

.. code-block:: python

   import rioxarray as rxr
   import numpy as np
   
   # Get NIR and Red bands
   urls = item.get_band_urls(['B08', 'B04'])  # NIR, Red for Sentinel-2
   
   # Load bands
   nir = rxr.open_rasterio(urls['B08'])
   red = rxr.open_rasterio(urls['B04'])
   
   # Calculate NDVI
   ndvi = (nir - red) / (nir + red)
   
   # Calculate other indices
   
   # EVI (Enhanced Vegetation Index)
   blue = rxr.open_rasterio(item.get_asset_url('B02'))
   evi = 2.5 * ((nir - red) / (nir + 6 * red - 7.5 * blue + 1))
   
   # SAVI (Soil Adjusted Vegetation Index)
   L = 0.5  # Soil brightness correction factor
   savi = ((nir - red) / (nir + red + L)) * (1 + L)
   
   # Save results
   ndvi.rio.to_raster('ndvi.tif')
   evi.rio.to_raster('evi.tif')

How do I handle large datasets efficiently?
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Q**: My code is slow when processing many scenes. How do I optimize?

**A**: Use these optimization strategies:

**1. Use chunks for large files:**

.. code-block:: python

   # Load with chunking
   data = rxr.open_rasterio(url, chunks={'x': 1024, 'y': 1024})
   
   # Operations are lazy until compute()
   ndvi = (data_nir - data_red) / (data_nir + data_red)
   result = ndvi.compute()  # Execute computation

**2. Use overview levels for preview:**

.. code-block:: python

   # Load lower resolution for preview
   data_preview = rxr.open_rasterio(url, overview_level=2)
   
   # Process preview first, then full resolution
   if data_preview.mean() > threshold:
       data_full = rxr.open_rasterio(url)

**3. Process in batches:**

.. code-block:: python

   def process_items_in_batches(items, batch_size=5):
       """Process items in smaller batches."""
       for i in range(0, len(items), batch_size):
           batch = items[i:i+batch_size]
           
           # Process this batch
           for item in batch:
               # Your processing code here
               pass
           
           # Clean up memory
           import gc
           gc.collect()

CLI Usage Questions
-------------------

How do I use the command-line interface?
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Q**: What's the basic CLI workflow?

**A**: Follow this command sequence:

.. code-block:: bash

   # 1. Check installation
   ogapi --version
   
   # 2. Explore collections
   ogapi collections list --provider pc
   
   # 3. Search for data
   ogapi search items \
     --collections sentinel-2-l2a \
     --bbox "-122.5,47.5,-122.0,48.0" \
     --datetime "2024-06-01/2024-08-31" \
     --cloud-cover 20 \
     --output search_results.json
   
   # 4. Filter results (optional)
   ogapi utils filter-clouds search_results.json \
     --max-cloud-cover 15 \
     --output filtered_results.json
   
   # 5. Download data
   ogapi download search-results filtered_results.json \
     --assets "B04,B03,B02" \
     --destination "./rgb_data/"

How do I automate workflows with the CLI?
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Q**: Can I create automated scripts with the CLI?

**A**: Yes, create shell scripts for automation:

.. code-block:: bash

   #!/bin/bash
   # automated_download.sh
   
   BBOX="-122.5,47.5,-122.0,48.0"
   DATE_RANGE="2024-06-01/2024-08-31"
   OUTPUT_DIR="./automated_download_$(date +%Y%m%d)"
   
   # Create output directory
   mkdir -p "$OUTPUT_DIR"
   
   # Search for data
   ogapi search items \
     --collections sentinel-2-l2a \
     --bbox "$BBOX" \
     --datetime "$DATE_RANGE" \
     --cloud-cover 25 \
     --output "$OUTPUT_DIR/search_results.json"
   
   # Check if data found
   if [ $? -eq 0 ]; then
       echo "Search successful, starting download..."
       
       # Download RGB bands
       ogapi download search-results "$OUTPUT_DIR/search_results.json" \
         --assets "B04,B03,B02" \
         --destination "$OUTPUT_DIR/rgb_data/"
       
       echo "Download completed: $OUTPUT_DIR"
   else
       echo "Search failed, check parameters"
   fi

Common Workflow Patterns
------------------------

How do I set up a monitoring workflow?
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Q**: I want to regularly check for new data in my area. How do I set this up?

**A**: Create a monitoring system:

.. code-block:: python

   import schedule
   import time
   from datetime import datetime, timedelta
   
   def daily_monitoring():
       """Check for new data daily."""
       
       # Search for yesterday's data
       yesterday = (datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d')
       
       results = pc.search(
           collections=['sentinel-2-l2a'],
           bbox=your_monitoring_bbox,
           datetime=f"{yesterday}/{yesterday}",
           query={'eo:cloud_cover': {'lt': 30}},
           limit=5
       )
       
       items = results.get_all_items()
       
       if items:
           print(f"Found {len(items)} new scenes for {yesterday}")
           # Process or download new data
       else:
           print(f"No new clear data for {yesterday}")
   
   # Schedule daily checks
   schedule.every().day.at("09:00").do(daily_monitoring)
   
   # Run the scheduler
   while True:
       schedule.run_pending()
       time.sleep(60)

How do I compare data between different sensors?
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Q**: I want to compare Sentinel-2 and Landsat data for the same area

**A**: Use this comparison approach:

.. code-block:: python

   def compare_sensors(bbox, date_range):
       """Compare data from different sensors."""
       
       # Search Sentinel-2
       s2_results = pc.search(
           collections=['sentinel-2-l2a'],
           bbox=bbox,
           datetime=date_range,
           query={'eo:cloud_cover': {'lt': 20}},
           limit=10
       )
       
       # Search Landsat
       landsat_results = pc.search(
           collections=['landsat-c2-l2'],
           bbox=bbox,
           datetime=date_range,
           query={'eo:cloud_cover': {'lt': 20}},
           limit=10
       )
       
       s2_items = s2_results.get_all_items()
       landsat_items = landsat_results.get_all_items()
       
       print(f"Sentinel-2: {len(s2_items)} scenes")
       print(f"Landsat: {len(landsat_items)} scenes")
       
       # Compare temporal coverage
       s2_dates = [item.properties['datetime'][:10] for item in s2_items]
       landsat_dates = [item.properties['datetime'][:10] for item in landsat_items]
       
       print(f"S2 date range: {min(s2_dates)} to {max(s2_dates)}")
       print(f"Landsat date range: {min(landsat_dates)} to {max(landsat_dates)}")
       
       return s2_items, landsat_items

Error Handling Best Practices
------------------------------

How should I handle errors in my code?
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Q**: What's the best way to handle errors when using the API?

**A**: Use comprehensive error handling:

.. code-block:: python

   def robust_search(pc, collections, bbox, **kwargs):
       """Search with robust error handling."""
       
       try:
           # Attempt search
           results = pc.search(
               collections=collections,
               bbox=bbox,
               **kwargs
           )
           
           items = results.get_all_items()
           
           if not items:
               print("No items found. Try adjusting search parameters:")
               print(f"  - Expand bbox: {bbox}")
               print(f"  - Extend date range")
               print(f"  - Increase cloud cover threshold")
               return None
           
           return items
           
       except Exception as e:
           print(f"Search failed: {e}")
           
           # Provide specific guidance
           if "Invalid collection" in str(e):
               available = pc.list_collections()
               print(f"Available collections: {available[:5]}...")
           
           elif "Invalid bbox" in str(e):
               print("Check bbox format: [west, south, east, north]")
           
           elif "Invalid datetime" in str(e):
               print("Check date format: YYYY-MM-DD or YYYY-MM-DD/YYYY-MM-DD")
           
           return None
   
   # Usage with error handling
   items = robust_search(
       pc, 
       ['sentinel-2-l2a'], 
       [-122.5, 47.5, -122.0, 48.0],
       datetime='2024-06-01/2024-08-31'
   )
   
   if items:
       print(f"Success: Found {len(items)} items")
   else:
       print("Search failed, check error messages above")
