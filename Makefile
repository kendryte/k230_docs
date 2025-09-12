# Minimal makefile for Sphinx documentation with multi-language support

# Configurable variables
SPHINXOPTS          ?=
SPHINXBUILD         ?= sphinx-build
SPHINXMULTIVERSION  ?= sphinx-multiversion
SOURCEDIR_EN        = en
SOURCEDIR_ZH        = zh
CONFDIR             = .
BUILDDIR            = _build
WEB_DOCS_BUILDER_URL ?= https://ai.b-bug.org/~zhengshanshan/web-docs-builder
WGET                = wget -q

# Template files
STATIC_FILES := \
    _static/init_mermaid.js \
    _static/mermaid.min.js \
    _static/transform.js \
    _static/topbar.css \
    _static/custom-theme.css \
    _static/auto-nums.css

TEMPLATE_FILES := \
    _templates/versionsFlex.html \
    _templates/layout.html \
    _templates/Fleft.html \
    _templates/Footer.html \
    _templates/Fright.html \
    _templates/FleftEn.html \
    _templates/FooterEn.html \
    _templates/FrightEn.html \
    _templates/content.html \
    _templates/contentEn.html \
    _templates/login.html \
    _templates/loginEn.html \
    _templates/nav.html \
    _templates/navEn.html \
    _templates/logo.html \
    _templates/lang.html

TEMPLATE_ALL := $(STATIC_FILES) $(TEMPLATE_FILES)

# Directory creation
_static _templates:
	mkdir -p $@

# Pattern rules for downloads
_static/%: | _static
	$(WGET) $(WEB_DOCS_BUILDER_URL)/$@ -O $@

_templates/%: | _templates
	$(WGET) $(WEB_DOCS_BUILDER_URL)/$@ -O $@

# Ensure all templates are downloaded
download: $(TEMPLATE_ALL)

# Build targets
help:
	@$(SPHINXBUILD) -M help "$(SOURCEDIR_EN)" "$(BUILDDIR)" $(SPHINXOPTS)

html-en: download
	SPHINX_LANGUAGE=en $(SPHINXBUILD) -b html "$(SOURCEDIR_EN)" "$(BUILDDIR)/html/en" -c "$(CONFDIR)"

html-zh: download
	SPHINX_LANGUAGE=zh_CN $(SPHINXBUILD) -b html "$(SOURCEDIR_ZH)" "$(BUILDDIR)/html/zh" -c "$(CONFDIR)"

html: html-en html-zh

mhtml-en: download
	SPHINX_LANGUAGE=en $(SPHINXMULTIVERSION) "$(SOURCEDIR_EN)" "$(BUILDDIR)/en" $(SPHINXOPTS) -c "$(CONFDIR)"

mhtml-zh: download
	SPHINX_LANGUAGE=zh_CN $(SPHINXMULTIVERSION) "$(SOURCEDIR_ZH)" "$(BUILDDIR)/zh" $(SPHINXOPTS) -c "$(CONFDIR)"

mhtml: mhtml-en mhtml-zh

.PHONY: help download html html-en html-zh mhtml mhtml-en mhtml-zh