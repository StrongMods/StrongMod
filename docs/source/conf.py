# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

import os
import sys


sys.path.insert(0, os.path.abspath('../../strongmod/'))
from internal import game_controller_maker
from version import version

project = 'StrongMod'
copyright = '2023, .'
author = '.'
release = version
show_authors = False
html_show_copyright = False

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = ['sphinx.ext.duration', 'rst2pdf.pdfbuilder', 'sphinx.ext.autodoc']

templates_path = ['_templates']
exclude_patterns = []

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'traditional'
html_static_path = ['_static']

html_sidebars = {'**': ['globaltoc.html', 'relations.html', 'sourcelink.html', 'searchbox.html']}


class Dummy:
    def __getattr__(self, name):
        def dummy_method(*args, **kwargs):
            return Dummy()

        return dummy_method


dummy = Dummy()
game_controller_maker.GameControllerMaker = Dummy
