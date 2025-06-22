Troubleshooting Guide
====================

This comprehensive guide helps you resolve common issues when using Open Geodata API.

Installation Problems
---------------------

Package Installation Fails
~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Symptom**: ``pip install open-geodata-api`` fails

**Common Causes & Solutions**:

.. code-block:: bash

   # 1. Update pip and try again
   pip install --upgrade pip setuptools wheel
   pip install open-geodata-api
   
   # 2. Use virtual environment
   python -m venv ogapi_env
   source ogapi_env/bin/activate  # Linux/Mac
   pip install open-geodata-api
   
   # 3. Install without cache
   pip install --no-cache-dir open-geodata-api
   
   # 4. Install specific version
   pip install open-geodata-api==0.1.0

Dependency Conflicts
~~~~~~~~~~~~~~~~~~~~

**Symptom**: Conflicting requirements during installation

**Solutions**:

.. code-block:: bash

   # Create fresh environment
   python -m venv fresh_env
   source fresh_env/bin/activate
   pip install open-geodata-api[complete]
   
   # Use conda for geospatial dependencies
   conda create -n ogapi python=3.9
   conda activate ogapi
   conda install -c conda-forge rasterio geopandas
   pip install open-geodata-api

Geospatial Library Issues
~~~~~~~~~~~~~~~~~~~~~~~~~

**Symptom**: GDAL, rasterio, or geopandas installation fails

**Platform-Specific Solutions**:

.. code-block:: bash

   # Windows
   conda install -c conda-forge rasterio geopandas
   pip install open-geodata-api
   
   # macOS (especially M1/M2)
   brew install gdal
   pip install rasterio geopandas
   pip install open-geodata-api
   
   # Ubuntu/Debian Linux
   sudo apt-get install gdal-bin libgdal-dev
   pip install open-geodata-api[complete]

API Access Issues
-----------------

Authentication Problems
~~~~~~~~~~~~~~~~~~~~~~~

**Symptom**: Authentication errors with Planetary Computer

**Diagnostic Steps**:

.. code-block:: python

   # Test basic authentication
   try:
       import planetary_computer as pc
       print("planetary-computer package available")
       
       # Test signing capability
       test_url = "https://example.com/test.tif"
       signed = pc.sign_url(test_url)
       print("URL signing works")
       
   except ImportError:
       print("Install: pip install planetary-computer")
   except Exception as e:
       print(f"Authentication issue: {e}")

**Solutions**:

.. code-block:: bash

   # Install planetary-computer package
   pip install planetary-computer
   
   # Verify installation
   python -c "import planetary_computer; print('Success')"

Connection Timeouts
~~~~~~~~~~~~~~~~~~~

**Symptom**: Requests timeout or connection errors

**Solutions**:

.. code-block:: python

   # Increase timeout settings
   import open_geodata_api as ogapi
   
   # Create client with extended timeout
   pc = ogapi.planetary_computer(auto_sign=True)
   
   # Test connection
   try:
       collections = pc.list_collections()
       print(f"Connection successful: {len(collections)} collections")
   except Exception as e:
       print(f"Connection failed: {e}")
       print("Check internet connection and API status")

**Network Diagnostics**:

.. code-block:: bash

   # Test API endpoints
   curl -I https://planetarycomputer.microsoft.com/api/stac/v1/
   curl -I https://earth-search.aws.element84.com/v1/
   
   # Check DNS resolution
   nslookup planetarycomputer.microsoft.com
   nslookup earth-search.aws.element84.com

Search Problems
---------------

No Results Found
~~~~~~~~~~~~~~~~

**Symptom**: Search returns empty results unexpectedly

**Diagnostic Checklist**:

.. code-block:: python

   def diagnose_search_issue(bbox, datetime, collections):
       """Systematic diagnosis of search issues."""
       
       print("=== Search Diagnosis ===")
       
       # 1. Validate bbox format
       if len(bbox) != 4:
           print("❌ Invalid bbox: must have 4 values [west, south, east, north]")
           return
       
       west, south, east, north = bbox
       if west >= east or south >= north:
           print("❌ Invalid bbox: west >= east or south >= north")
           return
       
       print(f"✅ Bbox format valid: {bbox}")
       
       # 2. Check collection names
       pc = ogapi.planetary_computer()
       available_collections = pc.list_collections()
       
       for collection in collections:
           if collection not in available_collections:
               print(f"❌ Invalid collection: {collection}")
               similar = [c for c in available_collections if collection.lower() in c.lower()]
               if similar:
                   print(f"   Did you mean: {similar[:3]}")
           else:
               print(f"✅ Collection valid: {collection}")
       
       # 3. Test with relaxed criteria
       try:
           results = pc.search(
               collections=collections,
               bbox=bbox,
               datetime=datetime,
               query={'eo:cloud_cover': {'lt': 90}},  # Very relaxed
               limit=50
           )
           
           items = results.get_all_items()
           print(f"✅ Relaxed search found: {len(items)} items")
           
           if len(items) > 0:
               print("🔍 Try relaxing your cloud cover or date constraints")
           
       except Exception as e:
           print(f"❌ Search failed: {e}")

   # Usage
   diagnose_search_issue(
       bbox=[-122.5, 47.5, -122.0, 48.0],
       datetime='2024-01-01/2024-12-31',
       collections=['sentinel-2-l2a']
   )

**Common Fixes**:

.. code-block:: python

   # 1. Expand search area
   bbox = [-123.0, 47.0, -121.0, 49.0]  # Larger area
   
   # 2. Extend time range
   datetime = '2023-01-01/2024-12-31'  # Longer period
   
   # 3. Relax cloud cover
   query = {'eo:cloud_cover': {'lt': 80}}  # More permissive
   
   # 4. Increase limit
   limit = 100  # More results

Invalid Date Formats
~~~~~~~~~~~~~~~~~~~~

**Symptom**: Date-related errors in search

**Correct Formats**:

.. code-block:: python

   # Valid datetime formats
   valid_formats = [
       "2024-06-15",                    # Single date
       "2024-06-01/2024-06-30",         # Date range
       "2024-06-15T10:00:00Z",          # ISO format with time
       "2024-01-01T00:00:00Z/2024-12-31T23:59:59Z"  # Full ISO range
   ]
   
   # Invalid formats that cause errors
   invalid_formats = [
       "06/15/2024",                    # US format
       "15-06-2024",                    # European format
       "2024-6-15",                     # Missing zero padding
       "2024-06-01 to 2024-06-30",     # Wrong separator
   ]

Bbox Coordinate Issues
~~~~~~~~~~~~~~~~~~~~~~

**Symptom**: "Invalid bbox" or unexpected geographic results

**Common Mistakes**:

.. code-block:: python

   # ❌ Common bbox mistakes
   wrong_order = [47.5, -122.5, 48.0, -122.0]  # lat/lon swapped
   inverted = [-122.0, 47.5, -122.5, 48.0]     # west > east
   
   # ✅ Correct format: [west, south, east, north]
   correct_bbox = [-122.5, 47.5, -122.0, 48.0]

**Bbox Validation Function**:

.. code-block:: python

   def validate_bbox(bbox):
       """Validate bbox format and values."""
       if not isinstance(bbox, (list, tuple)) or len(bbox) != 4:
           return False, "Bbox must be [west, south, east, north]"
       
       west, south, east, north = bbox
       
       if not (-180 <= west <= 180 and -180 <= east <= 180):
           return False, "Longitude must be between -180 and 180"
       
       if not (-90 <= south <= 90 and -90 <= north <= 90):
           return False, "Latitude must be between -90 and 90"
       
       if west >= east:
           return False, "West coordinate must be less than east"
       
       if south >= north:
           return False, "South coordinate must be less than north"
       
       return True, "Valid bbox"

Data Access Problems
--------------------

URL Expiration Issues
~~~~~~~~~~~~~~~~~~~~~

**Symptom**: 403 Forbidden errors or "Access Denied"

**Diagnosis**:

.. code-block:: python

   from open_geodata_api.utils import is_url_expired, is_signed_url
   
   def diagnose_url_issue(url):
       """Diagnose URL access problems."""
       print(f"Analyzing URL: {url[:50]}...")
       
       if not is_signed_url(url):
           print("ℹ️  URL is not signed (normal for EarthSearch)")
           return
       
       if is_url_expired(url):
           print("❌ URL has expired")
           print("🔧 Solution: Re-generate URLs or use auto-refresh")
       else:
           print("✅ URL is signed and not expired")

**Solutions**:

.. code-block:: python

   # 1. Use auto-signing (recommended)
   pc = ogapi.planetary_computer(auto_sign=True)
   
   # 2. Refresh expired URLs manually
   from open_geodata_api.utils import re_sign_url_if_needed
   fresh_url = re_sign_url_if_needed(expired_url, provider='planetary_computer')
   
   # 3. Use download functions (handle expiration automatically)
   from open_geodata_api.utils import download_url
   download_url(url)  # Automatically handles expiration

Asset Not Found Errors
~~~~~~~~~~~~~~~~~~~~~~~

**Symptom**: KeyError for asset names

**Diagnosis**:

.. code-block:: python

   def diagnose_asset_issue(item, requested_asset):
       """Diagnose asset availability issues."""
       available_assets = item.list_assets()
       
       print(f"Requested asset: {requested_asset}")
       print(f"Available assets: {available_assets}")
       
       # Check for similar names
       similar = [a for a in available_assets if requested_asset.lower() in a.lower()]
       if similar:
           print(f"Similar assets found: {similar}")
       
       # Provider-specific suggestions
       if item.provider == 'planetary_computer':
           if requested_asset in ['red', 'green', 'blue']:
               print("💡 Try Planetary Computer naming: B04, B03, B02")
       elif item.provider == 'earth_search':
           if requested_asset in ['B04', 'B03', 'B02']:
               print("💡 Try EarthSearch naming: red, green, blue")

**Provider-Agnostic Solution**:

.. code-block:: python

   def get_rgb_assets_safe(item):
       """Safely get RGB assets regardless of provider."""
       assets = item.list_assets()
       
       # Try different naming conventions
       rgb_mappings = [
           (['B04', 'B03', 'B02'], 'Planetary Computer'),
           (['red', 'green', 'blue'], 'EarthSearch'),
           (['RED', 'GREEN', 'BLUE'], 'Uppercase'),
       ]
       
       for mapping, provider_name in rgb_mappings:
           if all(asset in assets for asset in mapping):
               print(f"Using {provider_name} naming: {mapping}")
               return mapping
       
       print(f"No standard RGB mapping found. Available: {assets}")
       return None

Memory and Performance Issues
-----------------------------

Out of Memory Errors
~~~~~~~~~~~~~~~~~~~~

**Symptom**: MemoryError when loading large datasets

**Solutions**:

.. code-block:: python

   # 1. Use chunking
   import rioxarray as rxr
   data = rxr.open_rasterio(url, chunks={'x': 1024, 'y': 1024})
   
   # 2. Use overview levels
   data_preview = rxr.open_rasterio(url, overview_level=2)  # Lower resolution
   
   # 3. Read specific windows
   import rasterio
   with rasterio.open(url) as src:
       window = rasterio.windows.Window(0, 0, 2048, 2048)  # Subset
       data = src.read(1, window=window)
   
   # 4. Process in batches
   def process_items_in_batches(items, batch_size=5):
       for i in range(0, len(items), batch_size):
           batch = items[i:i+batch_size]
           # Process batch
           yield batch

Slow Performance
~~~~~~~~~~~~~~~~

**Symptom**: Operations take too long

**Optimization Strategies**:

.. code-block:: python

   # 1. Limit search results
   results = pc.search(collections=['sentinel-2-l2a'], limit=10)  # Start small
   
   # 2. Use cloud filters early
   results = pc.search(
       collections=['sentinel-2-l2a'],
       query={'eo:cloud_cover': {'lt': 20}},  # Filter in search
       limit=20
   )
   
   # 3. Process specific assets only
   urls = item.get_band_urls(['B04', 'B03', 'B02'])  # Only RGB
   
   # 4. Use parallel processing
   from concurrent.futures import ThreadPoolExecutor
   
   def download_item(item):
       return item.get_all_asset_urls()
   
   with ThreadPoolExecutor(max_workers=4) as executor:
       results = list(executor.map(download_item, items[:10]))

CLI Issues
----------

Command Not Found
~~~~~~~~~~~~~~~~~~

**Symptom**: ``ogapi: command not found``

**Solutions**:

.. code-block:: bash

   # 1. Check if package is installed
   pip show open-geodata-api
   
   # 2. Verify Python scripts directory is in PATH
   python -m site --user-base
   
   # 3. Use Python module execution
   python -m open_geodata_api.cli.main --help
   
   # 4. Reinstall package
   pip uninstall open-geodata-api
   pip install open-geodata-api
   
   # 5. Check virtual environment
   which python
   which pip

CLI Parameter Errors
~~~~~~~~~~~~~~~~~~~~

**Symptom**: CLI commands fail with parameter errors

**Common Issues & Fixes**:

.. code-block:: bash

   # ❌ Common mistakes
   ogapi search items -bbox -122,47,-121,48  # Missing quotes
   ogapi search items --bbox="-122,47,-121,48"  # Wrong syntax
   
   # ✅ Correct usage
   ogapi search items --bbox "-122,47,-121,48"
   ogapi search items -b "-122,47,-121,48"
   
   # Complex JSON queries need proper quoting
   ogapi search items -q '{"eo:cloud_cover":{"lt":20}}'

Data Reading Issues
-------------------

Raster Loading Failures
~~~~~~~~~~~~~~~~~~~~~~~~

**Symptom**: Cannot open raster files from URLs

**Diagnostic Steps**:

.. code-block:: python

   def diagnose_raster_issue(url):
       """Diagnose raster loading problems."""
       print(f"Testing URL: {url[:50]}...")
       
       # 1. Test URL accessibility
       import requests
       try:
           response = requests.head(url, timeout=10)
           print(f"HTTP Status: {response.status_code}")
           if response.status_code != 200:
               print("❌ URL not accessible")
               return
       except Exception as e:
           print(f"❌ Network error: {e}")
           return
       
       # 2. Test with different libraries
       libraries = [
           ('rioxarray', lambda: __import__('rioxarray').open_rasterio(url)),
           ('rasterio', lambda: __import__('rasterio').open(url)),
           ('GDAL', lambda: __import__('osgeo.gdal', fromlist=['gdal']).Open(url))
       ]
       
       for lib_name, opener in libraries:
           try:
               data = opener()
               print(f"✅ {lib_name}: Success")
               if hasattr(data, 'close'):
                   data.close()
           except Exception as e:
               print(f"❌ {lib_name}: {e}")

Projection Issues
~~~~~~~~~~~~~~~~~

**Symptom**: Coordinate reference system errors

**Solutions**:

.. code-block:: python

   import rioxarray as rxr
   
   # Check CRS
   data = rxr.open_rasterio(url)
   print(f"Original CRS: {data.rio.crs}")
   
   # Reproject if needed
   data_reprojected = data.rio.reproject('EPSG:4326')  # WGS84
   
   # Set CRS if missing
   if data.rio.crs is None:
       data = data.rio.set_crs('EPSG:4326')

Getting Help
------------

Diagnostic Information
~~~~~~~~~~~~~~~~~~~~~~

When reporting issues, include this diagnostic information:

.. code-block:: python

   def generate_diagnostic_info():
       """Generate diagnostic information for bug reports."""
       import sys
       import platform
       
       print("=== System Information ===")
       print(f"Python version: {sys.version}")
       print(f"Platform: {platform.platform()}")
       print(f"Architecture: {platform.architecture()}")
       
       print("\n=== Package Versions ===")
       packages = [
           'open_geodata_api',
           'requests', 
           'pandas',
           'rioxarray',
           'rasterio',
           'geopandas',
           'planetary_computer'
       ]
       
       for package in packages:
           try:
               module = __import__(package)
               version = getattr(module, '__version__', 'unknown')
               print(f"{package}: {version}")
           except ImportError:
               print(f"{package}: not installed")
       
       print("\n=== Network Test ===")
       import requests
       endpoints = [
           'https://planetarycomputer.microsoft.com/api/stac/v1/',
           'https://earth-search.aws.element84.com/v1/'
       ]
       
       for endpoint in endpoints:
           try:
               response = requests.get(endpoint, timeout=5)
               print(f"{endpoint}: HTTP {response.status_code}")
           except Exception as e:
               print(f"{endpoint}: Error - {e}")

   # Run diagnostics
   generate_diagnostic_info()

Reporting Bugs
~~~~~~~~~~~~~~

**Before reporting, try these steps**:

1. **Search existing issues**: Check if the problem is already reported
2. **Update packages**: Ensure you're using the latest version
3. **Test with minimal example**: Create a simple reproduction case
4. **Check environment**: Try in a fresh virtual environment

**Include in bug reports**:

- Complete error traceback
- Minimal code to reproduce the issue
- System and package version information
- Expected vs actual behavior
- Any workarounds you've tried

**Where to report**:

- **GitHub Issues**: https://github.com/Mirjan-Ali-Sha/open-geodata-api/issues
- **Use appropriate labels**: bug, enhancement, documentation, etc.

Emergency Workarounds
---------------------

When All Else Fails
~~~~~~~~~~~~~~~~~~~

**Quick fixes for urgent situations**:

.. code-block:: python

   # 1. Bypass package and use direct API calls
   import requests
   
   def emergency_search(bbox, collection='sentinel-2-l2a'):
       """Direct API call bypass."""
       url = 'https://planetarycomputer.microsoft.com/api/stac/v1/search'
       
       payload = {
           'collections': [collection],
           'bbox': bbox,
           'limit': 10
       }
       
       response = requests.post(url, json=payload)
       return response.json()
   
   # 2. Use alternative packages temporarily
   # - pystac-client for STAC operations
   # - stackstac for array processing
   # - planetary-computer directly for signing
   
   # 3. Manual URL construction for known patterns
   def manual_url_construction(item_id, asset):
       """Manual URL construction for known patterns."""
       base_url = "https://sentinel2l2a01.blob.core.windows.net/sentinel2-l2"
       return f"{base_url}/{item_id}/{asset}.tif"

**Recovery procedures**:

.. code-block:: bash

   # 1. Complete package reinstall
   pip uninstall open-geodata-api
   pip cache purge
   pip install open-geodata-api[complete]
   
   # 2. Clean environment rebuild
   deactivate
   rm -rf your_env/
   python -m venv your_env
   source your_env/bin/activate
   pip install open-geodata-api[complete]
   
   # 3. Alternative installation methods
   conda install -c conda-forge open-geodata-api
   # or
   pip install git+https://github.com/Mirjan-Ali-Sha/open-geodata-api.git

This troubleshooting guide should help resolve most common issues. If problems persist, don't hesitate to seek help through the official support channels.
