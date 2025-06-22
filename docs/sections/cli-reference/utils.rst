Utility CLI Commands
====================

Utility commands for filtering, exporting, validating, analyzing, and summarizing satellite data operations.

Basic Usage
-----------

.. code-block:: bash

   ogapi utils --help
   ogapi utils filter-clouds --help
   ogapi utils export-urls --help
   ogapi utils validate-urls --help
   ogapi utils analyze --help

Commands Overview
-----------------

filter-clouds
~~~~~~~~~~~~~

Filter search results by cloud cover percentage with statistical reporting.

**Syntax**:

.. code-block:: bash

   ogapi utils filter-clouds <SEARCH_JSON_FILE> [OPTIONS]

**Arguments**:

- ``SEARCH_JSON_FILE``: JSON file containing search results

**Filtering Options**:

- ``--max-cloud-cover`` / ``-m``: Maximum cloud cover percentage [required]
- ``--min-cloud-cover``: Minimum cloud cover percentage [default: 0]

**Output Options**:

- ``--output`` / ``-o``: Save filtered results to JSON file
- ``--show-stats`` / ``--no-stats``: Show filtering statistics [default: show-stats]
- ``--format``: Output format (json, table, summary) [default: json]

**Examples**:

.. code-block:: bash

   # Filter to very clear scenes
   ogapi utils filter-clouds search_results.json --max-cloud-cover 15
   
   # Filter with range and save results
   ogapi utils filter-clouds search_results.json \
     --min-cloud-cover 5 \
     --max-cloud-cover 25 \
     --output filtered_results.json
   
   # Filter without showing statistics
   ogapi utils filter-clouds search_results.json \
     --max-cloud-cover 20 \
     --no-stats \
     --output clear_results.json

**Sample Output**:

.. code-block:: text

   Cloud Cover Filtering Results:
   =============================
   
   Input: search_results.json (25 items)
   Filter: Cloud cover ≤ 15%
   
   Filtering Statistics:
   ┌─────────────────────┬───────┬─────────────┐
   │ Cloud Cover Range   │ Count │ Percentage  │
   ├─────────────────────┼───────┼─────────────┤
   │ 0% - 5%            │   3   │    12.0%    │
   │ 5% - 10%           │   5   │    20.0%    │
   │ 10% - 15%          │   4   │    16.0%    │
   │ 15% - 25%          │   7   │    28.0%    │
   │ 25% - 50%          │   4   │    16.0%    │
   │ > 50%              │   2   │     8.0%    │
   └─────────────────────┴───────┴─────────────┘
   
   Results:
   ✅ Kept: 12 items (48.0%)
   ❌ Filtered out: 13 items (52.0%)
   
   Output saved to: filtered_results.json

export-urls
~~~~~~~~~~~

Export asset URLs from search results with flexible formatting options.

**Syntax**:

.. code-block:: bash

   ogapi utils export-urls <SEARCH_JSON_FILE> [OPTIONS]

**Arguments**:

- ``SEARCH_JSON_FILE``: JSON file containing search results

**Asset Selection**:

- ``--assets`` / ``-a``: Comma-separated list of assets to export
- ``--asset-pattern`` / ``-p``: Export assets matching pattern
- ``--all-assets``: Export all available assets [default]

**URL Options**:

- ``--signed`` / ``--unsigned``: Export signed or unsigned URLs [default: signed]
- ``--check-expiry`` / ``--no-check-expiry``: Check URL expiration [default: check-expiry]
- ``--refresh-expired``: Refresh expired URLs before export

**Output Options**:

- ``--output`` / ``-o``: Output JSON file [required]
- ``--format``: Export format (structured, flat, simple) [default: structured]
- ``--include-metadata``: Include item metadata in export

**Examples**:

.. code-block:: bash

   # Export all URLs
   ogapi utils export-urls search_results.json --output all_urls.json
   
   # Export specific assets
   ogapi utils export-urls search_results.json \
     --assets "B04,B03,B02" \
     --output rgb_urls.json
   
   # Export with pattern matching
   ogapi utils export-urls search_results.json \
     --asset-pattern "B0[1-8]" \
     --output optical_bands.json
   
   # Export in simple format
   ogapi utils export-urls search_results.json \
     --format simple \
     --assets "B04" \
     --output simple_urls.json
   
   # Export unsigned URLs
   ogapi utils export-urls search_results.json \
     --unsigned \
     --assets "B04,B03,B02" \
     --output unsigned_urls.json

**Output Formats**:

*Structured Format* (default):
.. code-block:: json

   {
     "export_metadata": {
       "timestamp": "2024-06-22T18:16:00Z",
       "source_file": "search_results.json",
       "total_items": 10,
       "assets_per_item": ["B04", "B03", "B02"]
     },
     "urls": {
       "S2A_MSIL2A_20240615...": {
         "B04": "https://example.com/B04.tif",
         "B03": "https://example.com/B03.tif",
         "B02": "https://example.com/B02.tif"
       }
     }
   }

*Simple Format*:
.. code-block:: json

   {
     "https://example.com/item1_B04.tif": "B04",
     "https://example.com/item1_B03.tif": "B03",
     "https://example.com/item2_B04.tif": "B04"
   }

validate-urls
~~~~~~~~~~~~~

Validate URLs in JSON files with comprehensive checks and repair options.

**Syntax**:

.. code-block:: bash

   ogapi utils validate-urls <URLS_JSON_FILE> [OPTIONS]

**Arguments**:

- ``URLS_JSON_FILE``: JSON file containing URLs to validate

**Validation Options**:

- ``--check-expiry`` / ``--no-check-expiry``: Check URL expiration [default: check-expiry]
- ``--check-access`` / ``--no-check-access``: Test HTTP accessibility [default: no-check-access]
- ``--provider`` / ``-p``: Provider hint for validation (pc, es, auto) [default: auto]

**Repair Options**:

- ``--fix-expired`` / ``--no-fix``: Attempt to fix expired URLs [default: no-fix]
- ``--output`` / ``-o``: Save validated/fixed URLs to new file

**Reporting Options**:

- ``--detailed`` / ``--summary``: Detailed or summary report [default: summary]
- ``--export-report``: Save validation report to JSON file

**Examples**:

.. code-block:: bash

   # Basic URL validation
   ogapi utils validate-urls urls.json
   
   # Comprehensive validation with access checks
   ogapi utils validate-urls urls.json \
     --check-access \
     --detailed
   
   # Validate and fix expired URLs
   ogapi utils validate-urls urls.json \
     --fix-expired \
     --output fixed_urls.json
   
   # Generate detailed validation report
   ogapi utils validate-urls urls.json \
     --detailed \
     --export-report validation_report.json

**Sample Output**:

.. code-block:: text

   URL Validation Report:
   =====================
   
   Source: urls.json
   Total URLs: 45
   
   Validation Results:
   ┌─────────────────────┬───────┬─────────────┐
   │ Status              │ Count │ Percentage  │
   ├─────────────────────┼───────┼─────────────┤
   │ ✅ Valid            │  38   │    84.4%    │
   │ ⚠️  Expired         │   5   │    11.1%    │
   │ ❌ Invalid          │   2   │     4.4%    │
   └─────────────────────┴───────┴─────────────┘
   
   Expired URLs:
     - item_123/B04.tif (expired 2 hours ago)
     - item_456/B03.tif (expired 45 minutes ago)
   
   Invalid URLs:
     - item_789/B02.tif (404 Not Found)
     - item_012/B08.tif (malformed URL)
   
   Recommendation: Use --fix-expired to refresh expired URLs

analyze
~~~~~~~

Analyze search results with comprehensive statistics and insights.

**Syntax**:

.. code-block:: bash

   ogapi utils analyze <SEARCH_JSON_FILE> [OPTIONS]

**Arguments**:

- ``SEARCH_JSON_FILE``: JSON file containing search results

**Analysis Options**:

- ``--metric`` / ``-m``: Analysis focus (cloud_cover, temporal, spatial, assets, quality) [default: all]
- ``--detailed`` / ``--summary``: Analysis depth [default: summary]

**Output Options**:

- ``--output`` / ``-o``: Save analysis results to JSON file
- ``--format``: Output format (table, json, report) [default: table]
- ``--charts`` / ``--no-charts``: Generate ASCII charts [default: charts]

**Examples**:

.. code-block:: bash

   # Complete analysis
   ogapi utils analyze search_results.json
   
   # Focus on cloud cover analysis
   ogapi utils analyze search_results.json --metric cloud_cover
   
   # Temporal analysis with detailed output
   ogapi utils analyze search_results.json \
     --metric temporal \
     --detailed \
     --output temporal_analysis.json
   
   # Generate comprehensive report
   ogapi utils analyze search_results.json \
     --format report \
     --output analysis_report.json

**Sample Output**:

.. code-block:: text

   Search Results Analysis:
   =======================
   
   Dataset Overview:
     Total Items: 25
     Date Range: 2024-06-01 to 2024-08-31 (92 days)
     Spatial Coverage: [-122.5, 47.5, -122.0, 48.0]
     Collections: sentinel-2-l2a
   
   Cloud Cover Analysis:
     Mean: 23.4%
     Median: 18.7%
     Min: 2.1%
     Max: 67.8%
     
     Distribution:
     0-10%   ████████ 8 items (32%)
     10-20%  ██████ 6 items (24%)
     20-30%  ████ 4 items (16%)
     30-40%  ███ 3 items (12%)
     40-50%  ██ 2 items (8%)
     50%+    ██ 2 items (8%)
   
   Temporal Analysis:
     Acquisition Frequency: Every 3.7 days (average)
     Best Month: July (8 items, 15.2% avg cloud cover)
     Platform Distribution:
       sentinel-2a: 13 items (52%)
       sentinel-2b: 12 items (48%)
   
   Quality Assessment:
     Excellent (< 10% clouds): 8 items (32%)
     Good (10-25% clouds): 10 items (40%)
     Fair (25-50% clouds): 5 items (20%)
     Poor (> 50% clouds): 2 items (8%)
   
   Recommendations:
     ✅ Good dataset for analysis (72% usable quality)
     💡 Consider filtering to < 25% cloud cover (18 items)
     📅 July data provides best quality options

download-summary
~~~~~~~~~~~~~~~~

Create comprehensive summaries of download operations.

**Syntax**:

.. code-block:: bash

   ogapi utils download-summary <DOWNLOAD_RESULTS_FILE> [OPTIONS]

**Arguments**:

- ``DOWNLOAD_RESULTS_FILE``: JSON file containing download results

**Summary Options**:

- ``--format``: Summary format (detailed, brief, json) [default: detailed]
- ``--include-failed`` / ``--success-only``: Include failed downloads [default: include-failed]

**Output Options**:

- ``--output`` / ``-o``: Save summary to file
- ``--charts`` / ``--no-charts``: Include ASCII charts [default: charts]

**Examples**:

.. code-block:: bash

   # Create detailed download summary
   ogapi utils download-summary download_results.json
   
   # Brief summary format
   ogapi utils download-summary download_results.json --format brief
   
   # Save summary to file
   ogapi utils download-summary download_results.json \
     --output download_report.json

**Sample Output**:

.. code-block:: text

   Download Summary Report:
   =======================
   
   Operation Details:
     Start Time: 2024-06-22 15:30:00 UTC
     End Time: 2024-06-22 16:45:00 UTC
     Duration: 1h 15m 0s
   
   Download Statistics:
     Total Files: 48
     Successfully Downloaded: 45 (93.8%)
     Failed Downloads: 3 (6.2%)
     Total Size: 12.4 GB
     Average Speed: 2.78 MB/s
   
   Success Rate by Asset:
     B04: ████████████████████ 16/16 (100%)
     B03: ████████████████████ 16/16 (100%)
     B02: ███████████████████▌ 15/16 (93.8%)
     B08: ████████████████████ 16/16 (100%)
   
   Failed Downloads:
     - S2A_MSIL2A_20240615.../B02.tif (Network timeout)
     - S2B_MSIL2A_20240618.../B02.tif (URL expired)
     - S2A_MSIL2A_20240620.../B02.tif (404 Not Found)
   
   Recommendations:
     🔄 Retry failed downloads with --resume
     🔗 Check URL expiration for failed items
     📊 Overall success rate is excellent (93.8%)

Advanced Utility Operations
---------------------------

Batch Processing
~~~~~~~~~~~~~~~~

.. code-block:: bash

   #!/bin/bash
   # Batch utility operations
   
   # Process multiple search result files
   for file in *_search_results.json; do
       echo "Processing $file..."
       
       # Filter by cloud cover
       ogapi utils filter-clouds "$file" \
         --max-cloud-cover 20 \
         --output "${file%.*}_filtered.json"
       
       # Export URLs
       ogapi utils export-urls "${file%.*}_filtered.json" \
         --assets "B04,B03,B02" \
         --output "${file%.*}_urls.json"
       
       # Validate URLs
       ogapi utils validate-urls "${file%.*}_urls.json" \
         --fix-expired \
         --output "${file%.*}_valid_urls.json"
   done

Quality Assessment Pipeline
~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: bash

   # Complete quality assessment workflow
   
   # 1. Analyze initial search results
   ogapi utils analyze search_results.json \
     --output initial_analysis.json
   
   # 2. Filter based on analysis recommendations
   ogapi utils filter-clouds search_results.json \
     --max-cloud-cover 25 \
     --output quality_filtered.json
   
   # 3. Re-analyze filtered results
   ogapi utils analyze quality_filtered.json \
     --output filtered_analysis.json
   
   # 4. Export URLs for best quality data
   ogapi utils export-urls quality_filtered.json \
     --assets "B08,B04" \
     --output analysis_ready_urls.json

Data Validation Workflow
~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: bash

   # Comprehensive data validation pipeline
   
   # 1. Export URLs from search results
   ogapi utils export-urls search_results.json \
     --all-assets \
     --output exported_urls.json
   
   # 2. Validate all URLs
   ogapi utils validate-urls exported_urls.json \
     --check-access \
     --detailed \
     --export-report validation_report.json
   
   # 3. Fix any issues found
   ogapi utils validate-urls exported_urls.json \
     --fix-expired \
     --output validated_urls.json
   
   # 4. Generate final validation summary
   ogapi utils validate-urls validated_urls.json \
     --summary

Integration with External Tools
-------------------------------

Export for External Processing
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: bash

   # Export for wget
   ogapi utils export-urls search_results.json \
     --format simple \
     --assets "B04" \
     --output wget_urls.json
   
   # Convert to wget script
   jq -r 'keys[]' wget_urls.json > wget_urls.txt
   
   # Export for aria2
   ogapi utils export-urls search_results.json \
     --format simple \
     --output aria2_urls.json

Statistical Analysis Export
~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: bash

   # Export analysis data for R/Python
   ogapi utils analyze search_results.json \
     --format json \
     --detailed \
     --output analysis_data.json
   
   # Extract specific metrics
   jq '.cloud_cover_distribution' analysis_data.json > cloud_cover_stats.json
   jq '.temporal_analysis' analysis_data.json > temporal_stats.json

Error Handling and Troubleshooting
-----------------------------------

Common Utility Issues
~~~~~~~~~~~~~~~~~~~~~

**File Format Errors**:

.. code-block:: bash

   # Validate JSON structure
   python -c "import json; json.load(open('search_results.json'))"
   
   # Check file structure
   jq 'keys' search_results.json

**Empty Results**:

.. code-block:: bash

   # Check why filtering returned no results
   ogapi utils filter-clouds search_results.json \
     --max-cloud-cover 100 \
     --show-stats  # See full distribution

**URL Validation Failures**:

.. code-block:: bash

   # Diagnose URL issues
   ogapi utils validate-urls urls.json \
     --detailed \
     --check-access

Performance Optimization
~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: bash

   # Disable expensive operations for large datasets
   ogapi utils validate-urls large_urls.json \
     --no-check-access \  # Skip HTTP requests
     --summary           # Minimal output
   
   # Process in chunks for very large files
   split -l 1000 large_search_results.json chunk_
   for chunk in chunk_*; do
       ogapi utils analyze "$chunk" --output "${chunk}_analysis.json"
   done

The utility commands provide essential tools for data quality management, validation, and analysis throughout the satellite data processing workflow.
