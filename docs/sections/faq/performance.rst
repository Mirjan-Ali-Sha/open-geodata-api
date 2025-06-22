Performance FAQ
===============

This section addresses common performance questions and optimization strategies.

Search Performance
------------------

Why are my searches slow?
~~~~~~~~~~~~~~~~~~~~~~~~~

**Q**: Search operations are taking a long time to complete.

**A**: Several factors can affect search performance:

**Common Causes**:

1. **Large search areas**: Very large bounding boxes require more processing
2. **Long time ranges**: Searching across many years of data
3. **No filtering**: Not using cloud cover or other filters
4. **High result limits**: Requesting too many results at once

**Optimization Strategies**:

.. code-block:: python

   # ❌ Slow: Large area, long time, no filters
   results = pc.search(
       collections=['sentinel-2-l2a'],
       bbox=[-180, -90, 180, 90],        # Global search
       datetime='2015-01-01/2024-12-31', # 9+ years
       limit=1000                        # Many results
   )
   
   # ✅ Fast: Focused search with filters
   results = pc.search(
       collections=['sentinel-2-l2a'],
       bbox=[-122.5, 47.5, -122.0, 48.0],  # Small area
       datetime='2024-06-01/2024-08-31',    # 3 months
       query={'eo:cloud_cover': {'lt': 20}}, # Quality filter
       limit=20                             # Reasonable limit
   )

How can I make searches faster?
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Q**: What are the best practices for fast searches?

**A**: Use these optimization techniques:

**1. Geographic Optimization**:

.. code-block:: python

   # Use smaller, focused bounding boxes
   bbox = [-122.1, 47.6, -122.0, 47.7]  # ~10km area instead of large regions
   
   # If you need large areas, consider splitting into tiles
   def tile_search(large_bbox, tile_size=0.5):
       """Split large area into smaller search tiles."""
       west, south, east, north = large_bbox
       
       tiles = []
       x = west
       while x < east:
           y = south
           while y < north:
               tile_bbox = [x, y, min(x + tile_size, east), min(y + tile_size, north)]
               tiles.append(tile_bbox)
               y += tile_size
           x += tile_size
       
       return tiles

**2. Temporal Optimization**:

.. code-block:: python

   # Use specific time periods instead of large ranges
   recent_data = pc.search(
       collections=['sentinel-2-l2a'],
       datetime='2024-06-01/2024-06-30',  # 1 month vs 1 year
       limit=10
   )
   
   # For time series, search incrementally
   def incremental_search(bbox, start_year, end_year):
       """Search year by year for better performance."""
       all_items = []
       
       for year in range(start_year, end_year + 1):
           yearly_results = pc.search(
               collections=['sentinel-2-l2a'],
               bbox=bbox,
               datetime=f'{year}-01-01/{year}-12-31',
               query={'eo:cloud_cover': {'lt': 30}},
               limit=50
           )
           all_items.extend(yearly_results.get_all_items())
       
       return all_items

**3. Filter Early and Often**:

.. code-block:: python

   # Apply filters in the search query, not after
   results = pc.search(
       collections=['sentinel-2-l2a'],
       bbox=bbox,
       query={
           'eo:cloud_cover': {'lt': 20},      # Cloud filter
           'platform': {'eq': 'sentinel-2a'}, # Platform filter
           's2:processing_baseline': {'gte': '04.00'}  # Processing version
       },
       limit=20
   )

Data Loading Performance
------------------------

Why is data loading slow?
~~~~~~~~~~~~~~~~~~~~~~~~~

**Q**: Loading raster data from URLs is very slow.

**A**: Data loading performance depends on several factors:

**Common Issues**:

1. **Full resolution loading**: Loading entire high-resolution files
2. **Network latency**: Distance from data servers
3. **No chunking**: Loading data without optimization
4. **Expired URLs**: Re-signing overhead for Planetary Computer

**Optimization Solutions**:

.. code-block:: python

   # ❌ Slow: Loading full resolution
   import rioxarray as rxr
   data = rxr.open_rasterio(url)  # Loads entire file
   
   # ✅ Fast: Use overview levels for preview
   data_preview = rxr.open_rasterio(url, overview_level=2)  # 4x smaller
   
   # ✅ Fast: Use chunking for large files
   data_chunked = rxr.open_rasterio(url, chunks={'x': 1024, 'y': 1024})
   
   # ✅ Fast: Read specific windows
   import rasterio
   with rasterio.open(url) as src:
       # Read only part of the image
       window = rasterio.windows.Window(0, 0, 2048, 2048)
       data_subset = src.read(1, window=window)

How can I speed up data downloads?
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Q**: Downloading multiple files is taking too long.

**A**: Use these download optimization strategies:

**1. Parallel Downloads**:

.. code-block:: python

   from open_geodata_api.utils import download_datasets
   from concurrent.futures import ThreadPoolExecutor
   
   # Use parallel downloading (built into utils)
   results = download_datasets(
       items,
       destination="./data/",
       max_workers=4,  # Parallel downloads
       chunk_size=8192  # Optimal chunk size
   )
   
   # Custom parallel implementation
   def parallel_download_urls(urls_dict, destination, max_workers=4):
       """Download URLs in parallel."""
       
       def download_single(url_item):
           asset_name, url = url_item
           return download_url(url, f"{destination}/{asset_name}.tif")
       
       with ThreadPoolExecutor(max_workers=max_workers) as executor:
           results = list(executor.map(download_single, urls_dict.items()))
       
       return results

**2. Smart Asset Selection**:

.. code-block:: python

   # Download only needed assets
   rgb_only = download_datasets(
       items,
       asset_keys=['B04', 'B03', 'B02'],  # Only RGB
       destination="./rgb_data/"
   )
   
   # For analysis, download specific bands
   ndvi_bands = download_datasets(
       items,
       asset_keys=['B08', 'B04'],  # NIR + Red for NDVI
       destination="./ndvi_data/"
   )

**3. Resume Interrupted Downloads**:

.. code-block:: python

   # Use resume capability
   results = download_datasets(
       items,
       destination="./data/",
       resume=True,  # Skip existing files
       verify_size=True  # Check file completeness
   )

Memory Performance
------------------

Why am I running out of memory?
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Q**: My code crashes with memory errors when processing satellite data.

**A**: Satellite imagery files can be very large. Use these memory management strategies:

**Memory-Efficient Loading**:

.. code-block:: python

   # ❌ Memory intensive: Loading everything at once
   data_list = []
   for item in items:
       urls = item.get_band_urls(['B04', 'B03', 'B02'])
       for band, url in urls.items():
           data = rxr.open_rasterio(url)  # Loads into memory
           data_list.append(data)
   
   # ✅ Memory efficient: Lazy loading and processing
   def process_items_efficiently(items, batch_size=5):
       """Process items in memory-efficient batches."""
       
       for i in range(0, len(items), batch_size):
           batch = items[i:i+batch_size]
           
           # Process batch
           for item in batch:
               urls = item.get_band_urls(['B04', 'B03', 'B02'])
               
               # Use context manager for automatic cleanup
               with rxr.open_rasterio(urls['B04'], chunks={'x': 512, 'y': 512}) as data:
                   # Process data
                   result = data.mean()
                   print(f"Mean value: {result.values}")
               
               # Data automatically freed
           
           # Force garbage collection between batches
           import gc
           gc.collect()

**Chunking and Dask**:

.. code-block:: python

   # Use chunking for large datasets
   import dask.array as da
   
   # Load with chunking
   data = rxr.open_rasterio(url, chunks={'x': 1024, 'y': 1024})
   
   # Operations are lazy until compute()
   mean_value = data.mean().compute()
   
   # Process multiple files with Dask
   def process_with_dask(urls_list):
       """Process multiple files efficiently with Dask."""
       
       # Load all files as Dask arrays
       arrays = []
       for url in urls_list:
           arr = da.from_array(rxr.open_rasterio(url, chunks={'x': 512, 'y': 512}))
           arrays.append(arr)
       
       # Stack arrays
       stacked = da.stack(arrays, axis=0)
       
       # Compute statistics efficiently
       mean_stack = stacked.mean(axis=0).compute()
       
       return mean_stack

How can I monitor memory usage?
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Q**: How do I track memory usage in my workflows?

**A**: Use these monitoring techniques:

.. code-block:: python

   import psutil
   import os
   
   def monitor_memory():
       """Monitor current memory usage."""
       process = psutil.Process(os.getpid())
       memory_info = process.memory_info()
       
       return {
           'rss_mb': memory_info.rss / 1024 / 1024,  # Resident Set Size
           'vms_mb': memory_info.vms / 1024 / 1024,  # Virtual Memory Size
           'percent': process.memory_percent()
       }
   
   # Monitor during processing
   def process_with_monitoring(items):
       """Process items with memory monitoring."""
       
       initial_memory = monitor_memory()
       print(f"Initial memory: {initial_memory['rss_mb']:.1f} MB")
       
       for i, item in enumerate(items):
           # Process item
           urls = item.get_all_asset_urls()
           
           # Check memory every 5 items
           if i % 5 == 0:
               current_memory = monitor_memory()
               memory_increase = current_memory['rss_mb'] - initial_memory['rss_mb']
               print(f"Item {i}: Memory usage: {current_memory['rss_mb']:.1f} MB (+{memory_increase:.1f} MB)")
               
               # Warning if memory usage is too high
               if current_memory['percent'] > 80:
                   print("⚠️ High memory usage detected!")

Network Performance
-------------------

How can I optimize for slow internet connections?
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Q**: My internet connection is slow. How can I optimize data access?

**A**: Use these strategies for slow connections:

**1. Use Overview Levels**:

.. code-block:: python

   # Download lower resolution for initial analysis
   def preview_workflow(items):
       """Fast preview workflow for slow connections."""
       
       for item in items:
           urls = item.get_band_urls(['B04', 'B03', 'B02'])
           
           # Load low-resolution preview (much smaller download)
           for band, url in urls.items():
               preview = rxr.open_rasterio(url, overview_level=3)  # 8x smaller
               print(f"{band} preview shape: {preview.shape}")

**2. Smart Caching**:

.. code-block:: python

   # Cache frequently accessed data
   import os
   from pathlib import Path
   
   def cached_data_access(url, cache_dir="./cache/"):
       """Access data with local caching."""
       
       # Create cache filename from URL
       cache_file = Path(cache_dir) / f"{hash(url)}.tif"
       cache_file.parent.mkdir(exist_ok=True)
       
       if cache_file.exists():
           print(f"Loading from cache: {cache_file}")
           return rxr.open_rasterio(str(cache_file))
       else:
           print(f"Downloading and caching: {url}")
           data = rxr.open_rasterio(url)
           data.rio.to_raster(str(cache_file))
           return data

**3. Bandwidth-Aware Processing**:

.. code-block:: python

   def bandwidth_aware_download(items, connection_speed='slow'):
       """Adjust download strategy based on connection speed."""
       
       if connection_speed == 'slow':
           # Download only essential bands
           asset_keys = ['B04', 'B08']  # Red + NIR for NDVI
           batch_size = 1  # Process one at a time
           overview_level = 2  # Lower resolution
           
       elif connection_speed == 'medium':
           asset_keys = ['B04', 'B03', 'B02', 'B08']  # RGB + NIR
           batch_size = 3
           overview_level = 1
           
       else:  # fast
           asset_keys = None  # All assets
           batch_size = 5
           overview_level = 0  # Full resolution
       
       return download_datasets(
           items,
           asset_keys=asset_keys,
           batch_size=batch_size,
           overview_level=overview_level
       )

Scaling and Large Datasets
---------------------------

How do I process thousands of scenes efficiently?
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Q**: I need to process thousands of satellite scenes. What's the best approach?

**A**: Use these scaling strategies:

**1. Hierarchical Processing**:

.. code-block:: python

   def hierarchical_processing(large_area_bbox, years):
       """Process large datasets hierarchically."""
       
       # Level 1: Overview analysis
       overview_results = {}
       
       for year in years:
           # Search with broad filters
           results = pc.search(
               collections=['sentinel-2-l2a'],
               bbox=large_area_bbox,
               datetime=f'{year}-01-01/{year}-12-31',
               query={'eo:cloud_cover': {'lt': 50}},  # Relaxed filter
               limit=100
           )
           
           # Quick quality assessment
           items = results.get_all_items()
           quality_items = filter_by_cloud_cover(items, max_cloud_cover=20)
           
           overview_results[year] = {
               'total_scenes': len(items),
               'quality_scenes': len(quality_items),
               'best_scenes': quality_items[:10]  # Top 10 for detailed analysis
           }
       
       # Level 2: Detailed processing of selected scenes
       for year, data in overview_results.items():
           if data['quality_scenes'] > 5:  # Only process years with good data
               process_detailed_analysis(data['best_scenes'])

**2. Distributed Processing**:

.. code-block:: python

   # Use Dask for distributed processing
   import dask
   from dask.distributed import Client
   
   def setup_distributed_processing():
       """Setup Dask cluster for large-scale processing."""
       
       # Local cluster
       client = Client('localhost:8786')
       
       # Or cloud cluster
       # client = Client('scheduler-address:8786')
       
       return client
   
   @dask.delayed
   def process_single_scene(item):
       """Process a single scene (Dask delayed function)."""
       urls = item.get_band_urls(['B08', 'B04'])
       
       # Load and process
       nir = rxr.open_rasterio(urls['B08'])
       red = rxr.open_rasterio(urls['B04'])
       
       # Calculate NDVI
       ndvi = (nir - red) / (nir + red)
       
       return {
           'item_id': item.id,
           'mean_ndvi': float(ndvi.mean()),
           'date': item.properties['datetime'][:10]
       }
   
   def process_large_dataset(items):
       """Process large dataset with Dask."""
       
       # Create delayed computations
       delayed_results = [process_single_scene(item) for item in items]
       
       # Compute in parallel
       results = dask.compute(*delayed_results)
       
       return list(results)

**3. Progressive Processing**:

.. code-block:: python

   def progressive_processing(items, checkpoint_interval=50):
       """Process with regular checkpoints for resumability."""
       
       results = []
       checkpoint_file = "processing_checkpoint.json"
       
       # Load previous progress
       start_index = 0
       if os.path.exists(checkpoint_file):
           with open(checkpoint_file, 'r') as f:
               checkpoint_data = json.load(f)
               start_index = checkpoint_data['last_processed_index']
               results = checkpoint_data['results']
           print(f"Resuming from item {start_index}")
       
       # Process remaining items
       for i in range(start_index, len(items)):
           try:
               # Process item
               result = process_single_item(items[i])
               results.append(result)
               
               # Save checkpoint
               if (i + 1) % checkpoint_interval == 0:
                   checkpoint_data = {
                       'last_processed_index': i + 1,
                       'results': results
                   }
                   with open(checkpoint_file, 'w') as f:
                       json.dump(checkpoint_data, f)
                   print(f"Checkpoint saved at item {i + 1}")
           
           except Exception as e:
               print(f"Error processing item {i}: {e}")
               continue
       
       return results

Performance Monitoring
----------------------

How do I benchmark my workflows?
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Q**: How can I measure and optimize the performance of my satellite data workflows?

**A**: Use these benchmarking techniques:

.. code-block:: python

   import time
   import psutil
   from contextlib import contextmanager
   
   @contextmanager
   def performance_monitor(operation_name):
       """Monitor performance of code blocks."""
       
       # Start monitoring
       start_time = time.time()
       start_memory = psutil.Process().memory_info().rss / 1024 / 1024
       
       print(f"Starting {operation_name}...")
       
       try:
           yield
       finally:
           # End monitoring
           end_time = time.time()
           end_memory = psutil.Process().memory_info().rss / 1024 / 1024
           
           duration = end_time - start_time
           memory_change = end_memory - start_memory
           
           print(f"✅ {operation_name} completed:")
           print(f"   Duration: {duration:.2f} seconds")
           print(f"   Memory change: {memory_change:+.1f} MB")
   
   # Usage
   with performance_monitor("Data search"):
       results = pc.search(collections=['sentinel-2-l2a'], limit=20)
   
   with performance_monitor("URL generation"):
       items = results.get_all_items()
       urls = [item.get_all_asset_urls() for item in items]
   
   with performance_monitor("Data download"):
       download_results = download_datasets(items[:5])

Performance Best Practices Summary
-----------------------------------

**Search Optimization**:
- Use small bounding boxes and short time ranges
- Apply filters early in the search query
- Limit results to what you actually need

**Data Loading Optimization**:
- Use overview levels for previews
- Implement chunking for large files
- Load only required bands/assets

**Memory Management**:
- Process data in batches
- Use lazy loading (Dask, chunked arrays)
- Implement proper cleanup between operations

**Network Optimization**:
- Cache frequently accessed data
- Use parallel downloads with rate limiting
- Choose appropriate chunk sizes

**Scaling Strategies**:
- Use hierarchical processing approaches
- Implement checkpointing for long-running jobs
- Consider distributed computing for very large datasets

These optimization strategies will help you build efficient, scalable satellite data processing workflows.
