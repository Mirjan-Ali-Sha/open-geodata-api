Client Classes
==============

Client classes provide access to different satellite data APIs with a unified interface.

BaseAPIClient
-------------

.. autoclass:: open_geodata_api.clients.base.BaseAPIClient
   :members:
   :undoc-members:
   :show-inheritance:

Abstract base class for all API clients defining the common interface.

**Abstract Methods**:

- ``list_collections()``: List available collections
- ``get_collection_info(collection_id)``: Get collection metadata
- ``search(**kwargs)``: Search for items

PlanetaryComputerCollections
----------------------------

.. autoclass:: open_geodata_api.clients.planetary_computer.PlanetaryComputerCollections
   :members:
   :undoc-members:
   :show-inheritance:

Client for accessing Microsoft Planetary Computer STAC API.

**Features**:

- Automatic URL signing for data access
- Comprehensive collection catalog
- Advanced search capabilities
- Authentication via planetary-computer package

**Authentication**:

Requires the ``planetary-computer`` package for URL signing:

.. code-block:: bash

   pip install planetary-computer

**Usage Example**:

.. code-block:: python

   import open_geodata_api as ogapi
   
   # Create client with auto-signing
   pc = ogapi.planetary_computer(auto_sign=True)
   
   # List collections
   collections = pc.list_collections()
   print(f"Available: {len(collections)} collections")
   
   # Get collection info
   info = pc.get_collection_info('sentinel-2-l2a')
   print(f"Title: {info['title']}")
   
   # Search for data
   results = pc.search(
       collections=['sentinel-2-l2a'],
       bbox=[-122.5, 47.5, -122.0, 48.0],
       datetime='2024-01-01/2024-03-31',
       query={'eo:cloud_cover': {'lt': 20}}
   )

**Advanced Search Options**:

.. code-block:: python

   # Complex query with multiple filters
   results = pc.search(
       collections=['sentinel-2-l2a'],
       bbox=[-122.5, 47.5, -122.0, 48.0],
       datetime='2024-06-01/2024-08-31',
       query={
           'eo:cloud_cover': {'lt': 20},
           'platform': {'eq': 'sentinel-2a'},
           's2:processing_baseline': {'gte': '04.00'}
       },
       limit=50
   )

EarthSearchCollections
----------------------

.. autoclass:: open_geodata_api.clients.earth_search.EarthSearchCollections
   :members:
   :undoc-members:
   :show-inheritance:

Client for accessing Element84 EarthSearch STAC API.

**Features**:

- No authentication required
- Open access to public datasets
- Direct COG (Cloud Optimized GeoTIFF) access
- AWS-hosted data

**Usage Example**:

.. code-block:: python

   import open_geodata_api as ogapi
   
   # Create client (no authentication needed)
   es = ogapi.earth_search()
   
   # List collections
   collections = es.list_collections()
   
   # Search for data
   results = es.search(
       collections=['sentinel-2-l2a'],
       bbox=[-122.5, 47.5, -122.0, 48.0],
       datetime='2024-01-01T00:00:00Z/2024-03-31T23:59:59Z',
       query={'eo:cloud_cover': {'lt': 20}}
   )

**Asset Naming Differences**:

.. code-block:: python

   # EarthSearch uses descriptive names
   item = es_results.get_all_items()[0]
   assets = item.list_assets()
   # Returns: ['coastal', 'blue', 'green', 'red', 'nir', 'swir16', 'swir22', ...]
   
   # Get RGB bands
   rgb_urls = item.get_band_urls(['red', 'green', 'blue'])

Client Comparison
-----------------

Feature Comparison
~~~~~~~~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 30 35 35

   * - Feature
     - Planetary Computer
     - EarthSearch
   * - **Authentication**
     - Required (planetary-computer package)
     - None required
   * - **URL Signing**
     - Automatic with auto_sign=True
     - Not needed
   * - **Asset Naming**
     - Original (B01, B02, B03...)
     - Descriptive (coastal, blue, green...)
   * - **Search Performance**
     - Fast with advanced filters
     - Good performance
   * - **Data Access**
     - Signed URLs (temporary)
     - Direct URLs (permanent)

When to Use Which
~~~~~~~~~~~~~~~~~

**Use Planetary Computer when**:
- You need comprehensive data coverage
- Performance is critical
- You want the latest datasets
- You can handle authentication requirements

**Use EarthSearch when**:
- You prefer no authentication
- You're doing quick exploration
- You need permanent URLs
- You want to avoid API quotas

Multi-Client Workflows
----------------------

Using Both Clients
~~~~~~~~~~~~~~~~~~

.. code-block:: python

   # Compare data availability
   def compare_providers(bbox, datetime_range, collection):
       """Compare data availability between providers."""
       
       pc = ogapi.planetary_computer(auto_sign=True)
       es = ogapi.earth_search()
       
       # Search both providers
       pc_results = pc.search(
           collections=[collection],
           bbox=bbox,
           datetime=datetime_range,
           limit=10
       )
       
       es_results = es.search(
           collections=[collection],
           bbox=bbox,
           datetime=datetime_range,
           limit=10
       )
       
       pc_items = pc_results.get_all_items()
       es_items = es_results.get_all_items()
       
       return {
           'planetary_computer': {
               'count': len(pc_items),
               'items': pc_items
           },
           'earth_search': {
               'count': len(es_items),
               'items': es_items
           }
       }

Unified Search Interface
~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   class UnifiedSearch:
       """Unified search across multiple providers."""
       
       def __init__(self):
           self.pc = ogapi.planetary_computer(auto_sign=True)
           self.es = ogapi.earth_search()
       
       def search_all(self, **kwargs):
           """Search all providers and combine results."""
           results = {}
           
           for name, client in [('pc', self.pc), ('es', self.es)]:
               try:
                   search_results = client.search(**kwargs)
                   items = search_results.get_all_items()
                   results[name] = items
               except Exception as e:
                   print(f"Search failed for {name}: {e}")
                   results[name] = []
           
           return results

Error Handling
--------------

Client Error Patterns
~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   def robust_client_usage():
       """Demonstrate robust client usage patterns."""
       
       try:
           # Try Planetary Computer first
           pc = ogapi.planetary_computer(auto_sign=True)
           results = pc.search(collections=['sentinel-2-l2a'], limit=5)
           return results.get_all_items()
           
       except ImportError:
           print("planetary-computer package not available")
           
       except Exception as e:
           print(f"Planetary Computer failed: {e}")
           
       try:
           # Fallback to EarthSearch
           es = ogapi.earth_search()
           results = es.search(collections=['sentinel-2-l2a'], limit=5)
           return results.get_all_items()
           
       except Exception as e:
           print(f"EarthSearch also failed: {e}")
           return []

Connection Issues
~~~~~~~~~~~~~~~~~

.. code-block:: python

   def test_client_connectivity():
       """Test client connectivity and diagnose issues."""
       
       clients = {
           'Planetary Computer': ogapi.planetary_computer(),
           'EarthSearch': ogapi.earth_search()
       }
       
       for name, client in clients.items():
           try:
               collections = client.list_collections()
               print(f"✅ {name}: Connected ({len(collections)} collections)")
           
           except requests.exceptions.Timeout:
               print(f"❌ {name}: Connection timeout")
           
           except requests.exceptions.ConnectionError:
               print(f"❌ {name}: Connection error")
           
           except Exception as e:
               print(f"❌ {name}: {e}")

Best Practices
--------------

Client Configuration
~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   # Recommended client setup
   
   # For production use
   pc = ogapi.planetary_computer(
       auto_sign=True,          # Enable automatic URL signing
       cache_signed_urls=True   # Cache signed URLs for performance
   )
   
   # For development/testing
   es = ogapi.earth_search(
       auto_validate=True       # Validate URLs when generated
   )

Resource Management
~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   # Use context managers for resource cleanup
   class ClientManager:
       def __init__(self, provider='pc'):
           self.provider = provider
           self.client = None
       
       def __enter__(self):
           if self.provider == 'pc':
               self.client = ogapi.planetary_computer(auto_sign=True)
           else:
               self.client = ogapi.earth_search()
           return self.client
       
       def __exit__(self, exc_type, exc_val, exc_tb):
           # Cleanup if needed
           if hasattr(self.client, 'close'):
               self.client.close()
   
   # Usage
   with ClientManager('pc') as client:
       results = client.search(collections=['sentinel-2-l2a'])
       items = results.get_all_items()
