# Minimal makefile for Sphinx documentation
#

# You can set these variables from the command line, and also
# from the environment for the first two.
SPHINXOPTS    ?=
SPHINXBUILD   ?= sphinx-build
SPHINXMULTIVERSION ?= sphinx-multiversion
SOURCEDIR     = .
BUILDDIR      = _build
WEB_DOCS_BUILDER_USER ?= gitlab+deploy-token-8
WEB_DOCS_BUILDER_TOKEN ?= _qsc99tPFsbcBhSbXH4S

# Put it first so that "make" without argument is like "make help".
help:
	@$(SPHINXBUILD) -M help "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)

.PHONY: help Makefile

# Catch-all target: route all unknown targets to Sphinx using the new
# "make mode" option.  $(O) is meant as a shortcut for $(SPHINXOPTS).
%: Makefile _templates/layout.html
	@$(SPHINXBUILD) -M $@ "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)

mhtml: _templates/layout.html
	@$(SPHINXMULTIVERSION) "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)

_templates/layout.html:
	git clone --depth 1 https://$(WEB_DOCS_BUILDER_USER):$(WEB_DOCS_BUILDER_TOKEN)@g.a-bug.org/huangziyi/web-docs-builder.git
	cp web-docs-builder/layout.html _templates/layout.html
	rm -rf web-docs-builder
