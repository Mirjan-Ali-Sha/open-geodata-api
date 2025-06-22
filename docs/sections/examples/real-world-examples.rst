Real-World Examples
===================

Complete real-world applications using Open Geodata API for various domains.

Agricultural Monitoring
-----------------------

Crop Health Assessment with NDVI
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   import open_geodata_api as ogapi
   from open_geodata_api.utils import filter_by_cloud_cover, download_items
   import numpy as np
   import rioxarray as rxr
   
   def monitor_crop_health(farm_bbox, planting_date, harvest_date):
       """Monitor crop health throughout growing season."""
       
       pc = ogapi.planetary_computer(auto_sign=True)
       
       # Search for growing season data
       results = pc.search(
           collections=['sentinel-2-l2a'],
           bbox=farm_bbox,
           datetime=f"{planting_date}/{harvest_date}",
           query={'eo:cloud_cover': {'lt': 30}},
           limit=50
       )
       
       # Filter for very clear images
       items = results.get_all_items()
       clear_items = filter_by_cloud_cover(items, max_cloud_cover=15)
       
       print(f"Found {len(clear_items)} clear images for crop monitoring")
       
       # Download NIR and Red bands for NDVI calculation
       download_results = download_items(
           clear_items,
           base_destination="./crop_monitoring/",
           asset_keys=['B08', 'B04'],  # NIR, Red
           create_product_folders=True
       )
       
       # Calculate NDVI for each date
       ndvi_time_series = {}
       
       for item_id, files in download_results.items():
           if 'B08' in files and 'B04' in files:
               # Load bands
               nir = rxr.open_rasterio(files['B08'])
               red = rxr.open_rasterio(files['B04'])
               
               # Calculate NDVI
               ndvi = (nir - red) / (nir + red)
               
               # Get date from item
               item = next(item for item in clear_items if item.id == item_id)
               date = item.properties['datetime'][:10]
               
               # Calculate mean NDVI for farm area
               mean_ndvi = float(ndvi.mean())
               ndvi_time_series[date] = mean_ndvi
               
               print(f"Date: {date}, Mean NDVI: {mean_ndvi:.3f}")
       
       return ndvi_time_series

   # Usage
   farm_bbox = [-120.1, 36.5, -120.0, 36.6]  # Central Valley, CA
   ndvi_data = monitor_crop_health(
       farm_bbox, 
       "2024-04-01",  # Planting
       "2024-09-30"   # Harvest
   )

Environmental Monitoring
-------------------------

Water Body Change Detection
~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   def detect_water_changes(reservoir_bbox, before_date, after_date):
       """Detect changes in water body extent."""
       
       pc = ogapi.planetary_computer(auto_sign=True)
       
       def get_water_extent(date_range, label):
           """Get water extent for a specific time period."""
           results = pc.search(
               collections=['sentinel-2-l2a'],
               bbox=reservoir_bbox,
               datetime=date_range,
               query={'eo:cloud_cover': {'lt': 10}},
               limit=5
           )
           
           items = results.get_all_items()
           if not items:
               print(f"No clear images found for {label}")
               return None
           
           # Use the clearest image
           best_item = min(items, key=lambda x: x.properties.get('eo:cloud_cover', 100))
           
           # Download water detection bands
           urls = best_item.get_band_urls(['B03', 'B08', 'B11'])  # Green, NIR, SWIR
           
           # Load bands
           green = rxr.open_rasterio(urls['B03'])
           nir = rxr.open_rasterio(urls['B08'])
           swir = rxr.open_rasterio(urls['B11'])
           
           # Calculate NDWI (Normalized Difference Water Index)
           ndwi = (green - nir) / (green + nir)
           
           # Water mask (NDWI > 0.3 typically indicates water)
           water_mask = ndwi > 0.3
           water_area_pixels = water_mask.sum()
           
           print(f"{label}: {water_area_pixels.values} water pixels")
           return water_mask, water_area_pixels.values
       
       # Get water extent before and after
       before_mask, before_area = get_water_extent(before_date, "Before")
       after_mask, after_area = get_water_extent(after_date, "After")
       
       if before_area and after_area:
           change_percent = ((after_area - before_area) / before_area) * 100
           print(f"Water area change: {change_percent:.1f}%")
           
           return {
               'before_area': before_area,
               'after_area': after_area,
               'change_percent': change_percent
           }
       
       return None

   # Usage - Monitor California reservoir during drought
   reservoir_bbox = [-120.95, 38.9, -120.85, 39.0]  # Folsom Lake, CA
   changes = detect_water_changes(
       reservoir_bbox,
       "2023-06-01/2023-06-30",  # Before dry season
       "2023-10-01/2023-10-31"   # After dry season
   )

Urban Development Analysis
--------------------------

Built-up Area Expansion
~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   def analyze_urban_expansion(city_bbox, years_to_compare):
       """Analyze urban expansion over multiple years."""
       
       pc = ogapi.planetary_computer(auto_sign=True)
       urban_data = {}
       
       for year in years_to_compare:
           print(f"Analyzing urban area for {year}...")
           
           # Search for annual data
           results = pc.search(
               collections=['sentinel-2-l2a'],
               bbox=city_bbox,
               datetime=f"{year}-06-01/{year}-08-31",  # Summer months
               query={'eo:cloud_cover': {'lt': 20}},
               limit=10
           )
           
           items = results.get_all_items()
           clear_items = filter_by_cloud_cover(items, max_cloud_cover=15)
           
           if not clear_items:
               continue
           
           # Use median composite approach
           urls_list = []
           for item in clear_items[:5]:  # Top 5 clearest
               urls = item.get_band_urls(['B04', 'B08', 'B11', 'B12'])
               urls_list.append(urls)
           
           # For simplicity, use first clear image
           urls = urls_list[0]
           
           # Load bands for urban analysis
           red = rxr.open_rasterio(urls['B04'])
           nir = rxr.open_rasterio(urls['B08'])
           swir1 = rxr.open_rasterio(urls['B11'])
           swir2 = rxr.open_rasterio(urls['B12'])
           
           # Calculate Built-up Index (combination of indices)
           ndvi = (nir - red) / (nir + red)
           ndbi = (swir1 - nir) / (swir1 + nir)  # Normalized Difference Built-up Index
           
           # Urban areas: high NDBI, low NDVI
           urban_mask = (ndbi > 0.1) & (ndvi < 0.2)
           urban_pixels = urban_mask.sum().values
           
           urban_data[year] = urban_pixels
           print(f"  {year}: {urban_pixels} urban pixels")
       
       # Calculate expansion rate
       years = sorted(urban_data.keys())
       if len(years) >= 2:
           first_year, last_year = years[0], years[-1]
           expansion_rate = (urban_data[last_year] - urban_data[first_year]) / (last_year - first_year)
           print(f"Average expansion: {expansion_rate:.0f} pixels/year")
       
       return urban_data

   # Usage - Analyze Phoenix, AZ urban expansion
   phoenix_bbox = [-112.3, 33.3, -111.9, 33.7]
   urban_expansion = analyze_urban_expansion(
       phoenix_bbox, 
       [2019, 2020, 2021, 2022, 2023, 2024]
   )

Climate Research
----------------

Temperature Trend Analysis
~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   def analyze_land_surface_temperature(study_area, years):
       """Analyze land surface temperature trends using Landsat thermal data."""
       
       pc = ogapi.planetary_computer(auto_sign=True)
       temperature_data = {}
       
       for year in years:
           print(f"Processing temperature data for {year}...")
           
           # Search for Landsat data (has thermal bands)
           results = pc.search(
               collections=['landsat-c2-l2'],
               bbox=study_area,
               datetime=f"{year}-06-01/{year}-08-31",  # Summer
               query={'eo:cloud_cover': {'lt': 30}},
               limit=20
           )
           
           items = results.get_all_items()
           clear_items = filter_by_cloud_cover(items, max_cloud_cover=20)
           
           if not clear_items:
               continue
           
           yearly_temps = []
           
           for item in clear_items[:5]:  # Process top 5 images
               # Get thermal and optical bands
               try:
                   thermal_url = item.get_asset_url('lwir11')  # Thermal band
                   red_url = item.get_asset_url('red')
                   nir_url = item.get_asset_url('nir08')
                   
                   # Load data
                   thermal = rxr.open_rasterio(thermal_url)
                   red = rxr.open_rasterio(red_url)
                   nir = rxr.open_rasterio(nir_url)
                   
                   # Calculate NDVI for vegetation mask
                   ndvi = (nir - red) / (nir + red)
                   
                   # Analyze temperature for different land cover types
                   urban_temp = thermal.where(ndvi < 0.2).mean().values  # Low vegetation (urban)
                   forest_temp = thermal.where(ndvi > 0.5).mean().values  # High vegetation
                   
                   date = item.properties['datetime'][:10]
                   yearly_temps.append({
                       'date': date,
                       'urban_temp': float(urban_temp),
                       'forest_temp': float(forest_temp),
                       'temp_difference': float(urban_temp - forest_temp)
                   })
                   
               except Exception as e:
                   print(f"Error processing item: {e}")
                   continue
           
           if yearly_temps:
               # Calculate annual averages
               avg_urban = np.mean([t['urban_temp'] for t in yearly_temps])
               avg_forest = np.mean([t['forest_temp'] for t in yearly_temps])
               avg_difference = avg_urban - avg_forest
               
               temperature_data[year] = {
                   'urban_temp': avg_urban,
                   'forest_temp': avg_forest,
                   'urban_heat_island': avg_difference,
                   'measurements': len(yearly_temps)
               }
               
               print(f"  {year}: Urban Heat Island effect = {avg_difference:.1f}K")
       
       return temperature_data

   # Usage - Study urban heat island in Las Vegas
   vegas_bbox = [-115.3, 36.0, -115.0, 36.3]
   temp_analysis = analyze_land_surface_temperature(
       vegas_bbox,
       [2020, 2021, 2022, 2023, 2024]
   )

Disaster Response
-----------------

Flood Extent Mapping
~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   def map_flood_extent(affected_area, pre_flood_date, post_flood_date):
       """Map flood extent using before/after satellite imagery."""
       
       pc = ogapi.planetary_computer(auto_sign=True)
       
       def get_water_extent(date_range, label):
           """Get water extent for before/after comparison."""
           results = pc.search(
               collections=['sentinel-1-grd'],  # SAR data works through clouds
               bbox=affected_area,
               datetime=date_range,
               limit=3
           )
           
           if not results.get_all_items():
               # Fallback to optical if SAR not available
               results = pc.search(
                   collections=['sentinel-2-l2a'],
                   bbox=affected_area,
                   datetime=date_range,
                   query={'eo:cloud_cover': {'lt': 50}},
                   limit=5
               )
           
           items = results.get_all_items()
           if not items:
               print(f"No images found for {label}")
               return None
           
           item = items[0]  # Use most recent
           
           # For Sentinel-2 (optical), use water detection
           if 'sentinel-2' in item.collection:
               urls = item.get_band_urls(['B03', 'B08'])  # Green, NIR
               green = rxr.open_rasterio(urls['B03'])
               nir = rxr.open_rasterio(urls['B08'])
               
               # NDWI for water detection
               ndwi = (green - nir) / (green + nir)
               water_mask = ndwi > 0.3
           
           # For Sentinel-1 (SAR), use backscatter analysis
           else:
               vh_url = item.get_asset_url('vh')  # Cross-polarization
               vh = rxr.open_rasterio(vh_url)
               
               # Water appears dark in SAR (low backscatter)
               water_mask = vh < vh.quantile(0.1)  # Bottom 10% of values
           
           return water_mask, item.properties['datetime'][:10]
       
       # Get before and after water extents
       print("Analyzing pre-flood conditions...")
       pre_mask, pre_date = get_water_extent(pre_flood_date, "Pre-flood")
       
       print("Analyzing post-flood conditions...")
       post_mask, post_date = get_water_extent(post_flood_date, "Post-flood")
       
       if pre_mask is not None and post_mask is not None:
           # Calculate flood extent (new water areas)
           flood_extent = post_mask & ~pre_mask
           flood_pixels = flood_extent.sum().values
           total_pixels = flood_extent.size
           flood_percentage = (flood_pixels / total_pixels) * 100
           
           print(f"Flood Analysis Results:")
           print(f"  Pre-flood date: {pre_date}")
           print(f"  Post-flood date: {post_date}")
           print(f"  Flooded area: {flood_pixels} pixels ({flood_percentage:.2f}% of region)")
           
           return {
               'pre_date': pre_date,
               'post_date': post_date,
               'flood_pixels': flood_pixels,
               'flood_percentage': flood_percentage,
               'flood_mask': flood_extent
           }
       
       return None

   # Usage - Analyze flooding from Hurricane Harvey
   houston_bbox = [-95.8, 29.5, -95.0, 30.0]
   flood_analysis = map_flood_extent(
       houston_bbox,
       "2017-08-20/2017-08-24",  # Before Hurricane Harvey
       "2017-08-28/2017-09-05"   # After Hurricane Harvey
   )

Multi-Sensor Analysis
---------------------

Cross-Platform Data Fusion
~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   def compare_sensor_data(study_area, date_range):
       """Compare data from multiple satellite sensors."""
       
       pc = ogapi.planetary_computer(auto_sign=True)
       sensor_data = {}
       
       # Define sensors and their key bands
       sensors = {
           'sentinel-2-l2a': {
               'red': 'B04',
               'nir': 'B08',
               'resolution': 10  # meters
           },
           'landsat-c2-l2': {
               'red': 'red',
               'nir': 'nir08',
               'resolution': 30  # meters
           }
       }
       
       for sensor, bands in sensors.items():
           print(f"Processing {sensor} data...")
           
           results = pc.search(
               collections=[sensor],
               bbox=study_area,
               datetime=date_range,
               query={'eo:cloud_cover': {'lt': 20}},
               limit=5
           )
           
           items = results.get_all_items()
           if not items:
               continue
           
           # Use clearest image
           best_item = min(items, key=lambda x: x.properties.get('eo:cloud_cover', 100))
           
           # Get URLs and calculate NDVI
           urls = best_item.get_band_urls([bands['red'], bands['nir']])
           
           red = rxr.open_rasterio(urls[bands['red']])
           nir = rxr.open_rasterio(urls[bands['nir']])
           
           # Calculate NDVI
           ndvi = (nir - red) / (nir + red)
           
           # Store results
           sensor_data[sensor] = {
               'item_id': best_item.id,
               'date': best_item.properties['datetime'][:10],
               'cloud_cover': best_item.properties.get('eo:cloud_cover'),
               'resolution': bands['resolution'],
               'mean_ndvi': float(ndvi.mean()),
               'std_ndvi': float(ndvi.std()),
               'ndvi_data': ndvi
           }
           
           print(f"  {sensor}: Mean NDVI = {sensor_data[sensor]['mean_ndvi']:.3f}")
       
       # Compare results
       if len(sensor_data) >= 2:
           sensors_list = list(sensor_data.keys())
           s1, s2 = sensors_list[0], sensors_list[1]
           
           ndvi_diff = abs(sensor_data[s1]['mean_ndvi'] - sensor_data[s2]['mean_ndvi'])
           
           print(f"\nCross-sensor comparison:")
           print(f"  NDVI difference: {ndvi_diff:.3f}")
           print(f"  Date difference: {sensor_data[s1]['date']} vs {sensor_data[s2]['date']}")
           
           # Resample to same resolution for pixel-wise comparison
           if sensor_data[s1]['resolution'] != sensor_data[s2]['resolution']:
               print(f"  Note: Different resolutions ({sensor_data[s1]['resolution']}m vs {sensor_data[s2]['resolution']}m)")
       
       return sensor_data

   # Usage - Compare Sentinel-2 and Landsat over agricultural area
   ag_area_bbox = [-120.5, 36.0, -120.0, 36.5]
   comparison = compare_sensor_data(
       ag_area_bbox,
       "2024-07-01/2024-07-31"
   )

Production Pipeline Example
---------------------------

Automated Monitoring System
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   import schedule
   import time
   from datetime import datetime, timedelta

   class AutomatedMonitoring:
       """Production-ready automated monitoring system."""
       
       def __init__(self, config):
           self.config = config
           self.pc = ogapi.planetary_computer(auto_sign=True)
           
       def daily_monitoring(self):
           """Run daily monitoring tasks."""
           print(f"Starting daily monitoring: {datetime.now()}")
           
           for site in self.config['monitoring_sites']:
               try:
                   self.process_site(site)
               except Exception as e:
                   print(f"Error processing site {site['name']}: {e}")
           
           print("Daily monitoring completed")
       
       def process_site(self, site):
           """Process a single monitoring site."""
           print(f"Processing site: {site['name']}")
           
           # Search for recent data
           yesterday = (datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d')
           
           results = self.pc.search(
               collections=site['collections'],
               bbox=site['bbox'],
               datetime=f"{yesterday}/{yesterday}",
               query={'eo:cloud_cover': {'lt': site['max_cloud_cover']}},
               limit=5
           )
           
           items = results.get_all_items()
           
           if items:
               # Process the clearest image
               best_item = min(items, key=lambda x: x.properties.get('eo:cloud_cover', 100))
               
               # Download and analyze
               self.analyze_site(best_item, site)
           else:
               print(f"  No clear imagery found for {site['name']}")
       
       def analyze_site(self, item, site):
           """Analyze imagery for a site."""
           urls = item.get_band_urls(site['analysis_bands'])
           
           # Load and analyze data
           for band, url in urls.items():
               data = rxr.open_rasterio(url)
               
               # Calculate statistics
               mean_val = float(data.mean())
               std_val = float(data.std())
               
               # Check for anomalies
               if site.get('alert_thresholds'):
                   threshold = site['alert_thresholds'].get(band)
                   if threshold and (mean_val > threshold['max'] or mean_val < threshold['min']):
                       self.send_alert(site, band, mean_val, threshold)
           
           print(f"  Analysis completed for {item.id}")
       
       def send_alert(self, site, band, value, threshold):
           """Send alert for anomalous values."""
           print(f"🚨 ALERT: {site['name']} - {band} value {value:.3f} outside threshold {threshold}")
           # In production: send email, SMS, or webhook notification
       
       def run(self):
           """Run the monitoring system."""
           # Schedule daily runs
           schedule.every().day.at("09:00").do(self.daily_monitoring)
           
           print("Automated monitoring system started")
           while True:
               schedule.run_pending()
               time.sleep(60)  # Check every minute

   # Configuration
   monitoring_config = {
       'monitoring_sites': [
           {
               'name': 'California_Vineyard_01',
               'bbox': [-120.1, 38.5, -120.0, 38.6],
               'collections': ['sentinel-2-l2a'],
               'max_cloud_cover': 30,
               'analysis_bands': ['B04', 'B08'],  # Red, NIR for NDVI
               'alert_thresholds': {
                   'B08': {'min': 0.2, 'max': 0.8}  # NIR reflectance
               }
           },
           {
               'name': 'Water_Reservoir_Monitor',
               'bbox': [-121.0, 37.0, -120.9, 37.1],
               'collections': ['sentinel-2-l2a'],
               'max_cloud_cover': 20,
               'analysis_bands': ['B03', 'B08'],  # Green, NIR for water detection
               'alert_thresholds': {
                   'B03': {'min': 0.05, 'max': 0.3}  # Water reflectance
               }
           }
       ]
   }

   # Usage (for production deployment)
   # monitor = AutomatedMonitoring(monitoring_config)
   # monitor.run()  # Runs continuously

These real-world examples demonstrate complete, production-ready applications using Open Geodata API for various domains including agriculture, environmental monitoring, urban planning, climate research, disaster response, and automated monitoring systems.
