Changelog
=========

All notable changes to Open Geodata API will be documented in this file.

The format is based on `Keep a Changelog <https://keepachangelog.com/en/1.0.0/>`_,
and this project adheres to `Semantic Versioning <https://semver.org/spec/v2.0.0.html>`_.

[Unreleased]
------------

### Added
- Performance optimizations for large dataset processing
- Advanced error recovery mechanisms
- Enhanced CLI workflows and batch processing
- Integration examples with popular ML frameworks

### Changed
- Improved memory management for large collections
- Enhanced URL caching mechanisms
- Optimized search performance

### Fixed
- URL expiration handling edge cases
- Memory leaks in batch processing
- CLI progress bar display issues

[0.1.0] - 2025-06-22
--------------------

### Added
- **Core STAC Classes**: Complete implementation of STACItem, STACItemCollection, and STACAsset
- **Multi-Provider Support**: Unified access to Planetary Computer and EarthSearch APIs
- **Automatic URL Management**: Intelligent URL signing, validation, and expiration handling
- **Comprehensive CLI**: Full command-line interface with collections, search, download, and utility commands
- **Smart Download System**: Intelligent downloading with progress tracking, resume capability, and folder organization
- **Filtering Utilities**: Cloud cover filtering, temporal filtering, and quality assessment tools
- **Error Recovery**: Robust error handling with automatic retry logic and helpful error messages
- **Documentation**: Complete documentation with examples, tutorials, and API reference

#### Core Features

**API Clients**:
- ``PlanetaryComputerCollections``: Client for Microsoft Planetary Computer with automatic URL signing
- ``EarthSearchCollections``: Client for Element84 EarthSearch with direct access
- Unified interface across both providers with consistent error handling

**Data Models**:
- ``STACItem``: Individual satellite scenes with metadata and asset management
- ``STACItemCollection``: Collections of items with bulk operations and DataFrame conversion
- ``STACAsset``: Individual files with provider-specific URL handling
- ``STACSearch``: Search result containers with pagination support

**Factory Functions**:
- ``planetary_computer(auto_sign=True)``: Create PC client with automatic URL signing
- ``earth_search()``: Create EarthSearch client with validation
- ``get_clients()``: Get both clients in a single call

#### Utility Functions

**Filtering**:
- ``filter_by_cloud_cover()``: Filter items by cloud cover percentage
- ``filter_by_date_range()``: Filter items by temporal criteria
- ``filter_by_geometry()``: Filter items by spatial intersection

**Download Management**:
- ``download_datasets()``: Universal download function with intelligent input detection
- ``download_url()``: Single file download with provider handling
- ``download_items()``: Bulk download with organization
- ``download_seasonal_data()``: Temporal dataset downloads
- Parallel downloading with configurable workers
- Resume capability for interrupted downloads
- Progress tracking with customizable progress bars

**URL Management**:
- ``is_url_expired()``: Check URL expiration status
- ``is_signed_url()``: Detect signed URLs
- ``re_sign_url_if_needed()``: Automatic URL refresh
- ``validate_urls()``: Batch URL validation

**Analysis Helpers**:
- ``create_download_summary()``: Generate download reports
- ``export_urls_to_json()``: Export URLs for external processing
- ``calculate_ndvi()``: Built-in NDVI calculation
- ``get_seasonal_statistics()``: Temporal analysis tools

#### Command Line Interface

**Collections Management**:
- ``ogapi collections list``: Browse available datasets
- ``ogapi collections search``: Find collections by keyword
- ``ogapi collections info``: Get detailed collection metadata

**Data Search**:
- ``ogapi search items``: Search for satellite imagery
- ``ogapi search quick``: Simplified search interface
- ``ogapi search compare``: Compare providers

**Item Management**:
- ``ogapi items info``: Get item details
- ``ogapi items assets``: List available assets
- ``ogapi items urls``: Generate asset URLs
- ``ogapi items compare``: Compare items by quality

**Download Operations**:
- ``ogapi download search-results``: Download from search results
- ``ogapi download url``: Download single files
- ``ogapi download urls-json``: Download from URL files
- ``ogapi download seasonal``: Download temporal datasets

**Utilities**:
- ``ogapi utils filter-clouds``: Cloud cover filtering
- ``ogapi utils export-urls``: URL export functionality
- ``ogapi utils validate-urls``: URL validation
- ``ogapi utils analyze``: Data analysis tools

#### Key Capabilities

**Unified API Access**:
- Single interface for multiple satellite data providers
- Consistent search parameters across providers
- Automatic provider detection and optimization
- Built-in best practices and error handling

**Intelligent URL Management**:
- Automatic URL signing for Planetary Computer
- Expiration detection and refresh
- Provider-specific optimizations
- Bulk URL operations with caching

**Flexible Data Reading**:
- Compatible with any raster reading library (rioxarray, rasterio, GDAL)
- No lock-in to specific processing frameworks
- Ready-to-use URLs for immediate data access
- Support for all common satellite data formats

**Production-Ready Features**:
- Comprehensive error handling and recovery
- Progress tracking and reporting
- Memory-efficient processing for large datasets
- Configurable timeouts and retry logic
- Logging and debugging support

#### Provider Support

**Planetary Computer**:
- Comprehensive collection catalog
- Automatic URL signing with planetary-computer package
- Advanced search capabilities with complex queries
- High-performance access to Microsoft's data catalog

**EarthSearch**:
- Open access with no authentication required
- Direct COG (Cloud Optimized GeoTIFF) access
- AWS-hosted data with global availability
- Permanent URLs with no expiration

#### Documentation and Examples

**Complete Documentation**:
- Getting started guide with step-by-step tutorials
- Comprehensive API reference with examples
- CLI documentation with usage patterns
- Real-world examples and use cases
- Troubleshooting guide with common solutions

**Example Workflows**:
- Basic data discovery and access
- Multi-temporal NDVI analysis
- Change detection workflows
- Agricultural monitoring examples
- Environmental monitoring applications
- Integration with popular libraries (Dask, GeoPandas, etc.)

#### Installation and Dependencies

**Core Dependencies**:
- ``requests >= 2.25.0``: HTTP client for API access
- ``pandas >= 1.3.0``: Data manipulation and analysis
- ``planetary-computer >= 1.0.0``: Planetary Computer integration
- ``tqdm >= 4.67.1``: Progress bars and tracking
- ``click >= 8.0.0``: Command-line interface framework

**Optional Dependencies**:
- ``rioxarray >= 0.11.0``: Raster I/O capabilities
- ``rasterio >= 1.3.0``: Geospatial raster processing
- ``xarray >= 0.19.0``: N-dimensional labeled arrays
- ``geopandas >= 0.10.0``: Geospatial data analysis
- ``shapely >= 1.8.0``: Geometric operations

**Installation Options**:
- ``pip install open-geodata-api``: Core package
- ``pip install open-geodata-api[io]``: With raster I/O
- ``pip install open-geodata-api[spatial]``: With spatial analysis
- ``pip install open-geodata-api[complete]``: Full installation

#### Platform Support

**Operating Systems**:
- Linux (all major distributions)
- macOS (10.14+ including Apple Silicon)
- Windows (10+)

**Python Versions**:
- Python 3.8+
- Tested on Python 3.8, 3.9, 3.10, 3.11

#### Breaking Changes
- N/A (initial release)

#### Migration Guide
- N/A (initial release)

#### Known Issues
- Large dataset processing may require significant memory
- Planetary Computer URLs expire and require periodic refresh
- Some geospatial dependencies may require system libraries (GDAL)

#### Performance Notes
- Automatic URL signing adds minimal overhead (~10ms per URL)
- Parallel downloads significantly improve throughput for multiple files
- Chunked loading recommended for files >1GB
- Search performance varies by provider and query complexity

#### Security Considerations
- Planetary Computer requires API authentication via planetary-computer package
- URLs may contain temporary access tokens
- No sensitive data is stored or transmitted by the package itself
- Users responsible for compliance with provider terms of service

### Contributors
- Mirjan Ali Sha (@Mirjan-Ali-Sha) - Initial development and architecture

### Acknowledgments
- Microsoft Planetary Computer team for the comprehensive data catalog
- Element84 team for EarthSearch and open data access
- STAC community for standardization efforts
- Python geospatial community for foundational libraries

---

## Version History Summary

| Version | Date       | Description                                    |
|---------|------------|------------------------------------------------|
| 0.1.0   | 2025-06-22 | Initial release with full feature set         |

## Upcoming Releases

### [0.2.0] - Planned Features
- Additional provider support (NASA EarthData, Google Earth Engine compatibility)
- Enhanced caching mechanisms with persistent storage
- Advanced spatial analysis integration
- Performance optimizations for very large datasets
- Jupyter widget integration for interactive exploration

### [0.3.0] - Future Enhancements
- Machine learning integration helpers
- Advanced temporal analysis tools
- Custom STAC API support
- Enhanced visualization capabilities
- Workflow orchestration tools

## Support and Community

**Bug Reports**: Report issues on `GitHub Issues <https://github.com/Mirjan-Ali-Sha/open-geodata-api/issues>`_

**Feature Requests**: Submit enhancement requests with detailed use cases

**Documentation**: Contributions to documentation are welcome

**Community**: Join discussions on `GitHub Discussions <https://github.com/Mirjan-Ali-Sha/open-geodata-api/discussions>`_

## Release Process

1. **Development**: Features developed on feature branches
2. **Testing**: Comprehensive testing including unit, integration, and performance tests
3. **Documentation**: Documentation updated for all changes
4. **Review**: Code review and approval process
5. **Release**: Semantic versioning with detailed changelog
6. **Distribution**: Automated distribution to PyPI

---

*This changelog follows semantic versioning. For details about our versioning strategy, see our contributing guide.*
