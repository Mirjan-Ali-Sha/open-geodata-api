Introduction
============

What is Open Geodata API?
-------------------------

**Open Geodata API** is a unified Python client library that provides seamless access to multiple open geospatial data APIs. It focuses on **API access, search, and URL management** while maintaining maximum flexibility for data reading and processing.

Supported APIs
--------------

.. list-table::
   :header-rows: 1
   :widths: 20 20 20 40

   * - API
     - Provider
     - Authentication
     - URL Handling
   * - **Planetary Computer**
     - Microsoft
     - API Key + Signing
     - Automatic signing
   * - **EarthSearch**
     - Element84/AWS
     - None required
     - URL validation

Package Architecture
--------------------

.. code-block:: text

   open-geodata-api/
   ├── Core Classes (Universal)
   │   ├── STACItem           # Individual products
   │   ├── STACItemCollection # Groups of products  
   │   ├── STACAsset          # Individual files
   │   └── STACSearch         # Search results
   ├── API Clients
   │   ├── PlanetaryComputerCollections
   │   └── EarthSearchCollections
   └── Utilities
       ├── URL signing (PC)
       ├── URL validation (ES)
       └── Filtering functions

Provider-Specific Handling
--------------------------

.. list-table::
   :header-rows: 1
   :widths: 25 25 25

   * - Feature
     - Planetary Computer
     - EarthSearch
   * - **Authentication**
     - Automatic via planetary-computer package
     - None required
   * - **URL Signing**
     - Automatic (auto_sign=True)
     - Not applicable
   * - **Asset Naming**
     - B01, B02, B03...
     - coastal, blue, green...
   * - **Cloud Cover**
     - eo:cloud_cover
     - eo:cloud_cover

Philosophy
----------

🎯 **Core Focus**: We provide URLs - you choose how to read them!  
📦 **Use Any Package**: rioxarray, rasterio, GDAL, or any package you prefer  
🚀 **Maximum Flexibility**: Zero restrictions on your workflow  

Key Benefits
------------

- **Unified interface** across multiple APIs
- **Automatic URL signing/validation**
- **Consistent error handling**
- **No lock-in** to specific data reading packages
- **Built-in best practices**
- **Production ready** with comprehensive testing
