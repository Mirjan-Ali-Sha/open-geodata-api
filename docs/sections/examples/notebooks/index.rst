Jupyter Notebooks
=================

Interactive Jupyter notebooks demonstrating Open Geodata API usage.

Available Notebooks
-------------------

.. toctree::
   :maxdepth: 1

   sentinel2-analysis
   landsat-timeseries
   multi-provider-comparison

Quick Start
-----------

To run these notebooks:

1. **Install Jupyter**:

.. code-block:: bash

   pip install jupyter
   pip install open-geodata-api[complete]

2. **Download notebooks** from the `examples repository <https://github.com/Mirjan-Ali-Sha/open-geodata-api-examples>`_

3. **Start Jupyter**:

.. code-block:: bash

   jupyter notebook

Notebook Descriptions
--------------------

**Sentinel-2 Analysis**
  Complete workflow for Sentinel-2 data analysis including NDVI calculation,
  cloud masking, and time series analysis.

**Landsat Time Series**
  Long-term analysis using Landsat archive data, demonstrating change
  detection and trend analysis techniques.

**Multi-Provider Comparison**
  Side-by-side comparison of data from Planetary Computer and EarthSearch,
  including data quality assessment and availability analysis.

Requirements
------------

All notebooks require:

- **Python 3.8+**
- **Jupyter notebook or JupyterLab**
- **open-geodata-api[complete]** (includes rioxarray, geopandas)
- **Additional packages**: matplotlib, seaborn, plotly (for visualizations)

Optional for enhanced functionality:

- **stackstac** (for efficient array stacking)
- **planetary-computer** (for PC authentication)
- **folium** (for interactive maps)

Installation command:

.. code-block:: bash

   pip install open-geodata-api[complete] matplotlib seaborn plotly folium stackstac

Interactive Features
--------------------

The notebooks include:

✅ **Interactive widgets** for parameter adjustment  
✅ **Progressive examples** from basic to advanced  
✅ **Error handling** and troubleshooting tips  
✅ **Visualization galleries** with various plot types  
✅ **Performance comparisons** between different approaches  
✅ **Best practices** and optimization techniques  

Contributing Notebooks
-----------------------

We welcome contributions of new notebooks! Please see the 
:doc:`../../development/contributing` guide for details on:

- Notebook structure and formatting
- Required documentation
- Testing procedures
- Submission process

The notebooks repository accepts examples for:

- Domain-specific applications
- Integration with new libraries
- Performance optimization techniques
- Educational tutorials
