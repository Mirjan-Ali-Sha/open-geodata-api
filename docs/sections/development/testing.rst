Testing Guide
=============

This guide covers testing practices, tools, and procedures for Open Geodata API.

Testing Philosophy
------------------

Our testing approach follows these principles:

**Comprehensive Coverage**
  Test all public APIs, error conditions, and integration points

**Fast Feedback**
  Unit tests execute quickly (<1s each) for rapid development cycles

**Realistic Integration**
  Integration tests use real APIs but are carefully rate-limited

**Deterministic Results**
  Tests produce consistent results across environments

**Clear Failures**
  Test failures provide actionable information for debugging

Test Structure
--------------

Test Organization
~~~~~~~~~~~~~~~~~

.. code-block:: text

   tests/
   ├── conftest.py              # Shared fixtures and configuration
   ├── unit/                    # Fast unit tests (no external calls)
   │   ├── test_core.py         # Core data model tests
   │   ├── test_clients.py      # Client logic tests (mocked)
   │   ├── test_utils.py        # Utility function tests
   │   └── test_cli.py          # CLI command tests (mocked)
   ├── integration/             # Real API integration tests
   │   ├── test_pc_integration.py     # Planetary Computer tests
   │   ├── test_es_integration.py     # EarthSearch tests
   │   └── test_cross_provider.py     # Multi-provider tests
   ├── performance/             # Performance and load tests
   │   ├── test_benchmarks.py   # Performance benchmarks
   │   └── test_memory.py       # Memory usage tests
   ├── fixtures/                # Test data and mock responses
   │   ├── sample_item.json     # Sample STAC item
   │   ├── sample_collection.json # Sample collection metadata
   │   └── mock_responses.py    # Mock API responses
   └── e2e/                     # End-to-end workflow tests
       ├── test_full_workflow.py # Complete user workflows
       └── test_cli_workflows.py # CLI workflow tests

Running Tests
-------------

Basic Test Execution
~~~~~~~~~~~~~~~~~~~~~

.. code-block:: bash

   # Run all tests
   pytest
   
   # Run with coverage
   pytest --cov=open_geodata_api
   
   # Run specific test categories
   pytest tests/unit/           # Unit tests only
   pytest tests/integration/    # Integration tests only
   
   # Run specific test file
   pytest tests/unit/test_core.py
   
   # Run specific test
   pytest tests/unit/test_core.py::test_stac_item_creation

Test Configuration
~~~~~~~~~~~~~~~~~~

Configure test execution with ``pytest.ini``:

.. code-block:: ini

   [tool:pytest]
   testpaths = tests
   python_files = test_*.py
   python_classes = Test*
   python_functions = test_*
   addopts = 
       --strict-markers
       --disable-warnings
       --tb=short
   markers =
       unit: Unit tests (no external dependencies)
       integration: Integration tests (real API calls)
       slow: Slow tests (> 5 seconds)
       cli: CLI-specific tests

Environment Variables
~~~~~~~~~~~~~~~~~~~~~

Control test behavior with environment variables:

.. code-block:: bash

   # Skip integration tests (for CI without API access)
   export SKIP_INTEGRATION_TESTS=1
   
   # Use specific test data location
   export TEST_DATA_DIR=/path/to/test/data
   
   # Enable detailed API logging in tests
   export TEST_API_DEBUG=1
   
   # Run tests with specific provider
   export TEST_PROVIDER=planetary_computer

Unit Testing
------------

Core Model Tests
~~~~~~~~~~~~~~~~

Test the core STAC data models:

.. code-block:: python

   # tests/unit/test_core.py
   import pytest
   from open_geodata_api.core.items import STACItem, STACAsset, STACItemCollection

   class TestSTACItem:
       """Test STACItem functionality."""
       
       def test_item_creation_from_valid_data(self, sample_item_data):
           """Test creating STACItem from valid STAC data."""
           item = STACItem(sample_item_data, provider='test_provider')
           
           assert item.id == sample_item_data['id']
           assert item.collection == sample_item_data['collection']
           assert item.provider == 'test_provider'
           assert len(item.assets) == len(sample_item_data['assets'])
       
       def test_item_creation_with_missing_id_raises_error(self):
           """Test that missing ID raises appropriate error."""
           invalid_data = {'collection': 'test', 'assets': {}}
           
           with pytest.raises(KeyError, match='id'):
               STACItem(invalid_data)
       
       def test_get_asset_url_returns_correct_url(self, sample_item):
           """Test asset URL retrieval."""
           url = sample_item.get_asset_url('B04')
           
           assert url.startswith('https://')
           assert 'B04' in url or 'red' in url  # Provider-specific naming
       
       def test_get_asset_url_with_invalid_asset_raises_error(self, sample_item):
           """Test error handling for invalid asset names."""
           with pytest.raises(KeyError, match='INVALID_ASSET'):
               sample_item.get_asset_url('INVALID_ASSET')
       
       def test_list_assets_returns_all_asset_names(self, sample_item):
           """Test asset name listing."""
           assets = sample_item.list_assets()
           
           assert isinstance(assets, list)
           assert len(assets) > 0
           assert all(isinstance(asset, str) for asset in assets)

   class TestSTACItemCollection:
       """Test STACItemCollection functionality."""
       
       def test_collection_creation_from_items_list(self, sample_items_data):
           """Test creating collection from list of items."""
           collection = STACItemCollection(sample_items_data, provider='test')
           
           assert len(collection) == len(sample_items_data)
           assert all(isinstance(item, STACItem) for item in collection)
       
       def test_to_dataframe_creates_valid_dataframe(self, sample_collection):
           """Test DataFrame conversion."""
           df = sample_collection.to_dataframe()
           
           assert len(df) == len(sample_collection)
           assert 'id' in df.columns
           assert 'datetime' in df.columns
           assert 'eo:cloud_cover' in df.columns
       
       def test_get_all_urls_returns_nested_dict(self, sample_collection):
           """Test bulk URL retrieval."""
           urls = sample_collection.get_all_urls(['B04', 'B03'])
           
           assert isinstance(urls, dict)
           assert len(urls) == len(sample_collection)
           
           for item_id, item_urls in urls.items():
               assert isinstance(item_urls, dict)
               assert 'B04' in item_urls or 'red' in item_urls

Client Tests (Mocked)
~~~~~~~~~~~~~~~~~~~~~

Test client logic without making real API calls:

.. code-block:: python

   # tests/unit/test_clients.py
   import pytest
   from unittest.mock import Mock, patch
   from open_geodata_api.clients.planetary_computer import PlanetaryComputerCollections

   class TestPlanetaryComputerClient:
       """Test Planetary Computer client with mocked responses."""
       
       @patch('requests.get')
       def test_list_collections_success(self, mock_get, mock_collections_response):
           """Test successful collection listing."""
           mock_get.return_value.json.return_value = mock_collections_response
           mock_get.return_value.status_code = 200
           
           client = PlanetaryComputerCollections()
           collections = client.list_collections()
           
           assert isinstance(collections, list)
           assert len(collections) > 0
           mock_get.assert_called_once()
       
       @patch('requests.get')
       def test_list_collections_handles_api_error(self, mock_get):
           """Test error handling for API failures."""
           mock_get.return_value.status_code = 500
           mock_get.return_value.raise_for_status.side_effect = Exception("API Error")
           
           client = PlanetaryComputerCollections()
           
           with pytest.raises(Exception, match="API Error"):
               client.list_collections()
       
       @patch('requests.post')
       def test_search_with_valid_parameters(self, mock_post, mock_search_response):
           """Test search with valid parameters."""
           mock_post.return_value.json.return_value = mock_search_response
           mock_post.return_value.status_code = 200
           
           client = PlanetaryComputerCollections()
           results = client.search(
               collections=['sentinel-2-l2a'],
               bbox=[-122, 47, -121, 48],
               datetime='2024-01-01/2024-03-31'
           )
           
           assert results is not None
           assert len(results.get_all_items()) > 0
           
           # Verify request parameters
           call_args = mock_post.call_args
           request_body = call_args[1]['json']
           assert request_body['collections'] == ['sentinel-2-l2a']
           assert request_body['bbox'] == [-122, 47, -121, 48]

Utility Function Tests
~~~~~~~~~~~~~~~~~~~~~~

Test utility functions with various inputs:

.. code-block:: python

   # tests/unit/test_utils.py
   import pytest
   from open_geodata_api.utils import filter_by_cloud_cover, is_url_expired

   class TestFilteringFunctions:
       """Test data filtering utilities."""
       
       def test_filter_by_cloud_cover_removes_cloudy_items(self, sample_collection):
           """Test cloud cover filtering."""
           # Add cloud cover properties to test items
           for i, item in enumerate(sample_collection):
               item.properties['eo:cloud_cover'] = i * 10  # 0%, 10%, 20%, etc.
           
           filtered = filter_by_cloud_cover(sample_collection, max_cloud_cover=15)
           
           # Should keep items with 0% and 10% cloud cover
           assert len(filtered) == 2
           for item in filtered:
               assert item.properties['eo:cloud_cover'] <= 15
       
       def test_filter_by_cloud_cover_handles_missing_cloud_data(self, sample_collection):
           """Test handling of items without cloud cover data."""
           # Remove cloud cover from some items
           for item in sample_collection[::2]:  # Every other item
               item.properties.pop('eo:cloud_cover', None)
           
           filtered = filter_by_cloud_cover(sample_collection, max_cloud_cover=20)
           
           # Should handle missing data gracefully
           assert isinstance(filtered, type(sample_collection))

   class TestURLManagement:
       """Test URL management utilities."""
       
       @pytest.mark.parametrize("url,expected", [
           ("https://example.com/data.tif", False),
           ("https://example.com/data.tif?sig=abc123", True),
           ("https://pc.example.com/data.tif?st=2024&se=2025", True),
       ])
       def test_is_signed_url_detection(self, url, expected):
           """Test signed URL detection."""
           from open_geodata_api.utils import is_signed_url
           
           assert is_signed_url(url) == expected
       
       def test_url_expiration_check_with_valid_url(self):
           """Test URL expiration checking."""
           # Create URL with future expiration
           future_url = "https://example.com/data.tif?se=2030-01-01T00:00:00Z"
           
           assert not is_url_expired(future_url)
       
       def test_url_expiration_check_with_expired_url(self):
           """Test detection of expired URLs."""
           # Create URL with past expiration
           past_url = "https://example.com/data.tif?se=2020-01-01T00:00:00Z"
           
           assert is_url_expired(past_url)

CLI Tests (Mocked)
~~~~~~~~~~~~~~~~~~

Test CLI commands without making external calls:

.. code-block:: python

   # tests/unit/test_cli.py
   import pytest
   from click.testing import CliRunner
   from unittest.mock import patch, Mock
   from open_geodata_api.cli.main import cli

   class TestCLICommands:
       """Test CLI command functionality."""
       
       def setup_method(self):
           """Set up test fixtures."""
           self.runner = CliRunner()
       
       def test_main_cli_help(self):
           """Test main CLI help command."""
           result = self.runner.invoke(cli, ['--help'])
           
           assert result.exit_code == 0
           assert 'Open Geodata API' in result.output
           assert 'collections' in result.output
           assert 'search' in result.output
       
       @patch('open_geodata_api.planetary_computer')
       def test_collections_list_command(self, mock_pc):
           """Test collections list command."""
           # Mock client and response
           mock_client = Mock()
           mock_client.list_collections.return_value = ['sentinel-2-l2a', 'landsat-c2-l2']
           mock_pc.return_value = mock_client
           
           result = self.runner.invoke(cli, ['collections', 'list', '--provider', 'pc'])
           
           assert result.exit_code == 0
           assert 'sentinel-2-l2a' in result.output
           assert 'landsat-c2-l2' in result.output
           mock_client.list_collections.assert_called_once()
       
       @patch('open_geodata_api.planetary_computer')
       def test_search_items_command_with_valid_params(self, mock_pc):
           """Test search items command with valid parameters."""
           # Mock search results
           mock_client = Mock()
           mock_results = Mock()
           mock_items = Mock()
           mock_items.__len__ = Mock(return_value=5)
           mock_results.get_all_items.return_value = mock_items
           mock_client.search.return_value = mock_results
           mock_pc.return_value = mock_client
           
           result = self.runner.invoke(cli, [
               'search', 'items',
               '--collections', 'sentinel-2-l2a',
               '--bbox', '-122,47,-121,48',
               '--datetime', '2024-01-01/2024-03-31'
           ])
           
           assert result.exit_code == 0
           assert 'Found 5 items' in result.output
           mock_client.search.assert_called_once()
       
       def test_search_items_command_with_invalid_bbox(self):
           """Test error handling for invalid bbox format."""
           result = self.runner.invoke(cli, [
               'search', 'items',
               '--collections', 'sentinel-2-l2a',
               '--bbox', 'invalid-bbox-format'
           ])
           
           assert result.exit_code != 0
           assert 'bbox must be comma-separated numbers' in result.output

Integration Testing
-------------------

Real API Tests
~~~~~~~~~~~~~~

Integration tests that make real API calls (rate-limited):

.. code-block:: python

   # tests/integration/test_pc_integration.py
   import pytest
   import os
   from open_geodata_api import planetary_computer

   @pytest.mark.integration
   @pytest.mark.skipif(
       os.getenv('SKIP_INTEGRATION_TESTS'), 
       reason="Integration tests disabled"
   )
   class TestPlanetaryComputerIntegration:
       """Integration tests with real Planetary Computer API."""
       
       def setup_method(self):
           """Set up test client."""
           self.pc = planetary_computer(auto_sign=True)
       
       def test_list_collections_returns_real_data(self):
           """Test that we can list real collections."""
           collections = self.pc.list_collections()
           
           assert isinstance(collections, list)
           assert len(collections) > 10  # Should have many collections
           assert 'sentinel-2-l2a' in collections
       
       def test_get_collection_info_for_sentinel2(self):
           """Test getting real collection information."""
           info = self.pc.get_collection_info('sentinel-2-l2a')
           
           assert info is not None
           assert info['id'] == 'sentinel-2-l2a'
           assert 'title' in info
           assert 'description' in info
           assert 'extent' in info
       
       @pytest.mark.slow
       def test_search_returns_real_items(self):
           """Test search with real API (marked as slow)."""
           results = self.pc.search(
               collections=['sentinel-2-l2a'],
               bbox=[-122.5, 47.5, -122.0, 48.0],
               datetime='2024-01-01/2024-03-31',
               limit=5
           )
           
           items = results.get_all_items()
           assert len(items) > 0
           
           # Test item properties
           item = items[0]
           assert item.id is not None
           assert item.collection == 'sentinel-2-l2a'
           assert 'datetime' in item.properties
           
           # Test URL generation
           assets = item.list_assets()
           assert len(assets) > 0
           
           url = item.get_asset_url(assets[0])
           assert url.startswith('https://')

Cross-Provider Tests
~~~~~~~~~~~~~~~~~~~~

Tests that verify consistent behavior across providers:

.. code-block:: python

   # tests/integration/test_cross_provider.py
   import pytest
   from open_geodata_api import planetary_computer, earth_search

   @pytest.mark.integration
   class TestCrossProviderCompatibility:
       """Test consistent behavior across providers."""
       
       def setup_method(self):
           """Set up clients for both providers."""
           self.pc = planetary_computer(auto_sign=True)
           self.es = earth_search()
       
       def test_both_providers_support_sentinel2(self):
           """Test that both providers have Sentinel-2 data."""
           pc_collections = self.pc.list_collections()
           es_collections = self.es.list_collections()
           
           assert 'sentinel-2-l2a' in pc_collections
           assert 'sentinel-2-l2a' in es_collections
       
       def test_search_interface_consistency(self):
           """Test that search interface is consistent."""
           search_params = {
               'collections': ['sentinel-2-l2a'],
               'bbox': [-122.5, 47.5, -122.0, 48.0],
               'datetime': '2024-01-01/2024-03-31',
               'limit': 3
           }
           
           # Both clients should accept same parameters
           pc_results = self.pc.search(**search_params)
           es_results = self.es.search(**search_params)
           
           pc_items = pc_results.get_all_items()
           es_items = es_results.get_all_items()
           
           # Both should return STACItemCollection objects
           assert hasattr(pc_items, 'to_dataframe')
           assert hasattr(es_items, 'to_dataframe')
           
           # Items should have consistent structure
           if pc_items and es_items:
               pc_item = pc_items[0]
               es_item = es_items[0]
               
               assert hasattr(pc_item, 'get_asset_url')
               assert hasattr(es_item, 'get_asset_url')

Performance Testing
-------------------

Benchmark Tests
~~~~~~~~~~~~~~~

Measure performance of key operations:

.. code-block:: python

   # tests/performance/test_benchmarks.py
   import pytest
   import time
   from open_geodata_api import planetary_computer

   @pytest.mark.slow
   class TestPerformanceBenchmarks:
       """Performance benchmarks for key operations."""
       
       def test_search_performance(self, benchmark):
           """Benchmark search operation performance."""
           pc = planetary_computer(auto_sign=True)
           
           def search_operation():
               return pc.search(
                   collections=['sentinel-2-l2a'],
                   bbox=[-122.5, 47.5, -122.0, 48.0],
                   limit=10
               )
           
           result = benchmark(search_operation)
           assert result is not None
       
       def test_url_generation_performance(self, benchmark, sample_item):
           """Benchmark URL generation performance."""
           
           def url_generation():
               return sample_item.get_all_asset_urls()
           
           urls = benchmark(url_generation)
           assert len(urls) > 0
       
       def test_dataframe_conversion_performance(self, benchmark, large_item_collection):
           """Benchmark DataFrame conversion for large collections."""
           
           def dataframe_conversion():
               return large_item_collection.to_dataframe()
           
           df = benchmark(dataframe_conversion)
           assert len(df) == len(large_item_collection)

Memory Usage Tests
~~~~~~~~~~~~~~~~~~

Monitor memory usage for large operations:

.. code-block:: python

   # tests/performance/test_memory.py
   import pytest
   import psutil
   import os
   from open_geodata_api.utils import download_datasets

   class TestMemoryUsage:
       """Test memory usage patterns."""
       
       def get_memory_usage(self):
           """Get current memory usage in MB."""
           process = psutil.Process(os.getpid())
           return process.memory_info().rss / 1024 / 1024
       
       def test_large_collection_memory_usage(self, large_item_collection):
           """Test memory usage doesn't grow excessively with large collections."""
           initial_memory = self.get_memory_usage()
           
           # Perform memory-intensive operations
           df = large_item_collection.to_dataframe()
           urls = large_item_collection.get_all_urls(['B04', 'B03', 'B02'])
           
           final_memory = self.get_memory_usage()
           memory_increase = final_memory - initial_memory
           
           # Memory increase should be reasonable (< 100MB for test data)
           assert memory_increase < 100, f"Memory increased by {memory_increase:.1f}MB"

Test Fixtures
-------------

Shared Test Data
~~~~~~~~~~~~~~~~

Create reusable test fixtures:

.. code-block:: python

   # tests/conftest.py
   import pytest
   import json
   from pathlib import Path

   @pytest.fixture
   def sample_item_data():
       """Load sample STAC item data."""
       fixtures_dir = Path(__file__).parent / 'fixtures'
       with open(fixtures_dir / 'sample_item.json') as f:
           return json.load(f)

   @pytest.fixture
   def sample_item(sample_item_data):
       """Create sample STACItem instance."""
       from open_geodata_api.core.items import STACItem
       return STACItem(sample_item_data, provider='test_provider')

   @pytest.fixture
   def sample_collection(sample_items_data):
       """Create sample STACItemCollection."""
       from open_geodata_api.core.collections import STACItemCollection
       return STACItemCollection(sample_items_data, provider='test_provider')

   @pytest.fixture
   def mock_collections_response():
       """Mock API response for collections list."""
       return {
           "collections": [
               {"id": "sentinel-2-l2a", "title": "Sentinel-2 Level-2A"},
               {"id": "landsat-c2-l2", "title": "Landsat Collection 2 Level-2"}
           ]
       }

Mock Responses
~~~~~~~~~~~~~~

Create realistic mock API responses:

.. code-block:: python

   # tests/fixtures/mock_responses.py
   MOCK_SEARCH_RESPONSE = {
       "type": "FeatureCollection",
       "features": [
           {
               "type": "Feature",
               "id": "S2A_MSIL2A_20240615T180921_N0510_R027_T11ULA_20240616T000511",
               "collection": "sentinel-2-l2a",
               "properties": {
                   "datetime": "2024-06-15T18:09:21.024000Z",
                   "eo:cloud_cover": 12.5,
                   "platform": "sentinel-2a"
               },
               "assets": {
                   "B04": {
                       "href": "https://example.com/B04.tif",
                       "type": "image/tiff",
                       "title": "Red"
                   },
                   "B03": {
                       "href": "https://example.com/B03.tif", 
                       "type": "image/tiff",
                       "title": "Green"
                   }
               },
               "bbox": [-122.5, 47.5, -122.0, 48.0]
           }
       ]
   }

Continuous Integration
----------------------

GitHub Actions Configuration
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Configure automated testing:

.. code-block:: yaml

   # .github/workflows/test.yml
   name: Tests
   
   on: [push, pull_request]
   
   jobs:
     test:
       runs-on: ubuntu-latest
       strategy:
         matrix:
           python-version: [3.8, 3.9, '3.10', 3.11]
       
       steps:
       - uses: actions/checkout@v3
       
       - name: Set up Python ${{ matrix.python-version }}
         uses: actions/setup-python@v3
         with:
           python-version: ${{ matrix.python-version }}
       
       - name: Install dependencies
         run: |
           python -m pip install --upgrade pip
           pip install -e .[dev]
       
       - name: Run unit tests
         run: pytest tests/unit/ --cov=open_geodata_api
       
       - name: Run integration tests
         run: pytest tests/integration/ -m "not slow"
         env:
           SKIP_INTEGRATION_TESTS: ${{ secrets.SKIP_INTEGRATION_TESTS }}
       
       - name: Upload coverage
         uses: codecov/codecov-action@v3
         with:
           file: ./coverage.xml

Test Coverage
~~~~~~~~~~~~~

Maintain high test coverage:

.. code-block:: bash

   # Generate coverage report
   pytest --cov=open_geodata_api --cov-report=html --cov-report=xml
   
   # View coverage report
   open htmlcov/index.html
   
   # Coverage targets
   # - Overall: >90%
   # - Core modules: >95%
   # - Critical paths: 100%

Best Practices
--------------

Writing Good Tests
~~~~~~~~~~~~~~~~~~

**1. Test Names Should Be Descriptive**

.. code-block:: python

   # Good
   def test_search_with_invalid_bbox_raises_value_error():
       
   # Bad
   def test_search_error():

**2. Arrange-Act-Assert Pattern**

.. code-block:: python

   def test_filter_by_cloud_cover():
       # Arrange
       items = create_test_items_with_cloud_cover([10, 20, 30])
       
       # Act
       filtered = filter_by_cloud_cover(items, max_cloud_cover=25)
       
       # Assert
       assert len(filtered) == 2


**3. Test One Thing at a Time**

.. code-block:: python

   # Good - focused test
   def test_stac_item_has_correct_id():
       item = STACItem(sample_data)
       assert item.id == sample_data['id']
   
   def test_stac_item_has_correct_collection():
       item = STACItem(sample_data)
       assert item.collection == sample_data['collection']
   
   # Bad - testing multiple things
   def test_stac_item_properties():
       item = STACItem(sample_data)
       assert item.id == sample_data['id']
       assert item.collection == sample_data['collection']
       assert len(item.assets) > 0  # Different concern

**4. Use Descriptive Assertions**

.. code-block:: python

   # Good - clear assertion messages
   def test_search_returns_expected_count():
       results = client.search(limit=5)
       items = results.get_all_items()
       
       assert len(items) == 5, f"Expected 5 items, got {len(items)}"
   
   # Even better - use pytest's detailed output
   def test_search_filters_by_cloud_cover():
       items = search_with_cloud_filter(max_cloud=20)
       
       for item in items:
           cloud_cover = item.properties.get('eo:cloud_cover', 0)
           assert cloud_cover <= 20, (
               f"Item {item.id} has cloud cover {cloud_cover}% > 20%"
           )

**5. Isolate Tests from External Dependencies**

.. code-block:: python

   # Use dependency injection for testability
   class APIClient:
       def __init__(self, http_client=None):
           self.http_client = http_client or requests
       
       def search(self, **kwargs):
           response = self.http_client.post(self.search_url, json=kwargs)
           return response.json()
   
   # Test with mock client
   def test_search_handles_api_error():
       mock_client = Mock()
       mock_client.post.side_effect = requests.exceptions.Timeout()
       
       client = APIClient(http_client=mock_client)
       
       with pytest.raises(requests.exceptions.Timeout):
           client.search(collections=['test'])

Advanced Testing Techniques
----------------------------

Property-Based Testing
~~~~~~~~~~~~~~~~~~~~~~

Use hypothesis for property-based testing:

.. code-block:: python

   from hypothesis import given, strategies as st
   
   @given(
       west=st.floats(min_value=-180, max_value=179),
       south=st.floats(min_value=-90, max_value=89),
       east=st.floats(min_value=-179, max_value=180),
       north=st.floats(min_value=-89, max_value=90)
   )
   def test_bbox_validation_with_random_coordinates(west, south, east, north):
       """Test bbox validation with random valid coordinates."""
       from open_geodata_api.utils import validate_bbox
       
       # Ensure proper ordering
       if west >= east:
           west, east = east - 1, west + 1
       if south >= north:
           south, north = north - 1, south + 1
       
       bbox = [west, south, east, north]
       is_valid, message = validate_bbox(bbox)
       
       assert is_valid, f"Valid bbox rejected: {bbox}, message: {message}"

Parameterized Tests
~~~~~~~~~~~~~~~~~~~

Test multiple scenarios efficiently:

.. code-block:: python

   @pytest.mark.parametrize("provider,expected_naming", [
       ('planetary_computer', ['B01', 'B02', 'B03', 'B04']),
       ('earth_search', ['coastal', 'blue', 'green', 'red']),
   ])
   def test_asset_naming_conventions(provider, expected_naming, mock_item_factory):
       """Test that different providers use expected asset naming."""
       item = mock_item_factory(provider=provider, assets=expected_naming)
       
       available_assets = item.list_assets()
       
       for expected_asset in expected_naming:
           assert expected_asset in available_assets

   @pytest.mark.parametrize("cloud_cover,should_pass", [
       (0, True),
       (15, True),
       (20, True),
       (25, False),
       (50, False),
       (100, False),
   ])
   def test_cloud_cover_filtering(cloud_cover, should_pass, sample_item):
       """Test cloud cover filtering with various thresholds."""
       sample_item.properties['eo:cloud_cover'] = cloud_cover
       
       filtered = filter_by_cloud_cover([sample_item], max_cloud_cover=20)
       
       if should_pass:
           assert len(filtered) == 1
       else:
           assert len(filtered) == 0

Snapshot Testing
~~~~~~~~~~~~~~~~

Test complex output structures:

.. code-block:: python

   def test_dataframe_conversion_structure(sample_collection, snapshot):
       """Test that DataFrame conversion maintains expected structure."""
       df = sample_collection.to_dataframe()
       
       # Test structure matches snapshot
       structure = {
           'columns': list(df.columns),
           'dtypes': {col: str(dtype) for col, dtype in df.dtypes.items()},
           'shape': df.shape
       }
       
       assert structure == snapshot

Test Data Management
--------------------

Fixture Factories
~~~~~~~~~~~~~~~~~

Create flexible test data:

.. code-block:: python

   @pytest.fixture
   def stac_item_factory():
       """Factory for creating test STAC items."""
       def _create_item(
           item_id=None,
           collection='test-collection',
           cloud_cover=10,
           assets=None,
           provider='test'
       ):
           if assets is None:
               assets = ['B02', 'B03', 'B04', 'B08']
           
           return {
               'id': item_id or f'test-item-{uuid.uuid4()}',
               'collection': collection,
               'properties': {
                   'datetime': '2024-06-15T12:00:00Z',
                   'eo:cloud_cover': cloud_cover
               },
               'assets': {
                   asset: {
                       'href': f'https://example.com/{asset}.tif',
                       'type': 'image/tiff'
                   } for asset in assets
               },
               'bbox': [-122.5, 47.5, -122.0, 48.0]
           }
       
       return _create_item

Test Data Builders
~~~~~~~~~~~~~~~~~~

Use builder pattern for complex test data:

.. code-block:: python

   class STACItemBuilder:
       """Builder for creating test STAC items."""
       
       def __init__(self):
           self.reset()
       
       def reset(self):
           self._data = {
               'id': 'test-item',
               'collection': 'test-collection',
               'properties': {'datetime': '2024-06-15T12:00:00Z'},
               'assets': {},
               'bbox': [-122.5, 47.5, -122.0, 48.0]
           }
           return self
       
       def with_id(self, item_id):
           self._data['id'] = item_id
           return self
       
       def with_cloud_cover(self, cloud_cover):
           self._data['properties']['eo:cloud_cover'] = cloud_cover
           return self
       
       def with_assets(self, asset_names):
           self._data['assets'] = {
               name: {
                   'href': f'https://example.com/{name}.tif',
                   'type': 'image/tiff'
               } for name in asset_names
           }
           return self
       
       def build(self):
           return self._data.copy()

   # Usage in tests
   def test_with_builder(stac_item_builder):
       item_data = (stac_item_builder
                   .with_id('clear-scene')
                   .with_cloud_cover(5)
                   .with_assets(['B04', 'B03', 'B02'])
                   .build())
       
       item = STACItem(item_data)
       assert item.properties['eo:cloud_cover'] == 5

Test Environment Management
---------------------------

Environment-Specific Configuration
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   # conftest.py
   import os
   import pytest

   def pytest_configure(config):
       """Configure pytest environment."""
       # Set test-specific environment variables
       os.environ['OGAPI_CACHE_DIR'] = '/tmp/ogapi_test_cache'
       os.environ['OGAPI_LOG_LEVEL'] = 'DEBUG'
       
       # Register custom markers
       config.addinivalue_line(
           "markers", "integration: marks tests as integration tests"
       )
       config.addinivalue_line(
           "markers", "slow: marks tests as slow"
       )

   @pytest.fixture(scope='session', autouse=True)
   def test_environment_setup():
       """Set up test environment."""
       # Create test directories
       test_dirs = ['/tmp/ogapi_test_cache', '/tmp/ogapi_test_downloads']
       for directory in test_dirs:
           os.makedirs(directory, exist_ok=True)
       
       yield
       
       # Cleanup
       import shutil
       for directory in test_dirs:
           if os.path.exists(directory):
               shutil.rmtree(directory)

Test Isolation
~~~~~~~~~~~~~~

Ensure tests don't interfere with each other:

.. code-block:: python

   @pytest.fixture(autouse=True)
   def isolate_tests():
       """Isolate each test from others."""
       # Clear any global state
       import open_geodata_api
       if hasattr(open_geodata_api, '_global_config'):
           open_geodata_api._global_config.clear()
       
       # Reset any module-level caches
       import open_geodata_api.utils
       if hasattr(open_geodata_api.utils, '_url_cache'):
           open_geodata_api.utils._url_cache.clear()
       
       yield
       
       # Post-test cleanup
       # Any additional cleanup needed

Debugging Tests
---------------

Test Debugging Techniques
~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   def test_with_debugging_info(sample_item, caplog):
       """Test with enhanced debugging information."""
       import logging
       
       # Enable debug logging for this test
       caplog.set_level(logging.DEBUG)
       
       # Add debugging breakpoint if needed
       if os.getenv('DEBUG_TESTS'):
           import pdb; pdb.set_trace()
       
       # Perform test operations
       urls = sample_item.get_all_asset_urls()
       
       # Check logs for debugging info
       debug_messages = [record.message for record in caplog.records 
                        if record.levelname == 'DEBUG']
       
       # Assert with debugging context
       assert len(urls) > 0, f"No URLs found. Debug info: {debug_messages}"

Custom Assertions
~~~~~~~~~~~~~~~~~

Create domain-specific assertions:

.. code-block:: python

   def assert_valid_stac_item(item):
       """Custom assertion for STAC item validation."""
       assert hasattr(item, 'id'), "STAC item must have ID"
       assert hasattr(item, 'collection'), "STAC item must have collection"
       assert hasattr(item, 'properties'), "STAC item must have properties"
       assert hasattr(item, 'assets'), "STAC item must have assets"
       
       # Validate ID format
       assert isinstance(item.id, str), "Item ID must be string"
       assert len(item.id) > 0, "Item ID cannot be empty"
       
       # Validate datetime
       if 'datetime' in item.properties:
           datetime_str = item.properties['datetime']
           # Add datetime format validation
           import datetime
           try:
               datetime.datetime.fromisoformat(datetime_str.replace('Z', '+00:00'))
           except ValueError:
               pytest.fail(f"Invalid datetime format: {datetime_str}")

   def assert_valid_bbox(bbox):
       """Custom assertion for bbox validation."""
       assert isinstance(bbox, (list, tuple)), "Bbox must be list or tuple"
       assert len(bbox) == 4, "Bbox must have 4 coordinates"
       
       west, south, east, north = bbox
       assert west < east, f"West ({west}) must be less than east ({east})"
       assert south < north, f"South ({south}) must be less than north ({north})"
       assert -180 <= west <= 180, f"West longitude out of range: {west}"
       assert -180 <= east <= 180, f"East longitude out of range: {east}"
       assert -90 <= south <= 90, f"South latitude out of range: {south}"
       assert -90 <= north <= 90, f"North latitude out of range: {north}"

Test Reporting and Metrics
---------------------------

Custom Test Reports
~~~~~~~~~~~~~~~~~~~

Generate detailed test reports:

.. code-block:: python

   # conftest.py
   @pytest.fixture(scope='session', autouse=True)
   def test_metrics_collector():
       """Collect test metrics throughout session."""
       metrics = {
           'start_time': time.time(),
           'test_counts': defaultdict(int),
           'slow_tests': [],
           'failed_tests': []
       }
       
       yield metrics
       
       # Generate final report
       end_time = time.time()
       total_time = end_time - metrics['start_time']
       
       print(f"\n=== Test Session Summary ===")
       print(f"Total time: {total_time:.2f} seconds")
       print(f"Test counts: {dict(metrics['test_counts'])}")
       
       if metrics['slow_tests']:
           print(f"Slow tests (>5s):")
           for test_name, duration in metrics['slow_tests']:
               print(f"  {test_name}: {duration:.2f}s")

   def pytest_runtest_call(item):
       """Hook to measure test execution time."""
       start_time = time.time()
       yield
       end_time = time.time()
       
       duration = end_time - start_time
       if duration > 5.0:  # Mark as slow if > 5 seconds
           if hasattr(item.session, 'test_metrics'):
               item.session.test_metrics['slow_tests'].append((item.name, duration))

Coverage Analysis
~~~~~~~~~~~~~~~~~

Analyze test coverage in detail:

.. code-block:: bash

   # Generate detailed coverage reports
   pytest --cov=open_geodata_api \
          --cov-report=html \
          --cov-report=xml \
          --cov-report=term-missing \
          --cov-fail-under=90

   # Generate coverage for specific modules
   pytest --cov=open_geodata_api.core \
          --cov=open_geodata_api.utils \
          --cov-report=html:htmlcov_core_utils

Continuous Integration Integration
----------------------------------

GitHub Actions Test Matrix
~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: yaml

   # .github/workflows/comprehensive-tests.yml
   name: Comprehensive Tests
   
   on: [push, pull_request]
   
   jobs:
     test-matrix:
       runs-on: ${{ matrix.os }}
       strategy:
         fail-fast: false
         matrix:
           os: [ubuntu-latest, windows-latest, macos-latest]
           python-version: ['3.8', '3.9', '3.10', '3.11']
           test-type: [unit, integration]
           include:
             - python-version: '3.11'
               os: ubuntu-latest
               test-type: performance
       
       steps:
       - uses: actions/checkout@v3
       
       - name: Set up Python ${{ matrix.python-version }}
         uses: actions/setup-python@v3
         with:
           python-version: ${{ matrix.python-version }}
       
       - name: Install GDAL (Ubuntu)
         if: matrix.os == 'ubuntu-latest'
         run: |
           sudo apt-get update
           sudo apt-get install gdal-bin libgdal-dev
       
       - name: Install dependencies
         run: |
           python -m pip install --upgrade pip
           pip install -e .[dev,complete]
       
       - name: Run unit tests
         if: matrix.test-type == 'unit'
         run: |
           pytest tests/unit/ -v --cov=open_geodata_api --cov-report=xml
       
       - name: Run integration tests
         if: matrix.test-type == 'integration'
         run: |
           pytest tests/integration/ -v -m "not slow"
         env:
           SKIP_SLOW_TESTS: true
       
       - name: Run performance tests
         if: matrix.test-type == 'performance'
         run: |
           pytest tests/performance/ -v --benchmark-only
       
       - name: Upload coverage to Codecov
         if: matrix.test-type == 'unit'
         uses: codecov/codecov-action@v3
         with:
           file: ./coverage.xml
           flags: unittests
           name: codecov-umbrella

Quality Gates
~~~~~~~~~~~~~

Implement quality gates for releases:

.. code-block:: yaml

   quality-gate:
     runs-on: ubuntu-latest
     needs: [test-matrix]
     
     steps:
     - name: Quality Gate Check
       run: |
         echo "Checking quality metrics..."
         
         # Coverage threshold
         coverage_threshold=90
         
         # Performance regression threshold
         performance_threshold=10  # 10% slower is acceptable
         
         # Test success rate threshold
         success_rate_threshold=95
         
         # Add actual quality gate logic here

Pre-commit Hooks for Testing
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: yaml

   # .pre-commit-config.yaml
   repos:
   - repo: local
     hooks:
     - id: run-tests
       name: Run fast tests
       entry: pytest tests/unit/ -x --tb=short
       language: system
       types: [python]
       pass_filenames: false
     
     - id: check-coverage
       name: Check test coverage
       entry: pytest tests/unit/ --cov=open_geodata_api --cov-fail-under=85
       language: system
       types: [python]
       pass_filenames: false

This comprehensive testing guide provides the foundation for maintaining high code quality and reliability in the Open Geodata API project.
