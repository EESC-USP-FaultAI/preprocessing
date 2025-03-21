# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

import sys, os
import warnings
sys.path.insert(0, os.path.abspath('..'))

import numpydoc.docscrape as np_docscrape

project = 'Pre-Processing Functions'
copyright = '2024, LSEE'
author = 'LSEE'
version = '0.1'


# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.autosummary',
    'sphinx.ext.coverage',
    'sphinx.ext.mathjax',
    'sphinx.ext.intersphinx',
    'numpydoc',
    'nbsphinx',
    'sphinx_design',
    'matplotlib.sphinxext.plot_directive',
]

# Add any paths that contain templates here, relative to this directory.
templates_path = ['_templates']

# The suffix of source filenames.
source_suffix = '.rst'

# The main toctree document.
master_doc = 'index'

nbsphinx_execute = 'always'

# Else, today_fmt is used as the format for a strftime call.
today_fmt = '%B %d, %Y'

# List of documents that shouldn't be included in the build.
#unused_docs = []

# The reST default role (used for this markup: `text`) to use for all documents.
default_role = "autolink"

# List of directories, relative to source directories, that shouldn't be searched
# for source files.
exclude_dirs = []

# If true, '()' will be appended to :func: etc. cross-reference text.
add_function_parentheses = False


exclude_patterns = [  '_build', '**.ipynb_checkpoints'
]



exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']


# -----------------------------------------------------------------------------
# HTML output
# -----------------------------------------------------------------------------

html_theme = 'pydata_sphinx_theme'

html_logo = '_static/logo.svg'
html_favicon = '_static/logo.svg'


html_sidebars = {
    "index": "search-button-field",
    "**": ["search-button-field", "sidebar-nav-bs"]
}

html_theme_options = {
    "github_url": "",
    "header_links_before_dropdown": 6,
    "icon_links": [],
    "logo": {
        "text": "LSEE",
    },
    "navbar_start": ["navbar-logo"],
    "navbar_end": ["theme-switcher", "navbar-icon-links"],
    "navbar_persistent": [],
    "show_version_warning_banner": True,
    "secondary_sidebar_items": ["page-toc"],
    "show_nav_level": 2,
    "show_prev_next": False,
}

html_title = f"{project} Manual"
html_static_path = ['_static']
html_last_updated_fmt = '%b %d, %Y'
html_css_files = [
    "lsee.css",
]


# html_additional_pages = {
#     'index': 'indexcontent.html',
# }
html_additional_pages = {}
html_use_modindex = True
html_domain_indices = False
html_copy_source = False
html_file_suffix = '.html'

htmlhelp_basename = 'LSEE'


intersphinx_mapping = {
    'python': ('https://docs.python.org/3', None),
    'numpy': ('https://numpy.org/devdocs', None),
    'neps': ('https://numpy.org/neps', None),
    'matplotlib': ('https://matplotlib.org/stable', None),
    'asv': ('https://asv.readthedocs.io/en/stable/', None),
    'statsmodels': ('https://www.statsmodels.org/stable', None),
}

numpydoc_use_plots = True
np_docscrape.ClassDoc.extra_public_methods = [  # should match class.rst
    '__call__', '__mul__', '__getitem__', '__len__',
]


import math
plot_include_source = True
plot_formats = [('png', 96)]
plot_html_show_formats = False
plot_html_show_source_link = False

phi = (math.sqrt(5) + 1)/2

font_size = 13*72/96.0  # 13 px

plot_rcparams = {
    'font.size': font_size,
    'axes.titlesize': font_size,
    'axes.labelsize': font_size,
    'xtick.labelsize': font_size,
    'ytick.labelsize': font_size,
    'legend.fontsize': font_size,
    'figure.figsize': (3*phi, 3),
    'figure.subplot.bottom': 0.2,
    'figure.subplot.left': 0.2,
    'figure.subplot.right': 0.9,
    'figure.subplot.top': 0.85,
    'figure.subplot.wspace': 0.4,
    'text.usetex': False,
}




autosummary_generate = True


autodoc_default_options = {
    'inherited-members': None,
}
autodoc_typehints = 'none'


coverage_ignore_modules = r"""
    """.split()
coverage_ignore_functions = r"""
    test($|_) (some|all)true bitwise_not cumproduct pkgload
    generic\.
    """.split()
coverage_ignore_classes = r"""
    """.split()

coverage_c_path = []
coverage_c_regexes = {}
coverage_ignore_c_items = {}




