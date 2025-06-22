Factory Functions
=================

Factory functions provide convenient ways to create API clients and access common functionality.

Client Factory Functions
------------------------

planetary_computer
~~~~~~~~~~~~~~~~~~

.. autofunction:: open_geodata_api.planetary_computer

Create a Planetary Computer API client with optional configuration.

**Parameters**:

- ``auto_sign`` (bool): Enable automatic URL signing (default: True)
- ``cache_signed_urls`` (bool): Cache signed URLs for performance (default: True)
- ``**kwargs``: Additional configuration options

**Usage Example**:

.. code-block:: python

   import open_geodata_api as ogapi
   
   # Basic usage with auto-signing
   pc = ogapi.planetary_computer(auto_sign=True)
   
   # Advanced configuration
   pc = ogapi.planetary_computer(
       auto_sign=True,
       cache_signed_urls=True,
       timeout=60,
       max_retries=3
   )

earth_search
~~~~~~~~~~~~

.. autofunction:: open_geodata_api.earth_search

Create an EarthSearch API client with optional configuration.

**Parameters**:

- ``auto_validate`` (bool): Enable automatic URL validation (default: False)
- ``**kwargs``: Additional configuration options

**Usage Example**:

.. code-block:: python

   import open_geodata_api as ogapi
   
   # Basic usage
   es = ogapi.earth_search()
   
   # With validation
   es = ogapi.earth_search(auto_validate=True)

get_clients
~~~~~~~~~~~

.. autofunction:: open_geodata_api.get_clients

Get both Planetary Computer and EarthSearch clients in a single call.

**Parameters**:

- ``pc_auto_sign`` (bool): Enable auto-signing for PC client (default: True)
- ``es_auto_validate`` (bool): Enable validation for ES client (default: False)
- ``**kwargs``: Additional configuration for both clients

**Returns**: Dictionary with 'planetary_computer' and 'earth_search' keys

**Usage Example**:

.. code-block:: python

   import open_geodata_api as ogapi
   
   # Get both clients
   clients = ogapi.get_clients(pc_auto_sign=True)
   
   pc = clients['planetary_computer']
   es = clients['earth_search']
   
   # Compare results
   pc_results = pc.search(collections=['sentinel-2-l2a'], limit=5)
   es_results = es.search(collections=['sentinel-2-l2a'], limit=5)

Utility Factory Functions
-------------------------

create_search_config
~~~~~~~~~~~~~~~~~~~~

.. autofunction:: open_geodata_api.create_search_config

Create a reusable search configuration object.

**Parameters**:

- ``collections`` (list): List of collection names
- ``bbox`` (list): Bounding box coordinates
- ``datetime`` (str): Date range
- ``query`` (dict): Additional query parameters
- ``**kwargs``: Other search parameters

**Usage Example**:

.. code-block:: python

   # Create reusable search configuration
   config = ogapi.create_search_config(
       collections=['sentinel-2-l2a'],
       bbox=[-122.5, 47.5, -122.0, 48.0],
       datetime='2024-06-01/2024-08-31',
       query={'eo:cloud_cover': {'lt': 20}}
   )
   
   # Use with different clients
   pc_results = pc.search(**config)
   es_results = es.search(**config)

create_download_config
~~~~~~~~~~~~~~~~~~~~~

.. autofunction:: open_geodata_api.create_download_config

Create a download configuration for batch operations.

**Parameters**:

- ``destination`` (str): Base download directory
- ``asset_keys`` (list): Assets to download
- ``create_folders`` (bool): Create organized folder structure
- ``**kwargs``: Additional download options

**Usage Example**:

.. code-block:: python

   # Create download configuration
   download_config = ogapi.create_download_config(
       destination="./satellite_data/",
       asset_keys=['B04', 'B03', 'B02'],
       create_folders=True,
       max_workers=4
   )
   
   # Use for downloading
   from open_geodata_api.utils import download_datasets
   results = download_datasets(items, **download_config)

Configuration Management
------------------------

set_global_defaults
~~~~~~~~~~~~~~~~~~~

.. autofunction:: open_geodata_api.set_global_defaults

Set global default parameters for all clients and operations.

**Parameters**:

- ``default_provider`` (str): Default provider ('pc' or 'es')
- ``auto_sign`` (bool): Default auto-signing behavior
- ``timeout`` (int): Default timeout for requests
- ``**kwargs``: Additional global settings

**Usage Example**:

.. code-block:: python

   # Set global defaults
   ogapi.set_global_defaults(
       default_provider='pc',
       auto_sign=True,
       timeout=60,
       max_retries=3
   )
   
   # Subsequent client creation uses defaults
   pc = ogapi.planetary_computer()  # Uses global defaults

get_global_config
~~~~~~~~~~~~~~~~~

.. autofunction:: open_geodata_api.get_global_config

Get current global configuration settings.

**Returns**: Dictionary of current global settings

**Usage Example**:

.. code-block:: python

   # Check current configuration
   config = ogapi.get_global_config()
   print(f"Default provider: {config['default_provider']}")
   print(f"Auto-sign enabled: {config['auto_sign']}")

Validation Functions
--------------------

validate_bbox
~~~~~~~~~~~~~

.. autofunction:: open_geodata_api.validate_bbox

Validate bounding box format and coordinates.

**Parameters**:

- ``bbox`` (list): Bounding box as [west, south, east, north]

**Returns**: Tuple of (is_valid, error_message)

**Usage Example**:

.. code-block:: python

   # Validate bbox before search
   bbox = [-122.5, 47.5, -122.0, 48.0]
   is_valid, message = ogapi.validate_bbox(bbox)
   
   if is_valid:
       results = pc.search(collections=['sentinel-2-l2a'], bbox=bbox)
   else:
       print(f"Invalid bbox: {message}")

validate_datetime
~~~~~~~~~~~~~~~~~

.. autofunction:: open_geodata_api.validate_datetime

Validate datetime format for search operations.

**Parameters**:

- ``datetime_str`` (str): Datetime string to validate

**Returns**: Tuple of (is_valid, normalized_datetime)

**Usage Example**:

.. code-block:: python

   # Validate and normalize datetime
   is_valid, normalized = ogapi.validate_datetime("2024-06-01/2024-08-31")
   
   if is_valid:
       results = pc.search(
           collections=['sentinel-2-l2a'],
           datetime=normalized
       )

Helper Functions
----------------

info
~~~~

.. autofunction:: open_geodata_api.info

Display package information and system status.

**Usage Example**:

.. code-block:: python

   # Display package information
   ogapi.info()
   
   # Output:
   # Open Geodata API v0.1.0
   # Python: 3.9.7
   # Platform: Linux-5.4.0-x86_64
   # Dependencies: ✓ requests ✓ pandas ✓ planetary-computer

check_providers
~~~~~~~~~~~~~~~

.. autofunction:: open_geodata_api.check_providers

Check connectivity and status of all supported providers.

**Returns**: Dictionary with provider status information

**Usage Example**:

.. code-block:: python

   # Check provider status
   status = ogapi.check_providers()
   
   for provider, info in status.items():
       if info['available']:
           print(f"✅ {provider}: Available ({info['collections']} collections)")
       else:
           print(f"❌ {provider}: {info['error']}")

Advanced Factory Patterns
-------------------------

Custom Client Factory
~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   def create_custom_client(provider, region=None, **kwargs):
       """Create customized client based on requirements."""
       
       if provider == 'pc':
           client = ogapi.planetary_computer(
               auto_sign=True,
               cache_signed_urls=True,
               **kwargs
           )
       elif provider == 'es':
           client = ogapi.earth_search(
               auto_validate=True,
               **kwargs
           )
       else:
           raise ValueError(f"Unknown provider: {provider}")
       
       # Add region-specific optimizations
       if region == 'europe':
           client.timeout = 120  # Longer timeout for EU
       elif region == 'asia':
           client.max_retries = 5  # More retries for Asia
       
       return client

Configuration Builder
~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   class SearchConfigBuilder:
       """Builder pattern for search configurations."""
       
       def __init__(self):
           self.config = {}
       
       def collections(self, *collections):
           self.config['collections'] = list(collections)
           return self
       
       def bbox(self, west, south, east, north):
           self.config['bbox'] = [west, south, east, north]
           return self
       
       def datetime(self, start, end=None):
           if end:
               self.config['datetime'] = f"{start}/{end}"
           else:
               self.config['datetime'] = start
           return self
       
       def cloud_cover(self, max_cloud):
           if 'query' not in self.config:
               self.config['query'] = {}
           self.config['query']['eo:cloud_cover'] = {'lt': max_cloud}
           return self
       
       def limit(self, count):
           self.config['limit'] = count
           return self
       
       def build(self):
           return self.config.copy()
   
   # Usage
   config = (SearchConfigBuilder()
            .collections('sentinel-2-l2a')
            .bbox(-122.5, 47.5, -122.0, 48.0)
            .datetime('2024-06-01', '2024-08-31')
            .cloud_cover(20)
            .limit(10)
            .build())
   
   results = pc.search(**config)

Error Handling Patterns
-----------------------

Robust Client Creation
~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   def create_robust_client(preferred_provider='pc'):
       """Create client with fallback options."""
       
       providers = ['pc', 'es'] if preferred_provider == 'pc' else ['es', 'pc']
       
       for provider in providers:
           try:
               if provider == 'pc':
                   return ogapi.planetary_computer(auto_sign=True)
               else:
                   return ogapi.earth_search()
           
           except ImportError as e:
               print(f"Cannot create {provider} client: {e}")
               continue
           
           except Exception as e:
               print(f"Failed to create {provider} client: {e}")
               continue
       
       raise RuntimeError("Could not create any client")

Factory with Validation
~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   def validated_search_factory(provider, **search_params):
       """Create search with parameter validation."""
       
       # Validate bbox
       if 'bbox' in search_params:
           is_valid, message = ogapi.validate_bbox(search_params['bbox'])
           if not is_valid:
               raise ValueError(f"Invalid bbox: {message}")
       
       # Validate datetime
       if 'datetime' in search_params:
           is_valid, normalized = ogapi.validate_datetime(search_params['datetime'])
           if not is_valid:
               raise ValueError(f"Invalid datetime: {search_params['datetime']}")
           search_params['datetime'] = normalized
       
       # Create client and search
       if provider == 'pc':
           client = ogapi.planetary_computer(auto_sign=True)
       else:
           client = ogapi.earth_search()
       
       return client.search(**search_params)

These factory functions provide convenient, validated ways to create clients and configure operations while maintaining flexibility for advanced use cases.
