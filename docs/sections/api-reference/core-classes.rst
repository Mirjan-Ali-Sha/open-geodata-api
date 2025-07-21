Core Classes
============

The core classes provide STAC-compliant data models for working with satellite imagery metadata and assets.

STACItem
--------

.. autoclass:: open_geodata_api.core.items.STACItem
   :members:
   :undoc-members:
   :show-inheritance:

Represents a single satellite scene or product with metadata and associated assets.

**Key Properties**:

- ``id``: Unique identifier for the item
- ``collection``: Collection this item belongs to
- ``properties``: Metadata dictionary including datetime, cloud cover, etc.
- ``assets``: Dictionary of available assets (files)
- ``bbox``: Bounding box coordinates
- ``provider``: Data provider name

**Usage Example**:

.. code-block:: python

   # Create from search results
   item = results.get_all_items()[0]
   
   # Access metadata
   print(f"Item ID: {item.id}")
   print(f"Date: {item.properties['datetime']}")
   print(f"Cloud cover: {item.properties['eo:cloud_cover']}%")
   
   # Get asset URLs
   red_url = item.get_asset_url('B04')
   all_urls = item.get_all_asset_urls()

STACItemCollection
------------------

.. autoclass:: open_geodata_api.core.collections.STACItemCollection
   :members:
   :undoc-members:
   :show-inheritance:

Collection of STAC items with bulk operations and data conversion capabilities.

**Key Features**:

- Iterable container for multiple STACItems
- Bulk URL retrieval across all items
- DataFrame conversion for analysis
- Filtering and subsetting operations

**Usage Example**:

.. code-block:: python

   # Create from search results
   items = results.get_all_items()
   
   # Collection operations
   print(f"Found {len(items)} items")
   
   # Convert to DataFrame
   df = items.to_dataframe()
   
   # Bulk URL retrieval
   all_urls = items.get_all_urls(['B04', 'B03', 'B02'])
   
   # Iteration
   for item in items:
       print(f"Processing {item.id}")

STACAsset
---------

.. autoclass:: open_geodata_api.core.assets.STACAsset
   :members:
   :undoc-members:
   :show-inheritance:

Represents a single asset (file) within a STAC item.

**Key Properties**:

- ``href``: URL to the asset file
- ``type``: MIME type of the asset
- ``title``: Human-readable title
- ``roles``: List of asset roles (e.g., 'data', 'thumbnail')

**Usage Example**:

.. code-block:: python

   # Access asset directly
   asset = item.assets['B04']
   
   print(f"Asset URL: {asset.href}")
   print(f"Asset type: {asset.type}")
   print(f"Asset title: {asset.title}")
   
   # Get signed URL if needed
   signed_url = asset.get_signed_url()

STACSearch
----------

.. autoclass:: open_geodata_api.core.search.STACSearch
   :members:
   :undoc-members:
   :show-inheritance:

Container for search results with pagination and metadata.

**Key Features**:

- Lazy loading of search results
- Pagination support
- Search metadata and statistics
- Result caching

**Usage Example**:

.. code-block:: python

   # Search returns STACSearch object
   search_results = client.search(collections=['sentinel-2-l2a'])
   
   # Access results
   items = search_results.get_all_items()
   
   # Check metadata
   print(f"Total results: {search_results.total_results}")
   print(f"Returned: {len(items)} items")

Common Patterns
---------------

Working with Multiple Items
~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   # Process multiple items efficiently
   items = results.get_all_items()
   
   for item in items:
       # Check data quality
       cloud_cover = item.properties.get('eo:cloud_cover', 100)
       if cloud_cover < 20:
           # Get URLs for analysis
           urls = item.get_band_urls(['B08', 'B04'])  # NIR, Red
           print(f"Clear scene: {item.id}")

Provider-Agnostic Asset Access
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   def get_rgb_urls(item):
       """Get RGB URLs regardless of provider."""
       assets = item.list_assets()
       
       # Try different naming conventions
       if all(band in assets for band in ['B04', 'B03', 'B02']):
           return item.get_band_urls(['B04', 'B03', 'B02'])  # PC
       elif all(band in assets for band in ['red', 'green', 'blue']):
           return item.get_band_urls(['red', 'green', 'blue'])  # ES
       else:
           print(f"Available assets: {assets}")
           return {}

Data Conversion
~~~~~~~~~~~~~~~

.. code-block:: python

   # Convert collection to DataFrame for analysis
   df = items.to_dataframe()
   
   # Filter by date
   summer_items = df[df['datetime'].str.contains('2024-0[678]')]
   
   # Group by month
   monthly_counts = df.groupby(df['datetime'].str[:7]).size()
   print("Monthly data availability:")
   print(monthly_counts)

Error Handling
~~~~~~~~~~~~~~

.. code-block:: python

   # Robust asset access
   def safe_get_asset_url(item, asset_name):
       """Safely get asset URL with error handling."""
       try:
           return item.get_asset_url(asset_name)
       except KeyError:
           available = item.list_assets()
           print(f"Asset {asset_name} not found. Available: {available}")
           return None
       except Exception as e:
           print(f"Error getting URL for {asset_name}: {e}")
           return None
