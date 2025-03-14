# Minimal makefile for Sphinx documentation
#

# You can set these variables from the command line, and also
# from the environment for the first two.
SPHINXOPTS    ?=
SPHINXBUILD   ?= sphinx-build
SPHINXMULTIVERSION ?= sphinx-multiversion
SOURCEDIR_EN  = en
SOURCEDIR_ZH  = zh
SOURCEDIR = .
CONFDIR       = .
CONFDIRRTT    = rtt-config
BUILDDIR      = _build
WEB_DOCS_BUILDER_URL ?= https://ai.b-bug.org/~zhengshanshan/web-docs-builder
TEMPLATE = _static/init_mermaid.js _static/mermaid.min.js _templates/versionsFlex.html _templates/Fleft.html _templates/Footer.html _templates/Fright.html  _templates/FleftEn.html _templates/FooterEn.html _templates/FrightEn.html _templates/content.html _templates/contentEn.html  _templates/layout.html _static/topbar.css _static/custom-theme.css

# Put it first so that "make" without argument is like "make help".
help:
	@$(SPHINXBUILD) -M help "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)

.PHONY: help Makefile

html: html-en html-zh html-zh-rtt html-en-rtt

html-en: Makefile $(TEMPLATE)
	SPHINX_LANGUAGE=en $(SPHINXBUILD) -b html "$(SOURCEDIR_EN)" "$(BUILDDIR)/html/en" -c "$(CONFDIR)"

html-zh: Makefile $(TEMPLATE)
	SPHINX_LANGUAGE=zh_CN $(SPHINXBUILD) -b html "$(SOURCEDIR_ZH)" "$(BUILDDIR)/html/zh" -c "$(CONFDIR)"

html-zh-rtt: Makefile $(TEMPLATE)
	SPHINX_LANGUAGE=zh_CN $(SPHINXBUILD) -b html "$(SOURCEDIR_ZH)" "$(BUILDDIR)/html/zh/rtt" -c "$(CONFDIRRTT)"

html-en-rtt: Makefile $(TEMPLATE)
	SPHINX_LANGUAGE=zh_CN $(SPHINXBUILD) -b html "$(SOURCEDIR_EN)" "$(BUILDDIR)/html/en/rtt" -c "$(CONFDIRRTT)"

mhtml: mhtml_cn mhtml_en mhtml_cn_rtt mhtml_en_rtt

mhtml_cn: $(TEMPLATE)
	SPHINX_LANGUAGE=zh_CN $(SPHINXMULTIVERSION) "$(SOURCEDIR_ZH)" "$(BUILDDIR)/zh" $(SPHINXOPTS) -c "$(CONFDIR)"

mhtml_cn_rtt: $(TEMPLATE)
	SPHINX_LANGUAGE=zh_CN $(SPHINXMULTIVERSION) "$(SOURCEDIR_ZH)" "$(BUILDDIR)/zh/rtt" $(SPHINXOPTS) -c "$(CONFDIRRTT)"

# 英文
mhtml_en: $(TEMPLATE)
	SPHINX_LANGUAGE=en $(SPHINXMULTIVERSION) "$(SOURCEDIR_EN)" "$(BUILDDIR)/en" $(SPHINXOPTS) -c "$(CONFDIR)"

mhtml_en_rtt: $(TEMPLATE)
	SPHINX_LANGUAGE=zh_CN $(SPHINXMULTIVERSION) "$(SOURCEDIR_EN)" "$(BUILDDIR)/en/rtt" $(SPHINXOPTS) -c "$(CONFDIRRTT)"

_templates:
	mkdir $@

_templates/versionsFlex.html: _templates
	wget $(WEB_DOCS_BUILDER_URL)/$@ -O $@

_templates/layout.html: _templates
	wget $(WEB_DOCS_BUILDER_URL)/$@ -O $@

_templates/Fleft.html: _templates
	wget $(WEB_DOCS_BUILDER_URL)/$@ -O $@

_templates/Footer.html: _templates
	wget $(WEB_DOCS_BUILDER_URL)/$@ -O $@

_templates/Fright.html: _templates
	wget $(WEB_DOCS_BUILDER_URL)/$@ -O $@

_templates/FleftEn.html: _templates
	wget $(WEB_DOCS_BUILDER_URL)/$@ -O $@

_templates/FooterEn.html: _templates
	wget $(WEB_DOCS_BUILDER_URL)/$@ -O $@

_templates/FrightEn.html: _templates
	wget $(WEB_DOCS_BUILDER_URL)/$@ -O $@

_templates/contentEn.html: _templates
	wget $(WEB_DOCS_BUILDER_URL)/$@ -O $@

_templates/content.html: _templates
	wget $(WEB_DOCS_BUILDER_URL)/$@ -O $@

_static/topbar.css:
	wget $(WEB_DOCS_BUILDER_URL)/$@ -O $@

_static/custom-theme.css:
	wget $(WEB_DOCS_BUILDER_URL)/$@ -O $@

_static/init_mermaid.js: 
	wget $(WEB_DOCS_BUILDER_URL)/$@ -O $@

_static/mermaid.min.js: 
	wget $(WEB_DOCS_BUILDER_URL)/$@ -O $@
