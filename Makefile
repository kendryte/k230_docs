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
BUILDDIR      = _build
WEB_DOCS_BUILDER_URL ?= https://ai.b-bug.org/~zhengshanshan/web-docs-builder

# Put it first so that "make" without argument is like "make help".
help:
	@$(SPHINXBUILD) -M help "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)

.PHONY: help Makefile

# Catch-all target: route all unknown targets to Sphinx using the new
# "make mode" option.  $(O) is meant as a shortcut for $(SPHINXOPTS).
# %: Makefile _static/init_mermaid.js _templates/versionsFlex.html _static/topbar.css _static/custom-theme.css
# 	@$(SPHINXBUILD) -M $@ "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)

# mhtml: _static/init_mermaid.js _templates/versionsFlex.html _static/topbar.css _static/custom-theme.css
# 	@$(SPHINXMULTIVERSION) "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)

html: html-en html-zh

html-en: Makefile _static/init_mermaid.js _templates/versionsFlex.html _static/topbar.css _static/custom-theme.css
	SPHINX_LANGUAGE=en $(SPHINXBUILD) -b html "$(SOURCEDIR_EN)" "$(BUILDDIR)/html/en" -c "$(CONFDIR)"

html-zh: Makefile _static/init_mermaid.js _templates/versionsFlex.html _static/topbar.css _static/custom-theme.css
	SPHINX_LANGUAGE=zh_CN $(SPHINXBUILD) -b html "$(SOURCEDIR_ZH)" "$(BUILDDIR)/html/zh" -c "$(CONFDIR)"

mhtml: mhtml_cn mhtml_en

# mhtml: _static/init_mermaid.js _templates/versionsFlex.html _static/topbar.css _static/custom-theme.css
# 	@$(SPHINXMULTIVERSION) "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)

mhtml_cn: _static/init_mermaid.js  _static/topbar.css _static/custom-theme.css  _templates/versionsFlex.html
	SPHINX_LANGUAGE=zh_CN $(SPHINXMULTIVERSION) "$(SOURCEDIR_ZH)" "$(BUILDDIR)/zh" $(SPHINXOPTS) -c "$(CONFDIR)"

# 英文
mhtml_en: _static/init_mermaid.js  _static/topbar.css _static/custom-theme.css  _templates/versionsFlex.html
	SPHINX_LANGUAGE=en $(SPHINXMULTIVERSION) "$(SOURCEDIR_EN)" "$(BUILDDIR)/en" $(SPHINXOPTS) -c "$(CONFDIR)"

_templates:
	mkdir $@

_static/init_mermaid.js: _templates
	wget $(WEB_DOCS_BUILDER_URL)/$@ -O $@

_templates/versionsFlex.html: _templates
	wget $(WEB_DOCS_BUILDER_URL)/$@ -O $@

_static/topbar.css:
	wget $(WEB_DOCS_BUILDER_URL)/$@ -O $@

_static/custom-theme.css:
	wget $(WEB_DOCS_BUILDER_URL)/$@ -O $@
