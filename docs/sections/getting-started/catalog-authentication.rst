Universal Catalog Authentication
=================================

The Universal Catalog Client supports flexible authentication for STAC APIs that require it.

Authentication Methods
----------------------

Bearer Token Authentication
~~~~~~~~~~~~~~~~~~~~~~~~~~~

Most STAC APIs use Bearer token authentication:

.. code-block:: python

   import open_geodata_api as ogapi

   client = ogapi.catalog(
       "https://api-with-auth.com/stac/",
       auth_token="your-bearer-token-here"
   )

The token is automatically added to request headers as:

.. code-block:: text

   Authorization: Bearer your-bearer-token-here

Custom Headers
~~~~~~~~~~~~~~

For APIs requiring additional authentication headers:

.. code-block:: python

   client = ogapi.catalog(
       "https://custom-api.com/stac/",
       headers={
           "X-API-Key": "your-api-key",
           "X-User-ID": "your-user-id",
           "Authorization": "Custom auth-string"
       }
   )

Combined Authentication
~~~~~~~~~~~~~~~~~~~~~~~

Use both bearer token and custom headers:

.. code-block:: python

   client = ogapi.catalog(
       "https://secure-api.com/stac/",
       auth_token="bearer-token",
       headers={
           "X-API-Key": "additional-key",
           "X-Client-ID": "client-123"
       }
   )

No Authentication
~~~~~~~~~~~~~~~~~

For public APIs, simply omit authentication parameters:

.. code-block:: python

   client = ogapi.catalog("https://earth-search.aws.element84.com/v1")

Getting Authentication Tokens
------------------------------

Different providers have different methods for obtaining tokens:

DLR EOC STAC Catalog
~~~~~~~~~~~~~~~~~~~~

1. Register at https://geoservice.dlr.de
2. Navigate to API Access
3. Generate an access token
4. Use the token in your client:

.. code-block:: python

   client = ogapi.catalog(
       "https://geoservice.dlr.de/eoc/ogc/stac/v1/",
       auth_token="your-dlr-token"
   )

OpenEO
~~~~~~

1. Create account at openEO provider
2. Obtain authentication token via OpenEO Connect
3. Use in Universal Catalog Client:

.. code-block:: python

   client = ogapi.catalog(
       "https://earthengine.openeo.org/v1.0/",
       auth_token="your-openeo-token"
   )

Environment Variables
---------------------

Store tokens securely using environment variables:

.. code-block:: bash

   # Set environment variable
   export STAC_API_TOKEN="your-token-here"

.. code-block:: python

   import os
   import open_geodata_api as ogapi

   # Read token from environment
   token = os.getenv("STAC_API_TOKEN")

   client = ogapi.catalog(
       "https://secure-api.com/stac/",
       auth_token=token
   )

Configuration File
------------------

Store API configurations in a file:

**config.json:**

.. code-block:: json

   {
     "dlr_eoc": {
       "url": "https://geoservice.dlr.de/eoc/ogc/stac/v1/",
       "token": "your-dlr-token"
     },
     "openeo": {
       "url": "https://earthengine.openeo.org/v1.0/",
       "token": "your-openeo-token"
     }
   }

**Usage:**

.. code-block:: python

   import json
   import open_geodata_api as ogapi

   # Load configuration
   with open("config.json") as f:
       config = json.load(f)

   # Create clients from config
   dlr_client = ogapi.catalog(
       config["dlr_eoc"]["url"],
       auth_token=config["dlr_eoc"]["token"]
   )

   openeo_client = ogapi.catalog(
       config["openeo"]["url"],
       auth_token=config["openeo"]["token"]
   )

Security Best Practices
-----------------------

1. **Never commit tokens** to version control
2. **Use environment variables** for sensitive data
3. **Rotate tokens regularly** 
4. **Use different tokens** for different environments (dev/prod)
5. **Set appropriate timeouts** to avoid hanging connections
6. **Enable SSL verification** in production (``verify_ssl=True``)

Troubleshooting Authentication
-------------------------------

**Issue: 401 Unauthorized**

.. code-block:: python

   # Check if token is valid
   try:
       client = ogapi.catalog(api_url, auth_token=token)
       collections = client.list_collections()
       print("✓ Authentication successful")
   except Exception as e:
       print(f"✗ Authentication failed: {e}")
       print("Check: Token validity, format, expiration")

**Issue: 403 Forbidden**

Check if your token has the necessary permissions for the requested operation.

**Issue: SSL Certificate Error**

For development environments only:

.. code-block:: python

   client = ogapi.catalog(
       api_url,
       auth_token=token,
       verify_ssl=False  # Only for development!
   )
