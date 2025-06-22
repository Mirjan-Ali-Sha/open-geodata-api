Integration Examples
====================

Examples of integrating Open Geodata API with popular Python libraries and tools.

Integration with Dask
---------------------

Parallel Processing Large Datasets
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   import dask
   from dask.distributed import Client
   import open_geodata_api as ogapi
   from open_geodata_api.utils import download_items
   
   def setup_dask_processing():
       """Set up Dask for parallel satellite data processing."""
       
       # Start Dask client
       client = Client('localhost:8786')  # Or use local client
       print(f"Dask dashboard: {client.dashboard_link}")
       
       return client
   
   @dask.delayed
   def process_single_item(item, bands=['B04', 'B03', 'B02']):
       """Process a single STAC item (delayed function)."""
       import rioxarray as rxr
       import numpy as np
       
       try:
           # Get URLs for required bands
           urls = item.get_band_urls(bands)
           
           # Load data lazily
           data_arrays = {}
           for band, url in urls.items():
               data_arrays[band] = rxr.open_rasterio(url, chunks={'x': 512, 'y': 512})
           
           # Calculate NDVI if NIR and Red available
           if 'B08' in data_arrays and 'B04' in data_arrays:
               nir = data_arrays['B08']
               red = data_arrays['B04']
               ndvi = (nir - red) / (nir + red)
               
               return {
                   'item_id': item.id,
                   'date': item.properties['datetime'][:10],
                   'mean_ndvi': float(ndvi.mean().compute()),
                   'std_ndvi': float(ndvi.std().compute())
               }
           
           return {'item_id': item.id, 'status': 'processed'}
           
       except Exception as e:
           return {'item_id': item.id, 'error': str(e)}
   
   def dask_batch_processing(items, max_workers=4):
       """Process items in parallel using Dask."""
       
       # Create delayed computations
       delayed_results = []
       for item in items:
           delayed_result = process_single_item(item, ['B08', 'B04', 'B03', 'B02'])
           delayed_results.append(delayed_result)
       
       # Execute computations in parallel
       print(f"Processing {len(items)} items with Dask...")
       results = dask.compute(*delayed_results, scheduler='threads', num_workers=max_workers)
       
       return list(results)
   
   # Usage
   pc = ogapi.planetary_computer(auto_sign=True)
   results = pc.search(collections=['sentinel-2-l2a'], limit=20)
   items = results.get_all_items()
   
   # Process with Dask
   dask_results = dask_batch_processing(items[:10])
   
   for result in dask_results:
       if 'mean_ndvi' in result:
           print(f"{result['item_id']}: NDVI = {result['mean_ndvi']:.3f}")

Integration with GeoPandas
--------------------------

Spatial Analysis with Vector Data
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   import geopandas as gpd
   from shapely.geometry import box
   import open_geodata_api as ogapi
   from open_geodata_api.utils import filter_by_cloud_cover
   
   def analyze_by_administrative_boundaries():
       """Analyze satellite data by administrative boundaries."""
       
       # Load administrative boundaries (example: US counties)
       # You could load this from any source
       counties = gpd.read_file('path_to_counties.shp')  # Or use web service
       
       # Example: Focus on California counties
       ca_counties = counties[counties['STATE'] == 'CA'].head(5)
       
       pc = ogapi.planetary_computer(auto_sign=True)
       county_analysis = {}
       
       for idx, county in ca_counties.iterrows():
           county_name = county['NAME']
           county_geom = county.geometry
           
           # Convert geometry to bbox for search
           bbox = [county_geom.bounds[0], county_geom.bounds[1], 
                   county_geom.bounds[2], county_geom.bounds[3]]
           
           print(f"Analyzing {county_name} County...")
           
           # Search for satellite data
           results = pc.search(
               collections=['sentinel-2-l2a'],
               bbox=bbox,
               datetime='2024-06-01/2024-08-31',
               query={'eo:cloud_cover': {'lt': 30}},
               limit=10
           )
           
           items = results.get_all_items()
           clear_items = filter_by_cloud_cover(items, max_cloud_cover=20)
           
           if clear_items:
               # Analyze data for this county
               analysis_results = analyze_county_data(clear_items, county_geom)
               county_analysis[county_name] = analysis_results
           
       return county_analysis
   
   def analyze_county_data(items, county_geometry):
       """Analyze satellite data clipped to county boundary."""
       import rioxarray as rxr
       import rasterio.mask
       
       # Use the clearest image
       best_item = min(items, key=lambda x: x.properties.get('eo:cloud_cover', 100))
       
       # Get NDVI bands
       urls = best_item.get_band_urls(['B08', 'B04'])  # NIR, Red
       
       # Load and clip data to county boundary
       nir = rxr.open_rasterio(urls['B08'])
       red = rxr.open_rasterio(urls['B04'])
       
       # Clip to county boundary
       nir_clipped = nir.rio.clip([county_geometry], crs=nir.rio.crs)
       red_clipped = red.rio.clip([county_geometry], crs=red.rio.crs)
       
       # Calculate NDVI
       ndvi = (nir_clipped - red_clipped) / (nir_clipped + red_clipped)
       
       # Calculate statistics
       return {
           'date': best_item.properties['datetime'][:10],
           'cloud_cover': best_item.properties.get('eo:cloud_cover'),
           'mean_ndvi': float(ndvi.mean()),
           'median_ndvi': float(ndvi.median()),
           'std_ndvi': float(ndvi.std()),
           'area_pixels': int(ndvi.count())
       }

Integration with Plotly
-----------------------

Interactive Visualizations
~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   import plotly.graph_objects as go
   import plotly.express as px
   from plotly.subplots import make_subplots
   import pandas as pd
   
   def create_interactive_dashboard(time_series_data):
       """Create interactive dashboard for satellite data analysis."""
       
       # Create subplots
       fig = make_subplots(
           rows=2, cols=2,
           subplot_titles=('NDVI Time Series', 'Cloud Cover Distribution', 
                          'Data Availability', 'Quality Metrics'),
           specs=[[{"secondary_y": True}, {"type": "histogram"}],
                  [{"type": "bar"}, {"type": "scatter"}]]
       )
       
       # Convert data to DataFrame
       df = pd.DataFrame(time_series_data)
       df['date'] = pd.to_datetime(df['date'])
       
       # 1. NDVI Time Series
       fig.add_trace(
           go.Scatter(x=df['date'], y=df['ndvi'], name='NDVI', line=dict(color='green')),
           row=1, col=1
       )
       
       # Add cloud cover on secondary y-axis
       fig.add_trace(
           go.Scatter(x=df['date'], y=df['cloud_cover'], name='Cloud Cover (%)', 
                     line=dict(color='gray', dash='dash')),
           row=1, col=1, secondary_y=True
       )
       
       # 2. Cloud Cover Distribution
       fig.add_trace(
           go.Histogram(x=df['cloud_cover'], name='Cloud Cover', nbinsx=20),
           row=1, col=2
       )
       
       # 3. Data Availability by Month
       monthly_counts = df.groupby(df['date'].dt.month).size()
       fig.add_trace(
           go.Bar(x=monthly_counts.index, y=monthly_counts.values, name='Scenes per Month'),
           row=2, col=1
       )
       
       # 4. Quality vs Availability
       fig.add_trace(
           go.Scatter(x=df['cloud_cover'], y=df['ndvi'], mode='markers', 
                     name='Quality vs Cloud Cover',
                     marker=dict(color=df['ndvi'], colorscale='Viridis', showscale=True)),
           row=2, col=2
       )
       
       # Update layout
       fig.update_layout(
           title_text="Satellite Data Analysis Dashboard",
           showlegend=True,
           height=800
       )
       
       # Update y-axis labels
       fig.update_yaxes(title_text="NDVI", row=1, col=1)
       fig.update_yaxes(title_text="Cloud Cover (%)", row=1, col=1, secondary_y=True)
       fig.update_yaxes(title_text="Frequency", row=1, col=2)
       fig.update_yaxes(title_text="Scene Count", row=2, col=1)
       fig.update_yaxes(title_text="NDVI", row=2, col=2)
       
       # Update x-axis labels
       fig.update_xaxes(title_text="Date", row=1, col=1)
       fig.update_xaxes(title_text="Cloud Cover (%)", row=1, col=2)
       fig.update_xaxes(title_text="Month", row=2, col=1)
       fig.update_xaxes(title_text="Cloud Cover (%)", row=2, col=2)
       
       return fig
   
   def create_map_visualization(items):
       """Create interactive map of search results."""
       
       # Extract metadata
       map_data = []
       for item in items:
           map_data.append({
               'id': item.id,
               'date': item.properties['datetime'][:10],
               'cloud_cover': item.properties.get('eo:cloud_cover', 0),
               'center_lat': sum(item.bbox[1::2]) / 2,  # Average of lat bounds
               'center_lon': sum(item.bbox[0::2]) / 2,  # Average of lon bounds
           })
       
       df = pd.DataFrame(map_data)
       
       # Create map
       fig = px.scatter_mapbox(
           df, lat='center_lat', lon='center_lon',
           color='cloud_cover',
           size='cloud_cover',
           hover_data=['id', 'date'],
           color_continuous_scale='RdYlBu_r',
           mapbox_style='open-street-map',
           title='Satellite Scene Locations and Quality'
       )
       
       fig.update_layout(
           mapbox=dict(center=dict(lat=df['center_lat'].mean(), 
                                  lon=df['center_lon'].mean()),
                      zoom=8),
           height=600
       )
       
       return fig

Integration with Jupyter Widgets
---------------------------------

Interactive Notebooks
~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   import ipywidgets as widgets
   from IPython.display import display
   import open_geodata_api as ogapi
   
   def create_interactive_search_widget():
       """Create interactive widget for satellite data search."""
       
       # Define widgets
       provider_widget = widgets.Dropdown(
           options=['pc', 'es'],
           value='pc',
           description='Provider:'
       )
       
       collection_widget = widgets.Dropdown(
           options=['sentinel-2-l2a', 'landsat-c2-l2'],
           value='sentinel-2-l2a',
           description='Collection:'
       )
       
       bbox_widget = widgets.Text(
           value='-122.5,47.5,-122.0,48.0',
           description='Bbox:'
       )
       
       date_range_widget = widgets.Text(
           value='2024-06-01/2024-08-31',
           description='Date Range:'
       )
       
       cloud_cover_widget = widgets.FloatSlider(
           value=30,
           min=0,
           max=100,
           step=5,
           description='Max Cloud Cover:'
       )
       
       limit_widget = widgets.IntSlider(
           value=10,
           min=1,
           max=50,
           description='Max Results:'
       )
       
       search_button = widgets.Button(description='Search')
       output_widget = widgets.Output()
       
       # Search function
       def on_search_click(b):
           with output_widget:
               output_widget.clear_output()
               
               try:
                   # Parse inputs
                   bbox = [float(x.strip()) for x in bbox_widget.value.split(',')]
                   
                   # Create client
                   if provider_widget.value == 'pc':
                       client = ogapi.planetary_computer(auto_sign=True)
                   else:
                       client = ogapi.earth_search()
                   
                   # Perform search
                   print(f"Searching {provider_widget.value.upper()}...")
                   results = client.search(
                       collections=[collection_widget.value],
                       bbox=bbox,
                       datetime=date_range_widget.value,
                       query={'eo:cloud_cover': {'lt': cloud_cover_widget.value}},
                       limit=limit_widget.value
                   )
                   
                   items = results.get_all_items()
                   print(f"Found {len(items)} items")
                   
                   # Display results
                   if items:
                       df = items.to_dataframe()
                       display(df[['datetime', 'eo:cloud_cover', 'platform']])
                   
               except Exception as e:
                   print(f"Search failed: {e}")
       
       search_button.on_click(on_search_click)
       
       # Layout
       search_form = widgets.VBox([
           provider_widget,
           collection_widget,
           bbox_widget,
           date_range_widget,
           cloud_cover_widget,
           limit_widget,
           search_button
       ])
       
       return widgets.VBox([search_form, output_widget])

Integration with MLflow
-----------------------

Experiment Tracking
~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   import mlflow
   import mlflow.sklearn
   import numpy as np
   from sklearn.ensemble import RandomForestRegressor
   from sklearn.model_selection import train_test_split
   from sklearn.metrics import mean_squared_error, r2_score
   
   def ml_experiment_with_satellite_data():
       """Run ML experiment with satellite data tracking."""
       
       # Start MLflow experiment
       mlflow.set_experiment("satellite_data_ndvi_prediction")
       
       with mlflow.start_run():
           # Log parameters
           mlflow.log_param("data_source", "sentinel-2-l2a")
           mlflow.log_param("provider", "planetary_computer")
           mlflow.log_param("max_cloud_cover", 20)
           
           # Get satellite data
           pc = ogapi.planetary_computer(auto_sign=True)
           results = pc.search(
               collections=['sentinel-2-l2a'],
               bbox=[-120.0, 36.0, -119.5, 36.5],
               datetime='2024-01-01/2024-06-30',
               query={'eo:cloud_cover': {'lt': 20}},
               limit=50
           )
           
           items = results.get_all_items()
           mlflow.log_param("total_scenes", len(items))
           
           # Extract features and targets (example)
           features = []
           targets = []
           
           for item in items[:20]:  # Subset for example
               try:
                   # Get spectral bands
                   urls = item.get_band_urls(['B02', 'B03', 'B04', 'B08'])
                   
                   # Load data and calculate features
                   bands_data = {}
                   for band, url in urls.items():
                       data = rxr.open_rasterio(url)
                       bands_data[band] = float(data.mean())
                   
                   # Features: reflectance values
                   feature_vector = [bands_data['B02'], bands_data['B03'], 
                                   bands_data['B04'], bands_data['B08']]
                   
                   # Target: NDVI
                   nir = bands_data['B08']
                   red = bands_data['B04']
                   ndvi = (nir - red) / (nir + red)
                   
                   features.append(feature_vector)
                   targets.append(ndvi)
                   
               except Exception as e:
                   print(f"Error processing {item.id}: {e}")
                   continue
           
           # Convert to arrays
           X = np.array(features)
           y = np.array(targets)
           
           mlflow.log_param("features_shape", X.shape)
           mlflow.log_param("targets_shape", y.shape)
           
           # Split data
           X_train, X_test, y_train, y_test = train_test_split(
               X, y, test_size=0.2, random_state=42
           )
           
           # Train model
           model = RandomForestRegressor(n_estimators=100, random_state=42)
           model.fit(X_train, y_train)
           
           # Make predictions
           y_pred = model.predict(X_test)
           
           # Calculate metrics
           mse = mean_squared_error(y_test, y_pred)
           r2 = r2_score(y_test, y_pred)
           
           # Log metrics
           mlflow.log_metric("mse", mse)
           mlflow.log_metric("r2_score", r2)
           
           # Log model
           mlflow.sklearn.log_model(model, "random_forest_model")
           
           print(f"Experiment completed: MSE={mse:.4f}, R2={r2:.4f}")
           
           return model, (mse, r2)

Integration with Streamlit
--------------------------

Web Applications
~~~~~~~~~~~~~~~~

.. code-block:: python

   import streamlit as st
   import pandas as pd
   import plotly.express as px
   import open_geodata_api as ogapi
   from open_geodata_api.utils import filter_by_cloud_cover
   
   def create_streamlit_app():
       """Create Streamlit web app for satellite data exploration."""
       
       st.title("🛰️ Satellite Data Explorer")
       st.markdown("Interactive exploration of satellite imagery using Open Geodata API")
       
       # Sidebar controls
       st.sidebar.header("Search Parameters")
       
       provider = st.sidebar.selectbox("Provider", ["pc", "es"], index=0)
       collection = st.sidebar.selectbox(
           "Collection", 
           ["sentinel-2-l2a", "landsat-c2-l2"]
       )
       
       # Bbox input
       st.sidebar.subheader("Area of Interest")
       col1, col2 = st.sidebar.columns(2)
       with col1:
           west = st.number_input("West", value=-122.5)
           south = st.number_input("South", value=47.5)
       with col2:
           east = st.number_input("East", value=-122.0)
           north = st.number_input("North", value=48.0)
       
       bbox = [west, south, east, north]
       
       # Date range
       date_range = st.sidebar.text_input(
           "Date Range", 
           value="2024-06-01/2024-08-31"
       )
       
       # Quality filters
       max_cloud_cover = st.sidebar.slider("Max Cloud Cover (%)", 0, 100, 30)
       max_results = st.sidebar.slider("Max Results", 1, 50, 10)
       
       # Search button
       if st.sidebar.button("Search"):
           with st.spinner("Searching for satellite data..."):
               try:
                   # Create client
                   if provider == "pc":
                       client = ogapi.planetary_computer(auto_sign=True)
                   else:
                       client = ogapi.earth_search()
                   
                   # Perform search
                   results = client.search(
                       collections=[collection],
                       bbox=bbox,
                       datetime=date_range,
                       query={'eo:cloud_cover': {'lt': max_cloud_cover}},
                       limit=max_results
                   )
                   
                   items = results.get_all_items()
                   
                   if items:
                       st.success(f"Found {len(items)} items!")
                       
                       # Store in session state
                       st.session_state['items'] = items
                       st.session_state['search_params'] = {
                           'provider': provider,
                           'collection': collection,
                           'bbox': bbox,
                           'date_range': date_range
                       }
                   else:
                       st.warning("No items found. Try adjusting your search parameters.")
                       
               except Exception as e:
                   st.error(f"Search failed: {e}")
       
       # Display results
       if 'items' in st.session_state:
           items = st.session_state['items']
           
           # Create tabs
           tab1, tab2, tab3 = st.tabs(["📊 Results", "🗺️ Map", "📈 Analysis"])
           
           with tab1:
               st.subheader("Search Results")
               
               # Convert to dataframe
               df = items.to_dataframe(include_geometry=False)
               
               # Display table
               st.dataframe(df[['datetime', 'eo:cloud_cover', 'platform']])
               
               # Download button
               csv = df.to_csv(index=False)
               st.download_button(
                   label="Download CSV",
                   data=csv,
                   file_name="satellite_search_results.csv",
                   mime="text/csv"
               )
           
           with tab2:
               st.subheader("Scene Locations")
               
               # Create map data
               map_data = []
               for item in items:
                   map_data.append({
                       'lat': sum(item.bbox[1::2]) / 2,
                       'lon': sum(item.bbox[0::2]) / 2,
                       'cloud_cover': item.properties.get('eo:cloud_cover', 0),
                       'date': item.properties['datetime'][:10]
                   })
               
               map_df = pd.DataFrame(map_data)
               
               # Plot map
               fig = px.scatter_mapbox(
                   map_df, lat='lat', lon='lon',
                   color='cloud_cover',
                   hover_data=['date'],
                   color_continuous_scale='RdYlBu_r',
                   mapbox_style='open-street-map',
                   zoom=8
               )
               
               st.plotly_chart(fig, use_container_width=True)
           
           with tab3:
               st.subheader("Data Analysis")
               
               # Cloud cover distribution
               fig_hist = px.histogram(
                   df, x='eo:cloud_cover',
                   title="Cloud Cover Distribution",
                   nbins=20
               )
               st.plotly_chart(fig_hist, use_container_width=True)
               
               # Time series
               df['date'] = pd.to_datetime(df['datetime'])
               fig_time = px.scatter(
                   df, x='date', y='eo:cloud_cover',
                   title="Cloud Cover Over Time"
               )
               st.plotly_chart(fig_time, use_container_width=True)
   
   # Run the app with: streamlit run app.py
   if __name__ == "__main__":
       create_streamlit_app()

These integration examples show how to combine Open Geodata API with popular Python libraries for advanced data processing, visualization, machine learning, and web application development.
