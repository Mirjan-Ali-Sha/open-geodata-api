CLI Reference ("open-geodata-api=> 0.2.0")
=========================================

The Open Geodata API provides a comprehensive command-line interface (CLI) through the `ogapi` command, enabling users to interact with satellite data APIs easily from the terminal.

.. toctree::
   :maxdepth: 2

   collections
   search
   items
   download
   utils
   workflows

Overview
--------

**ogapi collections** - Discover and explore satellite data collections
**ogapi search** - Find satellite imagery with filters
**ogapi items** - Work with individual scenes and assets
**ogapi download** - Download satellite data intelligently
**ogapi utils** - Utility commands for processing and analysis
**ogapi workflows** - Predefined workflows for common tasks

Usage
-----

.. code-block:: bash

   # Show general help
   ogapi --help

   # Show help for a specific command group
   ogapi collections --help

   # Show help for a specific command
   ogapi search items --help

Examples
--------

.. code-block:: bash

   # List all collections
   ogapi collections list

   # Search for Sentinel-2 data
   ogapi search items --collections sentinel-2-l2a --bbox "-122.5,47.5,-122.0,48.0" --limit 5

   # Download specific bands
   ogapi download search-results search_results.json --assets "B04,B03,B02" --destination ./rgb_data/

   # Filter search results by cloud cover
   ogapi utils filter-clouds search_results.json --max-cloud-cover 20

   # Run a predefined workflow
   ogapi workflows seasonal-analysis --config seasonal_config.yaml
