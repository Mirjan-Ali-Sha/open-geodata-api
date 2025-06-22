Installation FAQ
================

Package Installation Issues
----------------------------

Package Not Found
~~~~~~~~~~~~~~~~~~

**Q**: ``pip install open-geodata-api`` fails with "No matching distribution found"

**A**: This usually indicates the package name is incorrect or not yet available on PyPI.

**Solutions:**

.. code-block:: bash

   # Check exact package name
   pip search open-geodata-api
   
   # Try alternative installation methods
   pip install --upgrade pip
   pip install open-geodata-api --no-cache-dir
   
   # Install from source (development)
   git clone https://github.com/Mirjan-Ali-Sha/open-geodata-api.git
   cd open-geodata-api
   pip install -e .

Dependency Conflicts
~~~~~~~~~~~~~~~~~~~~

**Q**: Installation fails with dependency conflicts

**A**: This happens when existing packages conflict with requirements.

**Solutions:**

.. code-block:: bash

   # Create fresh virtual environment
   python -m venv fresh_env
   source fresh_env/bin/activate  # Linux/Mac
   # or fresh_env\Scripts\activate  # Windows
   
   # Install with specific versions
   pip install open-geodata-api==0.1.0
   
   # Install without dependencies (advanced)
   pip install open-geodata-api --no-deps
   # Then install dependencies manually

Permission Errors
~~~~~~~~~~~~~~~~~~

**Q**: "Permission denied" errors during installation

**A**: Usually caused by insufficient permissions or system Python usage.

**Solutions:**

.. code-block:: bash

   # Use user installation
   pip install --user open-geodata-api
   
   # Use virtual environment (recommended)
   python -m venv ogapi_env
   source ogapi_env/bin/activate
   pip install open-geodata-api
   
   # On Windows with permission issues
   python -m pip install --user open-geodata-api

Optional Dependencies
---------------------

Raster I/O Dependencies
~~~~~~~~~~~~~~~~~~~~~~~

**Q**: ImportError for rioxarray or rasterio

**A**: These are optional dependencies for data reading.

**Solutions:**

.. code-block:: bash

   # Install with I/O dependencies
   pip install open-geodata-api[io]
   
   # Or install individually
   pip install rioxarray rasterio xarray
   
   # If GDAL issues on Windows
   conda install -c conda-forge rasterio
   # Then: pip install open-geodata-api

Spatial Analysis Dependencies
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Q**: Cannot import geopandas or shapely

**A**: These are needed for spatial operations.

**Solutions:**

.. code-block:: bash

   # Install spatial dependencies
   pip install open-geodata-api[spatial]
   
   # If installation fails, use conda
   conda install -c conda-forge geopandas
   pip install open-geodata-api
   
   # For complete installation
   pip install open-geodata-api[complete]

Platform-Specific Issues
-------------------------

Windows Installation
~~~~~~~~~~~~~~~~~~~~

**Q**: Issues installing on Windows

**A**: Windows often has issues with geospatial dependencies.

**Solutions:**

.. code-block:: bash

   # Use conda for geospatial packages
   conda install -c conda-forge rasterio geopandas
   pip install open-geodata-api
   
   # Or use pre-compiled wheels
   pip install --find-links https://girder.github.io/large_image_wheels GDAL
   pip install rasterio geopandas
   pip install open-geodata-api
   
   # For Windows Subsystem for Linux (WSL)
   # Follow Linux installation instructions

macOS Installation
~~~~~~~~~~~~~~~~~~

**Q**: Issues on macOS, especially M1/M2 Macs

**A**: Apple Silicon Macs require special handling for some packages.

**Solutions:**

.. code-block:: bash

   # Use conda-forge for M1/M2 Macs
   conda install -c conda-forge rasterio geopandas
   pip install open-geodata-api
   
   # Or use Homebrew for GDAL
   brew install gdal
   pip install rasterio geopandas
   pip install open-geodata-api
   
   # For Rosetta compatibility
   arch -x86_64 pip install open-geodata-api[complete]

Linux Installation
~~~~~~~~~~~~~~~~~~

**Q**: Missing system dependencies on Linux

**A**: Linux may need system packages for geospatial libraries.

**Solutions:**

.. code-block:: bash

   # Ubuntu/Debian
   sudo apt-get update
   sudo apt-get install gdal-bin libgdal-dev python3-gdal
   pip install open-geodata-api[complete]
   
   # CentOS/RHEL/Fedora
   sudo yum install gdal gdal-devel
   # or: sudo dnf install gdal gdal-devel
   pip install open-geodata-api[complete]
   
   # Arch Linux
   sudo pacman -S gdal
   pip install open-geodata-api[complete]

Virtual Environment Issues
---------------------------

Environment Not Found
~~~~~~~~~~~~~~~~~~~~~~

**Q**: "command not found" after installing in virtual environment

**A**: Virtual environment not activated or PATH issues.

**Solutions:**

.. code-block:: bash

   # Ensure environment is activated
   source venv/bin/activate  # Linux/Mac
   venv\Scripts\activate     # Windows
   
   # Verify installation
   which python
   which pip
   python -c "import open_geodata_api; print('Success!')"
   
   # Check if CLI is available
   ogapi --version

Multiple Python Versions
~~~~~~~~~~~~~~~~~~~~~~~~~

**Q**: Installed in wrong Python version

**A**: Multiple Python installations can cause confusion.

**Solutions:**

.. code-block:: bash

   # Check Python version
   python --version
   python3 --version
   
   # Use specific Python version
   python3.9 -m pip install open-geodata-api
   
   # In virtual environment
   python -m venv --python=python3.9 ogapi_env
   source ogapi_env/bin/activate
   pip install open-geodata-api

Development Installation
-------------------------

Editable Installation
~~~~~~~~~~~~~~~~~~~~~

**Q**: How to install for development

**A**: Use editable installation for active development.

**Solutions:**

.. code-block:: bash

   # Clone repository
   git clone https://github.com/Mirjan-Ali-Sha/open-geodata-api.git
   cd open-geodata-api
   
   # Create development environment
   python -m venv dev_env
   source dev_env/bin/activate
   
   # Editable installation with dev dependencies
   pip install -e .[dev]
   
   # Verify development setup
   pytest
   black --check .
   flake8

Testing Installation
~~~~~~~~~~~~~~~~~~~~

**Q**: How to verify installation is working

**A**: Run these verification steps:

.. code-block:: python

   # Test 1: Basic import
   import open_geodata_api as ogapi
   print(f"Version: {ogapi.__version__}")
   
   # Test 2: Client creation
   pc = ogapi.planetary_computer()
   es = ogapi.earth_search()
   print("Clients created successfully")
   
   # Test 3: Basic functionality
   collections = pc.list_collections()
   print(f"Found {len(collections)} collections")
   
   # Test 4: CLI availability
   import subprocess
   result = subprocess.run(['ogapi', '--version'], capture_output=True, text=True)
   print(f"CLI version: {result.stdout}")

Common Error Messages
---------------------

"No module named 'open_geodata_api'"
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Causes:**
- Package not installed
- Wrong virtual environment
- Installation failed silently

**Solutions:**

.. code-block:: bash

   # Check if installed
   pip list | grep open-geodata-api
   
   # Reinstall
   pip uninstall open-geodata-api
   pip install open-geodata-api
   
   # Check Python path
   python -c "import sys; print(sys.path)"

"GDAL not found" or similar geospatial errors
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Causes:**
- Missing system GDAL installation
- Version conflicts
- Platform-specific issues

**Solutions:**

.. code-block:: bash

   # Check GDAL installation
   gdalinfo --version
   
   # Install system GDAL first
   # Then install Python packages
   pip install GDAL==$(gdal-config --version) --global-option=build_ext --global-option="-I/usr/include/gdal"
   
   # Or use conda
   conda install -c conda-forge gdal rasterio geopandas

"Failed building wheel" errors
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Causes:**
- Missing build tools
- Compilation errors
- Platform incompatibility

**Solutions:**

.. code-block:: bash

   # Update build tools
   pip install --upgrade pip setuptools wheel
   
   # Install build dependencies
   pip install cython numpy
   
   # Use pre-compiled wheels
   pip install --only-binary=all open-geodata-api[complete]
   
   # For stubborn packages, use conda
   conda install -c conda-forge problematic_package

Getting Additional Help
-----------------------

When to Seek Help
~~~~~~~~~~~~~~~~~

Seek additional help when:
- Multiple installation attempts fail
- Platform-specific issues persist
- Dependency conflicts cannot be resolved
- Documentation doesn't cover your specific case

How to Report Installation Issues
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

When reporting issues, include:

.. code-block:: bash

   # System information
   python --version
   pip --version
   uname -a  # Linux/Mac
   # or: systeminfo  # Windows
   
   # Environment information
   pip list
   conda list  # if using conda
   
   # Error details
   pip install open-geodata-api --verbose

**Submit to:**
- GitHub Issues: https://github.com/Mirjan-Ali-Sha/open-geodata-api/issues
- Include the "installation" label
- Provide full error traceback
- Mention your platform and Python version
