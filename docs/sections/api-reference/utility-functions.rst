Utility Functions Reference
===========================

Complete reference for all utility functions in the ``open_geodata_api.utils`` module.

Overview
--------

The utils module provides essential helper functions for data filtering, downloading, URL management, and processing satellite data. These functions are designed to work seamlessly with the core STAC classes.

**Main Categories**:

- :ref:`filtering-functions` - Data quality and criteria filtering
- :ref:`download-functions` - Intelligent downloading and management  
- :ref:`url-management` - URL signing, validation, and refresh
- :ref:`data-processing` - Analysis and conversion helpers
- :ref:`batch-processing` - Large-scale data processing
- :ref:`analysis-helpers` - NDVI calculation and statistics
- :ref:`error-handling` - Robust error handling utilities
- :ref:`configuration` - Global configuration management

.. _filtering-functions:

Filtering Functions
-------------------

filter_by_cloud_cover
~~~~~~~~~~~~~~~~~~~~~~

.. py:function:: filter_by_cloud_cover(items, max_cloud_cover)

   Filter STAC items by maximum cloud cover percentage.

   :param items: Collection of STAC items to filter
   :type items: STACItemCollection or list of STACItem
   :param max_cloud_cover: Maximum allowed cloud cover percentage (0-100)
   :type max_cloud_cover: float
   :returns: Filtered collection with items below cloud cover threshold
   :rtype: STACItemCollection
   :raises ValueError: If max_cloud_cover is not between 0 and 100

**Basic Usage**:

.. code-block:: python

    from open_geodata_api.utils import filter_by_cloud_cover
    
    # Filter to very clear scenes
    clear_items = filter_by_cloud_cover(items, max_cloud_cover=15)
    print(f"Filtered from {len(items)} to {len(clear_items)} clear items")
    
    # Different quality levels
    excellent_quality = filter_by_cloud_cover(items, max_cloud_cover=5)   # Almost no clouds
    good_quality = filter_by_cloud_cover(items, max_cloud_cover=20)       # Light clouds
    acceptable_quality = filter_by_cloud_cover(items, max_cloud_cover=50) # Moderate clouds

**Advanced Usage**:

.. code-block:: python

    # Chain with other filters for complex workflows
    seasonal_items = filter_by_date_range(items, '2024-06-01', '2024-08-31')
    clear_summer = filter_by_cloud_cover(seasonal_items, max_cloud_cover=20)
    
    # Quality analysis workflow
    def analyze_data_quality(items):
        quality_levels = {
            'excellent': filter_by_cloud_cover(items, 5),
            'good': filter_by_cloud_cover(items, 20),
            'acceptable': filter_by_cloud_cover(items, 50)
        }
        
        for level, filtered_items in quality_levels.items():
            print(f"{level.title()}: {len(filtered_items)} items")
            
        return quality_levels
    
    quality_analysis = analyze_data_quality(items)

**Error Handling**:

.. code-block:: python

    try:
        # Validate cloud cover threshold
        if not 0 <= max_cloud_cover <= 100:
            raise ValueError("Cloud cover must be between 0 and 100")
            
        filtered_items = filter_by_cloud_cover(items, max_cloud_cover)
        
    except ValueError as e:
        print(f"Invalid cloud cover threshold: {e}")
    except Exception as e:
        print(f"Filtering failed: {e}")

filter_by_date_range
~~~~~~~~~~~~~~~~~~~~~

.. py:function:: filter_by_date_range(items, start_date, end_date)

   🧠 INTELLIGENT: Filter items by date range with flexible input formats.

   :param items: Collection of STAC items to filter
   :type items: STACItemCollection or list of STACItem
   :param start_date: Start date (inclusive) - supports multiple formats
   :type start_date: str, datetime, or None
   :param end_date: End date (inclusive) - supports multiple formats  
   :type end_date: str, datetime, or None
   :returns: Items within the specified date range
   :rtype: STACItemCollection

**Flexible Date Format Examples**:

.. code-block:: python

    from open_geodata_api.utils import filter_by_date_range
    from datetime import datetime
    
    # 1. ISO 8601 strings (recommended)
    summer_items = filter_by_date_range(
        items,
        start_date='2024-06-01',
        end_date='2024-08-31'
    )
    
    # 2. Full ISO datetime strings
    precise_items = filter_by_date_range(
        items,
        start_date='2024-06-01T00:00:00Z',
        end_date='2024-08-31T23:59:59Z'
    )
    
    # 3. Python datetime objects
    summer_items = filter_by_date_range(
        items,
        start_date=datetime(2024, 6, 1),
        end_date=datetime(2024, 8, 31)
    )
    
    # 4. Natural language dates (intelligent parsing)
    readable_items = filter_by_date_range(
        items,
        start_date="June 1, 2024",
        end_date="Aug 31, 2024"
    )
    
    # 5. Mixed formats
    mixed_items = filter_by_date_range(
        items,
        start_date="2024-01-01",        # ISO string
        end_date="Mar 31, 2024"         # Natural language
    )

**One-Sided Filtering**:

.. code-block:: python

    # Only filter by start date (everything after)
    recent_items = filter_by_date_range(
        items,
        start_date='2024-06-01',
        end_date=None
    )
    
    # Only filter by end date (everything before)
    historical_items = filter_by_date_range(
        items,
        start_date=None,
        end_date='2024-06-01'
    )

**Seasonal Analysis Workflow**:

.. code-block:: python

    def get_seasonal_data(items, year=2024):
        """Extract seasonal data for analysis."""
        seasons = {
            'spring': filter_by_date_range(items, f'{year}-03-01', f'{year}-05-31'),
            'summer': filter_by_date_range(items, f'{year}-06-01', f'{year}-08-31'),
            'fall': filter_by_date_range(items, f'{year}-09-01', f'{year}-11-30'),
            'winter': filter_by_date_range(items, f'{year}-12-01', f'{year+1}-02-28')
        }
        
        for season, season_items in seasons.items():
            print(f"{season.title()}: {len(season_items)} items")
            
        return seasons
    
    seasonal_data = get_seasonal_data(items)

**Time Series Analysis**:

.. code-block:: python

    # Monthly breakdown for detailed analysis
    def monthly_breakdown(items, year=2024):
        monthly_data = {}
        
        for month in range(1, 13):
            if month == 12:
                next_month = 1
                next_year = year + 1
            else:
                next_month = month + 1
                next_year = year
                
            start_date = f'{year}-{month:02d}-01'
            end_date = f'{next_year}-{next_month:02d}-01'
            
            monthly_items = filter_by_date_range(items, start_date, end_date)
            monthly_data[f'{year}-{month:02d}'] = monthly_items
            
        return monthly_data
    
    monthly_data = monthly_breakdown(items)

filter_by_geometry
~~~~~~~~~~~~~~~~~~~

.. py:function:: filter_by_geometry(items, geometry)

   🧠 INTELLIGENT: Filter items that intersect with geometry - automatically detects input format.

   :param items: Collection of STAC items to filter
   :type items: STACItemCollection
   :param geometry: Geometry to filter by (auto-detects format)
   :type geometry: Various supported formats
   :returns: Items that intersect with the geometry
   :rtype: STACItemCollection

**Supported Geometry Formats**:

.. code-block:: python

    from open_geodata_api.utils import filter_by_geometry
    
    # 1. Bounding box [minx, miny, maxx, maxy]
    bbox_items = filter_by_geometry(items, [-122.5, 47.5, -122.0, 48.0])
    
    # 2. Point coordinates [x, y]
    point_items = filter_by_geometry(items, [-122.3321, 47.6062])
    
    # 3. Diagonal points [[x1, y1], [x2, y2]]
    diagonal_items = filter_by_geometry(items, [[-122.5, 47.5], [-122.0, 48.0]])
    
    # 4. GeoJSON Point
    geojson_point = {"type": "Point", "coordinates": [-122.3321, 47.6062]}
    point_geojson_items = filter_by_geometry(items, geojson_point)
    
    # 5. GeoJSON Polygon
    geojson_polygon = {
        "type": "Polygon",
        "coordinates": [[
            [-122.5, 47.5], [-122.0, 47.5],
            [-122.0, 48.0], [-122.5, 48.0], [-122.5, 47.5]
        ]]
    }
    polygon_items = filter_by_geometry(items, geojson_polygon)

**Shapely Integration** (if available):

.. code-block:: python

    try:
        from shapely.geometry import Point, Polygon, box
        
        # Shapely Point
        shapely_point = Point(-122.3321, 47.6062)
        shapely_point_items = filter_by_geometry(items, shapely_point)
        
        # Shapely Polygon
        shapely_polygon = Polygon([
            (-122.5, 47.5), (-122.0, 47.5),
            (-122.0, 48.0), (-122.5, 48.0)
        ])
        shapely_polygon_items = filter_by_geometry(items, shapely_polygon)
        
        # Shapely Box (equivalent to bbox)
        shapely_box = box(-122.5, 47.5, -122.0, 48.0)
        box_items = filter_by_geometry(items, shapely_box)
        
    except ImportError:
        print("Install shapely for enhanced geometry support: pip install shapely")

**GeoPandas Integration** (if available):

.. code-block:: python

    try:
        import geopandas as gpd
        from shapely.geometry import box
        
        # Load from file
        gdf = gpd.read_file('area_of_interest.geojson')
        
        # Filter using GeoPandas geometry
        geopandas_items = filter_by_geometry(items, gdf.geometry.iloc[0])
        
        # Create GeoPandas geometry from scratch
        study_area = gpd.GeoDataFrame({
            'name': ['Study Area'],
            'geometry': [box(-122.5, 47.5, -122.0, 48.0)]
        })
        
        study_items = filter_by_geometry(items, study_area.geometry.iloc[0])
        
    except ImportError:
        print("Install geopandas for GIS integration: pip install geopandas")

**WKT (Well-Known Text) Support**:

.. code-block:: python

    # WKT Point
    wkt_point = "POINT(-122.3321 47.6062)"
    wkt_point_items = filter_by_geometry(items, wkt_point)
    
    # WKT Polygon  
    wkt_polygon = "POLYGON((-122.5 47.5, -122.0 47.5, -122.0 48.0, -122.5 48.0, -122.5 47.5))"
    wkt_polygon_items = filter_by_geometry(items, wkt_polygon)
    
    # WKT from file
    with open('study_area.wkt', 'r') as f:
        wkt_from_file = f.read()
        wkt_file_items = filter_by_geometry(items, wkt_from_file)

**Complex Spatial Analysis Workflow**:

.. code-block:: python

    def multi_area_analysis(items, areas_of_interest):
        """Analyze multiple areas of interest."""
        results = {}
        
        for area_name, geometry in areas_of_interest.items():
            # Filter items for this area
            area_items = filter_by_geometry(items, geometry)
            
            # Apply additional filters
            clear_items = filter_by_cloud_cover(area_items, max_cloud_cover=20)
            recent_items = filter_by_date_range(clear_items, '2024-01-01', None)
            
            results[area_name] = {
                'total_items': len(area_items),
                'clear_items': len(clear_items), 
                'recent_clear_items': len(recent_items),
                'items': recent_items
            }
            
        return results
    
    # Define multiple study areas
    study_areas = {
        'urban_center': [-122.35, 47.60, -122.30, 47.65],
        'forest_area': [[-122.45, 47.55], [-122.40, 47.60]],
        'coastal_region': {
            "type": "Polygon",
            "coordinates": [[
                [-122.50, 47.50], [-122.25, 47.50],
                [-122.25, 47.75], [-122.50, 47.75], [-122.50, 47.50]
            ]]
        }
    }
    
    analysis_results = multi_area_analysis(items, study_areas)

.. _download-functions:

Download Functions
------------------

download_datasets
~~~~~~~~~~~~~~~~~~

.. py:function:: download_datasets(data_source, destination='./', asset_keys=None, **kwargs)

   Universal download function that intelligently handles various input types.

   :param data_source: Data to download (STACItemCollection, URL dict, or file path)
   :type data_source: STACItemCollection, dict, or str
   :param destination: Base destination directory
   :type destination: str or Path
   :param asset_keys: Specific assets to download (None for all)
   :type asset_keys: list of str or None
   :param kwargs: Additional download options
   :returns: Download results with file paths
   :rtype: dict

**Basic Download Examples**:

.. code-block:: python

    from open_geodata_api.utils import download_datasets
    import os
    
    # 1. Download from STAC items (most common)
    results = download_datasets(
        items, 
        destination="./satellite_data/",
        asset_keys=['B04', 'B03', 'B02']  # RGB bands
    )
    
    # 2. Download all assets
    all_results = download_datasets(items, destination="./complete_data/")
    
    # 3. Download with progress tracking
    progress_results = download_datasets(
        items,
        destination="./data/",
        show_progress=True,
        max_workers=4
    )

**Advanced Download Configuration**:

.. code-block:: python

    # Comprehensive download with all options
    advanced_results = download_datasets(
        items,
        destination="./analysis_ready/",
        asset_keys=['B08', 'B04', 'B03', 'B02'],  # NIR + RGB
        create_folders=True,           # Organize by item
        max_workers=6,                 # Parallel downloads
        chunk_size=8192,              # Download chunk size
        show_progress=True,            # Progress bar
        timeout=120,                  # Request timeout
        retries=3,                    # Retry failed downloads
        verify_ssl=True,              # SSL verification
        headers={'User-Agent': 'MyApp/1.0'}  # Custom headers
    )
    
    # Check results
    print(f"Successfully downloaded: {advanced_results['successful_downloads']}")
    print(f"Failed downloads: {advanced_results['failed_downloads']}")
    print(f"Total size: {advanced_results['total_size_mb']:.2f} MB")

**Different Input Types**:

.. code-block:: python

    # 1. From URL dictionary
    url_dict = {
        'item1': {
            'B04': 'https://example.com/item1_B04.tif',
            'B03': 'https://example.com/item1_B03.tif'
        },
        'item2': {
            'B04': 'https://example.com/item2_B04.tif',
            'B03': 'https://example.com/item2_B03.tif'
        }
    }
    url_results = download_datasets(url_dict, destination="./from_urls/")
    
    # 2. From JSON file
    json_results = download_datasets(
        "exported_urls.json", 
        destination="./from_json/"
    )
    
    # 3. From seasonal data structure
    seasonal_data = {
        'spring_2024': {
            'urls': url_dict,
            'metadata': {'season': 'spring', 'year': 2024}
        }
    }
    seasonal_results = download_datasets(
        seasonal_data, 
        seasons=['spring_2024'],
        destination="./seasonal/"
    )

**Production Download Workflow**:

.. code-block:: python

    def production_download_workflow(items, base_dir="./production/"):
        """Production-ready download workflow with error handling."""
        
        # Create organized directory structure
        os.makedirs(base_dir, exist_ok=True)
        
        # Download different asset types separately
        workflows = {
            'rgb': {
                'assets': ['B04', 'B03', 'B02'],
                'folder': 'rgb_bands',
                'description': 'RGB composite bands'
            },
            'nir': {
                'assets': ['B08'],
                'folder': 'nir_bands', 
                'description': 'Near-infrared band'
            },
            'analysis': {
                'assets': ['B08', 'B04', 'B11', 'B12'],
                'folder': 'analysis_bands',
                'description': 'Vegetation and moisture analysis'
            }
        }
        
        all_results = {}
        
        for workflow_name, config in workflows.items():
            print(f"\n🔄 Downloading {config['description']}...")
            
            workflow_dir = os.path.join(base_dir, config['folder'])
            
            try:
                results = download_datasets(
                    items,
                    destination=workflow_dir,
                    asset_keys=config['assets'],
                    create_folders=True,
                    show_progress=True,
                    max_workers=4,
                    retries=3
                )
                
                all_results[workflow_name] = results
                print(f"✅ {workflow_name}: {results['successful_downloads']} files downloaded")
                
            except Exception as e:
                print(f"❌ {workflow_name} failed: {e}")
                all_results[workflow_name] = {'error': str(e)}
        
        return all_results
    
    # Execute production workflow
    production_results = production_download_workflow(items)

download_url
~~~~~~~~~~~~

.. py:function:: download_url(url, destination=None, provider=None, **kwargs)

   Download a single file from URL with automatic provider handling.

   :param url: URL to download
   :type url: str
   :param destination: Local file path or directory
   :type destination: str or Path or None
   :param provider: Provider hint for URL handling
   :type provider: str or None
   :returns: Path to downloaded file
   :rtype: str

**Single File Downloads**:

.. code-block:: python

    from open_geodata_api.utils import download_url
    
    # Simple download (auto-generates filename)
    file_path = download_url("https://example.com/B04.tif")
    print(f"Downloaded to: {file_path}")
    
    # Download to specific location
    specific_path = download_url(
        "https://example.com/B04.tif",
        destination="./data/red_band.tif"
    )
    
    # Download with provider optimization
    pc_path = download_url(
        "https://planetarycomputer.microsoft.com/api/stac/v1/collections/sentinel-2-l2a/items/item.tif",
        destination="./pc_data/",
        provider="planetary_computer"
    )

**Advanced Single File Download**:

.. code-block:: python

    # Download with comprehensive configuration
    advanced_path = download_url(
        url="https://example.com/large_file.tif",
        destination="./downloads/custom_name.tif",
        provider="earth_search",
        timeout=300,              # 5 minute timeout
        retries=5,               # Retry 5 times
        chunk_size=16384,        # 16KB chunks
        show_progress=True,      # Show progress bar
        verify_ssl=True,         # SSL verification
        headers={                # Custom headers
            'User-Agent': 'SatelliteAnalysis/1.0',
            'Accept': 'application/octet-stream'
        }
    )

**Batch Single Downloads**:

.. code-block:: python

    def download_url_list(urls, base_destination="./downloads/"):
        """Download a list of URLs with error handling."""
        results = {}
        
        for i, url in enumerate(urls, 1):
            try:
                print(f"Downloading {i}/{len(urls)}: {url}")
                
                file_path = download_url(
                    url,
                    destination=base_destination,
                    show_progress=True
                )
                
                results[url] = {
                    'success': True,
                    'path': file_path,
                    'size': os.path.getsize(file_path)
                }
                
            except Exception as e:
                results[url] = {
                    'success': False,
                    'error': str(e)
                }
                print(f"❌ Failed: {e}")
        
        return results
    
    # Download list of URLs
    url_list = [
        "https://example.com/file1.tif",
        "https://example.com/file2.tif", 
        "https://example.com/file3.tif"
    ]
    
    batch_results = download_url_list(url_list)

download_items
~~~~~~~~~~~~~~

.. py:function:: download_items(items, base_destination, asset_keys=None, create_product_folders=True, **kwargs)

   Download all assets from STAC items with intelligent organization.

   :param items: STAC items to download
   :type items: STACItemCollection or list of STACItem
   :param base_destination: Base directory for downloads
   :type base_destination: str or Path
   :param asset_keys: Specific assets to download
   :type asset_keys: list of str or None
   :param create_product_folders: Create separate folders for each item
   :type create_product_folders: bool
   :returns: Download results organized by item and asset
   :rtype: dict

**Organized Downloads**:

.. code-block:: python

    from open_geodata_api.utils import download_items
    
    # Download with automatic organization
    organized_results = download_items(
        items,
        base_destination="./organized_data/",
        asset_keys=['B08', 'B04', 'B03', 'B02'],
        create_product_folders=True  # Creates folder per item
    )
    
    # Results structure:
    # organized_data/
    # ├── item_20240601_tile_33UUP/
    # │   ├── B08.tif
    # │   ├── B04.tif
    # │   ├── B03.tif
    # │   └── B02.tif
    # └── item_20240602_tile_33UUP/
    #     ├── B08.tif
    #     ├── B04.tif
    #     ├── B03.tif
    #     └── B02.tif

**Flat Organization**:

.. code-block:: python

    # Download without folder organization
    flat_results = download_items(
        items,
        base_destination="./flat_data/",
        asset_keys=['B04', 'B03', 'B02'],
        create_product_folders=False  # All files in same directory
    )
    
    # Results structure:
    # flat_data/
    # ├── item1_B04.tif
    # ├── item1_B03.tif
    # ├── item1_B02.tif
    # ├── item2_B04.tif
    # ├── item2_B03.tif
    # └── item2_B02.tif

**Custom Organization Workflow**:

.. code-block:: python

    def custom_download_organization(items, base_dir="./custom_org/"):
        """Custom download organization by date and collection."""
        
        # Group items by date and collection
        grouped_items = {}
        
        for item in items:
            # Extract date and collection
            date_str = item.properties.get('datetime', '')[:10]  # YYYY-MM-DD
            collection = item.collection
            
            key = f"{collection}_{date_str}"
            if key not in grouped_items:
                grouped_items[key] = []
            grouped_items[key].append(item)
        
        all_results = {}
        
        for group_name, group_items in grouped_items.items():
            print(f"Downloading {group_name}: {len(group_items)} items")
            
            group_dir = os.path.join(base_dir, group_name)
            
            # Create STACItemCollection for this group
            from open_geodata_api.core.collections import STACItemCollection
            group_collection = STACItemCollection(
                [item.to_dict() for item in group_items],
                provider=group_items[0].provider if group_items else "unknown"
            )
            
            results = download_items(
                group_collection,
                base_destination=group_dir,
                asset_keys=['B08', 'B04', 'B03'],
                create_product_folders=True
            )
            
            all_results[group_name] = results
        
        return all_results
    
    custom_results = custom_download_organization(items)

**Quality Control Download**:

.. code-block:: python

    def quality_controlled_download(items, base_dir="./qc_data/"):
        """Download with quality control and validation."""
        
        # Pre-filter for quality
        high_quality_items = filter_by_cloud_cover(items, max_cloud_cover=10)
        
        if len(high_quality_items) == 0:
            print("No high-quality items found")
            return {}
        
        print(f"Downloading {len(high_quality_items)} high-quality items")
        
        # Download with validation
        results = download_items(
            high_quality_items,
            base_destination=base_dir,
            asset_keys=['B08', 'B04', 'B03', 'B02'],
            create_product_folders=True,
            verify_downloads=True,  # Verify file integrity
            min_file_size=1024*1024,  # Minimum 1MB files
            max_workers=3  # Conservative for quality
        )
        
        # Post-download validation
        validated_results = {}
        
        for item_id, item_results in results.items():
            validated_item = {}
            
            for asset_key, file_path in item_results.items():
                if file_path and os.path.exists(file_path):
                    file_size = os.path.getsize(file_path)
                    
                    if file_size > 1024*1024:  # At least 1MB
                        validated_item[asset_key] = {
                            'path': file_path,
                            'size_mb': file_size / (1024*1024),
                            'valid': True
                        }
                    else:
                        validated_item[asset_key] = {
                            'path': file_path,
                            'size_mb': file_size / (1024*1024),
                            'valid': False,
                            'reason': 'File too small'
                        }
                        
            validated_results[item_id] = validated_item
        
        return validated_results
    
    qc_results = quality_controlled_download(items)

download_seasonal_data
~~~~~~~~~~~~~~~~~~~~~~

.. py:function:: download_seasonal_data(seasonal_data, base_destination, seasons=None, asset_keys=None, **kwargs)

   Download seasonal data structures with temporal organization.

   :param seasonal_data: Seasonal data structure
   :type seasonal_data: dict
   :param base_destination: Base directory for seasonal downloads
   :type base_destination: str or Path
   :param seasons: Specific seasons to download (None for all)
   :type seasons: list of str or None
   :param asset_keys: Specific assets to download
   :type asset_keys: list of str or None
   :returns: Download results organized by season and item
   :rtype: dict

**Seasonal Data Download**:

.. code-block:: python

    from open_geodata_api.utils import download_seasonal_data
    
    # Prepare seasonal data structure
    seasonal_data = {
        'spring_2024': {
            'count': 45,
            'date_range': '2024-03-01/2024-05-31',
            'cloud_cover_avg': 15.2,
            'urls': {
                'item1': {'B08': 'url1', 'B04': 'url2', 'B03': 'url3'},
                'item2': {'B08': 'url4', 'B04': 'url5', 'B03': 'url6'}
            }
        },
        'summer_2024': {
            'count': 52,
            'date_range': '2024-06-01/2024-08-31', 
            'cloud_cover_avg': 8.7,
            'urls': {
                'item3': {'B08': 'url7', 'B04': 'url8', 'B03': 'url9'},
                'item4': {'B08': 'url10', 'B04': 'url11', 'B03': 'url12'}
            }
        },
        'fall_2024': {
            'count': 38,
            'date_range': '2024-09-01/2024-11-30',
            'cloud_cover_avg': 22.1, 
            'urls': {
                'item5': {'B08': 'url13', 'B04': 'url14', 'B03': 'url15'}
            }
        }
    }
    
    # Download all seasons
    all_seasonal_results = download_seasonal_data(
        seasonal_data,
        base_destination="./time_series_analysis/",
        asset_keys=['B08', 'B04', 'B03']
    )

**Selective Seasonal Download**:

.. code-block:: python

    # Download specific seasons only
    growing_season_results = download_seasonal_data(
        seasonal_data,
        base_destination="./growing_season/",
        seasons=['spring_2024', 'summer_2024'],  # Only growing season
        asset_keys=['B08', 'B04']  # NIR and Red for vegetation analysis
    )
    
    # Download for phenology analysis
    phenology_results = download_seasonal_data(
        seasonal_data,
        base_destination="./phenology_study/",
        seasons=['spring_2024', 'summer_2024', 'fall_2024'],
        asset_keys=['B08', 'B04', 'B03', 'B02'],
        create_season_folders=True,  # Organize by season
        max_workers=6
    )

**Multi-Year Seasonal Analysis**:

.. code-block:: python

    def multi_year_seasonal_download(items_by_year, base_dir="./multi_year/"):
        """Download and organize multi-year seasonal data."""
        
        all_results = {}
        
        for year, yearly_items in items_by_year.items():
            print(f"Processing year {year}...")
            
            # Create seasonal breakdown for this year
            year_seasonal_data = create_seasonal_breakdown(yearly_items, year)
            
            # Download seasonal data for this year
            year_results = download_seasonal_data(
                year_seasonal_data,
                base_destination=os.path.join(base_dir, str(year)),
                asset_keys=['B08', 'B04'],
                create_season_folders=True
            )
            
            all_results[year] = year_results
        
        return all_results
    
    def create_seasonal_breakdown(items, year):
        """Create seasonal data structure from items."""
        seasonal_items = {
            f'spring_{year}': filter_by_date_range(items, f'{year}-03-01', f'{year}-05-31'),
            f'summer_{year}': filter_by_date_range(items, f'{year}-06-01', f'{year}-08-31'),
            f'fall_{year}': filter_by_date_range(items, f'{year}-09-01', f'{year}-11-30'),
            f'winter_{year}': filter_by_date_range(items, f'{year}-12-01', f'{year+1}-02-28')
        }
        
        seasonal_data = {}
        
        for season_name, season_items in seasonal_items.items():
            if len(season_items) > 0:
                # Extract URLs from items
                urls = {}
                for item in season_items:
                    urls[item.id] = item.get_asset_urls(['B08', 'B04'])
                
                seasonal_data[season_name] = {
                    'count': len(season_items),
                    'urls': urls,
                    'metadata': {
                        'average_cloud_cover': sum(
                            item.properties.get('eo:cloud_cover', 0) 
                            for item in season_items
                        ) / len(season_items)
                    }
                }
        
        return seasonal_data
    
    # Example usage
    items_by_year = {
        2022: items_2022,
        2023: items_2023, 
        2024: items_2024
    }
    
    multi_year_results = multi_year_seasonal_download(items_by_year)

.. _url-management:

URL Management Functions
------------------------

is_url_expired
~~~~~~~~~~~~~~

.. py:function:: is_url_expired(url)

   Check if a signed URL has expired (with 30-second safety buffer).

   :param url: URL to check for expiration
   :type url: str
   :returns: True if URL is expired or about to expire
   :rtype: bool

**Basic Expiry Checking**:

.. code-block:: python

    from open_geodata_api.utils import is_url_expired
    
    # Check single URL
    url = item.get_asset_url('B04')
    if is_url_expired(url):
        print("URL has expired and needs re-signing")
        # Re-sign the URL
        fresh_url = item.get_asset_url('B04', auto_sign=True)
    else:
        print("URL is still valid")

**Batch URL Expiry Checking**:

.. code-block:: python

    def check_urls_expiry(items, asset_keys=['B04', 'B03', 'B02']):
        """Check expiry status of multiple URLs."""
        expiry_report = {
            'valid_urls': 0,
            'expired_urls': 0,
            'expired_items': []
        }
        
        for item in items:
            item_expired_assets = []
            
            for asset_key in asset_keys:
                try:
                    url = item.get_asset_url(asset_key)
                    
                    if is_url_expired(url):
                        item_expired_assets.append(asset_key)
                        expiry_report['expired_urls'] += 1
                    else:
                        expiry_report['valid_urls'] += 1
                        
                except Exception as e:
                    print(f"Error checking {item.id}/{asset_key}: {e}")
            
            if item_expired_assets:
                expiry_report['expired_items'].append({
                    'item_id': item.id,
                    'expired_assets': item_expired_assets
                })
        
        return expiry_report
    
    expiry_status = check_urls_expiry(items)
    print(f"Valid URLs: {expiry_status['valid_urls']}")
    print(f"Expired URLs: {expiry_status['expired_urls']}")

**Monitoring URL Expiry**:

.. code-block:: python

    import time
    from datetime import datetime
    
    def monitor_url_expiry(url, check_interval=3):
        """Monitor URL expiry in real-time."""
        print(f"🔍 Monitoring URL expiry every {check_interval} seconds...")
        
        while True:
            expired = is_url_expired(url)
            current_time = datetime.now().strftime("%H:%M:%S")
            
            if expired:
                print(f"🚨 [{current_time}] URL is expired!")
                break
            else:
                # Calculate remaining time (if possible)
                print(f"✅ [{current_time}] URL is still valid")
            
            time.sleep(check_interval)
    
    # Monitor a specific URL
    test_url = "https://example.com/data.tif?se=2024-12-31T23:59:59Z"
    monitor_url_expiry(test_url)

is_signed_url
~~~~~~~~~~~~~

.. py:function:: is_signed_url(url)

   Check if a URL contains signature parameters.

   :param url: URL to check for signatures
   :type url: str
   :returns: True if URL appears to be signed
   :rtype: bool

**URL Signature Detection**:

.. code-block:: python

    from open_geodata_api.utils import is_signed_url
    
    # Test different URL types
    urls_to_test = [
        "https://planetarycomputer.microsoft.com/api/stac/v1/data.tif?se=2024&sig=abc123",  # Signed
        "https://earth-search.aws.element84.com/v1/data.tif",  # Not signed
        "https://example.com/data.tif?token=xyz789",  # Signed (different format)
        "https://simple.com/data.tif"  # Not signed
    ]
    
    for url in urls_to_test:
        signed_status = is_signed_url(url)
        provider = "PC" if "planetarycomputer" in url else "ES" if "earth-search" in url else "Other"
        print(f"{provider:<5} | Signed: {signed_status} | {url[:50]}...")

**Provider-Specific URL Analysis**:

.. code-block:: python

    def analyze_url_signatures(items):
        """Analyze signature patterns across items."""
        signature_analysis = {
            'planetary_computer': {'signed': 0, 'unsigned': 0},
            'earth_search': {'signed': 0, 'unsigned': 0},
            'other': {'signed': 0, 'unsigned': 0}
        }
        
        for item in items:
            # Check common assets
            for asset_key in ['B04', 'B03', 'B02']:
                try:
                    url = item.get_asset_url(asset_key)
                    signed = is_signed_url(url)
                    
                    # Determine provider
                    if "planetarycomputer" in url:
                        provider = 'planetary_computer'
                    elif "earth-search" in url:
                        provider = 'earth_search'
                    else:
                        provider = 'other'
                    
                    # Update counts
                    if signed:
                        signature_analysis[provider]['signed'] += 1
                    else:
                        signature_analysis[provider]['unsigned'] += 1
                        
                except Exception as e:
                    continue
        
        return signature_analysis
    
    signature_report = analyze_url_signatures(items)
    
    for provider, counts in signature_report.items():
        total = counts['signed'] + counts['unsigned']
        if total > 0:
            signed_percent = (counts['signed'] / total) * 100
            print(f"{provider}: {signed_percent:.1f}% signed ({counts['signed']}/{total})")

re_sign_url_if_needed
~~~~~~~~~~~~~~~~~~~~~

.. py:function:: re_sign_url_if_needed(url, provider=None)

   Automatically re-sign expired URLs with warnings.

   :param url: URL to check and potentially re-sign
   :type url: str
   :param provider: Provider hint ('planetary_computer', 'earth_search', or None)
   :type provider: str or None
   :returns: Fresh URL (re-signed if needed)
   :rtype: str

**Automatic URL Refresh**:

.. code-block:: python

    from open_geodata_api.utils import re_sign_url_if_needed
    
    # Automatically handle potentially expired URLs
    potentially_expired_url = item.get_asset_url('B04')
    
    fresh_url = re_sign_url_if_needed(
        potentially_expired_url,
        provider="planetary_computer"
    )
    
    # Use fresh URL for data access
    import rioxarray
    data = rioxarray.open_rasterio(fresh_url)

**Bulk URL Refresh Workflow**:

.. code-block:: python

    def refresh_expired_urls(items, asset_keys=['B04', 'B03', 'B02']):
        """Refresh all expired URLs in a collection."""
        refreshed_urls = {}
        refresh_stats = {'refreshed': 0, 'already_valid': 0, 'failed': 0}
        
        for item in items:
            item_urls = {}
            
            for asset_key in asset_keys:
                try:
                    original_url = item.get_asset_url(asset_key)
                    
                    # Determine provider from URL or item metadata
                    provider = None
                    if "planetarycomputer" in original_url:
                        provider = "planetary_computer"
                    elif "earth-search" in original_url:
                        provider = "earth_search"
                    
                    # Refresh if needed
                    fresh_url = re_sign_url_if_needed(original_url, provider)
                    
                    if fresh_url != original_url:
                        refresh_stats['refreshed'] += 1
                        print(f"🔄 Refreshed {item.id}/{asset_key}")
                    else:
                        refresh_stats['already_valid'] += 1
                    
                    item_urls[asset_key] = fresh_url
                    
                except Exception as e:
                    refresh_stats['failed'] += 1
                    print(f"❌ Failed to refresh {item.id}/{asset_key}: {e}")
                    item_urls[asset_key] = None
            
            refreshed_urls[item.id] = item_urls
        
        print(f"\n📊 URL Refresh Summary:")
        print(f"   Refreshed: {refresh_stats['refreshed']}")
        print(f"   Already valid: {refresh_stats['already_valid']}")
        print(f"   Failed: {refresh_stats['failed']}")
        
        return refreshed_urls, refresh_stats
    
    refreshed_urls, stats = refresh_expired_urls(items)

**Production URL Management**:

.. code-block:: python

    def production_url_manager(items, cache_duration_hours=6):
        """Production-grade URL management with caching."""
        import pickle
        import time
        from pathlib import Path
        
        cache_file = Path("url_cache.pkl")
        url_cache = {}
        
        # Load existing cache
        if cache_file.exists():
            try:
                with open(cache_file, 'rb') as f:
                    cached_data = pickle.load(f)
                    
                # Check cache validity
                cache_age = time.time() - cached_data.get('timestamp', 0)
                if cache_age < cache_duration_hours * 3600:
                    url_cache = cached_data.get('urls', {})
                    print(f"📂 Loaded {len(url_cache)} URLs from cache")
            except Exception as e:
                print(f"⚠️ Cache load failed: {e}")
        
        # Process items
        fresh_urls = {}
        
        for item in items:
            item_id = item.id
            
            # Check cache first
            if item_id in url_cache:
                cached_item = url_cache[item_id]
                
                # Validate cached URLs
                all_valid = True
                for asset_key, cached_url in cached_item.items():
                    if is_url_expired(cached_url):
                        all_valid = False
                        break
                
                if all_valid:
                    fresh_urls[item_id] = cached_item
                    continue
            
            # Generate fresh URLs
            item_urls = {}
            for asset_key in ['B04', 'B03', 'B02']:
                try:
                    url = item.get_asset_url(asset_key)
                    fresh_url = re_sign_url_if_needed(url)
                    item_urls[asset_key] = fresh_url
                except Exception as e:
                    print(f"❌ Failed to get URL for {item_id}/{asset_key}: {e}")
            
            fresh_urls[item_id] = item_urls
        
        # Update cache
        cache_data = {
            'timestamp': time.time(),
            'urls': fresh_urls
        }
        
        try:
            with open(cache_file, 'wb') as f:
                pickle.dump(cache_data, f)
            print(f"💾 Saved {len(fresh_urls)} URLs to cache")
        except Exception as e:
            print(f"⚠️ Cache save failed: {e}")
        
        return fresh_urls
    
    managed_urls = production_url_manager(items)

validate_urls
~~~~~~~~~~~~~

.. py:function:: validate_urls(urls_dict, check_expiry=True, check_access=False)

   Validate a collection of URLs for accessibility and expiration.

   :param urls_dict: Dictionary of URLs to validate
   :type urls_dict: dict
   :param check_expiry: Whether to check URL expiration
   :type check_expiry: bool
   :param check_access: Whether to test HTTP accessibility
   :type check_access: bool
   :returns: Validation results with detailed status
   :rtype: dict

**Comprehensive URL Validation**:

.. code-block:: python

    from open_geodata_api.utils import validate_urls
    
    # Prepare URLs for validation
    urls_to_validate = {
        'item1': {
            'B04': 'https://example.com/item1_B04.tif',
            'B03': 'https://example.com/item1_B03.tif',
            'B02': 'https://example.com/item1_B02.tif'
        },
        'item2': {
            'B04': 'https://example.com/item2_B04.tif',
            'B03': 'https://example.com/item2_B03.tif',
            'B02': 'https://example.com/item2_B02.tif'
        }
    }
    
    # Basic validation (expiry only)
    basic_validation = validate_urls(
        urls_to_validate,
        check_expiry=True,
        check_access=False  # Skip HTTP checks for speed
    )
    
    print(f"Valid URLs: {basic_validation['valid_count']}")
    print(f"Expired URLs: {basic_validation['expired_count']}")
    print(f"Total URLs: {basic_validation['total_count']}")

**Full Validation with Access Testing**:

.. code-block:: python

    # Comprehensive validation (slower but thorough)
    full_validation = validate_urls(
        urls_to_validate,
        check_expiry=True,
        check_access=True,  # Test HTTP accessibility
        timeout=30,         # Request timeout
        verify_ssl=True     # SSL verification
    )
    
    print(f"\n📊 Full Validation Results:")
    print(f"   Total URLs: {full_validation['total_count']}")
    print(f"   Valid & Accessible: {full_validation['accessible_count']}")
    print(f"   Expired: {full_validation['expired_count']}")
    print(f"   Inaccessible: {full_validation['inaccessible_count']}")
    print(f"   Validation Success Rate: {full_validation['success_rate']:.1f}%")
    
    # Show detailed failures
    if full_validation['failed_urls']:
        print(f"\n❌ Failed URLs:")
        for failed_url, error in full_validation['failed_urls'].items():
            print(f"   {failed_url}: {error}")

**Production URL Validation Workflow**:

.. code-block:: python

    def production_url_validation(items, validation_level="basic"):
        """Production-grade URL validation workflow."""
        
        # Extract URLs from items
        urls_dict = {}
        for item in items:
            item_urls = {}
            for asset_key in ['B04', 'B03', 'B02']:
                try:
                    url = item.get_asset_url(asset_key)
                    item_urls[asset_key] = url
                except Exception as e:
                    print(f"⚠️ Could not get URL for {item.id}/{asset_key}: {e}")
            
            if item_urls:
                urls_dict[item.id] = item_urls
        
        print(f"🔍 Validating {len(urls_dict)} items...")
        
        # Choose validation parameters based on level
        if validation_level == "basic":
            validation_params = {
                'check_expiry': True,
                'check_access': False
            }
        elif validation_level == "thorough":
            validation_params = {
                'check_expiry': True,
                'check_access': True,
                'timeout': 30
            }
        else:  # "fast"
            validation_params = {
                'check_expiry': False,
                'check_access': False
            }
        
        # Run validation
        validation_results = validate_urls(urls_dict, **validation_params)
        
        # Generate report
        report = {
            'validation_level': validation_level,
            'total_items': len(urls_dict),
            'total_urls': validation_results['total_count'],
            'valid_urls': validation_results['valid_count'],
            'success_rate': validation_results['success_rate'],
            'recommendations': []
        }
        
        # Add recommendations based on results
        if validation_results['expired_count'] > 0:
            report['recommendations'].append(
                f"🔄 {validation_results['expired_count']} URLs need re-signing"
            )
        
        if validation_level == "thorough" and validation_results.get('inaccessible_count', 0) > 0:
            report['recommendations'].append(
                f"❌ {validation_results['inaccessible_count']} URLs are inaccessible"
            )
        
        if validation_results['success_rate'] < 90:
            report['recommendations'].append(
                "⚠️ Success rate below 90% - investigate URL issues"
            )
        
        return validation_results, report
    
    # Run production validation
    validation_results, report = production_url_validation(items, "thorough")
    
    print(f"\n📋 Validation Report:")
    print(f"   Level: {report['validation_level']}")
    print(f"   Items: {report['total_items']}")
    print(f"   URLs: {report['total_urls']}")
    print(f"   Success Rate: {report['success_rate']:.1f}%")
    
    if report['recommendations']:
        print(f"\n💡 Recommendations:")
        for rec in report['recommendations']:
            print(f"   {rec}")

.. _data-processing:

Data Processing Functions
-------------------------

create_download_summary
~~~~~~~~~~~~~~~~~~~~~~~~

.. py:function:: create_download_summary(download_results, output_file=None)

   Generate comprehensive download statistics and reports.

   :param download_results: Results from download operations
   :type download_results: dict
   :param output_file: Optional file to save summary
   :type output_file: str or Path or None
   :returns: Summary statistics
   :rtype: dict

**Basic Download Summary**:

.. code-block:: python

    from open_geodata_api.utils import create_download_summary
    
    # After downloading data
    download_results = download_items(
        items, 
        base_destination="./satellite_data/",
        asset_keys=['B08', 'B04', 'B03', 'B02']
    )
    
    # Create summary report
    summary = create_download_summary(
        download_results,
        output_file="download_report.json"
    )
    
    print(f"📊 Download Summary:")
    print(f"   Successfully downloaded: {summary['successful_downloads']}/{summary['total_files']} files")
    print(f"   Success rate: {summary['success_rate']:.1f}%")
    print(f"   Total size: {summary['total_size_gb']:.2f} GB")
    print(f"   Average file size: {summary['avg_file_size_mb']:.1f} MB")

**Detailed Download Analysis**:

.. code-block:: python

    def detailed_download_analysis(download_results):
        """Create detailed analysis of download results."""
        
        summary = create_download_summary(download_results)
        
        # Enhanced analysis
        analysis = {
            'basic_stats': summary,
            'asset_breakdown': {},
            'size_distribution': {},
            'failure_analysis': {},
            'performance_metrics': {}
        }
        
        # Analyze by asset type
        asset_stats = {}
        for item_id, item_results in download_results.items():
            for asset_key, result in item_results.items():
                if asset_key not in asset_stats:
                    asset_stats[asset_key] = {'success': 0, 'failed': 0, 'total_size': 0}
                
                if result.get('success', False):
                    asset_stats[asset_key]['success'] += 1
                    asset_stats[asset_key]['total_size'] += result.get('size_bytes', 0)
                else:
                    asset_stats[asset_key]['failed'] += 1
        
        analysis['asset_breakdown'] = asset_stats
        
        # Size distribution analysis
        file_sizes = []
        for item_results in download_results.values():
            for result in item_results.values():
                if result.get('success', False) and 'size_bytes' in result:
                    file_sizes.append(result['size_bytes'] / (1024*1024))  # MB
        
        if file_sizes:
            analysis['size_distribution'] = {
                'min_mb': min(file_sizes),
                'max_mb': max(file_sizes),
                'median_mb': sorted(file_sizes)[len(file_sizes)//2],
                'std_mb': (sum((x - sum(file_sizes)/len(file_sizes))**2 for x in file_sizes) / len(file_sizes))**0.5
            }
        
        return analysis
    
    detailed_analysis = detailed_download_analysis(download_results)

**Multi-Session Download Tracking**:

.. code-block:: python

    import json
    from datetime import datetime
    import os
    
    def track_download_sessions(download_results, session_name=None):
        """Track multiple download sessions for long-term analysis."""
        
        if session_name is None:
            session_name = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # Load existing tracking data
        tracking_file = "download_tracking.json"
        tracking_data = {}
        
        if os.path.exists(tracking_file):
            try:
                with open(tracking_file, 'r') as f:
                    tracking_data = json.load(f)
            except Exception as e:
                print(f"⚠️ Could not load tracking data: {e}")
        
        # Create summary for this session
        session_summary = create_download_summary(download_results)
        session_summary['session_name'] = session_name
        session_summary['timestamp'] = datetime.now().isoformat()
        
        # Add to tracking data
        tracking_data[session_name] = session_summary
        
        # Save updated tracking data
        try:
            with open(tracking_file, 'w') as f:
                json.dump(tracking_data, f, indent=2)
            print(f"📊 Session {session_name} saved to tracking")
        except Exception as e:
            print(f"⚠️ Could not save tracking data: {e}")
        
        # Generate multi-session analysis
        if len(tracking_data) > 1:
            multi_session_analysis = {
                'total_sessions': len(tracking_data),
                'total_files_all_sessions': sum(s['total_files'] for s in tracking_data.values()),
                'total_size_gb_all_sessions': sum(s.get('total_size_gb', 0) for s in tracking_data.values()),
                'average_success_rate': sum(s['success_rate'] for s in tracking_data.values()) / len(tracking_data),
                'sessions': list(tracking_data.keys())
            }
            
            print(f"\n📈 Multi-Session Summary:")
            print(f"   Total sessions: {multi_session_analysis['total_sessions']}")
            print(f"   Total files: {multi_session_analysis['total_files_all_sessions']}")
            print(f"   Total size: {multi_session_analysis['total_size_gb_all_sessions']:.2f} GB")
            print(f"   Average success rate: {multi_session_analysis['average_success_rate']:.1f}%")
            
            return session_summary, multi_session_analysis
        
        return session_summary, None
    
    # Track this download session
    session_summary, multi_session = track_download_sessions(
        download_results, 
        session_name="vegetation_analysis_2024"
    )

export_urls_to_json
~~~~~~~~~~~~~~~~~~~

.. py:function:: export_urls_to_json(items, output_file, asset_keys=None, signed=True, **kwargs)

   Export asset URLs to JSON file for external processing.

   :param items: STAC items to export URLs from
   :type items: STACItemCollection
   :param output_file: Output JSON file path
   :type output_file: str or Path
   :param asset_keys: Specific assets to export
   :type asset_keys: list of str or None
   :param signed: Whether to use signed URLs
   :type signed: bool
   :returns: Export metadata
   :rtype: dict

**Basic URL Export**:

.. code-block:: python

    from open_geodata_api.utils import export_urls_to_json
    
    # Export RGB URLs for external processing
    export_metadata = export_urls_to_json(
        items,
        output_file="rgb_urls.json",
        asset_keys=['B04', 'B03', 'B02'],
        signed=True
    )
    
    print(f"📤 Exported {export_metadata['total_urls']} URLs")
    print(f"   Items: {export_metadata['total_items']}")
    print(f"   Assets per item: {export_metadata['assets_per_item']}")
    print(f"   Output file: {export_metadata['output_file']}")

**Advanced Export with Metadata**:

.. code-block:: python

    # Export with comprehensive metadata
    comprehensive_export = export_urls_to_json(
        items,
        output_file="comprehensive_export.json",
        asset_keys=['B08', 'B04', 'B03', 'B02'],
        signed=True,
        include_metadata=True,     # Include item metadata
        include_geometry=True,     # Include item geometries
        include_properties=True,   # Include all properties
        organize_by_date=True,     # Group by acquisition date
        validate_urls=True         # Validate URLs before export
    )

**Organized Export Workflows**:

.. code-block:: python

    def organized_url_export(items, base_filename="urls_export"):
        """Export URLs organized by different criteria."""
        
        exports = {}
        
        # 1. Export by asset type
        asset_groups = {
            'rgb': ['B04', 'B03', 'B02'],
            'nir': ['B08'],
            'swir': ['B11', 'B12'],
            'analysis': ['B08', 'B04', 'B11', 'B12']
        }
        
        for group_name, asset_list in asset_groups.items():
            filename = f"{base_filename}_{group_name}.json"
            
            export_metadata = export_urls_to_json(
                items,
                output_file=filename,
                asset_keys=asset_list,
                signed=True,
                include_metadata=True
            )
            
            exports[group_name] = export_metadata
            print(f"📤 {group_name.upper()}: {export_metadata['total_urls']} URLs exported")
        
        # 2. Export by time period
        time_periods = {
            'recent': filter_by_date_range(items, '2024-06-01', None),
            'spring': filter_by_date_range(items, '2024-03-01', '2024-05-31'),
            'summer': filter_by_date_range(items, '2024-06-01', '2024-08-31')
        }
        
        for period_name, period_items in time_periods.items():
            if len(period_items) > 0:
                filename = f"{base_filename}_{period_name}.json"
                
                export_metadata = export_urls_to_json(
                    period_items,
                    output_file=filename,
                    asset_keys=['B08', 'B04', 'B03'],
                    signed=True
                )
                
                exports[f"time_{period_name}"] = export_metadata
                print(f"📅 {period_name.title()}: {export_metadata['total_urls']} URLs exported")
        
        return exports
    
    all_exports = organized_url_export(items)

**External Processing Integration**:

.. code-block:: python

    def export_for_external_tools(items, output_dir="./exports/"):
        """Export URLs formatted for different external tools."""
        
        os.makedirs(output_dir, exist_ok=True)
        
        # 1. Export for GDAL/rasterio batch processing
        gdal_export = export_urls_to_json(
            items,
            output_file=os.path.join(output_dir, "gdal_urls.json"),
            asset_keys=['B04', 'B03', 'B02'],
            format='gdal_compatible',
            include_vrt=True  # Generate VRT files
        )
        
        # 2. Export for R processing
        r_export = export_urls_to_json(
            items,
            output_file=os.path.join(output_dir, "r_urls.json"),
            asset_keys=['B08', 'B04'],
            format='r_compatible',
            include_metadata=True
        )
        
        # 3. Export for cloud processing (CSV format)
        csv_export = export_urls_to_json(
            items,
            output_file=os.path.join(output_dir, "cloud_urls.csv"),
            asset_keys=['B08', 'B04', 'B03', 'B02'],
            format='csv',
            include_coordinates=True,
            include_date=True
        )
        
        # 4. Export for machine learning workflows
        ml_export = export_urls_to_json(
            items,
            output_file=os.path.join(output_dir, "ml_dataset.json"),
            asset_keys=['B08', 'B04', 'B03', 'B02'],
            format='ml_ready',
            normalize_metadata=True,
            include_labels=True
        )
        
        export_summary = {
            'gdal_processing': gdal_export,
            'r_analysis': r_export,
            'cloud_processing': csv_export,
            'ml_workflow': ml_export
        }
        
        return export_summary
    
    external_exports = export_for_external_tools(items)

.. _batch-processing:

Batch Processing Functions
--------------------------

process_items_in_batches
~~~~~~~~~~~~~~~~~~~~~~~~

.. py:function:: process_items_in_batches(items, batch_size=10, process_func=None, **kwargs)

   Process large collections of items in memory-efficient batches.

   :param items: Items to process
   :type items: STACItemCollection or list
   :param batch_size: Number of items per batch
   :type batch_size: int
   :param process_func: Function to apply to each batch
   :type process_func: callable or None
   :returns: Generator yielding batch results
   :rtype: generator

**Basic Batch Processing**:

.. code-block:: python

    from open_geodata_api.utils import process_items_in_batches
    
    def download_batch(batch_items):
        """Process a single batch of items."""
        return download_items(
            batch_items, 
            "./batch_data/",
            asset_keys=['B04', 'B03', 'B02']
        )
    
    # Process large dataset in batches
    total_processed = 0
    
    for batch_num, batch_result in enumerate(process_items_in_batches(
        large_items_collection,
        batch_size=5,
        process_func=download_batch
    ), 1):
        
        batch_size = len(batch_result)
        total_processed += batch_size
        
        print(f"✅ Batch {batch_num}: {batch_size} items processed")
        print(f"   Total processed: {total_processed}")
        
        # Optional cleanup between batches
        import gc
        gc.collect()

**Memory-Efficient Large Dataset Processing**:

.. code-block:: python

    def memory_efficient_processing(items, total_memory_limit_gb=8):
        """Process items with memory constraints."""
        
        # Estimate memory usage per item (rough estimate)
        estimated_memory_per_item_mb = 50  # Depends on data type
        max_batch_size = int((total_memory_limit_gb * 1024) / estimated_memory_per_item_mb)
        
        # Ensure reasonable batch size
        batch_size = max(1, min(max_batch_size, 20))
        
        print(f"🧠 Processing {len(items)} items in batches of {batch_size}")
        print(f"   Estimated memory limit: {total_memory_limit_gb} GB")
        
        def memory_aware_processing(batch_items):
            """Process batch with memory monitoring."""
            import psutil
            import os
            
            # Monitor memory before processing
            process = psutil.Process(os.getpid())
            memory_before = process.memory_info().rss / (1024*1024*1024)  # GB
            
            # Process the batch
            results = download_items(
                batch_items,
                "./memory_efficient/",
                asset_keys=['B04', 'B03'],
                create_product_folders=True
            )
            
            # Monitor memory after processing
            memory_after = process.memory_info().rss / (1024*1024*1024)  # GB
            memory_used = memory_after - memory_before
            
            return {
                'download_results': results,
                'memory_used_gb': memory_used,
                'memory_before_gb': memory_before,
                'memory_after_gb': memory_after
            }
        
        # Process in batches with memory monitoring
        all_results = []
        memory_stats = []
        
        for batch_result in process_items_in_batches(
            items,
            batch_size=batch_size,
            process_func=memory_aware_processing
        ):
            all_results.append(batch_result['download_results'])
            memory_stats.append({
                'memory_used': batch_result['memory_used_gb'],
                'memory_peak': batch_result['memory_after_gb']
            })
            
            # Force garbage collection
            import gc
            gc.collect()
        
        # Analyze memory usage
        avg_memory_per_batch = sum(s['memory_used'] for s in memory_stats) / len(memory_stats)
        peak_memory = max(s['memory_peak'] for s in memory_stats)
        
        print(f"\n🧠 Memory Usage Analysis:")
        print(f"   Average per batch: {avg_memory_per_batch:.2f} GB")
        print(f"   Peak memory: {peak_memory:.2f} GB")
        print(f"   Memory efficiency: {len(items) / peak_memory:.1f} items/GB")
        
        return all_results, memory_stats
    
    results, memory_analysis = memory_efficient_processing(large_items_collection)

**Parallel Batch Processing**:

.. code-block:: python

    from concurrent.futures import ProcessPoolExecutor, as_completed
    import multiprocessing
    
    def parallel_batch_processing(items, max_workers=None):
        """Process batches in parallel for maximum throughput."""
        
        if max_workers is None:
            max_workers = min(4, multiprocessing.cpu_count())
        
        print(f"🚀 Parallel processing with {max_workers} workers")
        
        def process_batch_parallel(batch_items_data):
            """Process a batch in a separate process."""
            # Recreate STACItemCollection in the worker process
            from open_geodata_api.core.collections import STACItemCollection
            
            batch_collection = STACItemCollection(
                batch_items_data['items'],
                provider=batch_items_data['provider']
            )
            
            # Process the batch
            results = download_items(
                batch_collection,
                f"./parallel_batch_{batch_items_data['batch_id']}/",
                asset_keys=['B04', 'B03', 'B02']
            )
            
            return {
                'batch_id': batch_items_data['batch_id'],
                'results': results,
                'items_processed': len(batch_items_data['items'])
            }
        
        # Prepare batches for parallel processing
        batch_size = 5
        batches = []
        
        for i in range(0, len(items), batch_size):
            batch_items = items[i:i + batch_size]
            
            # Prepare batch data for serialization
            batch_data = {
                'batch_id': i // batch_size,
                'items': [item.to_dict() for item in batch_items],
                'provider': items.provider if hasattr(items, 'provider') else 'unknown'
            }
            
            batches.append(batch_data)
        
        # Process batches in parallel
        all_results = {}
        
        with ProcessPoolExecutor(max_workers=max_workers) as executor:
            # Submit all batches
            future_to_batch = {
                executor.submit(process_batch_parallel, batch_data): batch_data['batch_id']
                for batch_data in batches
            }
            
            # Collect results as they complete
            for future in as_completed(future_to_batch):
                batch_id = future_to_batch[future]
                
                try:
                    result = future.result()
                    all_results[batch_id] = result
                    
                    print(f"✅ Batch {batch_id}: {result['items_processed']} items completed")
                    
                except Exception as e:
                    print(f"❌ Batch {batch_id} failed: {e}")
                    all_results[batch_id] = {'error': str(e)}
        
        # Summarize parallel processing results
        successful_batches = sum(1 for r in all_results.values() if 'error' not in r)
        total_items_processed = sum(
            r.get('items_processed', 0) for r in all_results.values() 
            if 'error' not in r
        )
        
        print(f"\n🚀 Parallel Processing Summary:")
        print(f"   Successful batches: {successful_batches}/{len(batches)}")
        print(f"   Total items processed: {total_items_processed}")
        print(f"   Workers used: {max_workers}")
        
        return all_results
    
    parallel_results = parallel_batch_processing(large_items_collection)

parallel_download
~~~~~~~~~~~~~~~~~

.. py:function:: parallel_download(urls_dict, destination, max_workers=4, **kwargs)

   Download multiple URLs in parallel with progress tracking.

   :param urls_dict: Dictionary of URLs to download
   :type urls_dict: dict
   :param destination: Base destination directory
   :type destination: str or Path
   :param max_workers: Maximum number of parallel workers
   :type max_workers: int
   :returns: Download results with success/failure status
   :rtype: dict

**Basic Parallel Download**:

.. code-block:: python

    from open_geodata_api.utils import parallel_download
    
    # Prepare URLs for parallel download
    urls = {
        'red_band': 'https://example.com/B04.tif',
        'green_band': 'https://example.com/B03.tif',
        'blue_band': 'https://example.com/B02.tif',
        'nir_band': 'https://example.com/B08.tif'
    }
    
    # Download in parallel
    parallel_results = parallel_download(
        urls,
        destination="./parallel_data/",
        max_workers=4,
        show_progress=True
    )
    
    # Analyze results
    successful = sum(1 for r in parallel_results.values() if r.get('success'))
    total = len(parallel_results)
    
    print(f"📥 Parallel Download Results:")
    print(f"   Successful: {successful}/{total}")
    print(f"   Success rate: {successful/total*100:.1f}%")

**Advanced Parallel Download Configuration**:

.. code-block:: python

    # High-performance parallel download
    high_perf_results = parallel_download(
        urls,
        destination="./high_performance/",
        max_workers=8,              # More workers
        chunk_size=32768,           # Larger chunks (32KB)
        timeout=300,                # 5-minute timeout
        retries=3,                  # Retry failed downloads
        verify_ssl=True,            # SSL verification
        show_progress=True,         # Progress tracking
        preserve_timestamps=True,   # Preserve file timestamps
        compression='gzip',         # Accept compressed downloads
        headers={                   # Custom headers
            'User-Agent': 'HighPerformanceDownloader/1.0',
            'Accept-Encoding': 'gzip, deflate'
        }
    )

**Smart Parallel Download with Load Balancing**:

.. code-block:: python

    def smart_parallel_download(urls_dict, base_destination="./smart_parallel/"):
        """Intelligent parallel download with load balancing."""
        
        # Analyze URLs to optimize worker allocation
        url_analysis = {}
        
        for name, url in urls_dict.items():
            # Estimate file size and server characteristics
            if "planetarycomputer" in url:
                estimated_size = "large"
                server_type = "high_capacity"
            elif "earth-search" in url:
                estimated_size = "medium"
                server_type = "medium_capacity"
            else:
                estimated_size = "unknown"
                server_type = "unknown"
            
            url_analysis[name] = {
                'url': url,
                'estimated_size': estimated_size,
                'server_type': server_type
            }
        
        # Group URLs by server characteristics
        server_groups = {}
        for name, analysis in url_analysis.items():
            server_type = analysis['server_type']
            if server_type not in server_groups:
                server_groups[server_type] = []
            server_groups[server_type].append((name, analysis['url']))
        
        # Download each group with optimized settings
        all_results = {}
        
        for server_type, group_urls in server_groups.items():
            print(f"🔄 Processing {server_type} group: {len(group_urls)} URLs")
            
            # Optimize settings per server type
            if server_type == "high_capacity":
                workers = 6
                chunk_size = 32768
                timeout = 180
            elif server_type == "medium_capacity":
                workers = 4
                chunk_size = 16384
                timeout = 120
            else:
                workers = 2
                chunk_size = 8192
                timeout = 60
            
            # Convert to dict format
            group_dict = dict(group_urls)
            
            # Download this group
            group_results = parallel_download(
                group_dict,
                destination=os.path.join(base_destination, server_type),
                max_workers=workers,
                chunk_size=chunk_size,
                timeout=timeout,
                show_progress=True
            )
            
            all_results.update(group_results)
        
        return all_results
    
    smart_results = smart_parallel_download(urls)

**Robust Parallel Download with Error Recovery**:

.. code-block:: python

    def robust_parallel_download(urls_dict, destination, max_retries=3):
        """Parallel download with comprehensive error recovery."""
        
        results = {}
        failed_urls = {}
        
        # Initial parallel download attempt
        print("🚀 Starting initial parallel download...")
        
        initial_results = parallel_download(
            urls_dict,
            destination=destination,
            max_workers=4,
            timeout=120,
            show_progress=True
        )
        
        # Analyze initial results
        for url_name, result in initial_results.items():
            if result.get('success', False):
                results[url_name] = result
            else:
                failed_urls[url_name] = {
                    'url': urls_dict[url_name],
                    'error': result.get('error', 'Unknown error'),
                    'attempts': 1
                }
        
        # Retry failed downloads with different strategies
        for retry_attempt in range(max_retries):
            if not failed_urls:
                break
                
            print(f"🔄 Retry attempt {retry_attempt + 1}: {len(failed_urls)} failed URLs")
            
            # Adjust parameters for retry
            retry_workers = max(1, 4 - retry_attempt)  # Reduce workers each retry
            retry_timeout = 60 * (retry_attempt + 2)    # Increase timeout each retry
            
            retry_urls = {name: info['url'] for name, info in failed_urls.items()}
            
            retry_results = parallel_download(
                retry_urls,
                destination=destination,
                max_workers=retry_workers,
                timeout=retry_timeout,
                chunk_size=8192,  # Smaller chunks for reliability
                show_progress=True
            )
            
            # Update results
            new_failed = {}
            
            for url_name, result in retry_results.items():
                if result.get('success', False):
                    results[url_name] = result
                    print(f"✅ Recovered: {url_name}")
                else:
                    failed_urls[url_name]['attempts'] += 1
                    failed_urls[url_name]['error'] = result.get('error', 'Unknown error')
                    new_failed[url_name] = failed_urls[url_name]
            
            failed_urls = new_failed
        
        # Final summary
        successful_count = len(results)
        failed_count = len(failed_urls)
        total_count = successful_count + failed_count
        
        print(f"\n📊 Robust Download Summary:")
        print(f"   Successful: {successful_count}/{total_count}")
        print(f"   Failed: {failed_count}/{total_count}")
        print(f"   Success rate: {successful_count/total_count*100:.1f}%")
        
        if failed_urls:
            print(f"\n❌ Persistently failed URLs:")
            for name, info in failed_urls.items():
                print(f"   {name}: {info['error']} (after {info['attempts']} attempts)")
        
        return {
            'successful': results,
            'failed': failed_urls,
            'summary': {
                'total': total_count,
                'successful': successful_count,
                'failed': failed_count,
                'success_rate': successful_count/total_count*100
            }
        }
    
    robust_results = robust_parallel_download(urls, "./robust_downloads/")

.. _analysis-helpers:

Analysis Helper Functions
-------------------------

calculate_ndvi
~~~~~~~~~~~~~~

.. py:function:: calculate_ndvi(nir_url, red_url, output_path=None)

   Calculate NDVI from NIR and Red band URLs.

   :param nir_url: URL to Near-Infrared band
   :type nir_url: str
   :param red_url: URL to Red band
   :type red_url: str
   :param output_path: Optional path to save NDVI result
   :type output_path: str or Path or None
   :returns: NDVI data array
   :rtype: xarray.DataArray

**Basic NDVI Calculation**:

.. code-block:: python

    from open_geodata_api.utils import calculate_ndvi
    
    # Get band URLs from a STAC item
    item = items[0]  # First item from your collection
    band_urls = item.get_asset_urls(['B08', 'B04'])  # NIR, Red
    
    # Calculate NDVI
    ndvi = calculate_ndvi(
        nir_url=band_urls['B08'],
        red_url=band_urls['B04'],
        output_path="./ndvi_result.tif"
    )
    
    print(f"📊 NDVI Statistics:")
    print(f"   Mean NDVI: {ndvi.mean().values:.3f}")
    print(f"   Std NDVI: {ndvi.std().values:.3f}")
    print(f"   Min NDVI: {ndvi.min().values:.3f}")
    print(f"   Max NDVI: {ndvi.max().values:.3f}")

**Batch NDVI Calculation**:

.. code-block:: python

    def batch_ndvi_calculation(items, output_dir="./ndvi_results/"):
        """Calculate NDVI for multiple items."""
        
        os.makedirs(output_dir, exist_ok=True)
        ndvi_results = {}
        
        for i, item in enumerate(items):
            try:
                print(f"🌱 Processing NDVI {i+1}/{len(items)}: {item.id}")
                
                # Get band URLs
                band_urls = item.get_asset_urls(['B08', 'B04'])
                
                # Calculate NDVI
                output_file = os.path.join(output_dir, f"{item.id}_ndvi.tif")
                
                ndvi = calculate_ndvi(
                    nir_url=band_urls['B08'],
                    red_url=band_urls['B04'],
                    output_path=output_file
                )
                
                # Calculate statistics
                ndvi_stats = {
                    'mean': float(ndvi.mean().values),
                    'std': float(ndvi.std().values),
                    'min': float(ndvi.min().values),
                    'max': float(ndvi.max().values),
                    'file_path': output_file,
                    'date': item.properties.get('datetime', '')[:10]
                }
                
                ndvi_results[item.id] = ndvi_stats
                
                print(f"   ✅ Mean NDVI: {ndvi_stats['mean']:.3f}")
                
            except Exception as e:
                print(f"   ❌ Failed: {e}")
                ndvi_results[item.id] = {'error': str(e)}
        
        return ndvi_results
    
    # Calculate NDVI for all items
    all_ndvi_results = batch_ndvi_calculation(items)

**Advanced NDVI Analysis Workflow**:

.. code-block:: python

    def advanced_ndvi_analysis(items, analysis_name="vegetation_study"):
        """Comprehensive NDVI analysis with temporal tracking."""
        
        import pandas as pd
        import matplotlib.pyplot as plt
        
        analysis_dir = f"./ndvi_analysis_{analysis_name}/"
        os.makedirs(analysis_dir, exist_ok=True)
        
        # Calculate NDVI for all items
        ndvi_data = []
        
        for item in items:
            try:
                # Get metadata
                date = item.properties.get('datetime', '')[:10]
                cloud_cover = item.properties.get('eo:cloud_cover', 0)
                
                # Skip very cloudy images
                if cloud_cover > 30:
                    continue
                
                # Calculate NDVI
                band_urls = item.get_asset_urls(['B08', 'B04'])
                
                ndvi = calculate_ndvi(
                    nir_url=band_urls['B08'],
                    red_url=band_urls['B04'],
                    output_path=os.path.join(analysis_dir, f"{item.id}_ndvi.tif")
                )
                
                # Calculate comprehensive statistics
                ndvi_stats = {
                    'item_id': item.id,
                    'date': date,
                    'cloud_cover': cloud_cover,
                    'ndvi_mean': float(ndvi.mean().values),
                    'ndvi_std': float(ndvi.std().values),
                    'ndvi_min': float(ndvi.min().values),
                    'ndvi_max': float(ndvi.max().values),
                    'ndvi_median': float(ndvi.median().values),
                    'vegetation_fraction': float((ndvi > 0.3).sum() / ndvi.size),  # % with NDVI > 0.3
                    'healthy_vegetation': float((ndvi > 0.6).sum() / ndvi.size)    # % with NDVI > 0.6
                }
                
                ndvi_data.append(ndvi_stats)
                
            except Exception as e:
                print(f"⚠️ Failed to process {item.id}: {e}")
        
        # Create DataFrame for analysis
        df = pd.DataFrame(ndvi_data)
        
        if len(df) > 0:
            # Sort by date
            df['date'] = pd.to_datetime(df['date'])
            df = df.sort_values('date')
            
            # Save detailed results
            csv_path = os.path.join(analysis_dir, "ndvi_time_series.csv")
            df.to_csv(csv_path, index=False)
            
            # Generate temporal analysis plots
            plt.figure(figsize=(15, 10))
            
            # Plot 1: NDVI over time
            plt.subplot(2, 2, 1)
            plt.plot(df['date'], df['ndvi_mean'], 'g-o', label='Mean NDVI')
            plt.fill_between(df['date'], 
                           df['ndvi_mean'] - df['ndvi_std'],
                           df['ndvi_mean'] + df['ndvi_std'], 
                           alpha=0.3, color='green')
            plt.title('NDVI Time Series')
            plt.xlabel('Date')
            plt.ylabel('NDVI')
            plt.legend()
            plt.xticks(rotation=45)
            
            # Plot 2: Vegetation fractions
            plt.subplot(2, 2, 2)
            plt.plot(df['date'], df['vegetation_fraction'], 'b-o', label='Vegetation (>0.3)')
            plt.plot(df['date'], df['healthy_vegetation'], 'darkgreen', label='Healthy Veg (>0.6)')
            plt.title('Vegetation Coverage')
            plt.xlabel('Date')
            plt.ylabel('Fraction')
            plt.legend()
            plt.xticks(rotation=45)
            
            # Plot 3: Cloud cover vs NDVI
            plt.subplot(2, 2, 3)
            plt.scatter(df['cloud_cover'], df['ndvi_mean'], alpha=0.6)
            plt.xlabel('Cloud Cover (%)')
            plt.ylabel('Mean NDVI')
            plt.title('Cloud Cover vs NDVI')
            
            # Plot 4: NDVI distribution
            plt.subplot(2, 2, 4)
            plt.hist(df['ndvi_mean'], bins=20, alpha=0.7, color='green')
            plt.xlabel('Mean NDVI')
            plt.ylabel('Frequency')
            plt.title('NDVI Distribution')
            
            plt.tight_layout()
            plt.savefig(os.path.join(analysis_dir, 'ndvi_analysis.png'), dpi=300, bbox_inches='tight')
            plt.close()
            
            # Generate summary report
            summary = {
                'analysis_name': analysis_name,
                'total_scenes': len(df),
                'date_range': f"{df['date'].min().strftime('%Y-%m-%d')} to {df['date'].max().strftime('%Y-%m-%d')}",
                'average_ndvi': df['ndvi_mean'].mean(),
                'ndvi_trend': 'increasing' if df['ndvi_mean'].iloc[-1] > df['ndvi_mean'].iloc[0] else 'decreasing',
                'peak_vegetation_date': df.loc[df['ndvi_mean'].idxmax(), 'date'].strftime('%Y-%m-%d'),
                'peak_vegetation_ndvi': df['ndvi_mean'].max(),
                'average_vegetation_coverage': df['vegetation_fraction'].mean() * 100,
                'files_generated': len([f for f in os.listdir(analysis_dir) if f.endswith('.tif')])
            }
            
            print(f"\n🌱 NDVI Analysis Summary:")
            print(f"   Analysis: {summary['analysis_name']}")
            print(f"   Scenes processed: {summary['total_scenes']}")
            print(f"   Date range: {summary['date_range']}")
            print(f"   Average NDVI: {summary['average_ndvi']:.3f}")
            print(f"   Peak vegetation: {summary['peak_vegetation_ndvi']:.3f} on {summary['peak_vegetation_date']}")
            print(f"   Average vegetation coverage: {summary['average_vegetation_coverage']:.1f}%")
            
            return df, summary
        
        else:
            print("❌ No valid NDVI data could be calculated")
            return None, None
    
    # Run comprehensive NDVI analysis
    ndvi_df, analysis_summary = advanced_ndvi_analysis(items, "summer_2024")

**Time Series NDVI Analysis**:

.. code-block:: python

    def seasonal_ndvi_comparison(items_by_season):
        """Compare NDVI across different seasons."""
        
        seasonal_results = {}
        
        for season_name, season_items in items_by_season.items():
            print(f"🌱 Processing {season_name}...")
            
            season_ndvi = []
            
            for item in season_items:
                try:
                    band_urls = item.get_asset_urls(['B08', 'B04'])
                    
                    ndvi = calculate_ndvi(
                        nir_url=band_urls['B08'],
                        red_url=band_urls['B04']
                    )
                    
                    season_ndvi.append({
                        'mean': float(ndvi.mean().values),
                        'std': float(ndvi.std().values),
                        'date': item.properties.get('datetime', '')[:10]
                    })
                    
                except Exception as e:
                    continue
            
            if season_ndvi:
                seasonal_results[season_name] = {
                    'ndvi_values': [s['mean'] for s in season_ndvi],
                    'average_ndvi': sum(s['mean'] for s in season_ndvi) / len(season_ndvi),
                    'scene_count': len(season_ndvi),
                    'date_range': f"{min(s['date'] for s in season_ndvi)} to {max(s['date'] for s in season_ndvi)}"
                }
        
        # Generate seasonal comparison
        print(f"\n🌱 Seasonal NDVI Comparison:")
        for season, results in seasonal_results.items():
            print(f"   {season.title()}: {results['average_ndvi']:.3f} NDVI ({results['scene_count']} scenes)")
        
        return seasonal_results
    
    # Example usage with seasonal data
    seasonal_data = {
        'spring': filter_by_date_range(items, '2024-03-01', '2024-05-31'),
        'summer': filter_by_date_range(items, '2024-06-01', '2024-08-31'),
        'fall': filter_by_date_range(items, '2024-09-01', '2024-11-30')
    }
    
    seasonal_comparison = seasonal_ndvi_comparison(seasonal_data)

get_statistics
~~~~~~~~~~~~~~

.. py:function:: get_statistics(data_array, percentiles=[10, 25, 50, 75, 90])

   Calculate comprehensive statistics for raster data arrays.

   :param data_array: Input data array (xarray.DataArray or numpy.ndarray)
   :type data_array: xarray.DataArray or numpy.ndarray
   :param percentiles: Percentiles to calculate
   :type percentiles: list of numbers
   :returns: Dictionary of statistical measures
   :rtype: dict

**Basic Statistics Calculation**:

.. code-block:: python

    from open_geodata_api.utils import get_statistics
    import rioxarray
    
    # Load raster data
    data_url = item.get_asset_url('B04')  # Red band
    red_band = rioxarray.open_rasterio(data_url)
    
    # Calculate comprehensive statistics
    stats = get_statistics(red_band)
    
    print(f"📊 Red Band Statistics:")
    print(f"   Mean: {stats['mean']:.2f}")
    print(f"   Std: {stats['std']:.2f}")
    print(f"   Min: {stats['min']:.2f}")
    print(f"   Max: {stats['max']:.2f}")
    print(f"   Median: {stats['median']:.2f}")
    print(f"   25th percentile: {stats['p25']:.2f}")
    print(f"   75th percentile: {stats['p75']:.2f}")

**Multi-band Statistics Analysis**:

.. code-block:: python

    def multi_band_statistics(item, bands=['B02', 'B03', 'B04', 'B08']):
        """Calculate statistics for multiple bands."""
        
        band_stats = {}
        
        for band in bands:
            try:
                print(f"📊 Processing {band}...")
                
                # Load band data
                band_url = item.get_asset_url(band)
                band_data = rioxarray.open_rasterio(band_url)
                
                # Calculate statistics
                stats = get_statistics(
                    band_data,
                    percentiles=[5, 10, 25, 50, 75, 90, 95]
                )
                
                # Add band-specific metadata
                stats['band'] = band
                stats['band_description'] = {
                    'B02': 'Blue',
                    'B03': 'Green', 
                    'B04': 'Red',
                    'B08': 'Near-Infrared'
                }.get(band, band)
                
                band_stats[band] = stats
                
            except Exception as e:
                print(f"❌ Failed to process {band}: {e}")
                band_stats[band] = {'error': str(e)}
        
        return band_stats
    
    # Analyze multiple bands
    multi_stats = multi_band_statistics(items[0])
    
    # Display results in table format
    print(f"\n📊 Multi-Band Statistics Summary:")
    print(f"{'Band':<4} {'Color':<12} {'Mean':<8} {'Std':<8} {'Min':<8} {'Max':<8}")
    print("-" * 60)
    
    for band, stats in multi_stats.items():
        if 'error' not in stats:
            print(f"{band:<4} {stats['band_description']:<12} "
                  f"{stats['mean']:<8.1f} {stats['std']:<8.1f} "
                  f"{stats['min']:<8.1f} {stats['max']:<8.1f}")

**Temporal Statistics Analysis**:

.. code-block:: python

    def temporal_statistics_analysis(items, band='B08', output_dir="./temporal_stats/"):
        """Analyze statistics over time for vegetation monitoring."""
        
        import pandas as pd
        import matplotlib.pyplot as plt
        
        os.makedirs(output_dir, exist_ok=True)
        
        temporal_data = []
        
        for item in items:
            try:
                # Get date and metadata
                date = item.properties.get('datetime', '')[:10]
                cloud_cover = item.properties.get('eo:cloud_cover', 0)
                
                # Skip very cloudy images
                if cloud_cover > 20:
                    continue
                
                # Load and analyze band
                band_url = item.get_asset_url(band)
                band_data = rioxarray.open_rasterio(band_url)
                
                # Get comprehensive statistics
                stats = get_statistics(band_data, percentiles=[10, 25, 50, 75, 90])
                
                # Add temporal metadata
                stats.update({
                    'date': date,
                    'item_id': item.id,
                    'cloud_cover': cloud_cover,
                    'band': band
                })
                
                temporal_data.append(stats)
                
                print(f"✅ {date}: Mean={stats['mean']:.1f}, Std={stats['std']:.1f}")
                
            except Exception as e:
                print(f"❌ Failed {item.id}: {e}")
        
        if not temporal_data:
            print("❌ No valid temporal data collected")
            return None
        
        # Create DataFrame
        df = pd.DataFrame(temporal_data)
        df['date'] = pd.to_datetime(df['date'])
        df = df.sort_values('date')
        
        # Save temporal statistics
        csv_path = os.path.join(output_dir, f"temporal_stats_{band}.csv")
        df.to_csv(csv_path, index=False)
        
        # Generate temporal plots
        plt.figure(figsize=(15, 12))
        
        # Plot 1: Mean values over time
        plt.subplot(2, 3, 1)
        plt.plot(df['date'], df['mean'], 'b-o', linewidth=2)
        plt.title(f'{band} Mean Values Over Time')
        plt.xlabel('Date')
        plt.ylabel('Digital Number')
        plt.xticks(rotation=45)
        
        # Plot 2: Standard deviation
        plt.subplot(2, 3, 2)
        plt.plot(df['date'], df['std'], 'r-o', linewidth=2)
        plt.title(f'{band} Standard Deviation')
        plt.xlabel('Date')
        plt.ylabel('Standard Deviation')
        plt.xticks(rotation=45)
        
        # Plot 3: Percentile ranges
        plt.subplot(2, 3, 3)
        plt.fill_between(df['date'], df['p10'], df['p90'], alpha=0.3, label='10th-90th percentile')
        plt.fill_between(df['date'], df['p25'], df['p75'], alpha=0.5, label='25th-75th percentile')
        plt.plot(df['date'], df['median'], 'g-', linewidth=2, label='Median')
        plt.title(f'{band} Percentile Ranges')
        plt.xlabel('Date')
        plt.ylabel('Digital Number')
        plt.legend()
        plt.xticks(rotation=45)
        
        # Plot 4: Min/Max ranges
        plt.subplot(2, 3, 4)
        plt.plot(df['date'], df['min'], 'navy', label='Minimum', linewidth=2)
        plt.plot(df['date'], df['max'], 'darkred', label='Maximum', linewidth=2)
        plt.fill_between(df['date'], df['min'], df['max'], alpha=0.2)
        plt.title(f'{band} Min/Max Range')
        plt.xlabel('Date')
        plt.ylabel('Digital Number')
        plt.legend()
        plt.xticks(rotation=45)
        
        # Plot 5: Cloud cover correlation
        plt.subplot(2, 3, 5)
        plt.scatter(df['cloud_cover'], df['mean'], alpha=0.6)
        plt.xlabel('Cloud Cover (%)')
        plt.ylabel(f'{band} Mean Value')
        plt.title('Cloud Cover vs Band Values')
        
        # Plot 6: Statistical stability
        plt.subplot(2, 3, 6)
        coefficient_of_variation = df['std'] / df['mean'] * 100
        plt.plot(df['date'], coefficient_of_variation, 'purple', linewidth=2)
        plt.title('Coefficient of Variation')
        plt.xlabel('Date')
        plt.ylabel('CV (%)')
        plt.xticks(rotation=45)
        
        plt.tight_layout()
        plt.savefig(os.path.join(output_dir, f'temporal_analysis_{band}.png'), 
                   dpi=300, bbox_inches='tight')
        plt.close()
        
        # Generate summary statistics
        summary = {
            'band': band,
            'total_scenes': len(df),
            'date_range': f"{df['date'].min().strftime('%Y-%m-%d')} to {df['date'].max().strftime('%Y-%m-%d')}",
            'mean_stability': {
                'average': df['mean'].mean(),
                'std': df['mean'].std(),
                'cv': df['mean'].std() / df['mean'].mean() * 100
            },
            'temporal_trend': 'increasing' if df['mean'].iloc[-1] > df['mean'].iloc[0] else 'decreasing',
            'max_variation_date': df.loc[df['std'].idxmax(), 'date'].strftime('%Y-%m-%d'),
            'most_stable_date': df.loc[df['std'].idxmin(), 'date'].strftime('%Y-%m-%d')
        }
        
        print(f"\n📊 Temporal Statistics Summary for {band}:")
        print(f"   Scenes analyzed: {summary['total_scenes']}")
        print(f"   Date range: {summary['date_range']}")
        print(f"   Average mean value: {summary['mean_stability']['average']:.1f}")
        print(f"   Temporal stability (CV): {summary['mean_stability']['cv']:.1f}%")
        print(f"   Trend: {summary['temporal_trend']}")
        
        return df, summary
    
    # Run temporal analysis
    temporal_df, temporal_summary = temporal_statistics_analysis(items, 'B08')

.. _error-handling:

Error Handling Functions
------------------------

handle_download_errors
~~~~~~~~~~~~~~~~~~~~~~~

.. py:function:: handle_download_errors(error, retry_count=0, max_retries=3)

   Intelligent error handling for download operations with retry logic.

   :param error: Exception object to handle
   :type error: Exception
   :param retry_count: Current retry attempt number
   :type retry_count: int
   :param max_retries: Maximum number of retry attempts
   :type max_retries: int
   :returns: Retry decision and suggested action
   :rtype: dict

**Basic Error Handling**:

.. code-block:: python

    from open_geodata_api.utils import handle_download_errors
    import requests
    
    def robust_download_with_error_handling(url, destination, max_retries=3):
        """Download with intelligent error handling."""
        
        for attempt in range(max_retries + 1):
            try:
                # Attempt download
                response = requests.get(url, timeout=120)
                response.raise_for_status()
                
                # Save file
                with open(destination, 'wb') as f:
                    f.write(response.content)
                
                print(f"✅ Download successful: {destination}")
                return {'success': True, 'path': destination}
                
            except Exception as error:
                # Handle error intelligently
                error_analysis = handle_download_errors(error, attempt, max_retries)
                
                print(f"❌ Attempt {attempt + 1} failed: {error_analysis['error_type']}")
                print(f"   Reason: {error_analysis['description']}")
                
                if error_analysis['should_retry'] and attempt < max_retries:
                    wait_time = error_analysis['suggested_wait_time']
                    print(f"🔄 Retrying in {wait_time} seconds...")
                    
                    import time
                    time.sleep(wait_time)
                    
                    # Apply suggested modifications
                    if error_analysis['suggested_action'] == 'reduce_timeout':
                        # Implement timeout reduction logic
                        pass
                    elif error_analysis['suggested_action'] == 'change_headers':
                        # Implement header modification logic
                        pass
                        
                else:
                    print(f"💥 Giving up after {attempt + 1} attempts")
                    return {
                        'success': False, 
                        'error': str(error),
                        'error_analysis': error_analysis
                    }
        
        return {'success': False, 'error': 'Max retries exceeded'}
    
    # Use robust download
    result = robust_download_with_error_handling(
        "https://example.com/data.tif",
        "./robust_download.tif"
    )

**Comprehensive Error Handling Workflow**:

.. code-block:: python

    def comprehensive_error_handling_workflow(items, base_destination="./error_handled/"):
        """Download workflow with comprehensive error handling and reporting."""
        
        import json
        from datetime import datetime
        
        os.makedirs(base_destination, exist_ok=True)
        
        # Initialize error tracking
        error_log = {
            'session_id': datetime.now().strftime("%Y%m%d_%H%M%S"),
            'start_time': datetime.now().isoformat(),
            'total_items': len(items),
            'results': {},
            'error_summary': {},
            'retry_statistics': {}
        }
        
        success_count = 0
        error_types = {}
        retry_statistics = {'total_retries': 0, 'successful_retries': 0}
        
        for i, item in enumerate(items):
            print(f"\n📥 Processing item {i+1}/{len(items)}: {item.id}")
            
            item_results = {}
            
            # Try to download each asset
            for asset_key in ['B08', 'B04', 'B03', 'B02']:
                try:
                    asset_url = item.get_asset_url(asset_key)
                    destination = os.path.join(base_destination, f"{item.id}_{asset_key}.tif")
                    
                    # Attempt download with error handling
                    download_result = robust_download_with_error_handling(
                        asset_url, 
                        destination,
                        max_retries=3
                    )
                    
                    if download_result['success']:
                        item_results[asset_key] = {
                            'success': True,
                            'path': download_result['path'],
                            'size_bytes': os.path.getsize(download_result['path'])
                        }
                        success_count += 1
                    else:
                        # Analyze and log error
                        error_analysis = download_result.get('error_analysis', {})
                        error_type = error_analysis.get('error_type', 'unknown')
                        
                        item_results[asset_key] = {
                            'success': False,
                            'error': download_result['error'],
                            'error_type': error_type,
                            'error_analysis': error_analysis
                        }
                        
                        # Track error types
                        error_types[error_type] = error_types.get(error_type, 0) + 1
                        
                        # Track retry statistics
                        if 'retry_count' in error_analysis:
                            retry_statistics['total_retries'] += error_analysis['retry_count']
                            if error_analysis['retry_count'] > 0:
                                retry_statistics['successful_retries'] += 1
                
                except Exception as e:
                    print(f"   ❌ Unexpected error for {asset_key}: {e}")
                    item_results[asset_key] = {
                        'success': False,
                        'error': str(e),
                        'error_type': 'unexpected'
                    }
            
            error_log['results'][item.id] = item_results
        
        # Finalize error log
        error_log.update({
            'end_time': datetime.now().isoformat(),
            'success_count': success_count,
            'total_downloads_attempted': len(items) * 4,  # 4 assets per item
            'success_rate': success_count / (len(items) * 4) * 100,
            'error_summary': error_types,
            'retry_statistics': retry_statistics
        })
        
        # Save error log
        log_file = os.path.join(base_destination, "error_log.json")
        with open(log_file, 'w') as f:
            json.dump(error_log, f, indent=2)
        
        # Generate error report
        print(f"\n📊 Error Handling Summary:")
        print(f"   Total downloads attempted: {error_log['total_downloads_attempted']}")
        print(f"   Successful downloads: {success_count}")
        print(f"   Success rate: {error_log['success_rate']:.1f}%")
        print(f"   Total retries: {retry_statistics['total_retries']}")
        print(f"   Successful retry recoveries: {retry_statistics['successful_retries']}")
        
        if error_types:
            print(f"\n❌ Error Types Encountered:")
            for error_type, count in error_types.items():
                print(f"   {error_type}: {count} occurrences")
        
        return error_log
    
    # Run comprehensive error handling workflow
    error_report = comprehensive_error_handling_workflow(items)

validate_inputs
~~~~~~~~~~~~~~~

.. py:function:: validate_inputs(items=None, bbox=None, datetime=None, collections=None)

   Validate input parameters for STAC operations.

   :param items: STAC items to validate
   :type items: STACItemCollection or list or None
   :param bbox: Bounding box to validate
   :type bbox: list or None
   :param datetime: Date range to validate
   :type datetime: str or None
   :param collections: Collection names to validate
   :type collections: list or None
   :returns: Validation results with detailed feedback
   :rtype: dict

**Input Validation Examples**:

.. code-block:: python

    from open_geodata_api.utils import validate_inputs
    
    # Validate search parameters before executing
    validation = validate_inputs(
        bbox=[-122.5, 47.5, -122.0, 48.0],
        datetime="2024-06-01/2024-08-31",
        collections=["sentinel-2-l2a"]
    )
    
    if validation['valid']:
        print("✅ All inputs are valid")
        # Proceed with search
    else:
        print("❌ Input validation failed:")
        for error in validation['errors']:
            print(f"   - {error}")

**Comprehensive Validation Workflow**:

.. code-block:: python

    def validated_search_workflow(collections, bbox, datetime, **kwargs):
        """Search workflow with comprehensive input validation."""
        
        # Pre-search validation
        validation = validate_inputs(
            bbox=bbox,
            datetime=datetime,
            collections=collections
        )
        
        if not validation['valid']:
            print("❌ Input validation failed:")
            for error in validation['errors']:
                print(f"   - {error}")
            
            # Suggest corrections
            if validation.get('suggestions'):
                print("\n💡 Suggestions:")
                for suggestion in validation['suggestions']:
                    print(f"   - {suggestion}")
            
            return None
        
        print("✅ Input validation passed")
        
        # Additional validation with warnings
        if validation.get('warnings'):
            print("\n⚠️ Warnings:")
            for warning in validation['warnings']:
                print(f"   - {warning}")
        
        try:
            # Perform search with validated inputs
            import open_geodata_api as ogapi
            
            pc = ogapi.planetary_computer()
            results = pc.search(
                collections=collections,
                bbox=bbox,
                datetime=datetime,
                **kwargs
            )
            
            # Post-search validation
            items = results.get_all_items()
            
            post_validation = validate_inputs(items=items)
            
            if post_validation['valid']:
                print(f"✅ Search completed: {len(items)} valid items found")
                return items
            else:
                print("⚠️ Search completed but some results have issues:")
                for warning in post_validation.get('warnings', []):
                    print(f"   - {warning}")
                return items
                
        except Exception as e:
            print(f"❌ Search failed: {e}")
            return None
    
    # Use validated search
    validated_items = validated_search_workflow(
        collections=["sentinel-2-l2a"],
        bbox=[-122.5, 47.5, -122.0, 48.0],
        datetime="2024-06-01/2024-08-31",
        query={'eo:cloud_cover': {'lt': 20}}
    )

.. _configuration:

Configuration Management
------------------------

set_global_config
~~~~~~~~~~~~~~~~~~

.. py:function:: set_global_config(**config_params)

   Set global configuration parameters for the library.

   :param config_params: Configuration parameters to set
   :type config_params: various types
   :returns: Updated configuration dictionary
   :rtype: dict

**Global Configuration Setup**:

.. code-block:: python

    from open_geodata_api.utils import set_global_config, get_global_config
    
    # Set global configuration
    config = set_global_config(
        default_provider='planetary_computer',
        auto_sign_urls=True,
        max_download_workers=6,
        default_timeout=180,
        cache_size_mb=500,
        progress_bar=True,
        verbose_errors=False
    )
    
    print("🔧 Global configuration updated:")
    for key, value in config.items():
        print(f"   {key}: {value}")

get_global_config
~~~~~~~~~~~~~~~~~

.. py:function:: get_global_config(key=None)

   Get global configuration parameters.

   :param key: Specific configuration key (None for all)
   :type key: str or None
   :returns: Configuration value or full configuration
   :rtype: any or dict

**Configuration Usage Examples**:

.. code-block:: python

    # Get specific configuration value
    default_provider = get_global_config('default_provider')
    print(f"Default provider: {default_provider}")
    
    # Get all configuration
    full_config = get_global_config()
    print(f"Full configuration: {full_config}")
    
    # Use configuration in workflows
    def configured_download(items, destination="./configured_data/"):
        """Download using global configuration."""
        
        config = get_global_config()
        
        return download_items(
            items,
            base_destination=destination,
            max_workers=config.get('max_download_workers', 4),
            timeout=config.get('default_timeout', 120),
            show_progress=config.get('progress_bar', True)
        )
    
    # Use configured download
    configured_results = configured_download(items)

**Environment-Specific Configuration**:

.. code-block:: python

    def setup_environment_config(environment='development'):
        """Setup configuration for different environments."""
        
        if environment == 'development':
            config = set_global_config(
                default_provider='planetary_computer',
                auto_sign_urls=True,
                max_download_workers=2,  # Conservative for dev
                default_timeout=60,
                cache_size_mb=100,
                progress_bar=True,
                verbose_errors=True,     # Detailed errors in dev
                debug_mode=True
            )
        
        elif environment == 'production':
            config = set_global_config(
                default_provider='planetary_computer',
                auto_sign_urls=True,
                max_download_workers=8,  # Higher throughput
                default_timeout=300,
                cache_size_mb=1000,
                progress_bar=False,      # No progress bars in prod
                verbose_errors=False,
                debug_mode=False,
                retry_attempts=5
            )
        
        elif environment == 'testing':
            config = set_global_config(
                default_provider='planetary_computer',
                auto_sign_urls=False,    # Use mock URLs in tests
                max_download_workers=1,  # Single threaded for tests
                default_timeout=30,
                cache_size_mb=50,
                progress_bar=False,
                verbose_errors=True,
                debug_mode=True,
                mock_mode=True
            )
        
        print(f"🔧 Environment '{environment}' configuration applied")
        return config
    
    # Setup for different environments
    dev_config = setup_environment_config('development')
    prod_config = setup_environment_config('production')

Performance Optimization
------------------------

optimize_for_large_datasets
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. py:function:: optimize_for_large_datasets(dataset_size_gb, available_memory_gb)

   Optimize library settings for large dataset processing.

   :param dataset_size_gb: Expected dataset size in GB
   :type dataset_size_gb: float
   :param available_memory_gb: Available system memory in GB
   :type available_memory_gb: float
   :returns: Optimized configuration recommendations
   :rtype: dict

**Large Dataset Optimization**:

.. code-block:: python

    from open_geodata_api.utils import optimize_for_large_datasets
    
    # Optimize for large dataset processing
    optimization = optimize_for_large_datasets(
        dataset_size_gb=50.0,      # 50 GB dataset
        available_memory_gb=16.0   # 16 GB RAM available
    )
    
    print("🚀 Large Dataset Optimization:")
    print(f"   Recommended batch size: {optimization['batch_size']}")
    print(f"   Recommended workers: {optimization['max_workers']}")
    print(f"   Memory per worker: {optimization['memory_per_worker_mb']} MB")
    print(f"   Processing strategy: {optimization['strategy']}")
    
    # Apply optimizations
    optimized_config = set_global_config(**optimization['config'])

**Performance Benchmarking**:

.. code-block:: python

    def benchmark_download_performance(items, test_configs):
        """Benchmark different download configurations."""
        
        import time
        
        benchmark_results = {}
        
        for config_name, config in test_configs.items():
            print(f"\n🏃 Testing configuration: {config_name}")
            
            # Apply configuration
            set_global_config(**config)
            
            # Time the download
            start_time = time.time()
            
            try:
                results = download_items(
                    items[:5],  # Test with first 5 items
                    base_destination=f"./benchmark_{config_name}/",
                    asset_keys=['B04', 'B03'],
                    **config
                )
                
                end_time = time.time()
                
                # Calculate performance metrics
                download_time = end_time - start_time
                successful_downloads = sum(
                    1 for item_results in results.values() 
                    for result in item_results.values() 
                    if result.get('success', False)
                )
                
                benchmark_results[config_name] = {
                    'download_time': download_time,
                    'successful_downloads': successful_downloads,
                    'downloads_per_second': successful_downloads / download_time,
                    'config': config
                }
                
                print(f"   ✅ Time: {download_time:.2f}s, Downloads: {successful_downloads}")
                
            except Exception as e:
                benchmark_results[config_name] = {
                    'error': str(e),
                    'config': config
                }
                print(f"   ❌ Failed: {e}")
        
        # Find best configuration
        valid_results = {k: v for k, v in benchmark_results.items() if 'error' not in v}
        
        if valid_results:
            best_config = max(
                valid_results.items(),
                key=lambda x: x[1]['downloads_per_second']
            )
            
            print(f"\n🏆 Best Performance: {best_config[0]}")
            print(f"   Downloads per second: {best_config[1]['downloads_per_second']:.2f}")
            
            return best_config[1]['config']
        
        return None
    
    # Test different configurations
    test_configs = {
        'conservative': {
            'max_workers': 2,
            'timeout': 60,
            'chunk_size': 8192
        },
        'balanced': {
            'max_workers': 4,
            'timeout': 120,
            'chunk_size': 16384
        },
        'aggressive': {
            'max_workers': 8,
            'timeout': 180,
            'chunk_size': 32768
        }
    }
    
    best_config = benchmark_download_performance(items, test_configs)

Best Practices
--------------

**Memory Management**:

- Use batch processing for large datasets
- Monitor memory usage with ``psutil``
- Implement garbage collection between batches
- Use streaming downloads for very large files

**Error Handling**:

- Always implement retry logic for network operations
- Log errors with sufficient detail for debugging
- Provide fallback strategies for critical operations
- Validate inputs before expensive operations

**Performance Optimization**:

- Profile your workflows to identify bottlenecks
- Use parallel processing where appropriate
- Cache frequently accessed data
- Optimize batch sizes based on available resources

**URL Management**:

- Check URL expiration before use
- Implement automatic re-signing for Planetary Computer
- Cache signed URLs when possible
- Monitor URL validity in production systems

**Data Quality**:

- Filter by cloud cover before downloading
- Validate downloaded files
- Implement data quality checks
- Use temporal filtering for analysis

**Configuration Management**:

- Set up environment-specific configurations
- Use global settings for consistent behavior
- Document configuration choices
- Test configurations before production deployment

Examples Gallery
----------------

**Complete Vegetation Monitoring Workflow**:

.. code-block:: python

    def complete_vegetation_monitoring_workflow(
        area_of_interest,
        start_date,
        end_date,
        output_dir="./vegetation_monitoring/"
    ):
        """Complete end-to-end vegetation monitoring workflow."""
        
        import open_geodata_api as ogapi
        from open_geodata_api.utils import *
        
        print("🌱 Starting Vegetation Monitoring Workflow")
        
        # Step 1: Setup and Configuration
        setup_environment_config('production')
        optimize_for_large_datasets(10.0, 8.0)
        
        # Step 2: Search for Data
        pc = ogapi.planetary_computer(auto_sign=True)
        
        raw_results = pc.search(
            collections=["sentinel-2-l2a"],
            bbox=area_of_interest,
            datetime=f"{start_date}/{end_date}",
            query={'eo:cloud_cover': {'lt': 20}}
        )
        
        items = raw_results.get_all_items()
        print(f"📡 Found {len(items)} items")
        
        # Step 3: Quality Filtering
        clear_items = filter_by_cloud_cover(items, max_cloud_cover=15)
        temporal_items = filter_by_date_range(clear_items, start_date, end_date)
        spatial_items = filter_by_geometry(temporal_items, area_of_interest)
        
        print(f"🔍 After filtering: {len(spatial_items)} high-quality items")
        
        # Step 4: Download Data
        download_results = download_items(
            spatial_items,
            base_destination=os.path.join(output_dir, "satellite_data"),
            asset_keys=['B08', 'B04', 'B03', 'B02'],
            create_product_folders=True
        )
        
        # Step 5: NDVI Analysis
        ndvi_df, ndvi_summary = advanced_ndvi_analysis(
            spatial_items, 
            "vegetation_monitoring"
        )
        
        # Step 6: Statistical Analysis
        temporal_df, temporal_summary = temporal_statistics_analysis(
            spatial_items, 
            'B08',
            output_dir=os.path.join(output_dir, "statistics")
        )
        
        # Step 7: Generate Reports
        download_summary = create_download_summary(
            download_results,
            output_file=os.path.join(output_dir, "download_summary.json")
        )
        
        # Step 8: Export for External Use
        export_metadata = export_urls_to_json(
            spatial_items,
            output_file=os.path.join(output_dir, "data_urls.json"),
            asset_keys=['B08', 'B04', 'B03', 'B02'],
            include_metadata=True
        )
        
        # Final Summary
        workflow_summary = {
            'area_of_interest': area_of_interest,
            'date_range': f"{start_date} to {end_date}",
            'items_found': len(items),
            'items_processed': len(spatial_items),
            'downloads_successful': download_summary['successful_downloads'],
            'ndvi_analysis': ndvi_summary,
            'temporal_analysis': temporal_summary,
            'output_directory': output_dir
        }
        
        print(f"\n✅ Vegetation Monitoring Workflow Complete!")
        print(f"   Area: {area_of_interest}")
        print(f"   Period: {workflow_summary['date_range']}")
        print(f"   Items processed: {workflow_summary['items_processed']}")
        print(f"   Downloads: {workflow_summary['downloads_successful']}")
        print(f"   Average NDVI: {ndvi_summary.get('average_ndvi', 'N/A')}")
        print(f"   Output: {output_dir}")
        
        return workflow_summary
    
    # Run complete workflow
    seattle_vegetation = complete_vegetation_monitoring_workflow(
        area_of_interest=[-122.5, 47.5, -122.0, 48.0],
        start_date="2024-06-01",
        end_date="2024-08-31"
    )

See Also
--------

- :doc:`../quickstart` - Getting started with the library
- :doc:`../tutorials/filtering-data` - Data filtering tutorials
- :doc:`../tutorials/downloading-data` - Download tutorials
- :doc:`../api-reference/core-classes` - Core class documentation
- :doc:`../examples/advanced-workflows` - Advanced workflow examples

