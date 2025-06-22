Workflow CLI Commands
=====================

Predefined workflows for common satellite data processing tasks with automated configuration and best practices.

Basic Usage
-----------

.. code-block:: bash

   ogapi workflows --help
   ogapi workflows seasonal-analysis --help
   ogapi workflows batch-processing --help
   ogapi workflows quality-assessment --help

Commands Overview
-----------------

seasonal-analysis
~~~~~~~~~~~~~~~~~

Automated seasonal data collection, filtering, and organization for temporal analysis.

**Syntax**:

.. code-block:: bash

   ogapi workflows seasonal-analysis [OPTIONS]

**Configuration Options**:

- ``--config`` / ``-c``: YAML configuration file [required]
- ``--year`` / ``-y``: Year for seasonal analysis [default: current year]
- ``--output-dir`` / ``-o``: Base output directory [default: ./seasonal_analysis]

**Processing Options**:

- ``--dry-run``: Show planned operations without executing
- ``--resume``: Resume interrupted seasonal analysis
- ``--skip-download``: Perform analysis without downloading data

**Quality Options**:

- ``--max-cloud-cover``: Override config cloud cover limit
- ``--min-items-per-season``: Minimum items required per season [default: 3]

**Example Configuration** (seasonal_config.yaml):

.. code-block:: yaml

   # Seasonal Analysis Configuration
   study_area:
     bbox: [-122.5, 47.5, -122.0, 48.0]
     name: "Seattle_Study_Area"
   
   collections:
     - "sentinel-2-l2a"
   
   seasons:
     spring:
       start_month: 3
       end_month: 5
       description: "Growing season start"
     summer:
       start_month: 6
       end_month: 8
       description: "Peak growing season"
     fall:
       start_month: 9
       end_month: 11
       description: "Harvest season"
     winter:
       start_month: 12
       end_month: 2
       description: "Dormant season"
   
   quality_filters:
     max_cloud_cover: 25
     min_data_coverage: 80
   
   analysis_assets:
     - "B08"  # NIR
     - "B04"  # Red
     - "B03"  # Green
     - "B02"  # Blue
   
   processing:
     provider: "pc"
     max_items_per_season: 20
     download_data: true
     create_composites: true

**Examples**:

.. code-block:: bash

   # Run seasonal analysis for 2024
   ogapi workflows seasonal-analysis \
     --config seasonal_config.yaml \
     --year 2024 \
     --output-dir ./seasonal_2024/
   
   # Dry run to preview operations
   ogapi workflows seasonal-analysis \
     --config seasonal_config.yaml \
     --dry-run
   
   # Resume interrupted analysis
   ogapi workflows seasonal-analysis \
     --config seasonal_config.yaml \
     --resume \
     --output-dir ./seasonal_2024/
   
   # Analysis only (no downloads)
   ogapi workflows seasonal-analysis \
     --config seasonal_config.yaml \
     --skip-download

**Sample Output**:

.. code-block:: text

   Seasonal Analysis Workflow:
   ===========================
   
   Configuration:
     Study Area: Seattle_Study_Area [-122.5, 47.5, -122.0, 48.0]
     Year: 2024
     Collections: sentinel-2-l2a
     Provider: Planetary Computer
   
   Season Processing:
   =================
   
   🌱 Spring 2024 (Mar-May):
     Searching... Found 45 items
     Filtering... 28 items passed quality filters (62%)
     Downloading... 28 items, 4 assets each (112 files)
     Status: ✅ Complete
   
   ☀️ Summer 2024 (Jun-Aug):
     Searching... Found 52 items  
     Filtering... 38 items passed quality filters (73%)
     Downloading... 38 items, 4 assets each (152 files)
     Status: ✅ Complete
   
   🍂 Fall 2024 (Sep-Nov):
     Searching... Found 38 items
     Filtering... 22 items passed quality filters (58%)
     Downloading... 22 items, 4 assets each (88 files)
     Status: ✅ Complete
   
   ❄️ Winter 2024 (Dec) + 2025 (Jan-Feb):
     Searching... Found 18 items
     Filtering... 8 items passed quality filters (44%)
     Downloading... 8 items, 4 assets each (32 files)
     Status: ✅ Complete
   
   Analysis Summary:
   ================
     Total Items: 96
     Total Files Downloaded: 384
     Total Size: 23.8 GB
     Processing Time: 2h 15m
   
   Output Structure:
     ./seasonal_2024/
     ├── spring/
     │   ├── search_results.json
     │   ├── filtered_results.json
     │   ├── download_summary.json
     │   └── data/
     ├── summer/
     ├── fall/
     └── winter/
   
   Next Steps:
     📊 Run temporal analysis on downloaded data
     🌿 Calculate seasonal NDVI statistics
     📈 Generate seasonal change reports

batch-processing
~~~~~~~~~~~~~~~~

Configuration-driven batch processing for multiple areas, time periods, or analysis types.

**Syntax**:

.. code-block:: bash

   ogapi workflows batch-processing [OPTIONS]

**Configuration Options**:

- ``--config`` / ``-c``: YAML batch configuration file [required]
- ``--job-name`` / ``-j``: Specific job name to run (runs all if not specified)
- ``--output-dir`` / ``-o``: Base output directory [default: ./batch_processing]

**Processing Control**:

- ``--dry-run``: Preview all batch operations
- ``--resume``: Resume interrupted batch processing
- ``--parallel`` / ``--sequential``: Processing mode [default: parallel]
- ``--max-workers``: Maximum parallel workers [default: 4]

**Example Configuration** (batch_config.yaml):

.. code-block:: yaml

   # Batch Processing Configuration
   batch_jobs:
     california_agriculture:
       description: "California agricultural monitoring"
       study_areas:
         central_valley:
           bbox: [-121.0, 36.0, -120.0, 37.0]
           name: "Central Valley"
         salinas_valley:
           bbox: [-121.8, 36.2, -120.8, 36.8]
           name: "Salinas Valley"
       
       collections: ["sentinel-2-l2a"]
       date_range: "2024-01-01/2024-12-31"
       quality_filters:
         max_cloud_cover: 20
       assets: ["B08", "B04", "B03", "B02"]
       
     pacific_northwest_forests:
       description: "Forest monitoring in Pacific Northwest"
       study_areas:
         olympic_peninsula:
           bbox: [-124.0, 47.0, -123.0, 48.0]
           name: "Olympic Peninsula"
         cascade_range:
           bbox: [-122.0, 47.0, -121.0, 48.0]
           name: "Cascade Range"
       
       collections: ["sentinel-2-l2a", "landsat-c2-l2"]
       date_range: "2024-06-01/2024-09-30"
       quality_filters:
         max_cloud_cover: 30
       assets: ["B08", "B04"]
   
   global_settings:
     provider: "pc"
     download_data: true
     create_summaries: true
     max_items_per_area: 50

**Examples**:

.. code-block:: bash

   # Run all batch jobs
   ogapi workflows batch-processing \
     --config batch_config.yaml \
     --output-dir ./batch_results/
   
   # Run specific job
   ogapi workflows batch-processing \
     --config batch_config.yaml \
     --job-name california_agriculture
   
   # Sequential processing (for resource-limited systems)
   ogapi workflows batch-processing \
     --config batch_config.yaml \
     --sequential \
     --max-workers 1
   
   # Dry run to estimate resources needed
   ogapi workflows batch-processing \
     --config batch_config.yaml \
     --dry-run

**Sample Output**:

.. code-block:: text

   Batch Processing Workflow:
   =========================
   
   Configuration: batch_config.yaml
   Jobs: 2 (california_agriculture, pacific_northwest_forests)
   Processing Mode: Parallel (4 workers)
   
   Job 1/2: california_agriculture
   ===============================
   Description: California agricultural monitoring
   
   Area 1/2: Central Valley
     Search: sentinel-2-l2a (2024-01-01 to 2024-12-31)
     Results: 89 items found, 67 passed quality filters
     Download: 67 items × 4 assets = 268 files
     Status: ✅ Complete (15m 32s)
   
   Area 2/2: Salinas Valley  
     Search: sentinel-2-l2a (2024-01-01 to 2024-12-31)
     Results: 76 items found, 58 passed quality filters
     Download: 58 items × 4 assets = 232 files
     Status: ✅ Complete (12m 45s)
   
   Job 2/2: pacific_northwest_forests
   ==================================
   Description: Forest monitoring in Pacific Northwest
   
   Area 1/2: Olympic Peninsula
     Search: sentinel-2-l2a, landsat-c2-l2 (2024-06-01 to 2024-09-30)
     Results: 45 items found, 23 passed quality filters
     Download: 23 items × 2 assets = 46 files
     Status: ✅ Complete (8m 12s)
   
   Area 2/2: Cascade Range
     Search: sentinel-2-l2a, landsat-c2-l2 (2024-06-01 to 2024-09-30)
     Results: 38 items found, 19 passed quality filters
     Download: 19 items × 2 assets = 38 files
     Status: ✅ Complete (6m 55s)
   
   Batch Summary:
   =============
     Total Jobs: 2
     Total Areas: 4
     Total Items: 167
     Total Files: 584
     Total Size: 38.2 GB
     Processing Time: 43m 24s
     Success Rate: 100%

quality-assessment
~~~~~~~~~~~~~~~~~~

Comprehensive data quality filtering and assessment with recommendations.

**Syntax**:

.. code-block:: bash

   ogapi workflows quality-assessment [OPTIONS]

**Input Options**:

- ``--input`` / ``-i``: Input search results file [required]
- ``--config`` / ``-c``: Quality assessment configuration file

**Assessment Options**:

- ``--cloud-threshold``: Cloud cover threshold for quality assessment [default: 25]
- ``--coverage-threshold``: Data coverage threshold [default: 90]
- ``--temporal-gap-days``: Maximum acceptable gap between acquisitions [default: 10]

**Output Options**:

- ``--output-dir`` / ``-o``: Output directory for assessment results [default: ./quality_assessment]
- ``--generate-report``: Create detailed HTML report
- ``--export-recommendations``: Export processing recommendations

**Example Configuration** (quality_config.yaml):

.. code-block:: yaml

   # Quality Assessment Configuration
   quality_criteria:
     cloud_cover:
       excellent: 5      # < 5% cloud cover
       good: 15          # < 15% cloud cover  
       acceptable: 30    # < 30% cloud cover
       poor: 50          # < 50% cloud cover
       
     data_coverage:
       minimum: 80       # Minimum 80% data coverage
       preferred: 95     # Preferred 95% data coverage
       
     temporal_consistency:
       max_gap_days: 10  # Maximum 10-day gaps
       min_frequency: 5  # Minimum 5-day frequency
   
   assessment_priorities:
     - "temporal_distribution"
     - "cloud_cover_distribution" 
     - "data_coverage_analysis"
     - "spatial_consistency"
     - "platform_distribution"
   
   recommendations:
     generate_filtered_datasets: true
     suggest_optimal_subset: true
     identify_data_gaps: true
     recommend_additional_searches: true

**Examples**:

.. code-block:: bash

   # Basic quality assessment
   ogapi workflows quality-assessment \
     --input search_results.json \
     --output-dir ./quality_report/
   
   # Assessment with custom thresholds
   ogapi workflows quality-assessment \
     --input search_results.json \
     --cloud-threshold 20 \
     --coverage-threshold 85 \
     --generate-report
   
   # Assessment with detailed configuration
   ogapi workflows quality-assessment \
     --input search_results.json \
     --config quality_config.yaml \
     --export-recommendations

**Sample Output**:

.. code-block:: text

   Quality Assessment Report:
   =========================
   
   Dataset: search_results.json (156 items)
   Assessment Date: 2024-06-22 18:16:00 UTC
   
   Overall Quality Rating: B+ (Good)
   
   Cloud Cover Assessment:
   ----------------------
   ⭐ Excellent (< 5%):   23 items (14.7%)
   ✅ Good (5-15%):       45 items (28.8%)
   ⚠️  Acceptable (15-30%): 52 items (33.3%)
   ❌ Poor (30-50%):      28 items (17.9%)
   🚫 Unusable (> 50%):    8 items (5.1%)
   
   Quality Distribution:
   0-5%    ████████ 23 items
   5-15%   ████████████████ 45 items  
   15-30%  ████████████████████ 52 items
   30-50%  ████████ 28 items
   50%+    ██ 8 items
   
   Temporal Analysis:
   -----------------
   Date Range: 2024-01-15 to 2024-08-28 (225 days)
   Average Frequency: 1.4 days between acquisitions
   Maximum Gap: 8 days (within acceptable limits)
   Temporal Coverage: Excellent
   
   Platform Distribution:
   ---------------------
   Sentinel-2A: 78 items (50.0%)
   Sentinel-2B: 78 items (50.0%)
   Balance: Excellent
   
   Spatial Consistency:
   -------------------
   Coverage: 100% of study area covered
   Overlap: 95% average overlap between scenes
   Edge Effects: Minimal
   
   Recommendations:
   ===============
   
   🎯 Optimal Dataset (68 items):
     Use items with < 15% cloud cover for best results
     This provides 43.6% of data with excellent/good quality
     Temporal coverage: Every 3.3 days average
   
   📊 Analysis-Ready Subset (120 items):
     Use items with < 30% cloud cover for most analyses
     This provides 76.9% of data with acceptable+ quality
     Temporal coverage: Every 1.9 days average
   
   ⚠️  Data Gaps Identified:
     February 15-22: 7-day gap (winter weather)
     April 3-12: 9-day gap (cloud persistence)
     
   💡 Optimization Suggestions:
     1. Consider Landsat data to fill February gap
     2. Expand search area slightly for April gap
     3. Current dataset excellent for seasonal analysis
     4. Consider cloud masking for 15-30% cloud scenes
   
   📁 Generated Files:
     quality_assessment/
     ├── quality_report.html
     ├── optimal_dataset.json (68 items)
     ├── analysis_ready.json (120 items)
     ├── quality_statistics.json
     └── recommendations.txt

Advanced Workflow Features
--------------------------

Custom Workflow Creation
~~~~~~~~~~~~~~~~~~~~~~~~

Create custom workflow configurations:

.. code-block:: yaml

   # custom_workflow.yaml
   workflow_name: "custom_analysis"
   description: "Custom satellite data analysis workflow"
   
   steps:
     1_search:
       command: "search items"
       parameters:
         collections: ["sentinel-2-l2a"]
         bbox: [-122.5, 47.5, -122.0, 48.0]
         datetime: "2024-01-01/2024-12-31"
         cloud_cover: 30
       output: "search_results.json"
       
     2_filter:
       command: "utils filter-clouds"
       input: "search_results.json"
       parameters:
         max_cloud_cover: 20
       output: "filtered_results.json"
       
     3_analyze:
       command: "utils analyze"
       input: "filtered_results.json"
       parameters:
         detailed: true
       output: "analysis_report.json"
       
     4_download:
       command: "download search-results"
       input: "filtered_results.json"
       parameters:
         assets: ["B08", "B04", "B03", "B02"]
         destination: "./data/"

Workflow Chaining
~~~~~~~~~~~~~~~~~

.. code-block:: bash

   # Chain multiple workflows
   ogapi workflows seasonal-analysis --config seasonal_config.yaml
   ogapi workflows quality-assessment --input ./seasonal_2024/spring/search_results.json
   ogapi workflows batch-processing --config derived_batch_config.yaml

Error Recovery and Resumption
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: bash

   # Resume interrupted workflows
   ogapi workflows seasonal-analysis \
     --config seasonal_config.yaml \
     --resume \
     --output-dir ./seasonal_2024/
   
   # Check workflow status
   ls -la ./seasonal_2024/*/status.json

Integration and Automation
---------------------------

Cron Job Integration
~~~~~~~~~~~~~~~~~~~

Workflow CLI Commands (Continued)
=================================

Automation and Integration
~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: bash

   #!/bin/bash
   # automated_monitoring.sh
   # Daily satellite data monitoring workflow
   
   DATE=$(date +%Y-%m-%d)
   LOG_FILE="./logs/monitoring_${DATE}.log"
   
   echo "Starting automated monitoring for ${DATE}" | tee -a $LOG_FILE
   
   # Run seasonal analysis
   ogapi workflows seasonal-analysis \
     --config seasonal_config.yaml \
     --year $(date +%Y) \
     --output-dir "./monitoring_${DATE}/" 2>&1 | tee -a $LOG_FILE
   
   # Check status and send alerts if needed
   if [ $? -eq 0 ]; then
       echo "✅ Monitoring completed successfully" | tee -a $LOG_FILE
   else
       echo "❌ Monitoring failed" | tee -a $LOG_FILE
       # Send alert (email, webhook, etc.)
   fi

Docker Integration
~~~~~~~~~~~~~~~~~~

**Dockerfile for workflow automation**:

.. code-block:: dockerfile

   FROM python:3.9-slim
   
   # Install system dependencies
   RUN apt-get update && apt-get install -y \
       gdal-bin \
       libgdal-dev \
       && rm -rf /var/lib/apt/lists/*
   
   # Install Python packages
   RUN pip install open-geodata-api[complete]
   
   # Copy workflow configurations
   COPY ./configs/ /app/configs/
   COPY ./workflows/ /app/workflows/
   
   WORKDIR /app
   
   # Default command
   CMD ["ogapi", "workflows", "batch-processing", "--config", "/app/configs/batch_config.yaml"]

Kubernetes Workflow Jobs
~~~~~~~~~~~~~~~~~~~~~~~~~

**workflow-job.yaml**:

.. code-block:: yaml

   apiVersion: batch/v1
   kind: Job
   metadata:
     name: satellite-data-workflow
   spec:
     template:
       spec:
         containers:
         - name: ogapi-workflow
           image: your-registry/ogapi-workflows:latest
           command: ["ogapi", "workflows", "seasonal-analysis"]
           args: ["--config", "/config/seasonal_config.yaml"]
           volumeMounts:
           - name: config-volume
             mountPath: /config
           - name: output-volume
             mountPath: /output
         volumes:
         - name: config-volume
           configMap:
             name: workflow-config
         - name: output-volume
           persistentVolumeClaim:
             claimName: workflow-output-pvc
         restartPolicy: OnFailure

Monitoring and Alerting
-----------------------

Workflow Status Monitoring
~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: bash

   # Monitor workflow progress
   ogapi workflows status ./seasonal_2024/
   
   # Generate workflow report
   ogapi workflows report \
     --input-dir ./seasonal_2024/ \
     --output workflow_report.html \
     --format html

Health Checks
~~~~~~~~~~~~~

.. code-block:: bash

   #!/bin/bash
   # workflow_health_check.sh
   
   # Check API connectivity
   ogapi collections list --provider pc > /dev/null
   PC_STATUS=$?
   
   ogapi collections list --provider es > /dev/null
   ES_STATUS=$?
   
   # Check disk space
   DISK_USAGE=$(df -h /data | awk 'NR==2 {print $5}' | sed 's/%//')
   
   # Report status
   if [ $PC_STATUS -eq 0 ] && [ $ES_STATUS -eq 0 ] && [ $DISK_USAGE -lt 80 ]; then
       echo "✅ All systems operational"
       exit 0
   else
       echo "❌ System issues detected"
       echo "PC Status: $PC_STATUS, ES Status: $ES_STATUS, Disk Usage: ${DISK_USAGE}%"
       exit 1
   fi

Error Handling and Recovery
---------------------------

Workflow Recovery
~~~~~~~~~~~~~~~~~

.. code-block:: bash

   # Resume failed workflows
   ogapi workflows seasonal-analysis \
     --config seasonal_config.yaml \
     --resume \
     --output-dir ./seasonal_2024/
   
   # Retry specific failed components
   ogapi workflows batch-processing \
     --config batch_config.yaml \
     --job-name failed_job_name \
     --resume

Data Validation
~~~~~~~~~~~~~~~

.. code-block:: bash

   # Validate workflow outputs
   ogapi workflows validate \
     --workflow-dir ./seasonal_2024/ \
     --config seasonal_config.yaml \
     --check-completeness \
     --check-quality

Cleanup and Maintenance
~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: bash

   # Clean up temporary files
   ogapi workflows cleanup \
     --workflow-dir ./seasonal_2024/ \
     --remove-temp \
     --compress-logs
   
   # Archive completed workflows
   ogapi workflows archive \
     --source ./seasonal_2024/ \
     --destination ./archive/ \
     --compress

Performance Optimization
------------------------

Resource Management
~~~~~~~~~~~~~~~~~~~

**High-Performance Configuration**:

.. code-block:: yaml

   # performance_config.yaml
   performance:
     max_workers: 16
     memory_limit: "32G"
     disk_cache: true
     cache_size: "10G"
     
   download:
     chunk_size: 32768
     connection_pool_size: 20
     timeout: 300
     
   processing:
     lazy_loading: true
     batch_size: 100
     parallel_processing: true

**Resource-Constrained Configuration**:

.. code-block:: yaml

   # conservative_config.yaml
   performance:
     max_workers: 2
     memory_limit: "4G"
     disk_cache: false
     
   download:
     chunk_size: 4096
     connection_pool_size: 5
     timeout: 60
     
   processing:
     lazy_loading: true
     batch_size: 10
     parallel_processing: false

Benchmarking
~~~~~~~~~~~~

.. code-block:: bash

   # Benchmark workflow performance
   ogapi workflows benchmark \
     --config test_config.yaml \
     --iterations 3 \
     --output benchmark_report.json

Security and Compliance
-----------------------

Secure Configuration
~~~~~~~~~~~~~~~~~~~~

.. code-block:: yaml

   # secure_config.yaml
   security:
     encrypt_cache: true
     secure_temp_dir: "/secure/tmp"
     log_level: "WARNING"  # Reduced logging
     
   credentials:
     use_env_vars: true
     keyring_service: "ogapi_workflows"
     
   network:
     verify_ssl: true
     proxy_settings:
       http_proxy: "${HTTP_PROXY}"
       https_proxy: "${HTTPS_PROXY}"

Audit Logging
~~~~~~~~~~~~~

.. code-block:: bash

   # Enable audit logging
   export OGAPI_AUDIT_LOG="./audit/workflow_audit.log"
   export OGAPI_LOG_LEVEL="INFO"
   
   ogapi workflows seasonal-analysis \
     --config seasonal_config.yaml \
     --audit-mode

Data Governance
~~~~~~~~~~~~~~~

.. code-block:: yaml

   # governance_config.yaml
   data_governance:
     retention_policy:
       raw_data: "90 days"
       processed_data: "1 year"
       logs: "30 days"
       
     compliance:
       export_controls: true
       data_classification: "internal"
       approval_required: false
       
     metadata:
       track_lineage: true
       include_provenance: true
       tag_processing_version: true

Workflow Templates
------------------

Agricultural Monitoring
~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: yaml

   # agriculture_workflow.yaml
   workflow_name: "agricultural_monitoring"
   description: "Comprehensive agricultural monitoring workflow"
   
   study_areas:
     central_valley:
       bbox: [-121.0, 36.0, -120.0, 37.0]
       crop_type: "almonds"
       planting_date: "2024-02-15"
       harvest_date: "2024-08-30"
   
   monitoring_schedule:
     frequency: "weekly"
     priority_periods:
       - "2024-03-01/2024-05-31"  # Growing season
       - "2024-07-01/2024-08-31"  # Harvest approach
   
   analysis_products:
     - "ndvi_time_series"
     - "lai_estimation" 
     - "stress_detection"
     - "yield_prediction"

Environmental Monitoring
~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: yaml

   # environmental_workflow.yaml
   workflow_name: "environmental_monitoring"
   description: "Environmental change detection workflow"
   
   focus_areas:
     forest_health:
       collections: ["sentinel-2-l2a", "landsat-c2-l2"]
       indicators: ["ndvi", "moisture", "fire_risk"]
       
     water_quality:
       collections: ["sentinel-2-l2a"]
       indicators: ["turbidity", "chlorophyll", "temperature"]
       
     urban_expansion:
       collections: ["landsat-c2-l2"]
       indicators: ["built_up_index", "impervious_surface"]
   
   change_detection:
     baseline_period: "2020-01-01/2020-12-31"
     comparison_period: "2024-01-01/2024-12-31"
     threshold_settings:
       significant_change: 0.15
       trend_analysis: true

Disaster Response
~~~~~~~~~~~~~~~~~

.. code-block:: yaml

   # disaster_response_workflow.yaml
   workflow_name: "disaster_response"
   description: "Emergency response satellite monitoring"
   
   rapid_response:
     trigger_conditions:
       - "natural_disaster_alert"
       - "emergency_declaration"
     
     priority_collections:
       - "sentinel-1-grd"  # SAR for weather independence
       - "sentinel-2-l2a"  # Optical when clear
     
     processing_speed: "urgent"  # Skip quality filters
     max_cloud_cover: 80        # Accept poor quality in emergency
     
   damage_assessment:
     before_period: "30 days"   # 30 days before event
     after_period: "7 days"     # 7 days after event
     
     analysis_products:
       - "flood_extent"
       - "building_damage"
       - "infrastructure_impact"
       - "population_affected"

Troubleshooting Workflows
-------------------------

Common Workflow Issues
~~~~~~~~~~~~~~~~~~~~~

**Configuration Validation**:

.. code-block:: bash

   # Validate workflow configuration
   ogapi workflows validate-config \
     --config seasonal_config.yaml \
     --check-syntax \
     --check-resources

**Debugging Failed Workflows**:

.. code-block:: bash

   # Enable debug mode
   ogapi --verbose workflows seasonal-analysis \
     --config seasonal_config.yaml \
     --debug

**Resource Issues**:

.. code-block:: bash

   # Check resource usage
   ogapi workflows resource-check \
     --config seasonal_config.yaml \
     --estimate-requirements

Workflow Migration
~~~~~~~~~~~~~~~~~

.. code-block:: bash

   # Migrate workflows between versions
   ogapi workflows migrate \
     --from-version 0.1.0 \
     --to-version 0.2.0 \
     --config-dir ./configs/

Best Practices Summary
---------------------

**Configuration Management**:
- Use version control for workflow configurations
- Implement configuration validation
- Document workflow parameters and dependencies

**Resource Management**:
- Monitor resource usage during workflows
- Implement appropriate retry and timeout strategies
- Use parallel processing appropriately

**Data Management**:
- Implement data retention policies
- Use consistent naming conventions
- Track data lineage and provenance

**Error Handling**:
- Implement comprehensive error handling
- Use resume capabilities for long-running workflows
- Monitor workflow health and performance

**Security**:
- Secure credential management
- Implement audit logging
- Follow data governance requirements

The workflow commands provide powerful automation capabilities for complex satellite data processing pipelines while maintaining flexibility and reliability for production use.
