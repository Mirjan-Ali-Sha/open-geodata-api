Utility Functions Reference
===========================

Complete reference for all utility functions in the ``open_geodata_api.utils`` module.

Overview
--------

The utils module provides essential helper functions for data filtering, downloading, URL management, and processing satellite data. These functions are designed to work seamlessly with the core STAC classes.

**Main Categories**:

- :ref:`filtering-functions` - Data quality and criteria filtering
- :ref:`download-functions` - Intelligent downloading and management  
- :ref:`url-management` - URL signing, validation, and refresh
- :ref:`data-processing` - Analysis and conversion helpers

.. _filtering-functions:

Filtering Functions
-------------------

filter_by_cloud_cover
~~~~~~~~~~~~~~~~~~~~~~

.. py:function:: filter_by_cloud_cover(items, max_cloud_cover)

   Filter STAC items by maximum cloud cover percentage.

   :param items: Collection of STAC items to filter
   :type items: STACItemCollection or list of STACItem
   :param max_cloud_cover: Maximum allowed cloud cover percentage (0-100)
   :type max_cloud_cover: float
   :returns: Filtered collection with items below cloud cover threshold
   :rtype: STACItemCollection
   :raises ValueError: If max_cloud_cover is not between 0 and 100

   **Example**:

   .. code-block:: python

      from open_geodata_api.utils import filter_by_cloud_cover
      
      # Filter to very clear scenes
      clear_items = filter_by_cloud_cover(items, max_cloud_cover=15)
      print(f"Filtered from {len(items)} to {len(clear_items)} clear items")

   **Advanced Usage**:

   .. code-block:: python

      # Chain with other filters
      seasonal_items = filter_by_date_range(items, '2024-06-01', '2024-08-31')
      clear_summer = filter_by_cloud_cover(seasonal_items, max_cloud_cover=20)

filter_by_date_range
~~~~~~~~~~~~~~~~~~~~~

.. py:function:: filter_by_date_range(items, start_date, end_date)

   Filter items by date range.

   :param items: Collection of STAC items to filter
   :type items: STACItemCollection or list of STACItem
   :param start_date: Start date (inclusive)
   :type start_date: str or datetime
   :param end_date: End date (inclusive)  
   :type end_date: str or datetime
   :returns: Items within the specified date range
   :rtype: STACItemCollection

   **Example**:

   .. code-block:: python

      from open_geodata_api.utils import filter_by_date_range
      
      # Get summer data only
      summer_items = filter_by_date_range(
          items, 
          start_date='2024-06-01', 
          end_date='2024-08-31'
      )

filter_by_geometry
~~~~~~~~~~~~~~~~~~~

.. py:function:: filter_by_geometry(items, geometry, geometry_crs='EPSG:4326')

   Filter items that intersect with a specific geometry.

   :param items: Collection of STAC items to filter
   :type items: STACItemCollection
   :param geometry: Geometry to filter by (shapely geometry or GeoJSON)
   :type geometry: shapely.geometry or dict
   :param geometry_crs: CRS of the input geometry
   :type geometry_crs: str
   :returns: Items that intersect with the geometry
   :rtype: STACItemCollection

   **Example**:

   .. code-block:: python

      from shapely.geometry import Polygon
      from open_geodata_api.utils import filter_by_geometry
      
      # Create area of interest
      aoi = Polygon([(-122.5, 47.5), (-122.0, 47.5), 
                     (-122.0, 48.0), (-122.5, 48.0)])
      
      # Filter items intersecting AOI
      intersecting_items = filter_by_geometry(items, aoi)

.. _download-functions:

Download Functions
------------------

download_datasets
~~~~~~~~~~~~~~~~~~

.. py:function:: download_datasets(data_source, destination='./', asset_keys=None, **kwargs)

   Universal download function that intelligently handles various input types.

   :param data_source: Data to download (STACItemCollection, URL dict, or file path)
   :type data_source: STACItemCollection, dict, or str
   :param destination: Base destination directory
   :type destination: str or Path
   :param asset_keys: Specific assets to download (None for all)
   :type asset_keys: list of str or None
   :param kwargs: Additional download options
   :returns: Download results with file paths
   :rtype: dict

   **Supported Input Types**:

   .. code-block:: python

      from open_geodata_api.utils import download_datasets
      
      # 1. From STAC items
      results = download_datasets(items, destination="./data/")
      
      # 2. From URL dictionary  
      urls = {'item1': {'B04': 'url1', 'B03': 'url2'}}
      results = download_datasets(urls, destination="./data/")
      
      # 3. From JSON file
      results = download_datasets("exported_urls.json", destination="./data/")
      
      # 4. From seasonal data structure
      seasonal_data = {
          'spring_2024': {'urls': {'item1': {'B04': 'url1'}}}
      }
      results = download_datasets(seasonal_data, seasons=['spring_2024'])

   **Advanced Options**:

   .. code-block:: python

      # Download specific assets with custom organization
      results = download_datasets(
          items,
          destination="./satellite_data/",
          asset_keys=['B04', 'B03', 'B02'],
          create_folders=True,
          max_workers=4,
          chunk_size=8192,
          show_progress=True
      )

download_url
~~~~~~~~~~~~

.. py:function:: download_url(url, destination=None, provider=None, **kwargs)

   Download a single file from URL with automatic provider handling.

   :param url: URL to download
   :type url: str
   :param destination: Local file path or directory
   :type destination: str or Path or None
   :param provider: Provider hint for URL handling ('pc', 'es', or None for auto-detect)
   :type provider: str or None
   :returns: Path to downloaded file
   :rtype: str

   **Example**:

   .. code-block:: python

      from open_geodata_api.utils import download_url
      
      # Simple download
      path = download_url("https://example.com/data.tif")
      
      # Download to specific location
      path = download_url(
          "https://example.com/B04.tif",
          destination="./data/red_band.tif",
          provider="planetary_computer"
      )

download_items
~~~~~~~~~~~~~~

.. py:function:: download_items(items, base_destination, asset_keys=None, create_product_folders=True, **kwargs)

   Download all assets from STAC items with intelligent organization.

   :param items: STAC items to download
   :type items: STACItemCollection or list of STACItem
   :param base_destination: Base directory for downloads
   :type base_destination: str or Path
   :param asset_keys: Specific assets to download
   :type asset_keys: list of str or None
   :param create_product_folders: Create separate folders for each item
   :type create_product_folders: bool
   :returns: Download results organized by item and asset
   :rtype: dict

   **Example**:

   .. code-block:: python

      from open_geodata_api.utils import download_items
      
      # Download with folder organization
      results = download_items(
          items,
          base_destination="./analysis_ready/",
          asset_keys=['B08', 'B04'],  # NIR and Red for NDVI
          create_product_folders=True
      )
      
      # Results structure:
      # {
      #   'item_id_1': {'B08': '/path/to/item1/B08.tif', 'B04': '/path/to/item1/B04.tif'},
      #   'item_id_2': {'B08': '/path/to/item2/B08.tif', 'B04': '/path/to/item2/B04.tif'}
      # }

download_seasonal_data
~~~~~~~~~~~~~~~~~~~~~~

.. py:function:: download_seasonal_data(seasonal_data, base_destination, seasons=None, asset_keys=None, **kwargs)

   Download seasonal data structures with temporal organization.

   :param seasonal_data: Seasonal data structure
   :type seasonal_data: dict
   :param base_destination: Base directory for seasonal downloads
   :type base_destination: str or Path
   :param seasons: Specific seasons to download (None for all)
   :type seasons: list of str or None
   :param asset_keys: Specific assets to download
   :type asset_keys: list of str or None
   :returns: Download results organized by season and item
   :rtype: dict

   **Example**:

   .. code-block:: python

      from open_geodata_api.utils import download_seasonal_data
      
      seasonal_data = {
          'spring_2024': {
              'count': 50,
              'date_range': '2024-03-01/2024-05-31',
              'urls': {
                  'item1': {'B08': 'url1', 'B04': 'url2'},
                  'item2': {'B08': 'url3', 'B04': 'url4'}
              }
          },
          'summer_2024': {
              'count': 45,
              'date_range': '2024-06-01/2024-08-31', 
              'urls': {...}
          }
      }
      
      results = download_seasonal_data(
          seasonal_data,
          base_destination="./time_series/",
          seasons=['spring_2024', 'summer_2024'],
          asset_keys=['B08', 'B04']
      )

.. _url-management:

URL Management Functions
------------------------

is_url_expired
~~~~~~~~~~~~~~

.. py:function:: is_url_expired(url)

   Check if a signed URL has expired.

   :param url: URL to check for expiration
   :type url: str
   :returns: True if URL is expired, False otherwise
   :rtype: bool

   **Example**:

   .. code-block:: python

      from open_geodata_api.utils import is_url_expired
      
      url = item.get_asset_url('B04')
      if is_url_expired(url):
          print("URL has expired and needs re-signing")
      else:
          print("URL is still valid")

is_signed_url
~~~~~~~~~~~~~

.. py:function:: is_signed_url(url)

   Check if a URL contains signature parameters.

   :param url: URL to check for signatures
   :type url: str
   :returns: True if URL appears to be signed
   :rtype: bool

   **Example**:

   .. code-block:: python

      from open_geodata_api.utils import is_signed_url
      
      pc_url = "https://pc.example.com/data.tif?sig=abc123"
      es_url = "https://es.example.com/data.tif"
      
      print(f"PC URL signed: {is_signed_url(pc_url)}")  # True
      print(f"ES URL signed: {is_signed_url(es_url)}")  # False

re_sign_url_if_needed
~~~~~~~~~~~~~~~~~~~~~

.. py:function:: re_sign_url_if_needed(url, provider=None)

   Automatically re-sign expired URLs with warnings.

   :param url: URL to check and potentially re-sign
   :type url: str
   :param provider: Provider hint ('planetary_computer', 'earth_search', or None)
   :type provider: str or None
   :returns: Fresh URL (re-signed if needed)
   :rtype: str

   **Example**:

   .. code-block:: python

      from open_geodata_api.utils import re_sign_url_if_needed
      
      # Automatically handle expired URLs
      fresh_url = re_sign_url_if_needed(
          potentially_expired_url, 
          provider="planetary_computer"
      )
      
      # Use fresh URL for downloading
      import rioxarray
      data = rioxarray.open_rasterio(fresh_url)

validate_urls
~~~~~~~~~~~~~

.. py:function:: validate_urls(urls_dict, check_expiry=True, check_access=False)

   Validate a collection of URLs for accessibility and expiration.

   :param urls_dict: Dictionary of URLs to validate
   :type urls_dict: dict
   :param check_expiry: Whether to check URL expiration
   :type check_expiry: bool
   :param check_access: Whether to test HTTP accessibility
   :type check_access: bool
   :returns: Validation results with detailed status
   :rtype: dict

   **Example**:

   .. code-block:: python

      from open_geodata_api.utils import validate_urls
      
      urls = {
          'item1': {'B04': 'url1', 'B03': 'url2'},
          'item2': {'B04': 'url3', 'B03': 'url4'}
      }
      
      validation_results = validate_urls(
          urls,
          check_expiry=True,
          check_access=True
      )
      
      print(f"Valid URLs: {validation_results['valid_count']}")
      print(f"Expired URLs: {validation_results['expired_count']}")

.. _data-processing:

Data Processing Functions
-------------------------

create_download_summary
~~~~~~~~~~~~~~~~~~~~~~~~

.. py:function:: create_download_summary(download_results, output_file=None)

   Generate comprehensive download statistics and reports.

   :param download_results: Results from download operations
   :type download_results: dict
   :param output_file: Optional file to save summary
   :type output_file: str or Path or None
   :returns: Summary statistics
   :rtype: dict

   **Example**:

   .. code-block:: python

      from open_geodata_api.utils import create_download_summary
      
      # After downloading data
      download_results = download_items(items, base_destination="./data/")
      
      # Create summary report
      summary = create_download_summary(
          download_results,
          output_file="download_report.json"
      )
      
      print(f"Downloaded {summary['successful_downloads']}/{summary['total_files']} files")
      print(f"Success rate: {summary['success_rate']}")

export_urls_to_json
~~~~~~~~~~~~~~~~~~~

.. py:function:: export_urls_to_json(items, output_file, asset_keys=None, signed=True, **kwargs)

   Export asset URLs to JSON file for external processing.

   :param items: STAC items to export URLs from
   :type items: STACItemCollection
   :param output_file: Output JSON file path
   :type output_file: str or Path
   :param asset_keys: Specific assets to export
   :type asset_keys: list of str or None
   :param signed: Whether to use signed URLs
   :type signed: bool
   :returns: Export metadata
   :rtype: dict

   **Example**:

   .. code-block:: python

      from open_geodata_api.utils import export_urls_to_json
      
      # Export RGB URLs for external processing
      export_metadata = export_urls_to_json(
          items,
          output_file="rgb_urls.json",
          asset_keys=['B04', 'B03', 'B02'],
          signed=True
      )

Batch Processing Functions
--------------------------

process_items_in_batches
~~~~~~~~~~~~~~~~~~~~~~~~

.. py:function:: process_items_in_batches(items, batch_size=10, process_func=None, **kwargs)

   Process large collections of items in memory-efficient batches.

   :param items: Items to process
   :type items: STACItemCollection or list
   :param batch_size: Number of items per batch
   :type batch_size: int
   :param process_func: Function to apply to each batch
   :type process_func: callable or None
   :returns: Generator yielding batch results
   :rtype: generator

   **Example**:

   .. code-block:: python

      from open_geodata_api.utils import process_items_in_batches
      
      def download_batch(batch_items):
          return download_items(batch_items, "./batch_data/")
      
      # Process large dataset in batches
      for batch_result in process_items_in_batches(
          large_items_list, 
          batch_size=5, 
          process_func=download_batch
      ):
          print(f"Processed batch: {len(batch_result)} items")

parallel_download
~~~~~~~~~~~~~~~~~

.. py:function:: parallel_download(urls_dict, destination, max_workers=4, **kwargs)

   Download multiple URLs in parallel with progress tracking.

   :param urls_dict: Dictionary of URLs to download
   :type urls_dict: dict
   :param destination: Base destination directory
   :type destination: str or Path
   :param max_workers: Maximum number of parallel workers
   :type max_workers: int
   :returns: Download results with success/failure status
   :rtype: dict

   **Example**:

   .. code-block:: python

      from open_geodata_api.utils import parallel_download
      
      urls = {
          'red_band': 'https://example.com/B04.tif',
          'green_band': 'https://example.com/B03.tif',
          'blue_band': 'https://example.com/B02.tif'
      }
      
      results = parallel_download(
          urls,
          destination="./rgb_data/",
          max_workers=3
      )

Analysis Helper Functions
-------------------------

calculate_ndvi
~~~~~~~~~~~~~~

.. py:function:: calculate_ndvi(nir_url, red_url, output_path=None)

   Calculate NDVI from NIR and Red band URLs.

   :param nir_url: URL to Near-Infrared band
   :type nir_url: str
   :param red_url: URL to Red band
   :type red_url: str
   :param output_path: Optional path to save NDVI result
   :type output_path: str or Path or None
   :returns: NDVI data array
   :rtype: xarray.DataArray

   **Example**:

   .. code-block:: python

      from open_geodata_api.utils import calculate_ndvi
      
      # Get band URLs
      urls = item.get_band_urls(['B08', 'B04'])  # NIR, Red
      
      # Calculate NDVI
      ndvi = calculate_ndvi(
          nir_url=urls['B08'],
          red_url=urls['B04'],
          output_path="./ndvi_result.tif"
      )
      
      print(f"Mean NDVI: {ndvi.mean().values:.3f}")

get_seasonal_statistics
~~~~~~~~~~~~~~~~~~~~~~~

.. py:function:: get_seasonal_statistics(items_by_season, statistic='mean')

   Calculate statistics across seasonal data collections.

   :param items_by_season: Items organized by season
   :type items_by_season: dict
   :param statistic: Statistic to calculate ('mean', 'median', 'std', etc.)
   :type statistic: str
   :returns: Seasonal statistics
   :rtype: dict

   **Example**:

   .. code-block:: python

      from open_geodata_api.utils import get_seasonal_statistics
      
      seasonal_data = {
          'spring': spring_items,
          'summer': summer_items,
          'fall': fall_items
      }
      
      stats = get_seasonal_statistics(seasonal_data, statistic='mean')
      print(f"Seasonal NDVI means: {stats}")

Error Handling Utilities
-------------------------

robust_download
~~~~~~~~~~~~~~~

.. py:function:: robust_download(url, destination, max_retries=3, **kwargs)

   Download with comprehensive error handling and retry logic.

   :param url: URL to download
   :type url: str
   :param destination: Local destination path
   :type destination: str or Path
   :param max_retries: Maximum number of retry attempts
   :type max_retries: int
   :returns: Success status and file path
   :rtype: tuple

   **Example**:

   .. code-block:: python

      from open_geodata_api.utils import robust_download
      
      success, file_path = robust_download(
          url="https://example.com/large_file.tif",
          destination="./data/",
          max_retries=5,
          timeout=60
      )
      
      if success:
          print(f"Downloaded successfully: {file_path}")
      else:
          print("Download failed after retries")

validate_stac_item
~~~~~~~~~~~~~~~~~~

.. py:function:: validate_stac_item(item_data)

   Validate STAC item structure and content.

   :param item_data: STAC item data to validate
   :type item_data: dict
   :returns: Validation results with errors/warnings
   :rtype: dict

   **Example**:

   .. code-block:: python

      from open_geodata_api.utils import validate_stac_item
      
      validation = validate_stac_item(item.to_dict())
      
      if validation['valid']:
          print("Item is valid")
      else:
          print(f"Validation errors: {validation['errors']}")

Configuration and Settings
---------------------------

set_global_config
~~~~~~~~~~~~~~~~~

.. py:function:: set_global_config(**kwargs)

   Set global configuration options for utility functions.

   :param kwargs: Configuration parameters
   :returns: Updated configuration
   :rtype: dict

   **Available Options**:

   .. code-block:: python

      from open_geodata_api.utils import set_global_config
      
      # Configure default behavior
      config = set_global_config(
          default_timeout=60,           # Download timeout
          max_retries=5,               # Default retry count
          chunk_size=8192,             # Download chunk size
          show_progress=True,          # Show progress bars
          cache_signed_urls=True,      # Cache signed URLs
          auto_refresh_urls=True       # Auto-refresh expired URLs
      )

get_global_config
~~~~~~~~~~~~~~~~~

.. py:function:: get_global_config()

   Get current global configuration settings.

   :returns: Current configuration
   :rtype: dict

   **Example**:

   .. code-block:: python

      from open_geodata_api.utils import get_global_config
      
      config = get_global_config()
      print(f"Current timeout: {config['default_timeout']}")

Usage Patterns and Best Practices
----------------------------------

Chaining Utility Functions
~~~~~~~~~~~~~~~~~~~~~~~~~~~

Utility functions are designed to work together:

.. code-block:: python

   from open_geodata_api.utils import (
       filter_by_cloud_cover,
       filter_by_date_range,
       download_items,
       create_download_summary
   )
   
   # Chain operations for complete workflow
   def complete_workflow(items, destination):
       # Filter data
       clear_items = filter_by_cloud_cover(items, max_cloud_cover=20)
       summer_items = filter_by_date_range(
           clear_items, 
           '2024-06-01', 
           '2024-08-31'
       )
       
       # Download filtered data
       results = download_items(
           summer_items,
           base_destination=destination,
           asset_keys=['B08', 'B04', 'B03', 'B02']
       )
       
       # Generate summary
       summary = create_download_summary(results)
       
       return summary

Error Handling Best Practices
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Most utility functions include built-in error handling:

.. code-block:: python

   from open_geodata_api.utils import download_datasets
   
   try:
       results = download_datasets(
           items,
           destination="./data/",
           asset_keys=['B04', 'B03', 'B02']
       )
       
       # Check for any failures
       failed_downloads = [
           item_id for item_id, item_results in results.items()
           if not any(path for path in item_results.values())
       ]
       
       if failed_downloads:
           print(f"Failed to download: {failed_downloads}")
       
   except Exception as e:
       print(f"Download operation failed: {e}")

Performance Optimization
~~~~~~~~~~~~~~~~~~~~~~~~~

For large datasets, use these optimization patterns:

.. code-block:: python

   # Use batching for memory efficiency
   from open_geodata_api.utils import process_items_in_batches
   
   def optimized_processing(large_items_collection):
       for batch in process_items_in_batches(large_items_collection, batch_size=10):
           # Process each batch
           batch_results = download_items(batch, "./batch_data/")
           
           # Clean up between batches
           import gc
           gc.collect()

The utility functions provide a comprehensive toolkit for working with satellite data efficiently and reliably.
