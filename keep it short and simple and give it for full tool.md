<img src="https://r2cdn.perplexity.ai/pplx-full-logo-primary-dark%402x.png" class="logo" width="120"/>

# keep it short and simple and give it for full tool...

Based on the search results, here's a short and simple summary for the complete Open Geodata API tool:

## Open Geodata API - Complete Tool Summary

**🛰️ Unified Python Client for Satellite Data Access**

### **What It Does**

✅ **One Interface** - Access Microsoft Planetary Computer \& AWS EarthSearch APIs
✅ **Smart URLs** - Automatic signing, validation, and expiration handling
✅ **Your Choice** - Use any raster package (rioxarray, rasterio, GDAL)
✅ **Complete Workflow** - Search → Filter → Download → Analyze

### **Key Capabilities**

✅ **Python API** - Programmatic access with full flexibility
✅ **Command Line** - `ogapi` CLI for all operations with help
✅ **Smart Downloads** - Progress tracking, resume, batch processing
✅ **Data Filtering** - Cloud cover, temporal, quality-based filtering
✅ **URL Management** - Export, validate, and refresh URLs automatically

### **Installation \& Usage**

```bash
# Install
pip install open-geodata-api

# Python usage
import open_geodata_api as ogapi
pc = ogapi.planetary_computer(auto_sign=True)
results = pc.search(collections=["sentinel-2-l2a"], bbox=bbox)
urls = results.get_all_items()[^0].get_all_asset_urls()

# CLI usage
ogapi search items -c sentinel-2-l2a -b "bbox" -o results.json
ogapi download search-results results.json -a "B04,B03,B02"
```


### **Philosophy**

🎯 **Maximum Flexibility** - We provide URLs, you choose how to read data
🔓 **Zero Lock-in** - Works with any raster reading package
🚀 **Production Ready** - Robust error handling, comprehensive testing

**Perfect for:** Researchers, data scientists, and developers working with satellite imagery and geospatial analysis.

<div style="text-align: center">⁂</div>

