Item Management CLI Commands
============================

Manage individual satellite data items and their assets with detailed inspection and URL management.

Basic Usage
-----------

.. code-block:: bash

   ogapi items --help
   ogapi items info --help
   ogapi items assets --help
   ogapi items urls --help
   ogapi items compare --help

Commands Overview
-----------------

info
~~~~

Show detailed information about specific items from search results.

**Syntax**:

.. code-block:: bash

   ogapi items info <search_results_file> [OPTIONS]

**Arguments**:

- ``search_results_file``: JSON file containing search results

**Selection Options**:

- ``--item-index`` / ``-i``: Index of item to show info for [default: 0]
- ``--item-id`` / ``--id``: Specific item ID to show info for
- ``--all-items``: Show info for all items in results

**Display Options**:

- ``--show-all`` / ``--show-summary``: Show all metadata or summary only [default: summary]
- ``--show-geometry`` / ``--no-geometry``: Include geometry information
- ``--output`` / ``-o``: Save item info to JSON file

**Examples**:

.. code-block:: bash

   # Show info for first item
   ogapi items info search_results.json
   
   # Show info for specific item by index
   ogapi items info search_results.json --item-index 2
   
   # Show info for specific item by ID
   ogapi items info search_results.json \
     --item-id "S2A_MSIL2A_20240615T180921_N0510_R027_T11ULA_20240616T000511"
   
   # Show all metadata
   ogapi items info search_results.json --show-all
   
   # Save item details
   ogapi items info search_results.json \
     --show-all \
     --output item_details.json

**Sample Output**:

.. code-block:: text

   Item Information:
   ================
   
   Basic Details:
     ID: S2A_MSIL2A_20240615T180921_N0510_R027_T11ULA_20240616T000511
     Collection: sentinel-2-l2a
     Platform: sentinel-2a
     Instrument: msi
   
   Temporal Information:
     Acquisition Date: 2024-06-15T18:09:21.024000Z
     Processing Date: 2024-06-16T00:05:11.000000Z
   
   Quality Metrics:
     Cloud Cover: 12.5%
     Data Coverage: 100.0%
   
   Spatial Information:
     Bounding Box: [-122.5417, 47.4583, -121.4583, 48.4583]
     Geometry: POLYGON((-122.5417 47.4583, -121.4583 47.4583, ...))
   
   Available Assets: 17 assets
     Use 'ogapi items assets' to see detailed asset information

assets
~~~~~~

List and filter assets/bands for specific items.

**Syntax**:

.. code-block:: bash

   ogapi items assets <search_results_file> [OPTIONS]

**Selection Options**:

- ``--item-index`` / ``-i``: Index of item to list assets for [default: 0]
- ``--item-id`` / ``--id``: Specific item ID to list assets for

**Filtering Options**:

- ``--pattern`` / ``-p``: Filter assets by name pattern (regex)
- ``--type`` / ``-t``: Filter assets by MIME type
- ``--role`` / ``-r``: Filter assets by role (data, thumbnail, metadata)

**Display Options**:

- ``--show-urls`` / ``--no-urls``: Show asset URLs [default: no-urls]
- ``--show-details`` / ``--show-summary``: Show detailed or summary info [default: summary]
- ``--output`` / ``-o``: Save asset list to JSON file

**Examples**:

.. code-block:: bash

   # List all assets
   ogapi items assets search_results.json
   
   # Filter assets by pattern
   ogapi items assets search_results.json --pattern "B0[1-4]"
   
   # Show only data assets
   ogapi items assets search_results.json --role data
   
   # Show assets with URLs
   ogapi items assets search_results.json --show-urls
   
   # Filter by file type
   ogapi items assets search_results.json --type "image/tiff"
   
   # Save asset information
   ogapi items assets search_results.json --output assets_info.json

**Sample Output**:

.. code-block:: text

   Asset Information:
   =================
   
   Item: S2A_MSIL2A_20240615T180921_N0510_R027_T11ULA_20240616T000511
   
   Spectral Bands (10m resolution):
     B02 - Blue (490nm)           - image/tiff
     B03 - Green (560nm)          - image/tiff  
     B04 - Red (665nm)            - image/tiff
     B08 - NIR (842nm)            - image/tiff
   
   Spectral Bands (20m resolution):
     B05 - Red Edge (705nm)       - image/tiff
     B06 - Red Edge (740nm)       - image/tiff
     B07 - Red Edge (783nm)       - image/tiff
     B8A - NIR Narrow (865nm)     - image/tiff
     B11 - SWIR (1610nm)          - image/tiff
     B12 - SWIR (2190nm)          - image/tiff
   
   Auxiliary Data:
     AOT - Aerosol Optical Thickness  - image/tiff
     WVP - Water Vapour               - image/tiff
     SCL - Scene Classification       - image/tiff
     visual - True Color Image        - image/png
     thumbnail - Preview Image        - image/png

urls
~~~~

Get download URLs for specific assets of items.

**Syntax**:

.. code-block:: bash

   ogapi items urls <search_results_file> [OPTIONS]

**Selection Options**:

- ``--item-index`` / ``-i``: Index of item to get URLs for [default: 0]
- ``--item-id`` / ``--id``: Specific item ID to get URLs for
- ``--all-items``: Get URLs for all items in results

**Asset Selection**:

- ``--assets`` / ``-a``: Comma-separated list of specific assets
- ``--pattern`` / ``-p``: Get URLs for assets matching pattern
- ``--all-assets``: Get URLs for all available assets

**URL Options**:

- ``--signed`` / ``--unsigned``: Get signed or unsigned URLs [default: signed]
- ``--check-expiry`` / ``--no-check-expiry``: Check URL expiration [default: check-expiry]
- ``--refresh-expired``: Automatically refresh expired URLs

**Output Options**:

- ``--output`` / ``-o``: Save URLs to JSON file
- ``--format``: Output format (json, list, table) [default: table]

**Examples**:

.. code-block:: bash

   # Get RGB band URLs
   ogapi items urls search_results.json --assets "B04,B03,B02"
   
   # Get all URLs for an item
   ogapi items urls search_results.json --all-assets
   
   # Get URLs by pattern
   ogapi items urls search_results.json --pattern "B0[1-8]"
   
   # Get URLs for all items
   ogapi items urls search_results.json --all-items --assets "B04,B03,B02"
   
   # Save URLs to file
   ogapi items urls search_results.json \
     --assets "B08,B04" \
     --output ndvi_urls.json
   
   # Get unsigned URLs
   ogapi items urls search_results.json --unsigned --assets "B04,B03,B02"

**Sample Output**:

.. code-block:: text

   Asset URLs:
   ===========
   
   Item: S2A_MSIL2A_20240615T180921_N0510_R027_T11ULA_20240616T000511
   
   ┌─────────┬──────────────────────────────────────────────────────────────┬──────────┐
   │ Asset   │ URL                                                          │ Status   │
   ├─────────┼──────────────────────────────────────────────────────────────┼──────────┤
   │ B04     │ https://sentinel2l2a01.blob.core.windows.net/.../B04.tif... │ ✓ Valid  │
   │ B03     │ https://sentinel2l2a01.blob.core.windows.net/.../B03.tif... │ ✓ Valid  │
   │ B02     │ https://sentinel2l2a01.blob.core.windows.net/.../B02.tif... │ ✓ Valid  │
   └─────────┴──────────────────────────────────────────────────────────────┴──────────┘
   
   URLs saved to: ndvi_urls.json

compare
~~~~~~~

Compare multiple items by various quality metrics and characteristics.

**Syntax**:

.. code-block:: bash

   ogapi items compare <search_results_file> [OPTIONS]

**Comparison Options**:

- ``--max-items`` / ``-m``: Maximum number of items to compare [default: 10]
- ``--metric`` / ``-mt``: Comparison metric (cloud_cover, date, assets, quality) [default: cloud_cover]
- ``--sort-order``: Sort order (asc, desc) [default: asc for cloud_cover, desc for date]

**Output Options**:

- ``--output`` / ``-o``: Save comparison to JSON file
- ``--format``: Output format (table, json, summary) [default: table]
- ``--show-details``: Include detailed comparison metrics

**Examples**:

.. code-block:: bash

   # Compare by cloud cover (find clearest)
   ogapi items compare search_results.json
   
   # Compare by date (find most recent)
   ogapi items compare search_results.json --metric date
   
   # Compare asset availability
   ogapi items compare search_results.json --metric assets --max-items 5
   
   # Compare data quality
   ogapi items compare search_results.json --metric quality --show-details
   
   # Save comparison results
   ogapi items compare search_results.json \
     --metric cloud_cover \
     --output comparison.json

**Sample Output**:

.. code-block:: text

   Item Comparison (by Cloud Cover):
   =================================
   
   Compared 8 items from search results
   
   ┌─────┬─────────────────────────────────┬─────────────┬────────────┬──────────────┐
   │ Rank│ Item ID                         │ Date        │ Cloud Cover│ Platform     │
   ├─────┼─────────────────────────────────┼─────────────┼────────────┼──────────────┤
   │  1  │ S2B_MSIL2A_20240618T180919_... │ 2024-06-18  │    8.3%    │ sentinel-2b  │
   │  2  │ S2A_MSIL2A_20240615T180921_... │ 2024-06-15  │   12.5%    │ sentinel-2a  │
   │  3  │ S2A_MSIL2A_20240610T180921_... │ 2024-06-10  │   18.7%    │ sentinel-2a  │
   │  4  │ S2B_MSIL2A_20240608T180919_... │ 2024-06-08  │   25.1%    │ sentinel-2b  │
   └─────┴─────────────────────────────────┴─────────────┴────────────┴──────────────┘
   
   Best Item for Download:
     ID: S2B_MSIL2A_20240618T180919_N0510_R027_T11ULA_20240618T213456
     Date: 2024-06-18T18:09:19Z
     Cloud Cover: 8.3%
     Recommendation: Excellent quality for analysis

Advanced Item Operations
------------------------

Bulk Item Analysis
~~~~~~~~~~~~~~~~~~

.. code-block:: bash

   # Analyze all items in search results
   ogapi items info search_results.json --all-items --output all_items_info.json
   
   # Get URLs for all items and all assets
   ogapi items urls search_results.json --all-items --all-assets --output all_urls.json
   
   # Compare all items by multiple metrics
   for metric in cloud_cover date assets quality; do
       ogapi items compare search_results.json \
         --metric $metric \
         --output "comparison_by_${metric}.json"
   done

Asset Pattern Matching
~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: bash

   # Get only visible spectrum bands
   ogapi items assets search_results.json --pattern "B0[2-4]"
   
   # Get NIR and SWIR bands
   ogapi items assets search_results.json --pattern "B(08|11|12)"
   
   # Get all 10m resolution bands
   ogapi items assets search_results.json --pattern "B(02|03|04|08)"
   
   # Get quality and auxiliary data
   ogapi items assets search_results.json --pattern "(SCL|AOT|WVP)"

Quality Assessment Workflow
~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: bash

   # 1. Compare items by quality
   ogapi items compare search_results.json --metric quality --output quality_ranking.json
   
   # 2. Get detailed info for best items
   ogapi items info search_results.json --item-index 0 --show-all --output best_item.json
   
   # 3. Check asset availability for top item
   ogapi items assets search_results.json --item-index 0 --show-details
   
   # 4. Get URLs for analysis
   ogapi items urls search_results.json --item-index 0 --assets "B08,B04" --output ndvi_urls.json

Working with Multiple Items
---------------------------

Item Selection Strategies
~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: bash

   # Select by cloud cover threshold
   ogapi items compare search_results.json --metric cloud_cover | head -5
   
   # Select most recent items
   ogapi items compare search_results.json --metric date --sort-order desc | head -3
   
   # Select items with best asset coverage
   ogapi items compare search_results.json --metric assets --show-details

Batch URL Generation
~~~~~~~~~~~~~~~~~~~~

.. code-block:: bash

   #!/bin/bash
   # Generate URLs for multiple items and assets
   
   # Define asset groups
   rgb_assets="B04,B03,B02"
   ndvi_assets="B08,B04"
   all_bands="B01,B02,B03,B04,B05,B06,B07,B08,B8A,B09,B11,B12"
   
   # Generate URLs for different analysis types
   ogapi items urls search_results.json --all-items --assets "$rgb_assets" --output rgb_urls.json
   ogapi items urls search_results.json --all-items --assets "$ndvi_assets" --output ndvi_urls.json
   ogapi items urls search_results.json --all-items --assets "$all_bands" --output all_bands_urls.json

Error Handling and Troubleshooting
-----------------------------------

Common Issues
~~~~~~~~~~~~~

**Item Not Found**:

.. code-block:: bash

   # Check available items in search results
   ogapi items info search_results.json --all-items | grep "ID:"
   
   # Verify item index
   ogapi items compare search_results.json --format table

**Asset Not Available**:

.. code-block:: bash

   # Check what assets are actually available
   ogapi items assets search_results.json --item-index 0
   
   # Check asset naming conventions by provider
   ogapi items assets search_results.json --show-details

**URL Expiration**:

.. code-block:: bash

   # Check URL expiration status
   ogapi items urls search_results.json --check-expiry --assets "B04"
   
   # Refresh expired URLs
   ogapi items urls search_results.json --refresh-expired --assets "B04"

Debugging Item Issues
~~~~~~~~~~~~~~~~~~~~~

.. code-block:: bash

   # Verbose mode for detailed error information
   ogapi --verbose items info search_results.json
   
   # Validate search results file
   python -c "import json; json.load(open('search_results.json'))"
   
   # Check file structure
   jq '.features | length' search_results.json  # Number of items
   jq '.features[0] | keys' search_results.json  # Item structure

Integration with Other Commands
-------------------------------

Complete Workflow Examples
~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: bash

   # Quality-based selection and download
   ogapi search items -c sentinel-2-l2a -b "-122.5,47.5,-122.0,48.0" -o search.json
   ogapi items compare search.json --metric cloud_cover --output ranking.json
   ogapi items urls search.json --item-index 0 --assets "B04,B03,B02" --output best_rgb.json
   ogapi download urls-json best_rgb.json --destination "./best_quality/"
   
   # Multi-temporal analysis setup
   ogapi search items -c sentinel-2-l2a -b "-122.5,47.5,-122.0,48.0" -d "2024-01-01/2024-12-31" -o yearly.json
   ogapi items compare yearly.json --metric date --output temporal_ranking.json
   ogapi items urls yearly.json --all-items --assets "B08,B04" --output temporal_ndvi.json

The items commands provide comprehensive tools for inspecting, comparing, and managing individual satellite data items and their assets.
