# Minimal makefile for Sphinx documentation
#

# You can set these variables from the command line, and also
# from the environment for the first two.
SPHINXOPTS    ?=
SPHINXBUILD   ?= sphinx-build
SOURCEDIR     = source
BUILDDIR      = docs

# Put it first so that "make" without argument is like "make help".
help:
	@$(SPHINXBUILD) -M help "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)

.PHONY: help copy_codebooks

html:
	touch docs/.nojekyll
	@$(SPHINXBUILD) -b $@ "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)

codebook_pdfs:
	- mkdir codebooks
	pandoc -o codebooks/codebook_raw_data.pdf source/codebook_raw_data.rst
	pandoc -o codebooks/codebook_prepared_data.pdf source/codebook_prepared_data.rst

copy_codebooks: codebooks
	cp codebooks/codebook_raw_data.pdf ../webapi/data/codebook.pdf
	cp codebooks/codebook_prepared_data.pdf ../TrackingDataScripts/

clean:
	-rm -rI docs/*
	-rm -rI docs/.*
	-rm -I codebooks/*.pdf
