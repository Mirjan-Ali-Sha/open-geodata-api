'''
docs/
├── conf.py                     # Sphinx configuration
├── index.rst                   # Main landing page
├── requirements.txt            # Documentation dependencies
├── _static/                    # Static assets
│   ├── icon.png
│   ├── custom.css
│   └── images/
└── sections/                   # Main documentation sections
    ├── getting-started/
    │   ├── index.rst
    │   ├── installation.rst
    │   ├── quickstart.rst
    │   ├── configuration.rst
    │   └── first-steps.rst
    ├── examples/
    │   ├── index.rst
    │   ├── basic-workflows.rst
    │   ├── advanced-workflows.rst
    │   ├── real-world-examples.rst
    │   ├── integration-examples.rst
    │   └── notebooks/
    │       ├── index.rst
    │       ├── sentinel2-analysis.rst
    │       ├── landsat-timeseries.rst
    │       └── multi-provider-comparison.rst
    ├── api-reference/
    │   ├── index.rst
    │   ├── core-classes.rst
    │   ├── client-classes.rst
    │   ├── utility-functions.rst
    │   └── factory-functions.rst
    ├── cli-reference/
    │   ├── index.rst
    │   ├── collections.rst
    │   ├── search.rst
    │   ├── items.rst
    │   ├── download.rst
    │   ├── utils.rst
    │   └── workflows.rst
    ├── faq/
    │   ├── index.rst
    │   ├── general.rst
    │   ├── installation.rst
    │   ├── usage.rst
    │   ├── troubleshooting.rst
    │   └── performance.rst
    └── development/
        ├── index.rst
        ├── contributing.rst
        ├── architecture.rst
        ├── testing.rst
        ├── changelog.rst
        └── license.rst
'''
# ----------------------------------------------------------------
"""
Sphinx configuration for Open Geodata API documentation
"""

import os
import sys

# Add the project root to Python path
sys.path.insert(0, os.path.abspath('..'))
# Add the source package specifically
sys.path.insert(0, os.path.abspath('../open_geodata_api'))

# Project information
project = 'Open Geodata API'
author = 'Mirjan Ali Sha'
copyright = '2025, Mirjan Ali Sha'

# Version information
try:
    import open_geodata_api
    version = open_geodata_api.__version__
    release = version
except ImportError:
    version = '0.1.0'
    release = '0.1.0'

# Sphinx extensions
extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.autosummary',
    'sphinx.ext.viewcode',
    'sphinx.ext.napoleon',
    'sphinx.ext.intersphinx',
    'sphinx.ext.extlinks',
    'sphinx.ext.autosectionlabel',
    'sphinx_rtd_theme',
    'myst_parser',  # For markdown support
    'nbsphinx',  # For Jupyter Notebook support
    'sphinx_copybutton',  # For copy button functionality
]

# Extension configuration
autodoc_default_options = {
    'members': True,
    'member-order': 'bysource',
    'special-members': '__init__',
    'undoc-members': True,
    'exclude-members': '__weakref__'
}

napoleon_google_docstring = True
napoleon_numpy_docstring = True
napoleon_include_init_with_doc = False
napoleon_include_private_with_doc = False

copybutton_prompt_text = r">>> |\.\.\. |\$ "
copybutton_prompt_is_regexp = True

nbsphinx_execute = 'never'  # Changed to 'never' for faster builds

# Auto section label for right sidebar
autosectionlabel_prefix_document = True
autosectionlabel_maxdepth = 4

# Intersphinx mapping
intersphinx_mapping = {
    'python': ('https://docs.python.org/3/', None),
    'pandas': ('https://pandas.pydata.org/pandas-docs/stable/', None),
    'numpy': ('https://numpy.org/doc/stable/', None),
    'rasterio': ('https://rasterio.readthedocs.io/en/stable/', None),
    'xarray': ('https://xarray.pydata.org/en/stable/', None),
}

# HTML theme
html_theme = 'sphinx_rtd_theme'

# Updated theme options for dual sidebar layout
html_theme_options = {
    'navigation_depth': 4,           # 4-level depth for left sidebar
    'collapse_navigation': False,    # Keep all levels expanded
    'sticky_navigation': True,       # Sticky left sidebar
    'includehidden': True,          # Include hidden toctree entries
    'titles_only': False,           # Show full TOC, not just titles
    'logo_only': False,             # Show logo with text
    'display_version': True,        # Show version
    'prev_next_buttons_location': 'bottom',
    'style_external_links': True,
    'vcs_pageview_mode': '',
    # Remove problematic options
    'canonical_url': '',
    'analytics_id': '',
    'analytics_anonymize_ip': False,
}

# HTML configuration
html_title = f"{project} v{version}"
html_short_title = project
html_logo = '_static/icon.png'
html_favicon = '_static/icon.png'
html_static_path = ['_static']
html_css_files = ['custom.css']

# Template configuration for dual sidebar
templates_path = ['_templates']

# Sidebar configuration for dual layout
html_sidebars = {
    '**': [
        'globaltoc.html',    # Main navigation (left side)
        'localtoc.html',     # Current page TOC (will be moved to right)
        'relations.html',    # Previous/Next navigation
        'sourcelink.html',   # Source code links
        'searchbox.html'     # Search functionality
    ],
}

# HTML context for enhanced functionality
html_context = {
    'display_github': True,
    'github_user': 'Mirjan-Ali-Sha',
    'github_repo': 'open-geodata-api',
    'github_version': 'main',
    'conf_py_path': '/docs/',
    'show_right_sidebar': True,  # Enable right sidebar
    'layout_type': 'dual_sidebar',  # Custom layout identifier
}

# Source file configuration
source_suffix = {
    '.rst': None,
    '.md': None,
}

master_doc = 'index'
language = 'en'

# Build configuration
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']

# External links
extlinks = {
    'issue': ('https://github.com/Mirjan-Ali-Sha/open-geodata-api/issues/%s', 'issue %s'),
    'pr': ('https://github.com/Mirjan-Ali-Sha/open-geodata-api/pull/%s', 'PR %s'),
}

# Suppress specific warnings
suppress_warnings = ['autodoc.import_object']

# Mock imports for problematic modules
autodoc_mock_imports = [
    'open_geodata_api.clients',
]

# Custom setup function
def setup(app):
    app.add_css_file('custom.css')
    # Add custom JavaScript if needed
    # app.add_js_file('custom.js')
