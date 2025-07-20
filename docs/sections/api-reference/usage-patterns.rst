Usage Patterns
==============

The core classes provide STAC-compliant data models for working with satellite imagery metadata and assets.

Install The Module
------------------

.. code-block:: python

   pip install open-geodata-api['complete']

Initialize Module
------------------

.. code-block:: python

   import open_geodata_api as ogapi
   
   ogapi.info()

Define Clients
--------------

.. code-block:: python

    import open_geodata_api as ogapi

    # Create client with auto-signing
    pc = ogapi.planetary_computer(auto_sign=True)

    # Search for data
    pc_results = pc.search(
        collections=["sentinel-2-l2a"],
        bbox=[-122.5, 47.5, -122.0, 48.0],
        datetime="2024-01-01/2024-03-31"
    )

    # Get ready-to-use URLs
    pc_items = pc_results.get_all_items()
    print(f"PC Items: {len(pc_items)}")


    es = ogapi.earth_search()

    # Search for data
    es_results = es.search(
        collections=["sentinel-2-l2a"],
        bbox=[-122.5, 47.5, -122.0, 48.0],
        days= 200, #added to 0.2.9 version
        limit=150
    )

    # Get ready-to-use URLs
    es_items = es_results.get_all_items()
    print(f"ES Items: {len(es_items)}")

Get Available Collections
-------------------------

.. code-block:: python

   # Get available collections
   pc_collections = pc.list_collections()
   print(f"Available Collections in Planetary Computer: {pc_collections}")

   # Get collection details
   es_collection = es.list_collections()
   print(f"Available Collections in Earth Search: {es_collection}")

STACSearch API Reference
------------------------

.. code-block:: python

   len(pc_results.get_all_items())

.. code-block:: python

   len(es_results.get_all_items())

.. code-block:: python

   pc_results.item_collection()

.. code-block:: python

   es_results.item_collection()

.. code-block:: python

    pc_results.items()

.. code-block:: python
    es_results.items()