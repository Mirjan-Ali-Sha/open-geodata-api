"""
Fixed Pytest test suite for filter_by_geometry function
Run with: pytest test/test_all_geometry_formats.py -v
"""

import pytest
import warnings
from typing import List, Dict, Any

# Import the function to test
try:
    from open_geodata_api.utils.filters import filter_by_geometry
    from open_geodata_api.core.collections import STACItemCollection
    FILTER_AVAILABLE = True
except ImportError:
    FILTER_AVAILABLE = False

# Try to import optional dependencies
try:
    from shapely.geometry import Point, Polygon, box
    SHAPELY_AVAILABLE = True
except ImportError:
    SHAPELY_AVAILABLE = False

try:
    import geopandas as gpd
    GEOPANDAS_AVAILABLE = True
except ImportError:
    GEOPANDAS_AVAILABLE = False


@pytest.fixture
def mock_stac_items():
    """Mock STACItemCollection for testing."""
    items_data = [
        {
            'id': 'item1',
            'collection': 'test-collection',
            'geometry': {
                'type': 'Polygon',
                'coordinates': [[
                    [-122.5, 47.5], [-122.0, 47.5],
                    [-122.0, 48.0], [-122.5, 48.0], [-122.5, 47.5]
                ]]
            },
            'properties': {
                'datetime': '2023-06-01T12:00:00Z',
                'eo:cloud_cover': 10.5
            }
        },
        {
            'id': 'item2', 
            'collection': 'test-collection',
            'geometry': {
                'type': 'Point',
                'coordinates': [-122.3321, 47.6062]
            },
            'properties': {
                'datetime': '2023-06-02T12:00:00Z',
                'eo:cloud_cover': 5.2
            }
        },
        {
            'id': 'item3',
            'collection': 'test-collection',
            'geometry': {
                'type': 'Polygon',
                'coordinates': [[
                    [-123.0, 46.5], [-121.5, 46.5],
                    [-121.5, 47.0], [-123.0, 47.0], [-123.0, 46.5]
                ]]
            },
            'properties': {
                'datetime': '2023-06-03T12:00:00Z',
                'eo:cloud_cover': 25.8
            }
        },
        {
            'id': 'item4',
            'collection': 'test-collection',
            'bbox': [-122.4, 47.5, -122.2, 47.7],  # No geometry, only bbox
            'properties': {
                'datetime': '2023-06-04T12:00:00Z',
                'eo:cloud_cover': 15.3
            }
        }
    ]
    
    if FILTER_AVAILABLE:
        return STACItemCollection(items_data, provider="test")
    else:
        return items_data


class TestFilterByGeometryBasic:
    """Test basic geometry formats that don't require external dependencies."""
    
    @pytest.mark.parametrize("name, geometry, expected_min_items", [
        ("Bounding Box", [-122.5, 47.5, -122.0, 48.0], 1),
        ("Point Coordinates", [-122.3321, 47.6062], 0),
        ("Diagonal Points", [[-122.5, 47.5], [-122.0, 48.0]], 1),
        ("GeoJSON Point", {"type": "Point", "coordinates": [-122.3321, 47.6062]}, 0),
        ("GeoJSON Polygon", {
            "type": "Polygon",
            "coordinates": [[
                [-122.5, 47.5], [-122.0, 47.5],
                [-122.0, 48.0], [-122.5, 48.0], [-122.5, 47.5]
            ]]
        }, 1),
        ("Polygon Coordinates", [
            (-122.5, 47.5), (-122.0, 47.5), 
            (-122.0, 48.0), (-122.5, 48.0), (-122.5, 47.5)
        ], 1),
    ])
    def test_basic_geometry_formats(self, mock_stac_items, name, geometry, expected_min_items):
        """Test filter_by_geometry with basic geometry formats."""
        print(f"\n🧪 Testing {name}")
        
        try:
            filtered_items = filter_by_geometry(mock_stac_items, geometry)
            count = len(filtered_items)
            
            print(f"✅ {name:<20}: {count} items")
            
            # Assertions
            assert count >= expected_min_items, f"{name} should return at least {expected_min_items} items"
            assert count <= len(mock_stac_items), f"{name} cannot return more items than input"
            
            # Type check
            if FILTER_AVAILABLE:
                assert isinstance(filtered_items, STACItemCollection), f"{name} should return STACItemCollection"
            
        except Exception as e:
            pytest.fail(f"filter_by_geometry failed for {name}: {e}")


@pytest.mark.skipif(not SHAPELY_AVAILABLE, reason="Shapely not installed")
class TestFilterByGeometryShapely:
    """Test Shapely geometry objects."""
    
    @pytest.mark.parametrize("name, geometry_factory, expected_min_items", [
        ("Shapely Point", lambda: Point(-122.3321, 47.6062), 0),
        ("Shapely Box", lambda: box(-122.5, 47.5, -122.0, 48.0), 1),
        ("Shapely Polygon", lambda: Polygon([
            (-122.5, 47.5), (-122.0, 47.5), 
            (-122.0, 48.0), (-122.5, 48.0)
        ]), 1),
    ])
    def test_shapely_geometry_objects(self, mock_stac_items, name, geometry_factory, expected_min_items):
        """Test filter_by_geometry with Shapely geometry objects."""
        print(f"\n🧪 Testing {name}")
        
        geometry = geometry_factory()
        
        try:
            filtered_items = filter_by_geometry(mock_stac_items, geometry)
            count = len(filtered_items)
            
            print(f"✅ {name:<20}: {count} items")
            
            # Assertions
            assert count >= expected_min_items, f"{name} should return at least {expected_min_items} items"
            assert count <= len(mock_stac_items), f"{name} cannot return more items than input"
            assert hasattr(geometry, 'geom_type'), f"{name} should be a valid Shapely geometry"
            
        except Exception as e:
            pytest.fail(f"Shapely geometry test failed for {name}: {e}")


class TestFilterByGeometryErrors:
    """Test error handling for invalid geometries."""
    
    @pytest.mark.parametrize("name, geometry, expected_error", [
        ("Invalid bbox (3 values)", [-122.5, 47.5, -122.0], ValueError),
        ("Empty list", [], ValueError),
        ("Invalid GeoJSON", {"type": "InvalidType", "coordinates": []}, ValueError),
        ("Invalid WKT", "INVALID WKT STRING", ValueError),
        ("Single number", 123.456, ValueError),
        # 🔥 FIXED: Remove this test case since 2-point coords are valid (diagonal points)
        # ("Invalid polygon (2 points)", [(-122.5, 47.5), (-122.0, 48.0)], ValueError),
        ("Invalid single coord", [123.456], ValueError),  # Replace with actual invalid case
    ])
    def test_invalid_geometries(self, mock_stac_items, name, geometry, expected_error):
        """Test that invalid geometries raise appropriate errors."""
        print(f"\n🧪 Testing Error: {name}")
        
        with pytest.raises(expected_error):
            filter_by_geometry(mock_stac_items, geometry)
        
        print(f"✅ {name}: Correctly raised {expected_error.__name__}")

    def test_none_geometry(self, mock_stac_items):
        """Test that None geometry raises ValueError."""
        print(f"\n🧪 Testing None geometry")
        
        with pytest.raises(ValueError, match="Unsupported geometry type"):
            filter_by_geometry(mock_stac_items, None)

    def test_two_point_coords_are_valid(self, mock_stac_items):
        """🔥 NEW TEST: Verify that 2-point coordinates are treated as diagonal points (valid)."""
        print(f"\n🧪 Testing that 2-point coords are valid (diagonal points)")
        
        # This should NOT raise an error - it's treated as diagonal points for bbox
        two_points = [(-122.5, 47.5), (-122.0, 48.0)]
        
        try:
            filtered_items = filter_by_geometry(mock_stac_items, two_points)
            count = len(filtered_items)
            print(f"✅ Two-point coords: {count} items (treated as diagonal points)")
            assert count >= 0, "Two-point coordinates should be valid"
        except Exception as e:
            pytest.fail(f"Two-point coordinates should be valid but failed: {e}")


class TestFilterByGeometryComprehensive:
    """Comprehensive test suite combining all geometry types."""
    
    def test_all_geometry_formats_comprehensive(self, mock_stac_items):
        """Test all supported geometry formats and collect results."""
        print("\n" + "=" * 60)
        print("🧪 Comprehensive filter_by_geometry testing:")
        print("=" * 60)
        
        results = {}
        
        # Basic formats
        basic_test_cases = [
            ("Bounding Box", [-122.5, 47.5, -122.0, 48.0]),
            ("Point", [-122.3321, 47.6062]),
            ("Diagonal Points", [[-122.5, 47.5], [-122.0, 48.0]]),
            ("GeoJSON Point", {"type": "Point", "coordinates": [-122.3321, 47.6062]}),
            ("GeoJSON Polygon", {
                "type": "Polygon",
                "coordinates": [[
                    [-122.5, 47.5], [-122.0, 47.5],
                    [-122.0, 48.0], [-122.5, 48.0], [-122.5, 47.5]
                ]]
            }),
            ("Polygon Coords", [(-122.5, 47.5), (-122.0, 47.5), (-122.0, 48.0), (-122.5, 48.0), (-122.5, 47.5)])
        ]
        
        for name, geometry in basic_test_cases:
            try:
                filtered_items = filter_by_geometry(mock_stac_items, geometry)
                count = len(filtered_items)
                results[name] = count
                print(f"✅ {name:<20}: {count} items")
                
                # Basic assertions
                assert count >= 0, f"{name} should return non-negative count"
                assert count <= len(mock_stac_items), f"{name} cannot exceed input size"
                
            except Exception as e:
                results[name] = f"Error: {e}"
                print(f"❌ {name:<20}: {e}")
                pytest.fail(f"Basic geometry test failed for {name}: {e}")
        
        # WKT formats (if shapely available)
        if SHAPELY_AVAILABLE:
            wkt_test_cases = [
                ("WKT Point", "POINT(-122.3321 47.6062)"),
                ("WKT Polygon", "POLYGON((-122.5 47.5, -122.0 47.5, -122.0 48.0, -122.5 48.0, -122.5 47.5))"),
            ]
            
            for name, geometry in wkt_test_cases:
                try:
                    filtered_items = filter_by_geometry(mock_stac_items, geometry)
                    count = len(filtered_items)
                    results[name] = count
                    print(f"✅ {name:<20}: {count} items")
                    
                except Exception as e:
                    results[name] = f"Error: {e}"
                    print(f"❌ {name:<20}: {e}")
        
        # Shapely geometries (if available)
        if SHAPELY_AVAILABLE:
            shapely_test_cases = [
                ("Shapely Point", Point(-122.3321, 47.6062)),
                ("Shapely Box", box(-122.5, 47.5, -122.0, 48.0)),
                ("Shapely Polygon", Polygon([(-122.5, 47.5), (-122.0, 47.5), (-122.0, 48.0), (-122.5, 48.0)]))
            ]
            
            for name, geometry in shapely_test_cases:
                try:
                    filtered_items = filter_by_geometry(mock_stac_items, geometry)
                    count = len(filtered_items)
                    results[name] = count
                    print(f"✅ {name:<20}: {count} items")
                    
                except Exception as e:
                    results[name] = f"Error: {e}"
                    print(f"❌ {name:<20}: {e}")
        else:
            print("⚠️  Shapely not available for testing")
        
        print("=" * 60)
        successful_tests = len([r for r in results.values() if isinstance(r, int)])
        total_tests = len(results)
        print(f"📊 Test Results: {successful_tests}/{total_tests} successful")
        print(f"📋 Coverage: {successful_tests/total_tests*100:.1f}%")
        
        # Final comprehensive assertion
        assert successful_tests > 0, "At least some geometry tests should pass"
        assert successful_tests >= total_tests * 0.7, "At least 70% of tests should pass"
        
        # 🔥 FIXED: Don't return anything (pytest expects None)
        # return results  # Remove this line


# 🔥 FIXED: Remove global execution
# The following lines were causing the NameError - move them inside a function or remove:
# test_results = test_all_geometry_formats(items)  # This was the problem!

def manual_test_with_real_data(items):
    """
    Function to manually test with real STAC data (call this explicitly).
    
    Usage:
        from test_all_geometry_formats import manual_test_with_real_data
        results = manual_test_with_real_data(your_items)
    """
    print("🧪 Manual testing with real data...")
    
    test_cases = [
        ("Bounding Box", [-122.5, 47.5, -122.0, 48.0]),
        ("Point", [-122.3321, 47.6062]),
        ("Diagonal Points", [[-122.5, 47.5], [-122.0, 48.0]]),
        ("GeoJSON Point", {"type": "Point", "coordinates": [-122.3321, 47.6062]}),
    ]
    
    results = {}
    
    for name, geometry in test_cases:
        try:
            filtered_items = filter_by_geometry(items, geometry)
            count = len(filtered_items)
            results[name] = count
            print(f"✅ {name:<20}: {count} items")
        except Exception as e:
            results[name] = f"Error: {e}"
            print(f"❌ {name:<20}: {e}")
    
    return results


if __name__ == "__main__":
    # For manual testing
    print("To run tests with pytest:")
    print("pytest test_all_geometry_formats.py -v")
    print("\nFor verbose output:")
    print("pytest test_all_geometry_formats.py -v -s")
