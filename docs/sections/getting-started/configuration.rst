Configuration Reference
=======================

Complete guide to configuring and optimizing the open-geodata-api library for different environments and use cases. Most of the configuration options are not tested in the CI, so please use them with caution.

Overview
--------

The configuration system provides flexible control over:

- **Provider Settings** - Default providers and authentication
- **Download Behavior** - Timeouts, retries, and parallel processing
- **Memory Management** - Caching and batch processing optimization
- **Error Handling** - Retry strategies and logging levels
- **Performance Tuning** - Worker counts and resource allocation

Global Configuration
--------------------

set_global_config
~~~~~~~~~~~~~~~~~~

.. py:function:: set_global_config(**config_params)

   Set global configuration parameters for the library.

   :param config_params: Configuration parameters to set
   :type config_params: various types
   :returns: Updated configuration dictionary
   :rtype: dict

**Basic Configuration Setup**:

.. code-block:: python

    from open_geodata_api.utils import set_global_config
    
    # Basic configuration
    config = set_global_config(
        default_provider='planetary_computer',
        auto_sign_urls=True,
        max_download_workers=4,
        default_timeout=120,
        progress_bar=True
    )
    
    print("🔧 Configuration applied:")
    for key, value in config.items():
        print(f"   {key}: {value}")

**Advanced Configuration**:

.. code-block:: python

    # Production-ready configuration
    production_config = set_global_config(
        # Provider settings
        default_provider='planetary_computer',
        auto_sign_urls=True,
        provider_retry_attempts=3,
        
        # Download optimization
        max_download_workers=8,
        default_timeout=300,
        chunk_size=32768,
        max_retries=5,
        
        # Memory management
        cache_size_mb=1000,
        batch_size_auto=True,
        memory_limit_gb=8,
        
        # Performance
        progress_bar=False,  # Disable in production
        verbose_errors=False,
        parallel_downloads=True,
        
        # Quality control
        verify_downloads=True,
        min_file_size_mb=1,
        check_url_expiry=True
    )

get_global_config
~~~~~~~~~~~~~~~~~

.. py:function:: get_global_config(key=None)

   Get global configuration parameters.

   :param key: Specific configuration key (None for all)
   :type key: str or None
   :returns: Configuration value or full configuration
   :rtype: any or dict

**Configuration Retrieval**:

.. code-block:: python

    from open_geodata_api.utils import get_global_config
    
    # Get specific setting
    max_workers = get_global_config('max_download_workers')
    print(f"Max workers: {max_workers}")
    
    # Get all settings
    all_config = get_global_config()
    print("Current configuration:")
    for key, value in all_config.items():
        print(f"  {key}: {value}")

Environment-Specific Configuration
----------------------------------

**Development Environment**:

.. code-block:: python

    def setup_development_config():
        """Optimized for development and testing."""
        
        return set_global_config(
            # Conservative settings for development
            default_provider='planetary_computer',
            auto_sign_urls=True,
            max_download_workers=2,
            default_timeout=60,
            batch_size=5,
            
            # Development features
            progress_bar=True,
            verbose_errors=True,
            debug_mode=True,
            cache_size_mb=100,
            
            # Quality checks
            verify_downloads=True,
            validate_inputs=True,
            
            # Logging
            log_level='DEBUG',
            log_file='development.log'
        )
    
    # Apply development configuration
    dev_config = setup_development_config()

**Production Environment**:

.. code-block:: python

    def setup_production_config():
        """Optimized for production performance."""
        
        return set_global_config(
            # High-performance settings
            default_provider='planetary_computer',
            auto_sign_urls=True,
            max_download_workers=12,
            default_timeout=300,
            batch_size=20,
            
            # Production optimization
            progress_bar=False,
            verbose_errors=False,
            debug_mode=False,
            cache_size_mb=2000,
            
            # Reliability
            max_retries=5,
            verify_downloads=True,
            check_url_expiry=True,
            
            # Resource management
            memory_limit_gb=16,
            cleanup_temp_files=True,
            
            # Logging
            log_level='INFO',
            log_file='/var/log/geodata_api.log'
        )
    
    # Apply production configuration
    prod_config = setup_production_config()

**Testing Environment**:

.. code-block:: python

    def setup_testing_config():
        """Optimized for automated testing."""
        
        return set_global_config(
            # Test-friendly settings
            default_provider='planetary_computer',
            auto_sign_urls=False,  # Use mock URLs
            max_download_workers=1,
            default_timeout=30,
            batch_size=2,
            
            # Testing features
            progress_bar=False,
            verbose_errors=True,
            debug_mode=True,
            mock_mode=True,
            
            # Fast testing
            cache_size_mb=50,
            verify_downloads=False,
            
            # Test isolation
            temp_dir='./test_temp/',
            cleanup_temp_files=True
        )
    
    # Apply testing configuration
    test_config = setup_testing_config()

Performance Optimization
------------------------

optimize_for_large_datasets
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. py:function:: optimize_for_large_datasets(dataset_size_gb, available_memory_gb)

   Optimize library settings for large dataset processing.

   :param dataset_size_gb: Expected dataset size in GB
   :type dataset_size_gb: float
   :param available_memory_gb: Available system memory in GB
   :type available_memory_gb: float
   :returns: Optimized configuration recommendations
   :rtype: dict

**Automatic Optimization**:

.. code-block:: python

    from open_geodata_api.utils import optimize_for_large_datasets
    
    # Optimize for 100GB dataset with 32GB RAM
    optimization = optimize_for_large_datasets(
        dataset_size_gb=100.0,
        available_memory_gb=32.0
    )
    
    print("🚀 Optimization recommendations:")
    print(f"   Batch size: {optimization['batch_size']} items")
    print(f"   Max workers: {optimization['max_workers']}")
    print(f"   Memory per worker: {optimization['memory_per_worker_mb']} MB")
    print(f"   Processing strategy: {optimization['strategy']}")
    
    # Apply optimizations
    optimized_config = set_global_config(**optimization['config'])

**Manual Performance Tuning**:

.. code-block:: python

    def tune_for_performance(system_specs):
        """Manual performance tuning based on system specs."""
        
        cpu_cores = system_specs['cpu_cores']
        ram_gb = system_specs['ram_gb']
        storage_type = system_specs['storage_type']  # 'ssd' or 'hdd'
        
        # Calculate optimal settings
        if storage_type == 'ssd':
            max_workers = min(cpu_cores * 2, 16)
            chunk_size = 65536  # 64KB for SSD
        else:
            max_workers = min(cpu_cores, 8)
            chunk_size = 32768  # 32KB for HDD
        
        batch_size = max(5, min(ram_gb // 2, 50))
        
        return set_global_config(
            max_download_workers=max_workers,
            chunk_size=chunk_size,
            batch_size=batch_size,
            memory_limit_gb=ram_gb * 0.8,  # Use 80% of RAM
            cache_size_mb=min(ram_gb * 100, 4000)  # Up to 4GB cache
        )
    
    # Example system specifications
    my_system = {
        'cpu_cores': 8,
        'ram_gb': 16,
        'storage_type': 'ssd'
    }
    
    performance_config = tune_for_performance(my_system)

Configuration Profiles
----------------------

**Complete Configuration Profiles**:

.. code-block:: python

    class ConfigurationProfiles:
        """Pre-defined configuration profiles for common use cases."""
        
        @staticmethod
        def minimal():
            """Minimal resource usage configuration."""
            return set_global_config(
                max_download_workers=1,
                default_timeout=30,
                batch_size=1,
                cache_size_mb=50,
                progress_bar=False,
                verify_downloads=False
            )
        
        @staticmethod
        def balanced():
            """Balanced performance and resource usage."""
            return set_global_config(
                max_download_workers=4,
                default_timeout=120,
                batch_size=10,
                cache_size_mb=500,
                progress_bar=True,
                verify_downloads=True,
                max_retries=3
            )
        
        @staticmethod
        def high_performance():
            """Maximum performance configuration."""
            return set_global_config(
                max_download_workers=12,
                default_timeout=300,
                batch_size=25,
                cache_size_mb=2000,
                progress_bar=False,
                parallel_downloads=True,
                max_retries=5,
                chunk_size=65536
            )
        
        @staticmethod
        def research():
            """Configuration optimized for research workflows."""
            return set_global_config(
                max_download_workers=6,
                default_timeout=180,
                batch_size=15,
                cache_size_mb=1000,
                progress_bar=True,
                verify_downloads=True,
                verbose_errors=True,
                quality_checks=True,
                preserve_metadata=True
            )
    
    # Use predefined profiles
    ConfigurationProfiles.balanced()
    print("Applied balanced configuration profile")

Dynamic Configuration
---------------------

**Runtime Configuration Adjustment**:

.. code-block:: python

    def adaptive_configuration_manager():
        """Automatically adjust configuration based on runtime conditions."""
        
        import psutil
        import time
        
        def monitor_and_adjust():
            # Get current system status
            cpu_percent = psutil.cpu_percent(interval=1)
            memory_percent = psutil.virtual_memory().percent
            
            current_config = get_global_config()
            new_config = current_config.copy()
            
            # Adjust based on system load
            if cpu_percent > 80:
                # High CPU usage - reduce workers
                new_config['max_download_workers'] = max(1, current_config.get('max_download_workers', 4) - 1)
                print(f"🔧 Reduced workers due to high CPU: {new_config['max_download_workers']}")
            
            elif cpu_percent < 30:
                # Low CPU usage - can increase workers
                new_config['max_download_workers'] = min(8, current_config.get('max_download_workers', 4) + 1)
                print(f"🔧 Increased workers due to low CPU: {new_config['max_download_workers']}")
            
            if memory_percent > 85:
                # High memory usage - reduce batch size
                new_config['batch_size'] = max(1, current_config.get('batch_size', 10) // 2)
                print(f"🔧 Reduced batch size due to high memory: {new_config['batch_size']}")
            
            # Apply adjustments
            if new_config != current_config:
                set_global_config(**new_config)
        
        return monitor_and_adjust
    
    # Use adaptive configuration
    adaptive_monitor = adaptive_configuration_manager()
    adaptive_monitor()  # Call periodically during processing

Configuration Validation
------------------------

**Configuration Validation Examples**:

.. code-block:: python

    def validate_configuration(config=None):
        """Validate configuration parameters."""
        
        if config is None:
            config = get_global_config()
        
        validation_results = {
            'valid': True,
            'warnings': [],
            'errors': [],
            'recommendations': []
        }
        
        # Validate worker count
        max_workers = config.get('max_download_workers', 4)
        if max_workers > 16:
            validation_results['warnings'].append(
                f"High worker count ({max_workers}) may cause rate limiting"
            )
        elif max_workers < 1:
            validation_results['errors'].append("Worker count must be at least 1")
            validation_results['valid'] = False
        
        # Validate timeout
        timeout = config.get('default_timeout', 120)
        if timeout < 30:
            validation_results['warnings'].append(
                f"Short timeout ({timeout}s) may cause download failures"
            )
        elif timeout > 600:
            validation_results['recommendations'].append(
                f"Very long timeout ({timeout}s) - consider shorter value"
            )
        
        # Validate memory settings
        cache_size = config.get('cache_size_mb', 500)
        if cache_size > 4000:
            validation_results['warnings'].append(
                f"Large cache size ({cache_size}MB) may consume significant memory"
            )
        
        # Check for conflicting settings
        if config.get('progress_bar', True) and config.get('debug_mode', False):
            validation_results['warnings'].append(
                "Progress bar and debug mode may interfere with output"
            )
        
        return validation_results
    
    # Validate current configuration
    validation = validate_configuration()
    
    if validation['valid']:
        print("✅ Configuration is valid")
    else:
        print("❌ Configuration has errors:")
        for error in validation['errors']:
            print(f"   - {error}")
    
    if validation['warnings']:
        print("⚠️ Warnings:")
        for warning in validation['warnings']:
            print(f"   - {warning}")

Configuration Persistence
-------------------------

**Save and Load Configuration**:

.. code-block:: python

    import json
    import os
    from pathlib import Path
    
    def save_configuration(config_name="default", config_dir="~/.geodata_api/"):
        """Save current configuration to file."""
        
        config_path = Path(config_dir).expanduser()
        config_path.mkdir(parents=True, exist_ok=True)
        
        config_file = config_path / f"{config_name}.json"
        current_config = get_global_config()
        
        with open(config_file, 'w') as f:
            json.dump(current_config, f, indent=2)
        
        print(f"💾 Configuration saved to {config_file}")
        return str(config_file)
    
    def load_configuration(config_name="default", config_dir="~/.geodata_api/"):
        """Load configuration from file."""
        
        config_path = Path(config_dir).expanduser()
        config_file = config_path / f"{config_name}.json"
        
        if not config_file.exists():
            print(f"❌ Configuration file not found: {config_file}")
            return None
        
        with open(config_file, 'r') as f:
            config = json.load(f)
        
        set_global_config(**config)
        print(f"📂 Configuration loaded from {config_file}")
        return config
    
    # Save current configuration
    save_configuration("my_research_config")
    
    # Load saved configuration
    load_configuration("my_research_config")

**Configuration Templates**:

.. code-block:: python

    def create_configuration_templates():
        """Create configuration templates for different scenarios."""
        
        templates = {
            'vegetation_monitoring': {
                'default_provider': 'planetary_computer',
                'auto_sign_urls': True,
                'max_download_workers': 6,
                'batch_size': 15,
                'asset_preferences': ['B08', 'B04', 'B03', 'B02'],
                'quality_filters': {
                    'max_cloud_cover': 20,
                    'min_data_coverage': 80
                },
                'processing_options': {
                    'calculate_ndvi': True,
                    'temporal_analysis': True,
                    'export_statistics': True
                }
            },
            
            'change_detection': {
                'default_provider': 'planetary_computer',
                'auto_sign_urls': True,
                'max_download_workers': 8,
                'batch_size': 10,
                'asset_preferences': ['B08', 'B04', 'B11', 'B12'],
                'quality_filters': {
                    'max_cloud_cover': 10,
                    'temporal_consistency': True
                },
                'processing_options': {
                    'coregister_images': True,
                    'radiometric_correction': True,
                    'export_change_maps': True
                }
            },
            
            'water_mapping': {
                'default_provider': 'earth_search',
                'max_download_workers': 4,
                'batch_size': 8,
                'asset_preferences': ['B08', 'B11', 'B12'],
                'quality_filters': {
                    'max_cloud_cover': 15,
                    'water_mask_confidence': 0.8
                },
                'processing_options': {
                    'water_indices': ['NDWI', 'MNDWI'],
                    'flood_mapping': True,
                    'temporal_water_extent': True
                }
            }
        }
        
        # Save templates
        template_dir = Path("~/.geodata_api/templates/").expanduser()
        template_dir.mkdir(parents=True, exist_ok=True)
        
        for template_name, template_config in templates.items():
            template_file = template_dir / f"{template_name}.json"
            with open(template_file, 'w') as f:
                json.dump(template_config, f, indent=2)
            print(f"📋 Template saved: {template_name}")
        
        return templates
    
    # Create and save templates
    templates = create_configuration_templates()

Best Practices
--------------

**Configuration Management Best Practices**:

1. **Environment Separation**:
   - Use different configurations for dev/test/prod
   - Store configurations in version control
   - Use environment variables for sensitive settings

2. **Performance Optimization**:
   - Start with conservative settings
   - Monitor system resources during processing
   - Adjust based on actual performance metrics

3. **Error Handling**:
   - Always validate configuration before use
   - Implement fallback configurations
   - Log configuration changes

4. **Resource Management**:
   - Set memory limits based on available RAM
   - Configure appropriate timeouts
   - Balance worker count with system capacity

5. **Quality Assurance**:
   - Enable verification in production
   - Use progress bars for long operations
   - Implement comprehensive logging

**Complete Configuration Workflow Example**:

.. code-block:: python

    def complete_configuration_workflow():
        """Example of complete configuration management workflow."""
        
        print("🔧 Starting Configuration Workflow")
        
        # Step 1: Detect environment
        environment = os.getenv('GEODATA_ENV', 'development')
        print(f"📍 Environment: {environment}")
        
        # Step 2: Load base configuration
        if environment == 'production':
            base_config = setup_production_config()
        elif environment == 'testing':
            base_config = setup_testing_config()
        else:
            base_config = setup_development_config()
        
        # Step 3: Apply optimizations
        optimization = optimize_for_large_datasets(
            dataset_size_gb=50.0,
            available_memory_gb=16.0
        )
        
        optimized_config = {**base_config, **optimization['config']}
        set_global_config(**optimized_config)
        
        # Step 4: Validate configuration
        validation = validate_configuration()
        
        if not validation['valid']:
            print("❌ Configuration validation failed")
            for error in validation['errors']:
                print(f"   - {error}")
            return False
        
        # Step 5: Save configuration
        config_name = f"{environment}_optimized"
        save_configuration(config_name)
        
        # Step 6: Display final configuration
        final_config = get_global_config()
        print("\n✅ Final Configuration:")
        for key, value in final_config.items():
            print(f"   {key}: {value}")
        
        return True
    
    # Run complete workflow
    success = complete_configuration_workflow()

See Also
--------

- :doc:`../quickstart` - Getting started guide
- :doc:`../tutorials/optimization` - Performance optimization tutorials
- :doc:`../api-reference/utility-functions` - Utility functions documentation
- :doc:`../examples/advanced-workflows` - Advanced workflow examples
