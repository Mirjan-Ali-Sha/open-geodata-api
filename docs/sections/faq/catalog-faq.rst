Universal Catalog FAQ
=====================

General Questions
-----------------

**Q: What is the Universal Catalog Client?**

A: It's a flexible client that can connect to any STAC-compliant API endpoint, with or without authentication. It provides a consistent interface across all STAC APIs while handling provider-specific differences.

**Q: How is it different from Planetary Computer and Earth Search clients?**

A: The Universal Catalog Client is provider-agnostic:

- **Planetary Computer**: Specific to Microsoft Planetary Computer
- **Earth Search**: Specific to AWS Element84
- **Universal Catalog**: Works with any STAC API

**Q: Can I use it with public APIs?**

A: Yes! Simply omit the auth_token parameter for public APIs.

Authentication Questions
------------------------

**Q: What authentication methods are supported?**

A: Bearer token authentication and custom HTTP headers. Most STAC APIs use Bearer tokens.

**Q: What if my API uses a different authentication method?**

A: You can pass custom headers:

.. code-block:: python

   client = ogapi.catalog(
       api_url,
       headers={"Authorization": "Custom auth-method"}
   )

**Q: How do I store authentication tokens securely?**

A: Use environment variables or configuration files, never commit tokens to version control.

Technical Questions
-------------------

**Q: Which STAC versions are supported?**

A: STAC v1.0 and above. The client automatically detects the STAC version.

**Q: What if the search endpoint has a different URL pattern?**

A: The client automatically discovers the search endpoint from the root catalog links.

**Q: Can I use it with non-standard STAC implementations?**

A: Yes, as long as they follow STAC specifications. Custom behavior can be handled with additional headers or parameters.

**Q: Does it support pagination?**

A: Yes, through the same interface as other clients (``get_all_items()`` handles pagination automatically).

**Q: Can I disable SSL verification?**

A: Yes, but only for development:

.. code-block:: python

   client = ogapi.catalog(api_url, verify_ssl=False)

Usage Questions
---------------

**Q: How do I handle band name differences?**

A: The client includes automatic band name mapping. Use either standard names (B02, B03) or common names (blue, green):

.. code-block:: python

   # Both work!
   url1 = client.get_asset_url(item, 'B02')
   url2 = client.get_asset_url(item, 'blue')

**Q: Can I use it with existing workflows?**

A: Yes! It returns the same STACItem and STACItemCollection objects as other clients.

**Q: How do I know if an API requires authentication?**

A: Try connecting without a token first. If you get a 401 or 403 error, authentication is required.

Troubleshooting
---------------

**Q: "Failed to connect to STAC API" error**

A: Check:

1. API URL is correct and reachable
2. API is actually a STAC-compliant endpoint
3. Network connectivity
4. SSL certificate issues (try verify_ssl=False for testing)

**Q: "Search endpoint not available" error**

A: The API might not support search. Check API documentation or use get_collections() instead.

**Q: Getting empty results**

A: Verify:

1. Collection names are correct (use ``list_collections()``)
2. Bbox coordinates are in correct order [west, south, east, north]
3. Datetime format is correct
4. Query parameters match API expectations

Comparison with Other Clients
------------------------------

.. list-table::
   :header-rows: 1

   * - Feature
     - Planetary Computer
     - Earth Search
     - Universal Catalog
   * - Provider
     - Microsoft
     - Element84/AWS
     - Any STAC API
   * - Authentication
     - Automatic signing
     - None
     - Flexible (optional)
   * - Band Names
     - B01, B02, B03...
     - blue, green, red...
     - Both supported
   * - Custom APIs
     - No
     - No
     - Yes
   * - Setup Complexity
     - Low
     - Low
     - Low-Medium
