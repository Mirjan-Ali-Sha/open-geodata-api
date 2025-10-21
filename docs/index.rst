.. raw:: html

   <p align="center">
     <img src="_static/icon.png" alt="Open Geodata API Icon" width="150" height="150" />
   </p>

Open Geodata API Documentation
==============================

**🛰️ Unified Python Client for Satellite Data Access**

Open Geodata API provides seamless access to multiple open geospatial data APIs with automatic URL management, intelligent filtering, and maximum flexibility for data reading.

Notebook (API Testing):
-----------------------
Here you can access or download the full API References for testing the Open Geodata API:

- `Download Test Open GeoData API References [Notebook] <https://github.com/Mirjan-Ali-Sha/open-geodata-api/raw/main/Test_Open_GeoData_API_References.ipynb>`_

- `Open in Google Colab <https://colab.research.google.com/github/Mirjan-Ali-Sha/open-geodata-api/blob/main/Test_Open_GeoData_API_References.ipynb>`_

- `Launch Binder <https://mybinder.org/v2/gh/Mirjan-Ali-Sha/open-geodata-api/main?filepath=Test_Open_GeoData_API_References.ipynb>`_

**NOTE:** 
      This documentation is a work in progress. Contributions are welcome! I appreciate your patience as I continue to improve it. **AI** helped me a lot to generate this documentation, but it still needs a lot of work to be complete and polished. So maybe all Examples are not tested, and some sections may be incomplete or not fully accurate. If you find any issues, please open an issue on GitHub or contribute directly to the documentation.

.. raw:: html

   <div class="features-grid">
     <div class="feature-box">
       <h3>🎯 One Interface</h3>
       <p>Access Microsoft Planetary Computer & AWS EarthSearch APIs</p>
     </div>
     <div class="feature-box">
       <h3>🔐 Smart URLs</h3>
       <p>Automatic signing, validation, and expiration handling URLs</p>
     </div>
     <div class="feature-box">
       <h3>📦 Your Choice</h3>
       <p>Use any raster package (rioxarray, rasterio, GDAL) to read the data</p>
     </div>
     <div class="feature-box">
       <h3>🔄 Complete Workflow</h3>
       <p>Search → Filter → Download → Analyze</p>
     </div>
   </div>

Quick Start
-----------

.. code-block:: bash

   # Install the package
   pip install open-geodata-api

.. code-block:: python

   import open_geodata_api as ogapi

   # Create client with auto-signing
   pc = ogapi.planetary_computer(auto_sign=True)

   # Search for data
   results = pc.search(
       collections=["sentinel-2-l2a"],
       bbox=[-122.5, 47.5, -122.0, 48.0],
       datetime="2024-01-01/2024-03-31"
   )

   # Get ready-to-use URLs
   item = results.get_all_items()[0]
   blue_url = item.get_asset_url('B02')  # Automatically signed!

   # Use with ANY raster package
   import rioxarray
   data = rioxarray.open_rasterio(blue_url)

Documentation Sections
----------------------

.. toctree::
   :maxdepth: 2
   :caption: 🚀 Getting Started

   sections/getting-started/index
   sections/getting-started/installation
   sections/getting-started/quickstart
   sections/getting-started/configuration
   sections/getting-started/first-steps
   sections/getting-started/catalog-quickstart
   sections/getting-started/catalog-authentication

.. toctree::
   :maxdepth: 2
   :caption: 💡 Examples & Tutorials

   sections/examples/index
   sections/examples/real-world-examples
   sections/examples/integration-examples
   sections/examples/catalog-examples

.. toctree::
   :maxdepth: 2
   :caption: 📚 API Reference

   sections/api-reference/index
   sections/api-reference/core-classes
   sections/api-reference/client-classes
   sections/api-reference/utility-functions
   sections/api-reference/factory-functions
   sections/api-reference/collections
   sections/api-reference/usage-patterns
   sections/api-reference/catalog-client

.. toctree::
   :maxdepth: 2
   :caption: 🖥️ CLI Reference

   sections/cli-reference/index
   sections/cli-reference/collections

.. toctree::
   :maxdepth: 2
   :caption: ❓ FAQ & Help

   sections/faq/index
   sections/faq/general
   sections/faq/installation
   sections/faq/usage
   sections/faq/troubleshooting
   sections/faq/performance
   sections/faq/catalog-faq

.. toctree::
   :maxdepth: 2
   :caption: 🔧 Development

   sections/development/index
   sections/development/contributing
   sections/development/architecture
   sections/development/testing
   sections/development/changelog
   sections/development/license

Philosophy
----------

| 🎯 **Core Focus**: We provide URLs - you choose how to read them!  
| 📦 **Use Any Package**: rioxarray, rasterio, GDAL, or any package you prefer  
| 🚀 **Maximum Flexibility**: Zero restrictions on your workflow  

Perfect for researchers, data scientists, and developers working with satellite imagery and geospatial analysis.

Community & Support
-------------------

- **GitHub Repository**: `open-geodata-api <https://github.com/Mirjan-Ali-Sha/open-geodata-api>`_
- **Issue Tracker**: `Report Bugs <https://github.com/Mirjan-Ali-Sha/open-geodata-api/issues>`_
- **Documentation**: `Read the Docs <https://open-geodata-api.readthedocs.io>`_


Indices and Tables
------------------

* :ref:`genindex`
* :ref:`modindex`  
* :ref:`search`
