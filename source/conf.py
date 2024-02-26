# Configuration file for the Sphinx documentation builder.
#
# This file only contains a selection of the most common options. For a full
# list see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Path setup --------------------------------------------------------------

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.
#

import os
import sys
from datetime import date

sys.path.insert(0, os.path.abspath('../..'))


# -- Project information -----------------------------------------------------

project = 'MultiLA'
copyright = f'{date.today().year}, Markus Konrad'
author = 'Markus Konrad'


# -- General configuration ---------------------------------------------------

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = []

# Add any paths that contain templates here, relative to this directory.
templates_path = ['_templates']

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.

exclude_patterns = ['rst_epilog.rst']

# If true, '()' will be appended to :func: etc. cross-reference text.
add_function_parentheses = False

# If true, the current module name will be prepended to all description
# unit titles (such as .. function::).
add_module_names = True

# type hints
autodoc_typehints = 'description'
autodoc_typehints_format = 'short'

# The name of the Pygments (syntax highlighting) style to use.
pygments_style = 'sphinx'

# make rst_epilog a variable, so you can add other epilog parts to it
rst_epilog = ""    # read "global references" from rst_epilog.rst file
with open('rst_epilog.rst') as f:
    rst_epilog += f.read()

# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#

html_theme = "press"
html_static_path = ['static']

html_css_files = [
    'custom.css',
]

# Output file base name for HTML help builder.
htmlhelp_basename = '%sdoc' % project

# -- Options for LaTeX output ------------------------------------------------

latex_theme = "howto"
