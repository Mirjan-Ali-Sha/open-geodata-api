Search CLI Commands
===================

Search for satellite data items from various providers with comprehensive filtering options.

Basic Usage
-----------

.. code-block:: bash

   ogapi search --help
   ogapi search items --help
   ogapi search quick --help
   ogapi search compare --help

Commands Overview
-----------------

items
~~~~~

Search for satellite data items with detailed filters.

**Syntax**:

.. code-block:: bash

   ogapi search items [OPTIONS]

**Required Options**:

- ``--collections`` / ``-c``: Comma-separated collection names

**Search Options**:

- ``--provider`` / ``-p``: Data provider (pc, es, both) [default: pc]
- ``--bbox`` / ``-b``: Bounding box as "west,south,east,north"
- ``--datetime`` / ``-d``: Date range "YYYY-MM-DD/YYYY-MM-DD" or single date
- ``--query`` / ``-q``: JSON filter query for advanced filtering
- ``--limit`` / ``-l``: Maximum number of items to return [default: 10]

**Quality Filters**:

- ``--cloud-cover`` / ``-cc``: Maximum cloud cover percentage
- ``--min-cloud`` / ``--max-cloud``: Cloud cover range

**Output Options**:

- ``--output`` / ``-o``: Save results to JSON file
- ``--format``: Output format (json, table, summary) [default: table]
- ``--show-assets`` / ``--no-assets``: Show asset information [default: no-assets]

**Examples**:

.. code-block:: bash

   # Basic search
   ogapi search items -c sentinel-2-l2a -b "-122.5,47.5,-122.0,48.0"
   
   # Search with date range and cloud filter
   ogapi search items \
     -c sentinel-2-l2a \
     -b "-122.5,47.5,-122.0,48.0" \
     -d "2024-06-01/2024-08-31" \
     --cloud-cover 20
   
   # Advanced search with JSON query
   ogapi search items \
     -c sentinel-2-l2a \
     -b "-122.5,47.5,-122.0,48.0" \
     -q '{"eo:cloud_cover":{"lt":15},"platform":{"eq":"sentinel-2a"}}'
   
   # Save results to file
   ogapi search items \
     -c sentinel-2-l2a \
     -b "-122.5,47.5,-122.0,48.0" \
     --output search_results.json

**Sample Output**:

.. code-block:: text

   Search Results (Planetary Computer):
   ====================================
   
   Found 8 items for sentinel-2-l2a in the specified area
   
   Item 1:
     ID: S2A_MSIL2A_20240615T180921_N0510_R027_T11ULA_20240616T000511
     Date: 2024-06-15T18:09:21Z
     Cloud Cover: 12.5%
     Platform: sentinel-2a
   
   Item 2:
     ID: S2B_MSIL2A_20240618T180919_N0510_R027_T11ULA_20240618T213456
     Date: 2024-06-18T18:09:19Z
     Cloud Cover: 8.3%
     Platform: sentinel-2b
   
   ...
   
   Results saved to: search_results.json

quick
~~~~~

Quick search for recent clear data at a specific location.

**Syntax**:

.. code-block:: bash

   ogapi search quick COLLECTION BBOX [OPTIONS]

**Arguments**:

- ``COLLECTION``: Collection to search (e.g., "sentinel-2-l2a")
- ``BBOX``: Bounding box as "west,south,east,north"

**Options**:

- ``--provider`` / ``-p``: Data provider [default: pc]
- ``--days`` / ``-d``: Number of days back to search [default: 30]
- ``--cloud-cover`` / ``-cc``: Maximum cloud cover percentage [default: 30]
- ``--limit`` / ``-l``: Maximum results to show [default: 5]
- ``--output`` / ``-o``: Save results to JSON file

**Examples**:

.. code-block:: bash

   # Quick search for recent Sentinel-2 data
   ogapi search quick sentinel-2-l2a "-122.5,47.5,-122.0,48.0"
   
   # Search last 7 days with very low cloud cover
   ogapi search quick sentinel-2-l2a "-122.5,47.5,-122.0,48.0" \
     --days 7 --cloud-cover 10
   
   # Save quick search results
   ogapi search quick landsat-c2-l2 "-120.0,35.0,-119.0,36.0" \
     --output recent_landsat.json

**Sample Output**:

.. code-block:: text

   Quick Search Results:
   ====================
   
   Collection: sentinel-2-l2a
   Area: [-122.5, 47.5, -122.0, 48.0]
   Time Range: Last 30 days
   Cloud Cover: < 30%
   
   Found 3 clear scenes:
   
   1. 2024-06-18 (8.3% clouds) - S2B_MSIL2A_20240618...
   2. 2024-06-15 (12.5% clouds) - S2A_MSIL2A_20240615...
   3. 2024-06-10 (18.7% clouds) - S2A_MSIL2A_20240610...

compare
~~~~~~~

Compare data availability between Planetary Computer and EarthSearch.

**Syntax**:

.. code-block:: bash

   ogapi search compare [OPTIONS]

**Required Options**:

- ``--collections`` / ``-c``: Comma-separated collection names
- ``--bbox`` / ``-b``: Bounding box as "west,south,east,north"

**Optional Parameters**:

- ``--datetime`` / ``-d``: Date range for comparison
- ``--cloud-cover`` / ``-cc``: Maximum cloud cover percentage [default: 50]
- ``--limit`` / ``-l``: Maximum items per provider [default: 10]
- ``--output`` / ``-o``: Save comparison results to JSON file

**Examples**:

.. code-block:: bash

   # Compare Sentinel-2 availability
   ogapi search compare \
     -c sentinel-2-l2a \
     -b "-122.5,47.5,-122.0,48.0" \
     -d "2024-06-01/2024-08-31"
   
   # Compare with cloud filtering
   ogapi search compare \
     -c sentinel-2-l2a \
     -b "-122.5,47.5,-122.0,48.0" \
     --cloud-cover 25 \
     --output comparison.json
   
   # Compare multiple collections
   ogapi search compare \
     -c "sentinel-2-l2a,landsat-c2-l2" \
     -b "-120.0,35.0,-119.0,36.0"

**Sample Output**:

.. code-block:: text

   Provider Comparison Results:
   ===========================
   
   Search Parameters:
     Collections: sentinel-2-l2a
     Area: [-122.5, 47.5, -122.0, 48.0]
     Date Range: 2024-06-01 to 2024-08-31
     Max Cloud Cover: 50%
   
   Results Summary:
   ┌─────────────────────┬───────┬─────────────────┬─────────────────┐
   │ Provider            │ Items │ Avg Cloud Cover │ Date Range      │
   ├─────────────────────┼───────┼─────────────────┼─────────────────┤
   │ Planetary Computer  │   12  │      15.3%      │ 2024-06-02 to   │
   │                     │       │                 │ 2024-08-29      │
   ├─────────────────────┼───────┼─────────────────┼─────────────────┤
   │ EarthSearch         │   10  │      18.7%      │ 2024-06-05 to   │
   │                     │       │                 │ 2024-08-25      │
   └─────────────────────┴───────┴─────────────────┴─────────────────┘
   
   Asset Naming Differences:
     PC Assets: B01, B02, B03, B04, B05, B06, B07, B08, B8A, B09, B11, B12
     ES Assets: coastal, blue, green, red, rededge1, rededge2, rededge3, nir, nir08, nir09, swir16, swir22

Advanced Search Patterns
-------------------------

Complex JSON Queries
~~~~~~~~~~~~~~~~~~~~~

Use JSON queries for complex filtering:

.. code-block:: bash

   # Multiple platform filter
   ogapi search items -c sentinel-2-l2a \
     -q '{"platform":{"in":["sentinel-2a","sentinel-2b"]}}'
   
   # Date and quality combination
   ogapi search items -c sentinel-2-l2a \
     -q '{"eo:cloud_cover":{"lt":20},"view:sun_elevation":{"gt":30}}'
   
   # Processing baseline filter
   ogapi search items -c sentinel-2-l2a \
     -q '{"s2:processing_baseline":{"gte":"04.00"}}'

Batch Search Operations
~~~~~~~~~~~~~~~~~~~~~~~

Search multiple areas or time periods:

.. code-block:: bash

   #!/bin/bash
   # Script for batch searching multiple areas
   
   # Define areas of interest
   areas=(
       "-122.5,47.5,-122.0,48.0"  # Seattle
       "-74.2,40.6,-73.9,40.9"    # New York
       "-118.5,34.0,-118.0,34.3"  # Los Angeles
   )
   
   # Search each area
   for i in "${!areas[@]}"; do
       echo "Searching area $((i+1)): ${areas[i]}"
       ogapi search items \
         -c sentinel-2-l2a \
         -b "${areas[i]}" \
         -d "2024-06-01/2024-08-31" \
         --cloud-cover 25 \
         --output "area_${i}_results.json"
   done

Time Series Search
~~~~~~~~~~~~~~~~~~

Search for temporal analysis:

.. code-block:: bash

   # Monthly searches for seasonal analysis
   months=("01" "02" "03" "04" "05" "06" "07" "08" "09" "10" "11" "12")
   
   for month in "${months[@]}"; do
       start_date="2024-${month}-01"
       if [ "$month" = "12" ]; then
           end_date="2024-${month}-31"
       else
           next_month=$(printf "%02d" $((10#$month + 1)))
           end_date="2024-${next_month}-01"
       fi
       
       ogapi search items \
         -c sentinel-2-l2a \
         -b "-122.5,47.5,-122.0,48.0" \
         -d "${start_date}/${end_date}" \
         --cloud-cover 30 \
         --output "month_${month}_results.json"
   done

Working with Search Results
---------------------------

Analyzing Search Output
~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: bash

   # Get summary statistics from search results
   ogapi search items -c sentinel-2-l2a \
     -b "-122.5,47.5,-122.0,48.0" \
     --format summary
   
   # Export detailed table
   ogapi search items -c sentinel-2-l2a \
     -b "-122.5,47.5,-122.0,48.0" \
     --format table \
     --show-assets > detailed_results.txt

Chaining with Other Commands
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: bash

   # Search, filter, and download pipeline
   ogapi search items \
     -c sentinel-2-l2a \
     -b "-122.5,47.5,-122.0,48.0" \
     -d "2024-06-01/2024-08-31" \
     --output search_results.json
   
   # Filter results
   ogapi utils filter-clouds search_results.json \
     --max-cloud-cover 15 \
     --output filtered_results.json
   
   # Download RGB bands
   ogapi download search-results filtered_results.json \
     --assets "B04,B03,B02" \
     --destination "./rgb_data/"

Error Handling and Troubleshooting
-----------------------------------

Common Search Issues
~~~~~~~~~~~~~~~~~~~~

**No Results Found**:

.. code-block:: bash

   # Check if collections exist
   ogapi collections list --filter sentinel
   
   # Try broader search criteria
   ogapi search items -c sentinel-2-l2a \
     -b "-123.0,47.0,-121.0,49.0" \  # Larger area
     -d "2024-01-01/2024-12-31" \    # Longer time range
     --cloud-cover 80                # More permissive cloud filter

**Invalid Parameters**:

.. code-block:: bash

   # Validate bbox format (common mistake)
   # ❌ Wrong: --bbox "47.5,-122.5,48.0,-122.0"  (lat,lon order)
   # ✅ Correct: --bbox "-122.5,47.5,-122.0,48.0"  (west,south,east,north)
   
   # Validate date format
   # ❌ Wrong: --datetime "06/01/2024"
   # ✅ Correct: --datetime "2024-06-01"

**Provider Connection Issues**:

.. code-block:: bash

   # Test provider connectivity
   ogapi search items -c sentinel-2-l2a --provider pc --limit 1
   ogapi search items -c sentinel-2-l2a --provider es --limit 1
   
   # Use verbose mode for debugging
   ogapi --verbose search items -c sentinel-2-l2a

Search Performance Tips
~~~~~~~~~~~~~~~~~~~~~~~

1. **Use appropriate limits**: Start with small limits for testing
2. **Apply filters early**: Use cloud cover and date filters
3. **Choose optimal areas**: Smaller bounding boxes search faster
4. **Cache results**: Save search results to avoid repeated API calls

.. code-block:: bash

   # Fast search pattern
   ogapi search items \
     -c sentinel-2-l2a \
     -b "-122.1,47.6,-122.0,47.7" \  # Small area
     -d "2024-07-01/2024-07-31" \    # One month
     --cloud-cover 20 \              # Quality filter
     --limit 10                      # Reasonable limit
