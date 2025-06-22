Collections CLI Commands
========================

The collections command group provides tools for discovering and exploring satellite data collections.

Basic Usage
-----------

.. code-block:: bash

   ogapi collections --help
   ogapi collections list
   ogapi collections search <keyword>
   ogapi collections info <collection-id>

Commands Overview
-----------------

list
~~~~

List available collections from data providers.

**Syntax**:

.. code-block:: bash

   ogapi collections list [OPTIONS]

**Options**:

- ``--provider`` / ``-p``: Choose provider (pc, es, both) [default: both]
- ``--filter`` / ``-f``: Filter collections by keyword
- ``--output`` / ``-o``: Save results to JSON file
- ``--format``: Output format (table, json, list) [default: table]

**Examples**:

.. code-block:: bash

   # List all collections
   ogapi collections list
   
   # List from specific provider
   ogapi collections list --provider pc
   ogapi collections list -p es
   
   # Filter by keyword
   ogapi collections list --filter sentinel
   ogapi collections list -f "landsat"
   
   # Save to file
   ogapi collections list --output collections.json
   
   # Different output formats
   ogapi collections list --format json
   ogapi collections list --format list

**Sample Output**:

.. code-block:: text

   Available Collections (Planetary Computer):
   ┌─────────────────────┬─────────────────────────────────┬──────────────┐
   │ ID                  │ Title                           │ Provider     │
   ├─────────────────────┼─────────────────────────────────┼──────────────┤
   │ sentinel-2-l2a      │ Sentinel-2 Level-2A             │ PC           │
   │ landsat-c2-l2       │ Landsat Collection 2 Level-2    │ PC           │
   │ modis-061-MCD43A4   │ MODIS BRDF-Adjusted Reflectance │ PC           │
   └─────────────────────┴─────────────────────────────────┴──────────────┘

search
~~~~~~

Search for collections by keyword or pattern.

**Syntax**:

.. code-block:: bash

   ogapi collections search <keyword> [OPTIONS]

**Arguments**:

- ``keyword``: Search term to find in collection names/titles

**Options**:

- ``--provider`` / ``-p``: Provider to search (pc, es, both) [default: both]
- ``--output`` / ``-o``: Save results to JSON file
- ``--exact-match`` / ``--fuzzy``: Use exact vs fuzzy matching [default: fuzzy]

**Examples**:

.. code-block:: bash

   # Search for Sentinel collections
   ogapi collections search sentinel
   
   # Search specific provider
   ogapi collections search landsat --provider pc
   
   # Exact match search
   ogapi collections search "sentinel-2" --exact-match
   
   # Save search results
   ogapi collections search modis --output modis_collections.json

**Sample Output**:

.. code-block:: text

   Search Results for "sentinel":
   
   Found 3 collections:
   
   1. sentinel-2-l2a (Planetary Computer)
      Title: Sentinel-2 Level-2A
      Description: Sentinel-2 Level-2A provides atmospherically corrected...
   
   2. sentinel-2-l1c (EarthSearch)
      Title: Sentinel-2 Level-1C
      Description: Sentinel-2 Level-1C provides top-of-atmosphere...
   
   3. sentinel-1-grd (Planetary Computer)
      Title: Sentinel-1 GRD
      Description: Sentinel-1 Ground Range Detected...

info
~~~~

Get detailed information about a specific collection.

**Syntax**:

.. code-block:: bash

   ogapi collections info <collection-id> [OPTIONS]

**Arguments**:

- ``collection-id``: ID of the collection to get information about

**Options**:

- ``--provider`` / ``-p``: Provider to query (pc, es, auto) [default: auto]
- ``--output`` / ``-o``: Save information to JSON file
- ``--show-assets`` / ``--no-assets``: Include asset information [default: show-assets]
- ``--show-extent`` / ``--no-extent``: Include spatial/temporal extent [default: show-extent]

**Examples**:

.. code-block:: bash

   # Get collection information
   ogapi collections info sentinel-2-l2a
   
   # From specific provider
   ogapi collections info sentinel-2-l2a --provider pc
   
   # Save detailed info
   ogapi collections info landsat-c2-l2 --output landsat_info.json
   
   # Minimal info (no assets)
   ogapi collections info sentinel-2-l2a --no-assets --no-extent

**Sample Output**:

.. code-block:: text

   Collection: sentinel-2-l2a
   ===============================================
   
   Basic Information:
     Title: Sentinel-2 Level-2A
     Provider: Planetary Computer
     License: proprietary
     
   Description:
     Sentinel-2 Level-2A provides atmospherically corrected Surface 
     Reflectance imagery. This dataset contains all Sentinel-2 Level-2A 
     data from 2017 to present.
   
   Spatial Extent:
     Bounding Box: [-180.0, -90.0, 180.0, 90.0]
     
   Temporal Extent:
     Start: 2017-03-28T00:00:00Z
     End: None (ongoing)
     
   Available Assets:
     - B01: Coastal aerosol (60m)
     - B02: Blue (10m)
     - B03: Green (10m)
     - B04: Red (10m)
     - B05: Vegetation red edge (20m)
     - B06: Vegetation red edge (20m)
     - B07: Vegetation red edge (20m)
     - B08: NIR (10m)
     - B8A: Vegetation red edge (20m)
     - B09: Water vapour (60m)
     - B11: SWIR (20m)
     - B12: SWIR (20m)
     - AOT: Aerosol optical thickness
     - WVP: Water vapour
     - SCL: Scene classification
     - visual: True color image

Advanced Usage
--------------

Collection Comparison
~~~~~~~~~~~~~~~~~~~~~

Compare collections across providers:

.. code-block:: bash

   # Compare Sentinel-2 availability
   ogapi collections search sentinel-2 --provider both --output comparison.json
   
   # Then analyze the JSON file to see differences

Batch Collection Analysis
~~~~~~~~~~~~~~~~~~~~~~~~~

Get information for multiple collections:

.. code-block:: bash

   #!/bin/bash
   # Script to analyze multiple collections
   
   collections=("sentinel-2-l2a" "landsat-c2-l2" "modis-061-MCD43A4")
   
   for collection in "${collections[@]}"; do
       echo "Analyzing $collection..."
       ogapi collections info "$collection" --output "${collection}_info.json"
   done

Filtering and Discovery
~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: bash

   # Find all optical collections
   ogapi collections list --filter "optical" --output optical_collections.json
   
   # Find all Level-2 products
   ogapi collections list --filter "l2" --output level2_collections.json
   
   # Find MODIS products
   ogapi collections search modis --output modis_products.json

Collection Metadata Export
~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: bash

   # Export complete collection catalog
   ogapi collections list --provider pc --output pc_catalog.json
   ogapi collections list --provider es --output es_catalog.json
   
   # Create combined catalog
   # (requires custom script to merge JSON files)

Working with Collection Information
-----------------------------------

Understanding Collection IDs
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Collection IDs follow different conventions:

**Planetary Computer**:
- ``sentinel-2-l2a``: Sentinel-2 Level-2A
- ``landsat-c2-l2``: Landsat Collection 2 Level-2
- ``modis-061-MCD43A4``: MODIS product with version

**EarthSearch**:
- ``sentinel-2-l2a``: Same as PC for Sentinel-2
- ``landsat-c2-l2``: Same as PC for Landsat
- ``cop-dem-glo-30``: Copernicus DEM Global 30m

Asset Information
~~~~~~~~~~~~~~~~~

Collections contain different assets:

**Optical Imagery**:
- Spectral bands (B01, B02, etc. or blue, green, red)
- Quality masks (SCL, QA)
- Derived products (NDVI, visual composites)

**SAR Imagery**:
- Polarizations (VV, VH)
- Incidence angles
- Processing levels

**Auxiliary Data**:
- Metadata files
- Thumbnails
- Statistics

Temporal and Spatial Extent
~~~~~~~~~~~~~~~~~~~~~~~~~~~

Collections have defined coverage:

**Temporal Extent**:
- Start date: When data collection began
- End date: When it ended (or None for ongoing)
- Update frequency: How often new data is added

**Spatial Extent**:
- Global coverage: [-180, -90, 180, 90]
- Regional coverage: Specific bounding boxes
- Point-based: For weather stations, etc.

Common Workflows
----------------

Collection Discovery Workflow
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: bash

   # 1. Explore available collections
   ogapi collections list
   
   # 2. Search for specific type
   ogapi collections search "sentinel"
   
   # 3. Get detailed information
   ogapi collections info sentinel-2-l2a
   
   # 4. Save for later use
   ogapi collections info sentinel-2-l2a --output sentinel2_info.json

Provider Comparison Workflow
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: bash

   # 1. Check PC collections
   ogapi collections list --provider pc --output pc_collections.json
   
   # 2. Check ES collections
   ogapi collections list --provider es --output es_collections.json
   
   # 3. Compare specific collection
   ogapi collections info sentinel-2-l2a --provider pc --output pc_sentinel2.json
   ogapi collections info sentinel-2-l2a --provider es --output es_sentinel2.json

Collection Analysis Workflow
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: bash

   # 1. Find collections for your domain
   ogapi collections search "vegetation"
   ogapi collections search "water"
   ogapi collections search "urban"
   
   # 2. Analyze temporal coverage
   ogapi collections info selected-collection --show-extent
   
   # 3. Check asset availability
   ogapi collections info selected-collection --show-assets

Error Handling
--------------

Common Issues and Solutions
~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Collection Not Found**:

.. code-block:: bash

   # Error: Collection 'wrong-name' not found
   # Solution: Search for correct name
   ogapi collections search "partial-name"

**Provider Connection Issues**:

.. code-block:: bash

   # Error: Cannot connect to provider
   # Solution: Check internet connection and try other provider
   ogapi collections list --provider es  # Try EarthSearch instead

**No Collections Found**:

.. code-block:: bash

   # Warning: No collections match filter
   # Solution: Try broader search terms
   ogapi collections search "land"  # Instead of "landsat-8-specific"

Troubleshooting Tips
~~~~~~~~~~~~~~~~~~~

1. **Check Provider Status**:

.. code-block:: bash

   # Test connection to providers
   ogapi collections list --provider pc
   ogapi collections list --provider es

2. **Verify Collection Names**:

.. code-block:: bash

   # List all collections and grep for your interest
   ogapi collections list | grep -i "your-term"

3. **Use Verbose Mode**:

.. code-block:: bash

   # Get detailed error information
   ogapi --verbose collections info collection-name

The collections commands provide comprehensive tools for discovering and understanding available satellite data collections across multiple providers.
