Download CLI Commands
=====================

Download satellite data and assets with intelligent management, progress tracking, and resume capabilities.

Basic Usage
-----------

.. code-block:: bash

   ogapi download --help
   ogapi download url --help
   ogapi download search-results --help
   ogapi download urls-json --help
   ogapi download seasonal --help

Commands Overview
-----------------

url
~~~

Download a single file from URL with provider-specific handling.

**Syntax**:

.. code-block:: bash

   ogapi download url <URL> [OPTIONS]

**Arguments**:

- ``URL``: Direct URL to download

**Options**:

- ``--destination`` / ``-d``: Destination file path or directory
- ``--provider`` / ``-p``: Provider hint for URL handling (pc, es, auto) [default: auto]
- ``--check-expiry`` / ``--no-check-expiry``: Check and refresh expired URLs [default: check-expiry]
- ``--show-progress`` / ``--no-progress``: Show download progress [default: show-progress]
- ``--chunk-size``: Download chunk size in bytes [default: 8192]

**Examples**:

.. code-block:: bash

   # Download single file
   ogapi download url "https://example.com/sentinel2_B04.tif"
   
   # Download to specific location
   ogapi download url "https://example.com/B04.tif" \
     --destination "./data/red_band.tif"
   
   # Download with provider specification
   ogapi download url "https://pc.example.com/B04.tif" \
     --provider pc
   
   # Download without expiry check (faster)
   ogapi download url "https://es.example.com/B04.tif" \
     --no-check-expiry

**Sample Output**:

.. code-block:: text

   Downloading: https://example.com/sentinel2_B04.tif
   Destination: ./sentinel2_B04.tif
   Provider: planetary_computer (auto-detected)
   
   Downloading B04.tif: 100%|████████████| 245MB/245MB [02:15<00:00, 1.81MB/s]
   
   ✅ Download completed: ./sentinel2_B04.tif (245.2 MB)

search-results
~~~~~~~~~~~~~~

Download assets from search results JSON file with flexible filtering and organization.

**Syntax**:

.. code-block:: bash

   ogapi download search-results <SEARCH_JSON_FILE> [OPTIONS]

**Arguments**:

- ``SEARCH_JSON_FILE``: JSON file containing search results

**Asset Selection**:

- ``--assets`` / ``-a``: Comma-separated list of assets to download
- ``--asset-pattern`` / ``-ap``: Download assets matching pattern
- ``--all-assets``: Download all available assets

**Item Filtering**:

- ``--max-items`` / ``-m``: Maximum number of items to download [default: all]
- ``--cloud-cover`` / ``-cc``: Maximum cloud cover percentage
- ``--date-range`` / ``-dr``: Date range filter "YYYY-MM-DD/YYYY-MM-DD"
- ``--item-indices``: Specific item indices to download (comma-separated)

**Organization Options**:

- ``--destination`` / ``-d``: Base destination directory [default: ./downloads]
- ``--create-folders`` / ``--flat-structure``: Folder organization [default: create-folders]
- ``--folder-pattern``: Custom folder naming pattern

**Download Control**:

- ``--resume`` / ``--no-resume``: Resume interrupted downloads [default: resume]
- ``--max-workers`` / ``-w``: Number of parallel download workers [default: 4]
- ``--show-progress`` / ``--no-progress``: Show progress bars [default: show-progress]

**Examples**:

.. code-block:: bash

   # Download all assets from search results
   ogapi download search-results search_results.json
   
   # Download specific bands
   ogapi download search-results search_results.json \
     --assets "B04,B03,B02" \
     --destination "./rgb_data/"
   
   # Download with quality filtering
   ogapi download search-results search_results.json \
     --cloud-cover 15 \
     --max-items 5 \
     --assets "B08,B04"
   
   # Download with flat structure
   ogapi download search-results search_results.json \
     --assets "B04,B03,B02" \
     --flat-structure \
     --destination "./satellite_data/"
   
   # Resume interrupted downloads
   ogapi download search-results search_results.json \
     --resume \
     --destination "./data/"

**Sample Output**:

.. code-block:: text

   Download Configuration:
   ======================
   Source: search_results.json (8 items)
   Assets: B04, B03, B02
   Destination: ./rgb_data/
   Organization: Folders per item
   Max Workers: 4
   
   Processing Items:
   ================
   
   Item 1/8: S2A_MSIL2A_20240615T180921...
   ├── B04: Downloading... ████████████ 245MB/245MB [02:15<00:00, 1.81MB/s] ✅
   ├── B03: Downloading... ████████████ 232MB/232MB [02:05<00:00, 1.85MB/s] ✅
   └── B02: Downloading... ████████████ 228MB/228MB [02:02<00:00, 1.87MB/s] ✅
   
   Item 2/8: S2B_MSIL2A_20240618T180919...
   ├── B04: Downloading... ████████████ 241MB/241MB [02:12<00:00, 1.82MB/s] ✅
   ├── B03: Downloading... ████████████ 229MB/229MB [02:07<00:00, 1.80MB/s] ✅
   └── B02: Downloading... ████████████ 225MB/225MB [02:01<00:00, 1.85MB/s] ✅
   
   Download Summary:
   ================
   Total Files: 24
   Successfully Downloaded: 24
   Failed Downloads: 0
   Total Size: 5.8 GB
   Total Time: 18m 32s
   Average Speed: 1.84 MB/s

urls-json
~~~~~~~~~

Download files from a JSON file containing URLs.

**Syntax**:

.. code-block:: bash

   ogapi download urls-json <URLS_JSON_FILE> [OPTIONS]

**Arguments**:

- ``URLS_JSON_FILE``: JSON file containing URLs organized by item and asset

**Organization Options**:

- ``--destination`` / ``-d``: Base destination directory [default: ./downloads]
- ``--create-folders`` / ``--flat-structure``: Folder organization [default: create-folders]
- ``--preserve-structure``: Maintain JSON file structure in folders

**Download Control**:

- ``--max-workers`` / ``-w``: Number of parallel download workers [default: 4]
- ``--resume`` / ``--no-resume``: Resume interrupted downloads [default: resume]
- ``--validate-urls`` / ``--no-validate``: Validate URLs before downloading [default: validate-urls]

**Examples**:

.. code-block:: bash

   # Download from exported URLs
   ogapi download urls-json exported_urls.json
   
   # Custom destination with flat structure
   ogapi download urls-json urls.json \
     --destination "./downloads/" \
     --flat-structure
   
   # Parallel download with validation
   ogapi download urls-json urls.json \
     --max-workers 8 \
     --validate-urls \
     --destination "./validated_downloads/"

seasonal
~~~~~~~~

Download seasonal data from structured JSON file with temporal organization.

**Syntax**:

.. code-block:: bash

   ogapi download seasonal <SEASONAL_JSON_FILE> [OPTIONS]

**Arguments**:

- ``SEASONAL_JSON_FILE``: JSON file containing seasonal data structure

**Season Selection**:

- ``--seasons`` / ``-s``: Comma-separated list of seasons to download
- ``--all-seasons``: Download all seasons in file [default: all-seasons]

**Asset Selection**:

- ``--assets`` / ``-a``: Comma-separated list of assets to download
- ``--all-assets``: Download all available assets [default: all-assets]

**Organization Options**:

- ``--destination`` / ``-d``: Base destination directory [default: ./seasonal_downloads]
- ``--create-folders`` / ``--flat-structure``: Folder organization [default: create-folders]
- ``--temporal-folders``: Create separate folders for each season [default: enabled]

**Examples**:

.. code-block:: bash

   # Download all seasonal data
   ogapi download seasonal seasonal_data.json
   
   # Download specific seasons and assets
   ogapi download seasonal seasonal_data.json \
     --seasons "spring_2024,summer_2024" \
     --assets "B08,B04" \
     --destination "./time_series/"
   
   # Download with organized folder structure
   ogapi download seasonal seasonal_data.json \
     --create-folders \
     --temporal-folders \
     --destination "./temporal_analysis/"

**Sample Output**:

.. code-block:: text

   Seasonal Download Configuration:
   ===============================
   Source: seasonal_data.json
   Seasons: spring_2024, summer_2024, fall_2024, winter_2024
   Assets: B08, B04 (NDVI bands)
   Destination: ./seasonal_downloads/
   
   Season: spring_2024 (15 items)
   ==============================
   Downloading to: ./seasonal_downloads/spring_2024/
   ├── Item 1: S2A_MSIL2A_20240315... ✅ 2 assets
   ├── Item 2: S2B_MSIL2A_20240318... ✅ 2 assets
   └── ... (13 more items)
   
   Season: summer_2024 (22 items)
   ==============================
   Downloading to: ./seasonal_downloads/summer_2024/
   ├── Item 1: S2A_MSIL2A_20240615... ✅ 2 assets
   └── ... (21 more items)
   
   Download Complete!
   Total Seasons: 4
   Total Items: 87
   Total Files: 174
   Success Rate: 100%

batch
~~~~~

Download from batch configuration file with complex workflow support.

**Syntax**:

.. code-block:: bash

   ogapi download batch <CONFIG_FILE> [OPTIONS]

**Arguments**:

- ``CONFIG_FILE``: YAML or JSON configuration file

**Options**:

- ``--dry-run``: Show planned downloads without executing
- ``--validate-config``: Validate configuration file only
- ``--resume-from``: Resume from specific batch item

**Example Configuration** (YAML):

.. code-block:: yaml

   # batch_config.yaml
   batch_downloads:
     - name: "rgb_analysis"
       source_type: "search_results"
       source_file: "search_results.json"
       destination: "./rgb_analysis/"
       assets: ["B04", "B03", "B02"]
       max_items: 10
       cloud_cover: 20
       
     - name: "ndvi_analysis"
       source_type: "urls_json"
       source_file: "ndvi_urls.json"
       destination: "./ndvi_analysis/"
       create_folders: true
       
     - name: "seasonal_study"
       source_type: "seasonal"
       source_file: "seasonal_data.json"
       destination: "./seasonal_study/"
       seasons: ["spring_2024", "summer_2024"]
       assets: ["B08", "B04"]

**Examples**:

.. code-block:: bash

   # Test batch configuration (dry run)
   ogapi download batch config.yaml --dry-run
   
   # Execute batch download
   ogapi download batch config.yaml
   
   # Resume from specific item
   ogapi download batch config.yaml --resume-from "ndvi_analysis"

Advanced Download Features
--------------------------

Resume and Recovery
~~~~~~~~~~~~~~~~~~~

.. code-block:: bash

   # Resume interrupted downloads
   ogapi download search-results search_results.json \
     --resume \
     --destination "./data/"
   
   # Force re-download (skip resume)
   ogapi download search-results search_results.json \
     --no-resume \
     --destination "./data/"

Progress Tracking and Monitoring
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: bash

   # Enable detailed progress tracking
   ogapi download search-results search_results.json \
     --show-progress \
     --max-workers 2  # Fewer workers for cleaner progress display
   
   # Disable progress for automated scripts
   ogapi download search-results search_results.json \
     --no-progress \
     --destination "./automated_downloads/"

Custom Organization Patterns
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: bash

   # Custom folder pattern (if supported)
   ogapi download search-results search_results.json \
     --folder-pattern "{date}_{platform}_{item_id}" \
     --destination "./organized_data/"
   
   # Flat structure with custom naming
   ogapi download search-results search_results.json \
     --flat-structure \
     --destination "./flat_data/"

Performance Optimization
-------------------------

Parallel Downloads
~~~~~~~~~~~~~~~~~~

.. code-block:: bash

   # High-performance download (fast connection)
   ogapi download search-results search_results.json \
     --max-workers 8 \
     --chunk-size 16384 \
     --destination "./fast_downloads/"
   
   # Conservative download (slow connection)
   ogapi download search-results search_results.json \
     --max-workers 2 \
     --chunk-size 4096 \
     --destination "./conservative_downloads/"

Bandwidth Management
~~~~~~~~~~~~~~~~~~~~

.. code-block:: bash

   # For limited bandwidth
   ogapi download search-results search_results.json \
     --max-workers 1 \
     --assets "B04"  # Download only one band initially
   
   # For high-bandwidth connections
   ogapi download search-results search_results.json \
     --max-workers 10 \
     --all-assets

Error Handling and Troubleshooting
-----------------------------------

Common Download Issues
~~~~~~~~~~~~~~~~~~~~~~

**Download Failures**:

.. code-block:: bash

   # Check URL validity first
   ogapi items urls search_results.json --check-expiry --assets "B04"
   
   # Try downloading with URL refresh
   ogapi download search-results search_results.json \
     --assets "B04" \
     --check-expiry

**Disk Space Issues**:

.. code-block:: bash

   # Check available space before download
   df -h ./destination/
   
   # Download subset first
   ogapi download search-results search_results.json \
     --max-items 1 \
     --assets "B04"

**Network Issues**:

.. code-block:: bash

   # Reduce parallel workers for unstable connections
   ogapi download search-results search_results.json \
     --max-workers 1 \
     --resume

Recovery Strategies
~~~~~~~~~~~~~~~~~~~

.. code-block:: bash

   # Check what was already downloaded
   ls -la ./destination/
   
   # Resume with validation
   ogapi download search-results search_results.json \
     --resume \
     --destination "./destination/"
   
   # Force retry failed downloads
   ogapi download search-results search_results.json \
     --no-resume \
     --destination "./destination/"

Workflow Integration
--------------------

Complete Processing Pipelines
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: bash

   #!/bin/bash
   # Complete search-to-analysis pipeline
   
   # 1. Search for data
   ogapi search items \
     -c sentinel-2-l2a \
     -b "-122.5,47.5,-122.0,48.0" \
     -d "2024-06-01/2024-08-31" \
     --cloud-cover 20 \
     --output search_results.json
   
   # 2. Filter results
   ogapi utils filter-clouds search_results.json \
     --max-cloud-cover 15 \
     --output clear_results.json
   
   # 3. Download RGB data
   ogapi download search-results clear_results.json \
     --assets "B04,B03,B02" \
     --destination "./rgb_analysis/" \
     --max-workers 4
   
   # 4. Download NDVI data
   ogapi download search-results clear_results.json \
     --assets "B08,B04" \
     --destination "./ndvi_analysis/" \
     --max-workers 4

Monitoring and Reporting
~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: bash

   # Download with logging
   ogapi download search-results search_results.json \
     --destination "./monitored_downloads/" \
     --show-progress 2>&1 | tee download.log
   
   # Generate download summary
   ogapi utils download-summary download_results.json

The download commands provide comprehensive, robust downloading capabilities with intelligent organization, progress tracking, and error recovery for all types of satellite data workflows.
