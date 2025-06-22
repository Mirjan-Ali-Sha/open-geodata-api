Architecture and Design
=======================

This document describes the architecture and design principles of Open Geodata API.

Design Philosophy
-----------------

Core Principles
~~~~~~~~~~~~~~~

**1. Unified Interface**
   Provide a single, consistent interface across multiple satellite data APIs while preserving the unique capabilities of each provider.

**2. URL-Centric Approach**
   Focus on providing ready-to-use URLs rather than forcing users into specific data reading workflows. Users maintain complete freedom in how they process the data.

**3. Provider Abstraction**
   Abstract away the complexities of different API providers while maintaining transparency about the underlying data sources.

**4. Zero Lock-in**
   Ensure users can easily switch between providers or integrate with any raster processing library without being locked into our ecosystem.

**5. Production Ready**
   Build with robust error handling, comprehensive testing, and performance optimizations suitable for production deployments.

Package Architecture
--------------------

High-Level Structure
~~~~~~~~~~~~~~~~~~~~

.. code-block:: text

   open-geodata-api/
   ├── Core Layer (Provider-agnostic)
   │   ├── STAC Data Models
   │   ├── URL Management
   │   └── Common Interfaces
   ├── Provider Layer (API-specific)
   │   ├── Planetary Computer Client
   │   ├── EarthSearch Client
   │   └── Provider Abstractions
   ├── Utility Layer (Helper functions)
   │   ├── Filtering Functions
   │   ├── Download Management
   │   └── Data Processing Helpers
   ├── CLI Layer (Command-line interface)
   │   ├── Collection Commands
   │   ├── Search Commands
   │   ├── Download Commands
   │   └── Utility Commands
   └── Factory Layer (User interface)
       ├── Client Creation
       ├── Configuration Management
       └── Convenience Functions

Module Organization
~~~~~~~~~~~~~~~~~~~

**open_geodata_api/**

.. code-block:: text

   ├── __init__.py              # Public API exports
   ├── core/                    # Core data models and interfaces
   │   ├── __init__.py
   │   ├── items.py            # STACItem and STACAsset classes
   │   ├── collections.py      # STACItemCollection and search results
   │   └── base.py             # Base classes and interfaces
   ├── clients/                 # Provider-specific implementations
   │   ├── __init__.py
   │   ├── planetary_computer.py  # PC client implementation
   │   ├── earth_search.py       # EarthSearch client implementation
   │   └── base.py              # Base client interface
   ├── utils/                   # Utility functions
   │   ├── __init__.py
   │   ├── download.py         # Download functions
   │   ├── filtering.py        # Data filtering functions
   │   ├── url_management.py   # URL signing/validation
   │   └── helpers.py          # General helper functions
   ├── cli/                     # Command-line interface
   │   ├── __init__.py
   │   ├── main.py             # Main CLI entry point
   │   ├── collections.py      # Collection management commands
   │   ├── search.py           # Search commands
   │   ├── items.py            # Item management commands
   │   ├── download.py         # Download commands
   │   └── utils.py            # Utility commands
   └── factory.py              # Client factory functions

Core Layer Design
-----------------

STAC Data Models
~~~~~~~~~~~~~~~~

The core layer implements STAC (SpatioTemporal Asset Catalog) compliant data models:

.. code-block:: python

   class STACAsset:
       """Represents a single asset (file) within a STAC item."""
       
       def __init__(self, asset_data, provider=None):
           self.href = asset_data['href']
           self.type = asset_data.get('type')
           self.title = asset_data.get('title')
           self.provider = provider
       
       def get_signed_url(self):
           """Get signed URL if needed for this provider."""
           # Provider-specific URL signing logic

   class STACItem:
       """Represents a single satellite scene/product."""
       
       def __init__(self, item_data, provider=None):
           self.id = item_data['id']
           self.collection = item_data['collection']
           self.properties = item_data['properties']
           self.assets = {k: STACAsset(v, provider) for k, v in item_data['assets'].items()}
           self.bbox = item_data['bbox']
           self.provider = provider
       
       def get_asset_url(self, asset_name, signed=True):
           """Get URL for specific asset with automatic signing."""
           
       def get_all_asset_urls(self, signed=True):
           """Get URLs for all assets."""

   class STACItemCollection:
       """Collection of STAC items with bulk operations."""
       
       def __init__(self, items_data, provider=None):
           self.items = [STACItem(item, provider) for item in items_data]
           self.provider = provider
       
       def to_dataframe(self):
           """Convert to pandas DataFrame for analysis."""
           
       def get_all_urls(self, asset_keys=None):
           """Get URLs for all items and specified assets."""

URL Management System
~~~~~~~~~~~~~~~~~~~~~

The URL management system handles provider-specific requirements:

.. code-block:: python

   class URLManager:
       """Manages URL signing, validation, and refresh."""
       
       @staticmethod
       def is_signed_url(url):
           """Check if URL contains signature parameters."""
           
       @staticmethod
       def is_url_expired(url):
           """Check if signed URL has expired."""
           
       @staticmethod
       def sign_url(url, provider):
           """Sign URL for given provider."""
           
       @staticmethod
       def refresh_url_if_needed(url, provider):
           """Automatically refresh expired URLs."""

Provider Layer Design
---------------------

Base Client Interface
~~~~~~~~~~~~~~~~~~~~~

All provider clients implement a common interface:

.. code-block:: python

   class BaseAPIClient:
       """Base class for all API clients."""
       
       def __init__(self, **kwargs):
           self.provider_name = None
           self.base_url = None
       
       def list_collections(self):
           """List available collections."""
           raise NotImplementedError
       
       def get_collection_info(self, collection_id):
           """Get detailed collection information."""
           raise NotImplementedError
       
       def search(self, collections, bbox=None, datetime=None, query=None, limit=10):
           """Search for items."""
           raise NotImplementedError
       
       def _make_request(self, endpoint, params):
           """Make HTTP request with error handling."""
           raise NotImplementedError

Provider-Specific Implementations
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Each provider has its own implementation with specific optimizations:

**Planetary Computer Client:**

.. code-block:: python

   class PlanetaryComputerCollections(BaseAPIClient):
       """Planetary Computer API client."""
       
       def __init__(self, auto_sign=True):
           super().__init__()
           self.provider_name = 'planetary_computer'
           self.base_url = 'https://planetarycomputer.microsoft.com/api/stac/v1'
           self.auto_sign = auto_sign
           
           # Import PC package for signing
           try:
               import planetary_computer as pc
               self.pc = pc
           except ImportError:
               if auto_sign:
                   raise ImportError("planetary-computer package required for auto-signing")
       
       def search(self, **kwargs):
           """Search with automatic URL signing."""
           results = super().search(**kwargs)
           
           if self.auto_sign:
               # Sign all URLs in results
               results = self._sign_results(results)
           
           return results

**EarthSearch Client:**

.. code-block:: python

   class EarthSearchCollections(BaseAPIClient):
       """EarthSearch API client."""
       
       def __init__(self):
           super().__init__()
           self.provider_name = 'earth_search'
           self.base_url = 'https://earth-search.aws.element84.com/v1'
           # No authentication required
       
       def search(self, **kwargs):
           """Search with direct URL access."""
           results = super().search(**kwargs)
           # URLs are ready to use without signing
           return results

Data Flow Architecture
----------------------

Search Flow
~~~~~~~~~~~

.. code-block:: text

   User Request
        ↓
   [Factory Function] → Create appropriate client
        ↓
   [Client.search()] → Validate parameters
        ↓
   [HTTP Request] → Query provider API
        ↓
   [Response Processing] → Parse STAC JSON
        ↓
   [STACItemCollection] → Wrap in our data models
        ↓
   [URL Management] → Apply provider-specific URL handling
        ↓
   Return to User

URL Access Flow
~~~~~~~~~~~~~~~

.. code-block:: text

   User requests asset URL
        ↓
   [STACItem.get_asset_url()]
        ↓
   Check provider type
        ↓
   ┌─ Planetary Computer ─┐    ┌─ EarthSearch ─┐
   │ Check if signed      │    │ Direct URL    │
   │ Check expiration     │    │ Validate      │
   │ Re-sign if needed    │    │ Return        │
   │ Return signed URL    │    └───────────────┘
   └───────────────────────┘
        ↓
   Ready-to-use URL

Download Flow
~~~~~~~~~~~~~

.. code-block:: text

   User initiates download
        ↓
   [download_datasets()] → Detect input type
        ↓
   ┌─ STAC Items ─┐  ┌─ URL Dict ─┐  ┌─ JSON File ─┐
   │ Get URLs     │  │ Use direct │  │ Load URLs   │
   │ Apply filters│  │ URLs       │  │ Validate    │
   └──────────────┘  └────────────┘  └─────────────┘
        ↓
   [URL Management] → Refresh expired URLs
        ↓
   [Parallel Download] → Download with progress tracking
        ↓
   [File Organization] → Create folder structure
        ↓
   Return download results

Error Handling Strategy
-----------------------

Layered Error Handling
~~~~~~~~~~~~~~~~~~~~~~

**1. Network Layer**
   - Connection timeouts and retries
   - HTTP status code handling
   - Rate limiting compliance

**2. API Layer**
   - Provider-specific error codes
   - Authentication failures
   - Quota exceeded handling

**3. Data Layer**
   - Invalid STAC responses
   - Missing or malformed data
   - Type validation errors

**4. User Layer**
   - Helpful error messages
   - Suggested fixes
   - Graceful degradation

Error Recovery Mechanisms
~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   class RobustAPIClient:
       """Client with comprehensive error handling."""
       
       def _make_request_with_retry(self, url, params, max_retries=3):
           """Make request with automatic retry logic."""
           
           for attempt in range(max_retries + 1):
               try:
                   response = requests.get(url, params=params, timeout=30)
                   
                   if response.status_code == 200:
                       return response.json()
                   
                   elif response.status_code == 429:  # Rate limited
                       wait_time = 2 ** attempt  # Exponential backoff
                       time.sleep(wait_time)
                       continue
                   
                   elif response.status_code >= 500:  # Server error
                       if attempt < max_retries:
                           time.sleep(1)
                           continue
                   
                   else:
                       # Client error - don't retry
                       response.raise_for_status()
               
               except requests.exceptions.Timeout:
                   if attempt < max_retries:
                       continue
                   raise
               
               except requests.exceptions.ConnectionError:
                   if attempt < max_retries:
                       time.sleep(2)
                       continue
                   raise
           
           raise RuntimeError(f"Failed after {max_retries + 1} attempts")

Performance Considerations
--------------------------

Caching Strategy
~~~~~~~~~~~~~~~~

**1. Collection Metadata Caching**
   - Cache collection lists for short periods
   - Reduce redundant API calls
   - Configurable cache TTL

**2. URL Signing Caching**
   - Cache signed URLs until near expiration
   - Batch signing operations
   - Proactive refresh for long-running processes

**3. Search Result Caching**
   - Optional caching of search results
   - User-controlled cache behavior
   - Memory-efficient storage

Lazy Loading
~~~~~~~~~~~~

.. code-block:: python

   class LazySTACItemCollection:
       """Collection that loads items on demand."""
       
       def __init__(self, search_results, provider):
           self._raw_results = search_results
           self._items = None
           self.provider = provider
       
       @property
       def items(self):
           """Load items only when first accessed."""
           if self._items is None:
               self._items = [STACItem(item, self.provider) 
                             for item in self._raw_results]
           return self._items

Memory Management
~~~~~~~~~~~~~~~~~

**1. Streaming for Large Results**
   - Process items in batches
   - Generator-based iteration
   - Configurable batch sizes

**2. Efficient Data Structures**
   - Minimize memory footprint
   - Share common metadata
   - Lazy property evaluation

**3. Resource Cleanup**
   - Automatic connection pooling
   - Context managers for resources
   - Garbage collection hints

Testing Architecture
--------------------

Testing Strategy
~~~~~~~~~~~~~~~~

**1. Unit Tests**
   - Test individual functions and classes
   - Mock external API calls
   - Fast execution (< 1 second per test)

**2. Integration Tests**
   - Test provider API integration
   - Use real API calls (rate limited)
   - Verify end-to-end workflows

**3. Performance Tests**
   - Benchmark critical operations
   - Memory usage validation
   - Scalability testing

Mock Framework
~~~~~~~~~~~~~~

.. code-block:: python

   class MockAPIProvider:
       """Mock provider for testing."""
       
       def __init__(self, responses):
           self.responses = responses
           self.call_count = 0
       
       def get(self, url, **kwargs):
           """Mock HTTP GET response."""
           self.call_count += 1
           
           # Return predefined response based on URL
           for pattern, response in self.responses.items():
               if pattern in url:
                   return MockResponse(response)
           
           raise ValueError(f"No mock response for: {url}")

Extensibility Design
--------------------

Plugin Architecture
~~~~~~~~~~~~~~~~~~~

The design supports adding new providers:

.. code-block:: python

   class NewProviderClient(BaseAPIClient):
       """Template for new provider integration."""
       
       def __init__(self, **kwargs):
           super().__init__()
           self.provider_name = 'new_provider'
           self.base_url = 'https://api.newprovider.com'
           # Provider-specific initialization
       
       def list_collections(self):
           """Implement provider-specific collection listing."""
           
       def search(self, **kwargs):
           """Implement provider-specific search."""

Configuration System
~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   class Configuration:
       """Global configuration management."""
       
       def __init__(self):
           self.default_provider = 'planetary_computer'
           self.cache_ttl = 300  # 5 minutes
           self.max_retries = 3
           self.timeout = 30
       
       def update_from_env(self):
           """Update configuration from environment variables."""
           self.default_provider = os.getenv('OGAPI_DEFAULT_PROVIDER', self.default_provider)
           self.cache_ttl = int(os.getenv('OGAPI_CACHE_TTL', self.cache_ttl))

Future Architecture Considerations
----------------------------------

Planned Enhancements
~~~~~~~~~~~~~~~~~~~~

**1. Additional Providers**
   - NASA EarthData integration
   - Google Earth Engine compatibility
   - Custom STAC API support

**2. Advanced Caching**
   - Persistent cache storage
   - Distributed cache support
   - Smart cache invalidation

**3. Async Support**
   - Asynchronous API clients
   - Concurrent request handling
   - Improved performance for bulk operations

**4. Enhanced CLI**
   - Interactive mode
   - Configuration file support
   - Workflow orchestration

Backwards Compatibility
~~~~~~~~~~~~~~~~~~~~~~~

The architecture is designed to maintain backwards compatibility:

- Stable public API contracts
- Deprecation warnings for changes
- Migration guides for major updates
- Semantic versioning compliance

This architecture provides a solid foundation for reliable, extensible, and high-performance satellite data access while maintaining simplicity for end users.
