License and Legal Information
=============================

Software License
-----------------

Open Geodata API is licensed under the MIT License:

MIT License
~~~~~~~~~~~

.. code-block:: text

   MIT License

   Copyright (c) 2025 Mirjan Ali Sha

   Permission is hereby granted, free of charge, to any person obtaining a copy
   of this software and associated documentation files (the "Software"), to deal
   in the Software without restriction, including without limitation the rights
   to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
   copies of the Software, and to permit persons to whom the Software is
   furnished to do so, subject to the following conditions:

   The above copyright notice and this permission notice shall be included in all
   copies or substantial portions of the Software.

   THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
   IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
   FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
   AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
   LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
   OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
   SOFTWARE.

Third-Party API Services Disclaimer
------------------------------------

.. danger::
   **IMPORTANT NOTICE**: This software ("open-geodata-api") is a wrapper library that 
   provides access to third-party geospatial data APIs. The author(s) and 
   contributors of this software are **NOT responsible** for:

   1. The availability, accuracy, or reliability of third-party API services
   2. Any changes to third-party API terms of service or licensing
   3. Any costs, fees, or charges imposed by third-party API providers
   4. Any data licensing restrictions imposed by third-party providers
   5. Any service interruptions, data losses, or damages resulting from third-party services

.. warning::
   **USE AT YOUR OWN RISK**: Users of this software acknowledge that they use 
   third-party APIs at their own risk and are solely responsible for compliance 
   with all applicable terms of service, data licensing agreements, and usage 
   policies of the underlying API providers.

Third-Party API Licensing
--------------------------

This software integrates with the following third-party services. **Users MUST
review and comply with their respective terms of service and licensing**:

Microsoft Planetary Computer
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 25 75

   * - Aspect
     - Details
   * - **Provider**
     - Microsoft Corporation
   * - **API License**
     - Subject to Microsoft APIs Terms of Use
   * - **Data Licensing**
     - Varies by dataset (often CC-BY-4.0, but check individual datasets)
   * - **Authentication**
     - Required (free tier available)
   * - **Terms of Service**
     - https://learn.microsoft.com/en-us/legal/microsoft-apis/terms-of-use
   * - **Important Note**
     - Some datasets may have specific attribution or usage requirements

.. note::
   Planetary Computer provides access to a vast catalog of geospatial data, but each 
   dataset may have its own specific licensing terms. Always check individual dataset 
   metadata for licensing requirements.

Element84 EarthSearch (AWS Open Data)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 25 75

   * - Aspect
     - Details
   * - **Provider**
     - Element84 / Amazon Web Services
   * - **API License**
     - Open access (no API key required)
   * - **Data Licensing**
     - Varies by dataset (typically public domain or CC licenses)
   * - **Authentication**
     - Not required for public datasets
   * - **Terms of Service**
     - https://aws.amazon.com/opendata/terms/
   * - **Important Note**
     - While API access is free, data usage may be subject to individual dataset licensing terms

User Responsibilities
---------------------

By using this software, you acknowledge and agree that:

.. admonition:: Legal Compliance Requirements

   1. **API Terms Compliance**: You are responsible for reviewing and complying with all third-party API 
      terms of service and data licensing agreements

   2. **Liability Disclaimer**: You will not hold the authors or contributors of this software liable for 
      any violations of third-party terms or licensing requirements

   3. **Service Changes**: You understand that third-party API availability, performance, and terms 
      may change without notice

   4. **Cost Responsibility**: You are responsible for any costs or fees associated with third-party API usage

   5. **Data Attribution**: You will properly attribute data sources as required by individual dataset licenses

   6. **No Warranty**: You understand that this software is provided "as-is" without any guarantees 
      of functionality, availability, or fitness for any particular purpose

Data Licensing Complexity Warning
----------------------------------

.. danger::
   **⚠️ CRITICAL NOTICE**: Geospatial data licensing can be complex and varies 
   significantly between datasets, even within the same API service.

Common Licensing Scenarios
~~~~~~~~~~~~~~~~~~~~~~~~~~~

You may encounter various licensing scenarios:

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - License Type
     - Description & Requirements
   * - **Public Domain**
     - No restrictions on use
   * - **Creative Commons (CC-BY)**
     - Requires attribution to original source
   * - **Creative Commons (CC-BY-SA)**
     - Requires attribution + share-alike licensing
   * - **Commercial Restrictions**
     - Research/non-commercial use only
   * - **Government Restrictions**
     - Institutional use limitations
   * - **Temporal Restrictions**
     - Embargo periods before public access
   * - **Geographic Restrictions**
     - Country-specific licensing terms

.. warning::
   **ALWAYS CHECK INDIVIDUAL DATASET LICENSING** before using data in your projects.
   The APIs may provide licensing information in dataset metadata, but it is YOUR
   responsibility to verify and comply with these requirements.

   Failure to comply with data licensing terms may result in legal consequences
   that are entirely your responsibility.

Commercial Use Considerations
-----------------------------

If you plan to use this software or accessed data for commercial purposes:

.. admonition:: Commercial Use Checklist

   1. **Verify API Compliance**: Ensure your intended use complies with all third-party API terms
   2. **Check Dataset Licenses**: Review individual dataset licenses for commercial use restrictions
   3. **Commercial Agreements**: Consider whether you need commercial API agreements with providers
   4. **Attribution Requirements**: Ensure proper data attribution and licensing compliance in your products
   5. **Legal Consultation**: Consult with legal counsel if uncertain about licensing requirements

Recommended Best Practices
---------------------------

Data Access Best Practices
~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   # Example: Check dataset licensing before use
   def check_dataset_license(collection_info):
       """Always verify dataset licensing before use."""
       license_info = collection_info.get('license')
       if license_info:
           print(f"Dataset license: {license_info}")
           print("Please review licensing terms before using this data")
       else:
           print("⚠️ License information not available - verify before use")

General Best Practices
~~~~~~~~~~~~~~~~~~~~~~~

1. **Review Terms Regularly**: Always review API terms of service before using any third-party service
2. **Check Dataset Metadata**: Verify individual dataset metadata for specific licensing requirements
3. **Error Handling**: Implement proper error handling for API availability issues
4. **Respect Caching**: Cache data appropriately while respecting API terms and data licensing
5. **Proper Attribution**: Provide proper attribution for all data sources in your applications
6. **Monitor Usage**: Track API usage to avoid exceeding rate limits or quotas
7. **Secure Credentials**: Keep your API credentials secure and never commit them to version control
8. **Stay Updated**: Regularly review third-party terms for updates or changes

Support and Liability Limitation
---------------------------------

.. important::
   This software is provided as an open-source tool to facilitate access to 
   geospatial APIs. The authors provide **no warranty, support, or guarantees**.

For Support Issues
~~~~~~~~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 40 60

   * - Issue Type
     - Where to Get Help
   * - **Third-party API Access**
     - Contact the respective API provider directly
   * - **Data Licensing Questions**
     - Consult the dataset provider or legal counsel
   * - **Software Bugs**
     - Submit issues to the `project repository <https://github.com/Mirjan-Ali-Sha/open-geodata-api/issues>`_
   * - **Feature Requests**
     - Submit requests to the project repository
   * - **General Usage Questions**
     - Check the FAQ section or create a discussion

Liability Disclaimer
~~~~~~~~~~~~~~~~~~~~

.. danger::
   The authors expressly disclaim all liability for any direct, indirect, 
   incidental, special, or consequential damages arising from the use of this 
   software or third-party services accessed through it.

Attribution Requirements
------------------------

Software Attribution
~~~~~~~~~~~~~~~~~~~~~

When using this software in your projects, please consider citing:

.. code-block:: text

   Open Geodata API - Unified Python Client for Satellite Data Access
   Author: Mirjan Ali Sha
   GitHub: https://github.com/Mirjan-Ali-Sha/open-geodata-api
   License: MIT

Data Attribution
~~~~~~~~~~~~~~~~

Always provide proper attribution for the satellite data you use. Examples:

.. code-block:: text

   # For Sentinel-2 data via Planetary Computer:
   "Sentinel-2 imagery courtesy of the U.S. Geological Survey and European Space Agency, 
   accessed via Microsoft Planetary Computer"

   # For Landsat data via EarthSearch:
   "Landsat imagery courtesy of the U.S. Geological Survey, 
   accessed via Element84 EarthSearch"

Legal Document Information
--------------------------

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - Document Info
     - Details
   * - **Last Updated**
     - 2025-06-22
   * - **License Version**
     - 1.0
   * - **Document Type**
     - Software License + Third-Party Service Disclaimers
   * - **Governing Law**
     - Subject to applicable jurisdictions and third-party terms

.. note::
   This license document is provided for informational purposes. Users should 
   consult with legal counsel for specific questions about licensing compliance 
   and liability in their particular use cases.
