Universal Catalog Client API Reference
=======================================

.. module:: open_geodata_api.catalog

UniversalCatalogClient
----------------------

.. class:: UniversalCatalogClient(api_url, auth_token=None, headers=None, timeout=30, verify_ssl=True)

   A universal client for connecting to any STAC API endpoint with flexible authentication.

   :param str api_url: Base URL of the STAC API endpoint (required)
   :param str auth_token: Authentication token if required by the API (optional)
   :param dict headers: Additional headers to include in requests (optional)
   :param int timeout: Request timeout in seconds (default: 30)
   :param bool verify_ssl: Whether to verify SSL certificates (default: True)

   **Example:**

   .. code-block:: python

      import open_geodata_api as ogapi

      # Without authentication
      client = ogapi.catalog("https://earth-search.aws.element84.com/v1")

      # With authentication
      client = ogapi.catalog(
          "https://your-stac-api.com",
          auth_token="your-token-here",
          headers={"X-Custom-Header": "value"}
      )

Methods
-------

search()
~~~~~~~~

.. method:: search(collections=None, bbox=None, datetime=None, query=None, limit=100, **kwargs)

   Search for STAC items matching the specified criteria.

   :param list collections: List of collection IDs to search (optional)
   :param list bbox: Bounding box [west, south, east, north] (optional)
   :param str datetime: Datetime range in RFC3339 or YYYY-MM-DD format (optional)
   :param dict query: Additional query parameters (optional)
   :param int limit: Maximum number of items to return (default: 100)
   :param kwargs: Additional search parameters
   :return: STACSearch object containing results
   :rtype: STACSearch

   **Example:**

   .. code-block:: python

      results = client.search(
          collections=["sentinel-2-l2a"],
          bbox=[-122.5, 47.5, -122.0, 48.0],
          datetime="2024-01-01/2024-03-31",
          query={"eo:cloud_cover": {"lt": 20}},
          limit=50
      )

      items = results.get_all_items()

list_collections()
~~~~~~~~~~~~~~~~~~

.. method:: list_collections()

   Get list of available collection IDs.

   :return: List of collection ID strings
   :rtype: list

   **Example:**

   .. code-block:: python

      collections = client.list_collections()
      print(f"Available collections: {collections}")

get_collections()
~~~~~~~~~~~~~~~~~

.. method:: get_collections()

   Get detailed information about all available collections.

   :return: List of collection metadata dictionaries
   :rtype: list

   **Example:**

   .. code-block:: python

      collections = client.get_collections()
      for col in collections:
          print(f"{col['id']}: {col['title']}")

get_collection_info()
~~~~~~~~~~~~~~~~~~~~~

.. method:: get_collection_info(collection_id)

   Get detailed information about a specific collection.

   :param str collection_id: Collection ID
   :return: Collection metadata dictionary
   :rtype: dict

   **Example:**

   .. code-block:: python

      info = client.get_collection_info("sentinel-2-l2a")
      print(f"Title: {info['title']}")
      print(f"Description: {info['description']}")

get_asset_url()
~~~~~~~~~~~~~~~

.. method:: get_asset_url(item, asset_key, prefer_jp2=True)

   Get asset URL for a specific asset key with automatic band name mapping.

   :param STACItem item: STAC item object
   :param str asset_key: Asset key (e.g., 'B02', 'blue', 'red')
   :param bool prefer_jp2: Prefer JP2 format assets if available (default: True)
   :return: Asset URL if found, None otherwise
   :rtype: str or None

   **Example:**

   .. code-block:: python

      item = items[0]
      blue_url = client.get_asset_url(item, 'B02')  # or 'blue'
      print(f"Blue band URL: {blue_url}")

get_info()
~~~~~~~~~~

.. method:: get_info()

   Get client and endpoint information.

   :return: Dictionary containing client information
   :rtype: dict

   **Example:**

   .. code-block:: python

      info = client.get_info()
      print(f"API URL: {info['api_url']}")
      print(f"STAC Version: {info['stac_version']}")
      print(f"Authenticated: {info['authenticated']}")

Factory Function
----------------

.. function:: catalog(api_url, **kwargs)

   Factory function to create a UniversalCatalogClient instance.

   :param str api_url: STAC API endpoint URL
   :param kwargs: Additional client parameters
   :return: Configured client instance
   :rtype: UniversalCatalogClient

   **Example:**

   .. code-block:: python

      import open_geodata_api as ogapi

      client = ogapi.catalog(
          "https://your-stac-api.com",
          auth_token="token",
          timeout=60
      )

Parameters Reference
--------------------

.. list-table::
   :header-rows: 1
   :widths: 20 50 15 15

   * - Parameter
     - Description
     - Type
     - Default
   * - api_url
     - Base URL of the STAC API endpoint
     - str
     - Required
   * - auth_token
     - Authentication token (Bearer token)
     - str
     - None
   * - headers
     - Additional HTTP headers
     - dict
     - None
   * - timeout
     - Request timeout in seconds
     - int
     - 30
   * - verify_ssl
     - Verify SSL certificates
     - bool
     - True
