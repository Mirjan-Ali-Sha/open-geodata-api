Getting Started
===============

Welcome to Open Geodata API! This section will help you get up and running quickly with satellite data access.

.. toctree::
   :maxdepth: 2

   installation
   quickstart
   configuration
   first-steps

What You'll Learn
-----------------

📦 **Installation**: How to install the package and dependencies  
⚡ **Quick Start**: Your first 5 minutes with the API  
⚙️ **Configuration**: Setting up clients and authentication  
🚀 **First Steps**: Understanding core concepts and workflows  

Prerequisites
-------------

Before you begin, make sure you have:

- **Python 3.8+** installed on your system
- **Basic Python knowledge** (import statements, functions, working with dictionaries)
- **Internet connection** for API access
- **Optional**: Basic understanding of satellite imagery concepts

What is Open Geodata API?
-------------------------

Open Geodata API is a unified Python client library that provides seamless access to multiple open geospatial data APIs. It focuses on **API access, search, and URL management** while maintaining maximum flexibility for data reading and processing.

**Key Features**:

✅ **One Interface** - Access Microsoft Planetary Computer & AWS EarthSearch APIs  <br>
✅ **Unified Search** - Search across multiple collections with a single query  <br>
✅ **Automatic Signing** - Handles authentication and URL signing for you  <br>
✅ **Smart URLs** - Automatic signing, validation, and expiration handling  <br>
✅ **Your Choice** - Use any raster package (rioxarray, rasterio, GDAL)  <br>
✅ **Complete Workflow** - Search → Filter → Download → Analyze  <br>

**Philosophy**: We provide URLs - you choose how to read them!

Supported Data Sources
----------------------

**Microsoft Planetary Computer**
- Comprehensive collection catalog
- Automatic URL signing
- High-performance access
- Requires authentication (free tier available)

**Element84 EarthSearch**  
- Open access (no authentication)
- AWS-hosted data
- Direct COG access
- Permanent URLs

**Available Collections**:
- Sentinel-2 (optical imagery, 10-60m resolution)
- Landsat (long-term archive, 30m resolution)
- MODIS (daily global coverage, 250m-1km resolution)
- Sentinel-1 (SAR imagery, weather-independent)
- NAIP (high-resolution aerial imagery, US)
- And many more...

Quick Overview
--------------

Here's what a typical workflow looks like:

.. code-block:: python

   import open_geodata_api as ogapi
   
   # 1. Create client
   pc = ogapi.planetary_computer(auto_sign=True)
   
   # 2. Search for data
   results = pc.search(
       collections=["sentinel-2-l2a"],
       bbox=[-122.5, 47.5, -122.0, 48.0],
       datetime="2024-01-01/2024-03-31"
   )
   
   # 3. Get items and URLs
   items = results.get_all_items()
   item = items[0]
   blue_url = item.get_asset_url('B02')  # Automatically signed!
   
   # 4. Use with ANY raster package
   import rioxarray
   data = rioxarray.open_rasterio(blue_url)

Learning Path
-------------

**For Beginners**:
1. Start with :doc:`installation`
2. Follow the :doc:`quickstart` guide
3. Learn about :doc:`configuration`
4. Practice with :doc:`first-steps`

**For Experienced Users**:
1. Quick :doc:`installation`
2. Jump to :doc:`../examples/index` for advanced patterns
3. Check :doc:`../api-reference/index` for detailed documentation

**For CLI Users**:
1. Install the package
2. Try: ``ogapi collections list``
3. See :doc:`../cli-reference/index` for complete CLI documentation

Next Steps
----------

Ready to begin? Start with the installation guide!

.. raw:: html

   <div class="next-steps">
     <a href="installation.html" class="btn-primary">📦 Install Now</a>
     <a href="quickstart.html" class="btn-secondary">⚡ Quick Start</a>
   </div>

Need Help?
----------

- **Documentation**: Complete guides and examples
- **CLI Help**: ``ogapi --help`` for command-line assistance
- **GitHub Issues**: Report bugs or request features
- **Examples**: Check the examples repository for real-world use cases

Let's get started with satellite data access made simple! 🛰️
