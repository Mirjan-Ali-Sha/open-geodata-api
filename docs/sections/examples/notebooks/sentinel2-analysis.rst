Sentinel-2 Analysis Notebook
=============================

Interactive Jupyter notebook for comprehensive Sentinel-2 data analysis.

Notebook Overview
-----------------

This notebook demonstrates a complete workflow for Sentinel-2 satellite imagery analysis, including:

- Data discovery and filtering
- Multi-temporal analysis
- NDVI calculation and visualization
- Change detection
- Export and reporting

Prerequisites
-------------

.. code-block:: bash

   pip install open-geodata-api[complete] jupyter matplotlib seaborn plotly folium

Notebook Sections
-----------------

**1. Setup and Configuration**

.. code-block:: python

   import open_geodata_api as ogapi
   import rioxarray as rxr
   import matplotlib.pyplot as plt
   import pandas as pd
   import numpy as np
   from open_geodata_api.utils import filter_by_cloud_cover

   # Setup
   pc = ogapi.planetary_computer(auto_sign=True)
   study_area = [-122.5, 47.5, -122.0, 48.0]  # Seattle area

**2. Data Discovery**

.. code-block:: python

   # Search for Sentinel-2 data
   results = pc.search(
       collections=['sentinel-2-l2a'],
       bbox=study_area,
       datetime='2024-01-01/2024-12-31',
       query={'eo:cloud_cover': {'lt': 50}},
       limit=50
   )
   
   items = results.get_all_items()
   print(f"Found {len(items)} Sentinel-2 scenes")
   
   # Convert to DataFrame for analysis
   df = items.to_dataframe()
   df.head()

**3. Quality Assessment and Filtering**

.. code-block:: python

   # Cloud cover analysis
   plt.figure(figsize=(12, 4))
   
   plt.subplot(1, 2, 1)
   plt.hist(df['eo:cloud_cover'], bins=20, alpha=0.7)
   plt.xlabel('Cloud Cover (%)')
   plt.ylabel('Number of Scenes')
   plt.title('Cloud Cover Distribution')
   
   plt.subplot(1, 2, 2)
   df['date'] = pd.to_datetime(df['datetime'])
   plt.scatter(df['date'], df['eo:cloud_cover'], alpha=0.6)
   plt.xlabel('Date')
   plt.ylabel('Cloud Cover (%)')
   plt.title('Cloud Cover Over Time')
   plt.xticks(rotation=45)
   
   plt.tight_layout()
   plt.show()

**4. Multi-temporal NDVI Analysis**

.. code-block:: python

   # Filter for clear images
   clear_items = filter_by_cloud_cover(items, max_cloud_cover=20)
   
   # Calculate NDVI time series
   ndvi_time_series = []
   
   for item in clear_items[:12]:  # Process first 12 clear scenes
       try:
           # Get NIR and Red bands
           urls = item.get_band_urls(['B08', 'B04'])
           
           nir = rxr.open_rasterio(urls['B08'])
           red = rxr.open_rasterio(urls['B04'])
           
           # Calculate NDVI
           ndvi = (nir - red) / (nir + red)
           
           # Calculate statistics
           ndvi_time_series.append({
               'date': item.properties['datetime'][:10],
               'mean_ndvi': float(ndvi.mean()),
               'std_ndvi': float(ndvi.std()),
               'cloud_cover': item.properties.get('eo:cloud_cover', 0)
           })
           
       except Exception as e:
           print(f"Error processing {item.id}: {e}")

**5. Visualization and Analysis**

.. code-block:: python

   # Create comprehensive visualization
   ndvi_df = pd.DataFrame(ndvi_time_series)
   ndvi_df['date'] = pd.to_datetime(ndvi_df['date'])
   
   fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(15, 10))
   
   # NDVI time series
   ax1.plot(ndvi_df['date'], ndvi_df['mean_ndvi'], 'o-', color='green')
   ax1.set_title('NDVI Time Series')
   ax1.set_ylabel('Mean NDVI')
   ax1.tick_params(axis='x', rotation=45)
   
   # NDVI distribution
   ax2.hist(ndvi_df['mean_ndvi'], bins=15, alpha=0.7, color='green')
   ax2.set_title('NDVI Distribution')
   ax2.set_xlabel('NDVI')
   ax2.set_ylabel('Frequency')
   
   # NDVI vs Cloud Cover
   ax3.scatter(ndvi_df['cloud_cover'], ndvi_df['mean_ndvi'], alpha=0.7)
   ax3.set_title('NDVI vs Cloud Cover')
   ax3.set_xlabel('Cloud Cover (%)')
   ax3.set_ylabel('Mean NDVI')
   
   # Seasonal patterns
   ndvi_df['month'] = ndvi_df['date'].dt.month
   monthly_ndvi = ndvi_df.groupby('month')['mean_ndvi'].mean()
   ax4.plot(monthly_ndvi.index, monthly_ndvi.values, 'o-', color='darkgreen')
   ax4.set_title('Seasonal NDVI Pattern')
   ax4.set_xlabel('Month')
   ax4.set_ylabel('Mean NDVI')
   ax4.set_xticks(range(1, 13))
   
   plt.tight_layout()
   plt.show()

**6. Export and Reporting**

.. code-block:: python

   # Create summary report
   summary = {
       'analysis_period': f"{ndvi_df['date'].min()} to {ndvi_df['date'].max()}",
       'total_scenes': len(ndvi_df),
       'mean_ndvi': ndvi_df['mean_ndvi'].mean(),
       'ndvi_range': [ndvi_df['mean_ndvi'].min(), ndvi_df['mean_ndvi'].max()],
       'seasonal_variation': monthly_ndvi.max() - monthly_ndvi.min()
   }
   
   print("=== Sentinel-2 NDVI Analysis Summary ===")
   for key, value in summary.items():
       print(f"{key}: {value}")
   
   # Export data
   ndvi_df.to_csv('sentinel2_ndvi_analysis.csv', index=False)
   print("\nData exported to: sentinel2_ndvi_analysis.csv")

Download and Run
----------------

1. **Download the complete notebook**:
   
   Visit the `examples repository <https://github.com/Mirjan-Ali-Sha/open-geodata-api-examples>`_
   and download ``sentinel2_analysis.ipynb``

2. **Start Jupyter**:

.. code-block:: bash

   jupyter notebook sentinel2_analysis.ipynb

3. **Run cells sequentially** and modify parameters as needed

Key Learning Outcomes
---------------------

After completing this notebook, you will understand:

✅ **Data Discovery** - How to find and filter Sentinel-2 imagery  
✅ **Quality Assessment** - Evaluating data quality using cloud cover  
✅ **Multi-temporal Analysis** - Working with time series satellite data  
✅ **NDVI Calculation** - Computing vegetation indices from spectral bands  
✅ **Visualization** - Creating informative plots and charts  
✅ **Export Workflows** - Saving results for further analysis  

Extensions
----------

Try these extensions to deepen your understanding:

- **Change Detection**: Compare NDVI between two time periods
- **Spatial Analysis**: Focus on specific land cover types
- **Cross-sensor Comparison**: Compare with Landsat data
- **Advanced Indices**: Calculate EVI, SAVI, or other vegetation indices
- **Interactive Maps**: Use Folium for interactive visualizations
