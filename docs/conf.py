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
sys.path.insert(0, os.path.abspath('../'))
sys.path.insert(0, os.path.abspath('./'))


# -- Project information -----------------------------------------------------

project = 'datablend'
copyright = '2020, Bernard Hernandez'
author = 'Bernard Hernandez'

# The short X.Y version.  |version|
#version = '0.3.2'

# The full version, including alpha/beta/rc tags |release|
release = '0.0.1'


# -----------------------------------------------------------------------------
# Extensions
# -----------------------------------------------------------------------------

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.napoleon',
    'sphinx.ext.todo',
    #'sphinx.ext.coverage',
    'sphinx.ext.doctest',
    'sphinx.ext.autosummary',
    'sphinx.ext.githubpages',
    'sphinx_gallery.gen_gallery'
]

# ------------------
# Doc test
# ------------------
#doctest_global_setup = '''

# ------------------
# Autosummary
# ------------------
autodoc_default_flags = ['members']
autosummary_generate = True

# ------------------
# Napoleon extension
# ------------------
# Configuration parameters for napoleon extension
napoleon_google_docstring = False
napoleon_use_param = False
napoleon_use_ivar = True


# ------------------
# Sphinx gallery
# ------------------
# Information about the sphinx gallery configuration
# https://sphinx-gallery.github.io/stable/configuration.html

# Import library
from sphinx_gallery.sorting import FileNameSortKey

# Configuration for sphinx_gallery
sphinx_gallery_conf = {
    # path to your example scripts
    'examples_dirs': ['../examples/widgets',
                      '../examples/blender',
                      '../examples/template',
                      '../examples/correctors'],

    # path to where to save gallery generated output
    'gallery_dirs': ['_examples/widgets',
                     '_examples/blender',
                     '_examples/template',
                     '_examples/correctors'],

    'line_numbers': True,
    'download_all_examples': False,
    'within_subsection_order': FileNameSortKey}

# ------------------
# Todo extension
# ------------------
todo_include_todos = True

# -----------------------------------------------------------------------------
# Add any paths that contain templates here, relative to this directory.
templates_path = ['_templates']

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']


# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#
html_theme = 'sphinx_rtd_theme' #'alabaster'

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ['_static']