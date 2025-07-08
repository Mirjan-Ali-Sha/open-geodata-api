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
sys.path.insert(0, os.path.abspath('..'))

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
    'sphinx_rtd_theme',
    'myst_parser',  # For markdown support
    'sphinx_copybutton',
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
html_theme_options = {
    'navigation_depth': 4,
    'collapse_navigation': False,
    'sticky_navigation': True,
    'includehidden': True,
    'titles_only': False,
    'logo_only': True,
    # ------ Layout options ------
    'logo': 'Open Geodata API',
    'logo_name': True,
    'sidebar_width': '20%',
    'body_max_width': '65%',
    'body_min_width': '65%',
    'page_width': 'auto',
    'fixed_sidebar': True,
}

# HTML configuration
html_title = f"{project} v{version}"
html_short_title = project
html_logo = '_static/icon.png'
html_favicon = '_static/icon.png'
html_static_path = ['_static']
html_css_files = ['custom.css']

# HTML context
html_context = {
    'display_github': True,
    'github_user': 'Mirjan-Ali-Sha',
    'github_repo': 'open-geodata-api',
    'github_version': 'main',
    'conf_py_path': '/docs/',
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
templates_path = ['_templates']

# External links
extlinks = {
    'issue': ('https://github.com/Mirjan-Ali-Sha/open-geodata-api/issues/%s', 'issue %s'),
    'pr': ('https://github.com/Mirjan-Ali-Sha/open-geodata-api/pull/%s', 'PR %s'),
}

# Custom CSS for features grid
def setup(app):
    app.add_css_file('custom.css')
