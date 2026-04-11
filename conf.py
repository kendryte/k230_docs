# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

import datetime
import os
import sys

sys.path.append(os.path.abspath("exts"))

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = os.getenv("PROJECT") or "K230"
copyright = (
    str(datetime.datetime.now().year)
    + " 嘉楠 | "
    + "京ICP备2025124317号 | 京公网安备11010802045870号"
)
# author = os.getenv('AUTHOR') or 'Canaan'
# release = '0.1'
root_doc = os.getenv("ROOT_DOC") or "index"

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    "sphinx_copybutton",
    "myst_parser",
    "sphinx.ext.mathjax",
    "sphinx_multiversion",
    "sphinxcontrib.mermaid",
]
html_js_files = ["mermaid.min.js", "init_mermaid.js", "transform.js"]
source_suffix = {
    ".rst": "restructuredtext",
    ".md": "markdown",
}
html_title = "K230 RTOS Only"
templates_path = ["_templates"]
exclude_patterns = [".github/*", ".gitlab/*", "**/--*"]

# language = 'zh_CN'
language = os.getenv("SPHINX_LANGUAGE", "en")

# Set the title based on the language
html_title = "K230 Linux+RT-Smart SDK"
# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

myst_heading_anchors = 6
suppress_warnings = ["myst.header"]

html_copy_source = True
html_show_sourcelink = False

html_favicon = "favicon.ico"

# html_show_sphinx = False

html_theme = "sphinx_book_theme"
html_static_path = ["_static"]

myst_enable_extensions = [
    "dollarmath",  # 支持 $...$ 行内公式
    "amsmath",  # 支持 \begin{align} 等多行公式
]

html_css_files = ["topbar.css", "custom-theme.css", "auto-nums.css"]
locale_dirs = ["locale"]

html_theme_options = {
    "collapse_navigation": True,
    "repository_url": "https://github.com/kendryte/k230_docs",
    "navigation_depth": 7,
    "use_repository_button": True,
    "primary_sidebar_end": ["versionsFlex.html"],
    "footer_start": ["Fleft.html"],
    "footer_center": ["Footer.html"],
    "footer_end": ["Fright.html"],
    "navbar_start": ["logo.html"],
    "navbar_center": ["nav.html"],
    "navbar_end": ["login.html", "lang.html"],
    "article_footer_items": ["content.html"],
}

if language == "en":
    html_theme_options["footer_start"] = ["FleftEn.html"]
    html_theme_options["footer_center"] = ["FooterEn.html"]
    html_theme_options["footer_end"] = ["FrightEn.html"]
    html_theme_options["article_footer_items"] = ["contentEn.html"]
    html_theme_options["navbar_center"] = ["navEn.html"]
    html_theme_options["navbar_end"] = ["lang.html"]
    html_theme_options["article_footer_items"] = ["contentEn.html"]
    copyright = (
        str(datetime.datetime.now().year)
        + " Canaan | "
        + "Beijing ICP No. 2025124317 | Beijing Public Security Network No. 11010802045870"
    )

# -- Options for sphinx-multiversion (核心多版本配置) --------------------------

# 1. 构建 main 和 dev 分支
smv_branch_whitelist = r"^(main|dev)$"

# 2. 构建 v1.5 及以上版本的 Tag (排除 < 1.5)
# 逻辑：匹配 v1.6-1.9, 或者 v2 及以上的所有版本
smv_tag_whitelist = r"^v(1\.[6-9]|[2-9]|\d{2,})\.\d+.*$"

# 3. 远程分支匹配（兼容 CI 环境，匹配所有远程）
smv_remote_whitelist = r"^.*$"

# 4. 构建后是否自动切换到最新的版本（可选）
smv_latest_version = "main"
