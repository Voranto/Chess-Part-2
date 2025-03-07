import os
import sys
sys.path.insert(0, os.path.abspath('..'))


# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = 'Chess_Multiplayer'
copyright = '2025, Luca Siegel Moreno'
author = 'Luca Siegel Moreno'
release = '1.0'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = ['sphinx.ext.autodoc']

templates_path = ['_templates']
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']
html_baseurl = 'https://voranto.github.io/Chess-Part-2/docs/'


# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

#html_theme = 'alabaster'
html_theme = 'alabaster'
html_context = {
    'base_url': 'https://voranto.github.io/Chess-Part-2/docs/'
}
html_static_path = ['docs/_static']
