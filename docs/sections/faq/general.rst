General FAQ
===========

What is Open Geodata API?
--------------------------

**Q**: What exactly is Open Geodata API and how does it differ from other geospatial libraries?

**A**: Open Geodata API is a unified Python client that provides seamless access to multiple open geospatial data APIs, specifically Microsoft Planetary Computer and AWS EarthSearch. Unlike other libraries that focus on data processing, we focus on data **access** and **URL management**, giving you the flexibility to use any raster reading package you prefer.

Our core philosophy is: **We provide URLs - you choose how to read the data**.

Key differentiators:

- **Unified interface** across multiple APIs with consistent syntax
- **Automatic URL signing/validation** - no more expired URL headaches  
- **Zero lock-in** - works with any raster reading library
- **Built-in best practices** for search, filtering, and download
- **Production-ready** with robust error handling

What satellite data can I access?
----------------------------------

**Q**: What types of satellite data are available through the API?

**A**: Through Planetary Computer and EarthSearch, you can access:

**Optical Imagery:**
- **Sentinel-2** (10-60m resolution, 5-day revisit)
- **Landsat 8/9** (30m resolution, 16-day revisit)  
- **MODIS** (250m-1km resolution, daily)

**SAR Imagery:**
- **Sentinel-1** (10m resolution, weather-independent)

**Derived Products:**
- **NAIP** (high-resolution aerial imagery, US)
- **USGS 3DEP** (elevation data)
- **Various climate and environmental datasets**

Use ``ogapi collections list`` to see all available datasets.

How is this different from using APIs directly?
------------------------------------------------

**Q**: Why use this package instead of the provider APIs directly?

**A**: Several key advantages:

**Simplified Development:**
- Single learning curve vs. multiple API syntaxes
- Consistent error handling across providers
- Built-in best practices and optimizations

**URL Management:**
- Automatic signing for Planetary Computer URLs
- Automatic re-signing of expired URLs
- Validation for EarthSearch URLs
- No manual authentication workflow

**Flexibility:**
- Use any raster package (rioxarray, rasterio, GDAL)
- No vendor lock-in to specific processing libraries
- Easy switching between providers

**Production Features:**
- Robust error handling with helpful messages
- Comprehensive logging and debugging support
- CLI for automation and scripting

What are the costs involved?
----------------------------

**Q**: Are there any costs for using this service?

**A**: The software itself is free and open-source. However:

**API Access Costs:**
- **Planetary Computer**: Free tier available, may have usage limits
- **EarthSearch**: Completely free and open access
- **Data Transfer**: Standard cloud egress charges may apply for large downloads

**Infrastructure Costs:**
- You pay for your own compute/storage resources
- No additional costs from our software

**Best Practices for Cost Management:**
- Use cloud cover filters to reduce unnecessary downloads
- Download only required bands/assets
- Use overview levels for previews
- Consider regional data processing to minimize transfer costs

Do I need programming experience?
---------------------------------

**Q**: What level of programming knowledge do I need?

**A**: **Basic Python knowledge** is recommended, but we provide tools for different skill levels:

**Beginners:**
- Comprehensive CLI for command-line usage
- Copy-paste examples in documentation  
- Step-by-step tutorials with explanations

**Intermediate:**
- Python API with clear documentation
- Integration examples with popular libraries
- Pre-built workflows for common tasks

**Advanced:**
- Full API customization and extension
- Performance optimization techniques
- Production deployment patterns

**Learning Resources:**
- Start with :doc:`../getting-started/index`
- Follow :doc:`../examples/basic-workflows`
- Use CLI commands: ``ogapi --help``

Can I use this for commercial projects?
---------------------------------------

**Q**: Are there restrictions on commercial use?

**A**: **The software is MIT licensed** - you can use it commercially. However, you must comply with:

**Third-Party API Terms:**
- Review Planetary Computer terms of service
- Check EarthSearch/AWS usage policies
- Some datasets may have usage restrictions

**Data Licensing:**
- Each satellite dataset has its own license
- Most are public domain or Creative Commons
- Always check individual dataset metadata
- Provide proper attribution when required

**Recommendations:**
- Consult legal counsel for commercial applications
- Review all relevant terms of service
- Implement proper data attribution in your applications

What about data privacy and security?
--------------------------------------

**Q**: How is my data and usage tracked?

**A**: **We prioritize user privacy:**

**Our Software:**
- No tracking or analytics in the software
- No data collection or transmission to us
- Open-source code - you can verify everything

**Third-Party APIs:**
- Planetary Computer and EarthSearch have their own policies
- Review their respective privacy policies
- API usage may be logged by providers

**Best Practices:**
- Keep API credentials secure
- Don't commit credentials to version control
- Use environment variables for sensitive information
- Review third-party privacy policies

How do I get help and support?
-------------------------------

**Q**: Where can I get help when I have issues?

**A**: Multiple support channels available:

**Documentation:**
- Comprehensive docs at https://open-geodata-api.readthedocs.io
- FAQ sections for common issues
- Troubleshooting guides with solutions

**Community Support:**
- GitHub Issues for bug reports and feature requests
- GitHub Discussions for questions and sharing
- Stack Overflow with ``open-geodata-api`` tag

**Self-Help Resources:**
- Built-in help: ``ogapi --help`` for CLI
- Example repository with working code
- Interactive tutorials and notebooks

**Response Times:**
- Community support: Best effort
- Critical bugs: Usually addressed quickly
- Feature requests: Considered based on community needs

**When Reporting Issues:**
- Include version information: ``import open_geodata_api; print(open_geodata_api.__version__)``
- Provide minimal reproducible example
- Include full error traceback
- Specify your environment (OS, Python version)

What are the system requirements?
----------------------------------

**Q**: What do I need to run this software?

**A**: **Minimum Requirements:**

**Software:**
- Python 3.8 or higher
- 1GB+ RAM (more for large datasets)
- Internet connection for API access

**Operating Systems:**
- Linux (all distributions)
- macOS (10.14+)
- Windows (10+)

**Recommended Setup:**
- Python 3.9+ for best performance
- 8GB+ RAM for large-scale processing
- SSD storage for faster data access
- Virtual environment for dependency management

**Optional Dependencies:**
- ``rioxarray`` for raster I/O
- ``geopandas`` for spatial analysis
- ``planetary-computer`` for PC authentication

Can I contribute to the project?
---------------------------------

**Q**: How can I help improve the software?

**A**: **We welcome all types of contributions!**

**Ways to Contribute:**
- Report bugs and issues
- Suggest new features
- Improve documentation
- Add examples and tutorials
- Submit code improvements
- Share your use cases

**Getting Started:**
- See :doc:`../development/contributing` for detailed guidelines
- Check GitHub Issues for "good first issue" labels
- Join discussions to understand project direction

**Contribution Process:**
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

**Recognition:**
- All contributors are acknowledged
- Significant contributions earn maintainer status
- Community-driven development model

Is this production-ready?
-------------------------

**Q**: Can I use this in production applications?

**A**: **Yes, with proper planning:**

**Production Features:**
- Comprehensive error handling
- Automatic retry and recovery
- Extensive test coverage
- Performance optimizations
- CLI for automation

**Production Considerations:**
- Plan for API rate limits and quotas
- Implement monitoring and alerting
- Consider data backup and storage strategies
- Review third-party service availability SLAs
- Test thoroughly with your specific use cases

**Deployment Best Practices:**
- Use virtual environments
- Pin dependency versions
- Implement proper logging
- Monitor resource usage
- Have fallback strategies for API outages

**Production Support:**
- Community-driven support model
- No guaranteed SLA or commercial support
- Consider your risk tolerance and requirements
