"""
EarthSearch client implementation
"""
import requests
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Union, Any, Tuple
from ..core.search import STACSearch

class EarthSearchCollections:
    """Element84 Earth Search STAC API client."""

    def __init__(self, auto_validate: bool = False):
        self.base_url = "https://earth-search.aws.element84.com/v1"
        self.search_url = f"{self.base_url}/search"
        self.auto_validate = auto_validate
        self.collections = self._fetch_collections()
        self._collection_details = {}

    def _fetch_collections(self):
        """Fetch all collections from the Element84 Earth Search STAC API."""
        url = f"{self.base_url}/collections"
        try:
            response = requests.get(url)
            response.raise_for_status()
            data = response.json()
            collections = data.get('collections', [])
            return {col['id']: f"{self.base_url}/collections/{col['id']}" for col in collections}
        except requests.RequestException as e:
            print(f"Error fetching collections: {e}")
            return {}

    def list_collections(self):
        """Return a list of all available collection names."""
        return sorted(list(self.collections.keys()))

    def search_collections(self, keyword):
        """Search for collections containing a specific keyword."""
        keyword = keyword.lower()
        return [col for col in self.collections.keys() if keyword in col.lower()]

    def get_collection_info(self, collection_name):
        """Get detailed information about a specific collection."""
        if collection_name not in self.collections:
            return None

        if collection_name not in self._collection_details:
            try:
                response = requests.get(self.collections[collection_name])
                response.raise_for_status()
                self._collection_details[collection_name] = response.json()
            except requests.RequestException as e:
                print(f"Error fetching collection details: {e}")
                return None

        return self._collection_details[collection_name]

    def _format_datetime_rfc3339(self, datetime_input: Union[str, datetime]) -> str:
        """Convert various datetime formats to RFC3339 format."""
        if not datetime_input:
            return None

        if isinstance(datetime_input, datetime):
            return datetime_input.strftime('%Y-%m-%dT%H:%M:%SZ')

        datetime_str = str(datetime_input)

        if 'T' in datetime_str and datetime_str.endswith('Z'):
            return datetime_str

        if '/' in datetime_str:
            start_date, end_date = datetime_str.split('/')
            
            if 'T' not in start_date:
                start_rfc3339 = f"{start_date}T00:00:00Z"
            else:
                start_rfc3339 = start_date if start_date.endswith('Z') else f"{start_date}Z"

            if 'T' not in end_date:
                end_rfc3339 = f"{end_date}T23:59:59Z"
            else:
                end_rfc3339 = end_date if end_date.endswith('Z') else f"{end_date}Z"

            return f"{start_rfc3339}/{end_rfc3339}"

        if 'T' not in datetime_str:
            return f"{datetime_str}T00:00:00Z"

        if not datetime_str.endswith('Z'):
            return f"{datetime_str}Z"

        return datetime_str

    def search(self,
               collections: Optional[List[str]] = None,
               intersects: Optional[Dict] = None,
               bbox: Optional[List[float]] = None,
               datetime: Optional[Union[str, List[str], Tuple[str, str]]] = None,
               query: Optional[Dict] = None,
               limit: int = 100,
               max_items: Optional[int] = None) -> STACSearch:
        """Search for products with Element84 Earth Search integration."""

        search_payload = {}

        if collections:
            invalid_collections = [col for col in collections if col not in self.collections]
            if invalid_collections:
                raise ValueError(f"Invalid collections: {invalid_collections}")
            search_payload["collections"] = collections

        if intersects:
            search_payload["intersects"] = intersects

        if bbox:
            if len(bbox) != 4:
                raise ValueError("bbox must be [west, south, east, north]")
            search_payload["bbox"] = bbox

        if datetime:
            if isinstance(datetime, tuple) and len(datetime) == 2:
                start_date, end_date = datetime
                datetime_range = f"{start_date}/{end_date}"
            elif isinstance(datetime, list):
                datetime_range = "/".join(datetime)
            else:
                datetime_range = str(datetime)

            formatted_datetime = self._format_datetime_rfc3339(datetime_range)
            search_payload["datetime"] = formatted_datetime

        if query:
            search_payload["query"] = query

        search_payload["limit"] = min(limit, 1000)

        try:
            headers = {
                'Content-Type': 'application/json',
                'Accept': 'application/geo+json'
            }

            response = requests.post(self.search_url, json=search_payload, headers=headers)
            response.raise_for_status()
            data = response.json()

            if isinstance(data, dict) and 'features' in data:
                items = data.get("features", [])
            elif isinstance(data, list):
                items = data
            else:
                items = []

            if max_items and len(items) > max_items:
                items = items[:max_items]

            return STACSearch({
                "features": items,
                "total_returned": len(items),
                "search_params": search_payload,
                "collections_searched": collections or "all"
            }, provider="earthsearch")

        except requests.RequestException as e:
            print(f"Search error: {e}")
            return STACSearch({"features": [], "total_returned": 0, "error": str(e)}, provider="earthsearch")

    def create_bbox_from_center(self, lat: float, lon: float, buffer_km: float = 10) -> List[float]:
        """Create a bounding box around a center point."""
        buffer_deg = buffer_km / 111.0
        return [lon - buffer_deg, lat - buffer_deg, lon + buffer_deg, lat + buffer_deg]

    def create_geojson_polygon(self, coordinates: List[List[float]]) -> Dict:
        """Create a GeoJSON polygon for area of interest."""
        if coordinates[0] != coordinates[-1]:
            coordinates.append(coordinates[0])
        return {"type": "Polygon", "coordinates": [coordinates]}

    def __repr__(self):
        return f"EarthSearchCollections({len(self.collections)} collections available)"
