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
copyright = str(datetime.datetime.now().year) + ' 嘉楠 | ' + '京ICP备2025124317号 | 京公网安备11010802045870号'
# author = 'Canaan'
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

html_css_files = ['topbar.css', 'custom-theme.css']

html_js_files = [
    'mermaid.min.js',
    'init_mermaid.js',
    'transform.js'
]
def setup(app):
    # 获取当前构建版本（分支/标签）
    current_version = getattr(app.config, "smv_current_version", "dev")  # 默认main分支
    # 打印当前版本
    print(f"当前构建版本: {current_version}")
    if current_version == "dev":
        html_css_files.append('auto-nums.css')

html_theme_options = {
    'collapse_navigation': True,
    "repository_url": "https://github.com/kendryte/k230_docs",
    'navigation_depth': 7,
    "primary_sidebar_end": ["versionsFlex.html"],
    "use_repository_button": True,
    "footer_start": ["Fleft.html"],
	"footer_center": ["Footer.html"],
    "navbar_start" : ['logo.html'],
    "navbar_center" : ['nav.html'],
    "navbar_end" : ['login.html', 'lang.html'],
	"footer_end" : ["Fright.html"],
    "article_footer_items": ["content.html"]
}
if language == 'en':
    html_theme_options["footer_start"] = ["FleftEn.html"]
    html_theme_options["footer_center"] = ["FooterEn.html"]
    html_theme_options["footer_end"] = ["FrightEn.html"]
    html_theme_options["article_footer_items"] = ["contentEn.html"]
    html_theme_options["navbar_center"] = ["navEn.html"]
    html_theme_options["navbar_end"] =  ['lang.html']
    copyright = str(datetime.datetime.now().year) + ' Canaan | ' + 'Beijing ICP No. 2025124317 | Beijing Public Security Network No. 11010802045870'
