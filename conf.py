# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

import sys, os
import datetime

sys.path.append(os.path.abspath('exts'))

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = 'K230'
copyright = f'{datetime.datetime.now().year} Canaan Inc'
author = 'Canaan'
smv_default_version = 'dev'
# release = '0.1'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    'sphinx_copybutton',
    'myst_parser',
    'sphinx_multiversion',
    'sphinxcontrib.mermaid'
]
html_js_files = [
    'mermaid.min.js',
    'init_mermaid.js',
]
source_suffix = {
   '.rst': 'restructuredtext',  
    '.md': 'markdown',
}

templates_path = ['_templates']
exclude_patterns = ['venv', 'exts', 'en', 'zh/template']
# html_sidebars = { '**': ['globaltoc.html', 'relations.html', 'sourcelink.html', 'searchbox.html'] }

language = os.getenv('SPHINX_LANGUAGE', 'en')

# Set the title based on the language
html_title = 'K230 Linux+RT-Smart SDK'
# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

myst_heading_anchors = 6
suppress_warnings = ["myst.header"]

html_copy_source = True
html_show_sourcelink = False

html_favicon = 'favicon.ico'

# html_show_sphinx = False
html_theme = "sphinx_book_theme"
# html_theme = 'alabaster'
html_static_path = ['_static']

default_dark_mode = True

locale_dirs = ['locale']

html_css_files = ['topbar.css', 'custom-theme.css', 'auto-num.css']

html_theme_options = {
    'collapse_navigation': True,
    "repository_url": "https://github.com/kendryte/k230_docs",
    'navigation_depth': 7,
    "primary_sidebar_end": ["versionsFlex.html"],
    "use_repository_button": True,
    "footer_start": ["Fleft.html"],
	"footer_center": ["Footer.html"],
	"footer_end" : ["Fright.html"]
}
