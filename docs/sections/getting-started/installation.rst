Installation
============

Basic Installation
------------------

Install the core package from PyPI:

.. code-block:: bash

   pip install open-geodata-api

This installs the minimal dependencies needed for API access and URL management.

Optional Dependencies
---------------------

For Spatial Analysis
~~~~~~~~~~~~~~~~~~~~

.. code-block:: bash

   pip install open-geodata-api[spatial]

Includes: geopandas, shapely

For Raster Reading
~~~~~~~~~~~~~~~~~~

.. code-block:: bash

   # For raster I/O capabilities
   pip install open-geodata-api[io]

Includes: rioxarray, rasterio, xarray

For Complete Installation
~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: bash

   pip install open-geodata-api[complete]

Includes all optional dependencies: spatial analysis + raster I/O

Development Installation
------------------------

For contributors:

.. code-block:: bash

   git clone https://github.com/Mirjan-Ali-Sha/open-geodata-api.git
   cd open-geodata-api
   pip install -e .[dev]

CLI Installation
----------------
For command-line interface (CLI) usage, install the CLI package:

.. code-block:: bash

   pip install open-geodata-api[cli]

None Dependencies (Optional)
-----------------------------
For additional functionality that does not require any specific dependencies, you can install the package with no extra dependencies:
But this is not recommended unless you are sure you do not need any of the optional features.
User have to install the optional dependencies manually if needed. [This is useful for minimal installations or when you want to manage dependencies yourself.]
Requirements are `requests`, `planetary-computer`, `tqdm`, and `click` install them carefully.

.. code-block:: bash

   pip install open-geodata-api[none]

Verify Installation
-------------------

.. code-block:: python

   import open_geodata_api as ogapi
   ogapi.info()

Dependencies
------------

Core Dependencies
~~~~~~~~~~~~~~~~~

- `requests >= 2.25.0`
- `pandas >= 1.3.0`
- `planetary-computer >= 1.0.0`
- `tqdm >= 4.67.1`
- `click >= 8.0.0`

Optional Dependencies
~~~~~~~~~~~~~~~~~~~~~

- `geopandas >= 0.10.0` (for spatial operations)
- `rioxarray >= 0.11.0` (for raster reading)
- `rasterio >= 1.3.0` (for raster reading)
- `xarray >= 0.19.0` (for n-dimensional arrays)
- `shapely >= 1.8.0` (for geometric operations)

CLI Dependencies (Optional)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~
- `requests >= 2.25.0`
- `planetary-computer >= 1.0.0`
- `tqdm >= 4.67.1`
- `click >= 8.0.0`

System Requirements
-------------------

- Python 3.8+
- Operating System: Linux, macOS, Windows
- Memory: 1GB+ RAM recommended for large datasets
- Network: Internet connection for API access
