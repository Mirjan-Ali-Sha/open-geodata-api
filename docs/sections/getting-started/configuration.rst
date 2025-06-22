Configuration
=============

Learn how to configure Open Geodata API clients, authentication, and global settings for optimal performance.

Client Configuration
--------------------

Basic Client Setup
~~~~~~~~~~~~~~~~~~

Open Geodata API provides factory functions for easy client creation:

.. code-block:: python

   import open_geodata_api as ogapi
   
   # Planetary Computer with auto-signing
   pc = ogapi.planetary_computer(auto_sign=True)
   
   # EarthSearch (no auth required)
   es = ogapi.earth_search()
   
   # Get both clients at once
   clients = ogapi.get_clients(pc_auto_sign=True)
   pc = clients['planetary_computer']
   es = clients['earth_search']

Advanced Client Configuration
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Customize client behavior with additional parameters:

.. code-block:: python

   # Planetary Computer with custom settings
   pc = ogapi.planetary_computer(
       auto_sign=True,              # Enable automatic URL signing
       cache_signed_urls=True,      # Cache signed URLs for performance
       timeout=60,                  # Request timeout in seconds
       max_retries=3,              # Maximum retry attempts
       retry_delay=2               # Delay between retries (seconds)
   )
   
   # EarthSearch with validation
   es = ogapi.earth_search(
       auto_validate=True,         # Validate URLs when generated
       timeout=30,                 # Custom timeout
       base_url=None              # Use default endpoint
   )

Authentication Setup
--------------------

Planetary Computer Authentication
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Planetary Computer requires the ``planetary-computer`` package for URL signing:

**Installation**:

.. code-block:: bash

   pip install planetary-computer

**Basic Setup**:

.. code-block:: python

   # The planetary-computer package handles authentication automatically
   import open_geodata_api as ogapi
   
   try:
       pc = ogapi.planetary_computer(auto_sign=True)
       print("✅ Planetary Computer client ready")
   except ImportError:
       print("❌ Please install: pip install planetary-computer")

**Testing Authentication**:

.. code-block:: python

   # Test if signing works
   def test_pc_authentication():
       try:
           pc = ogapi.planetary_computer(auto_sign=True)
           
           # Try to list collections
           collections = pc.list_collections()
           print(f"✅ Authentication working: {len(collections)} collections available")
           
           # Test URL signing
           results = pc.search(collections=['sentinel-2-l2a'], limit=1)
           if results.get_all_items():
               item = results.get_all_items()[0]
               url = item.get_asset_url(item.list_assets()[0])
               print(f"✅ URL signing working: {url[:50]}...")
           
           return True
           
       except Exception as e:
           print(f"❌ Authentication failed: {e}")
           return False
   
   # Run test
   test_pc_authentication()

EarthSearch (No Authentication)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

EarthSearch requires no authentication:

.. code-block:: python

   # EarthSearch is ready to use immediately
   es = ogapi.earth_search()
   
   # Test connectivity
   try:
       collections = es.list_collections()
       print(f"✅ EarthSearch ready: {len(collections)} collections available")
   except Exception as e:
       print(f"❌ Connection failed: {e}")

Global Configuration
--------------------

Setting Default Behaviors
~~~~~~~~~~~~~~~~~~~~~~~~~

Configure global defaults for all operations:

.. code-block:: python

   # Set global defaults
   ogapi.set_global_defaults(
       default_provider='pc',       # Default to Planetary Computer
       auto_sign=True,             # Enable auto-signing by default
       timeout=60,                 # Default timeout
       max_retries=3,              # Default retry count
       cache_timeout=3600,         # Cache timeout (1 hour)
       download_chunk_size=8192,   # Default download chunk size
       show_progress=True          # Show progress bars by default
   )
   
   # Check current configuration
   config = ogapi.get_global_config()
   print(f"Current defaults: {config}")

Environment Variables
~~~~~~~~~~~~~~~~~~~~~

Configure behavior using environment variables:

.. code-block:: bash

   # Set environment variables
   export OGAPI_DEFAULT_PROVIDER="pc"
   export OGAPI_AUTO_SIGN="true"
   export OGAPI_TIMEOUT="60"
   export OGAPI_MAX_RETRIES="3"
   export OGAPI_CACHE_DIR="./ogapi_cache"
   export OGAPI_LOG_LEVEL="INFO"

.. code-block:: python

   # Environment variables are automatically loaded
   import open_geodata_api as ogapi
   
   # Create client using environment defaults
   pc = ogapi.planetary_computer()  # Uses ENV settings

Configuration Files
~~~~~~~~~~~~~~~~~~~

Use configuration files for complex setups:

**config.yaml**:

.. code-block:: yaml

   # Open Geodata API Configuration
   default_provider: "pc"
   
   planetary_computer:
     auto_sign: true
     cache_signed_urls: true
     timeout: 60
     max_retries: 3
   
   earth_search:
     auto_validate: false
     timeout: 30
     max_retries: 2
   
   download:
     chunk_size: 8192
     max_workers: 4
     show_progress: true
     resume_downloads: true
   
   quality:
     default_cloud_threshold: 30
     min_data_coverage: 80
   
   paths:
     cache_dir: "./ogapi_cache"
     download_dir: "./downloads"
     log_dir: "./logs"

**Loading Configuration**:

.. code-block:: python

   import yaml
   import open_geodata_api as ogapi
   
   # Load configuration
   with open('config.yaml', 'r') as f:
       config = yaml.safe_load(f)
   
   # Apply configuration
   ogapi.set_global_defaults(**config.get('default', {}))
   
   # Create clients with config
   pc_config = config.get('planetary_computer', {})
   pc = ogapi.planetary_computer(**pc_config)

Provider-Specific Configuration
-------------------------------

Planetary Computer Settings
~~~~~~~~~~~~~~~~~~~~~~~~~~~

Configure PC-specific behaviors:

.. code-block:: python

   # Advanced PC configuration
   pc = ogapi.planetary_computer(
       auto_sign=True,
       cache_signed_urls=True,     # Cache for performance
       cache_ttl=3600,             # Cache time-to-live (seconds)
       sign_batch_size=50,         # Batch URL signing
       retry_expired_urls=True,    # Auto-retry expired URLs
       prefer_cog=True,            # Prefer Cloud Optimized GeoTIFFs
       validate_collections=True   # Validate collection names
   )

EarthSearch Settings
~~~~~~~~~~~~~~~~~~~~

Configure ES-specific behaviors:

.. code-block:: python

   # Advanced ES configuration  
   es = ogapi.earth_search(
       auto_validate=True,         # Validate URLs
       check_availability=False,   # Skip availability checks
       prefer_aws_region='us-west-2',  # Preferred AWS region
       timeout=30,                 # Conservative timeout
       connection_pool_size=10     # HTTP connection pool size
   )

Performance Configuration
-------------------------

Optimizing for Speed
~~~~~~~~~~~~~~~~~~~~

Configure for maximum performance:

.. code-block:: python

   # High-performance setup
   config = {
       'timeout': 120,             # Longer timeout for large operations
       'max_retries': 5,           # More retries for reliability
       'connection_pool_size': 20, # More concurrent connections
       'cache_signed_urls': True,  # Aggressive caching
       'cache_ttl': 7200,         # 2-hour cache
       'batch_size': 100,         # Larger batch operations
       'download_chunk_size': 32768,  # Larger chunks
       'max_workers': 8           # More parallel workers
   }
   
   # Apply performance config
   pc = ogapi.planetary_computer(**config)

Optimizing for Reliability
~~~~~~~~~~~~~~~~~~~~~~~~~~~

Configure for maximum reliability:

.. code-block:: python

   # Reliability-focused setup
   config = {
       'timeout': 30,              # Conservative timeout
       'max_retries': 10,          # Many retries
       'retry_delay': 5,           # Longer delays between retries
       'exponential_backoff': True, # Exponential retry delays
       'validate_all_urls': True,   # Validate everything
       'auto_refresh_expired': True, # Auto-refresh expired URLs
       'connection_pool_size': 5,   # Conservative connection pool
       'rate_limit': 0.5          # Rate limiting (requests per second)
   }
   
   pc = ogapi.planetary_computer(**config)

Memory Management
~~~~~~~~~~~~~~~~~

Configure for large datasets:

.. code-block:: python

   # Memory-efficient configuration
   config = {
       'lazy_loading': True,       # Load data only when needed
       'chunk_processing': True,   # Process in chunks
       'max_cache_size': 1000,    # Limit cache size
       'gc_frequency': 100,       # Garbage collection frequency
       'streaming_downloads': True, # Stream large downloads
       'temp_dir': '/tmp/ogapi'   # Temporary file location
   }

Logging Configuration
---------------------

Setting Up Logging
~~~~~~~~~~~~~~~~~~

Configure logging for debugging and monitoring:

.. code-block:: python

   import logging
   import open_geodata_api as ogapi
   
   # Basic logging setup
   logging.basicConfig(
       level=logging.INFO,
       format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
       handlers=[
           logging.FileHandler('ogapi.log'),
           logging.StreamHandler()
       ]
   )
   
   # Enable debug logging for development
   logging.getLogger('open_geodata_api').setLevel(logging.DEBUG)

Advanced Logging
~~~~~~~~~~~~~~~~

.. code-block:: python

   # Advanced logging configuration
   import logging.config
   
   LOGGING_CONFIG = {
       'version': 1,
       'disable_existing_loggers': False,
       'formatters': {
           'detailed': {
               'format': '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
           },
           'simple': {
               'format': '%(levelname)s - %(message)s'
           }
       },
       'handlers': {
           'file': {
               'class': 'logging.FileHandler',
               'filename': 'ogapi_detailed.log',
               'formatter': 'detailed',
               'level': 'DEBUG'
           },
           'console': {
               'class': 'logging.StreamHandler',
               'formatter': 'simple',
               'level': 'INFO'
           }
       },
       'loggers': {
           'open_geodata_api': {
               'handlers': ['file', 'console'],
               'level': 'DEBUG',
               'propagate': False
           }
       }
   }
   
   logging.config.dictConfig(LOGGING_CONFIG)

Configuration Validation
-------------------------

Validating Your Setup
~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   def validate_configuration():
       """Comprehensive configuration validation."""
       
       print("🔧 Validating Open Geodata API Configuration...")
       
       # Test basic imports
       try:
           import open_geodata_api as ogapi
           print("✅ Package import successful")
       except ImportError as e:
           print(f"❌ Import failed: {e}")
           return False
       
       # Test client creation
       try:
           pc = ogapi.planetary_computer(auto_sign=True)
           print("✅ Planetary Computer client created")
       except Exception as e:
           print(f"⚠️ PC client creation failed: {e}")
       
       try:
           es = ogapi.earth_search()
           print("✅ EarthSearch client created")
       except Exception as e:
           print(f"❌ ES client creation failed: {e}")
           return False
       
       # Test connectivity
       try:
           collections = es.list_collections()
           print(f"✅ EarthSearch connectivity: {len(collections)} collections")
       except Exception as e:
           print(f"❌ EarthSearch connectivity failed: {e}")
       
       # Test search functionality
       try:
           results = es.search(collections=['sentinel-2-l2a'], limit=1)
           items = results.get_all_items()
           print(f"✅ Search functionality: {len(items)} test items")
       except Exception as e:
           print(f"❌ Search functionality failed: {e}")
       
       print("🎉 Configuration validation complete!")
       return True
   
   # Run validation
   validate_configuration()

Troubleshooting Configuration
-----------------------------

Common Configuration Issues
~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Import Errors**:

.. code-block:: python

   # Check package installation
   try:
       import open_geodata_api as ogapi
       print(f"✅ Package version: {ogapi.__version__}")
   except ImportError:
       print("❌ Package not installed: pip install open-geodata-api")

**Authentication Issues**:

.. code-block:: python

   # Test PC authentication
   try:
       import planetary_computer
       print("✅ Planetary Computer package available")
   except ImportError:
       print("❌ Install PC package: pip install planetary-computer")

**Connection Issues**:

.. code-block:: python

   # Test network connectivity
   import requests
   
   endpoints = [
       'https://planetarycomputer.microsoft.com/api/stac/v1/',
       'https://earth-search.aws.element84.com/v1/'
   ]
   
   for endpoint in endpoints:
       try:
           response = requests.get(endpoint, timeout=10)
           print(f"✅ {endpoint}: HTTP {response.status_code}")
       except Exception as e:
           print(f"❌ {endpoint}: {e}")

Configuration Best Practices
-----------------------------

**Security**:
- Never hardcode API keys in source code
- Use environment variables for sensitive settings
- Rotate authentication credentials regularly

**Performance**:
- Enable caching for frequently accessed data
- Use appropriate timeouts for your network conditions
- Configure retry logic for unreliable connections

**Reliability**:
- Implement proper error handling
- Use logging for debugging and monitoring
- Test configuration changes thoroughly

**Maintainability**:
- Use configuration files for complex setups
- Document custom configurations
- Version control configuration files

Next Steps
----------

With configuration complete, you're ready to explore:

- :doc:`first-steps` - Understanding core concepts
- :doc:`../examples/index` - Real-world examples  
- :doc:`../api-reference/index` - Complete API documentation

Your Open Geodata API setup is now optimized for your specific needs! 🚀
