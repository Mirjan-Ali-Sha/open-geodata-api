Changelog
=========

All notable changes to this project will be documented in this file.

The format is based on `Keep a Changelog <https://keepachangelog.com/en/1.0.0/>`_,
and this project adheres to `Semantic Versioning <https://semver.org/spec/v2.0.0.html>`_.

Unreleased
----------

Added
~~~~~

Changed
~~~~~~~

Fixed
~~~~~

[0.1.2] - 2025-06-21
---------------------

Added
~~~~~

* Initial release of Open Geodata API
* Support for Microsoft Planetary Computer API
* Support for Element84 EarthSearch API
* Unified STAC interface for both providers
* Automatic URL signing for Planetary Computer
* URL validation for EarthSearch
* Core STAC classes: STACItem, STACItemCollection, STACAssets
* Factory functions for easy client creation
* DataFrame conversion support
* URL export functionality
* Comprehensive documentation and examples
* MIT license with third-party disclaimers

Features
~~~~~~~

* **Unified API Access**: Single interface for multiple geospatial APIs
* **Automatic URL Management**: Provider-specific URL handling
* **Maximum Flexibility**: Use any raster reading package
* **Zero Lock-in**: No forced dependencies
* **Production Ready**: Robust error handling

Features of Extra Utils Functions
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
* **Intelligent Input Detection** - Automatically handles URLs, dicts, items, seasonal data
* **Automatic URL Management** - Re-signs expired URLs with warnings
* **Flexible Destinations** - File, directory, or auto-naming support
* **Progress Tracking** - Visual progress bars for downloads
* **Organized Structure** - Creates logical folder hierarchies
* **Error Handling** - Robust error handling with partial download support
* **Provider Awareness** - Handles PC signing and ES validation
* **Batch Processing** - Efficient handling of multiple files
* **Summary Reports** - Detailed download statistics