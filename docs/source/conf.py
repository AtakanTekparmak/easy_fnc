# Configuration file for the Sphinx documentation builder.

import os
import sys
#sys.path.insert(0, os.path.abspath('..'))

sys.path.insert(0, os.path.abspath('../..'))

import easy_fnc

# -- Project information -----------------------------------------------------

project = 'easy_fnc'
copyright = '2024, Atakan Tekparmak'
author = 'Atakan Tekparmak'

# The full version, including alpha/beta/rc tags
release = '0.2.1'

# -- General configuration ---------------------------------------------------

extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.napoleon',
    'sphinx.ext.viewcode',
]

templates_path = ['_templates']
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']

# -- Options for HTML output -------------------------------------------------

html_theme = 'sphinx_rtd_theme'
html_static_path = ['_static']