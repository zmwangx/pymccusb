#!/usr/bin/env python3

import inspect
import os
import sys

import sphinx_rtd_theme

# Skip loading libmccusb in the mccusb module
os.environ['SPHINX_BUILD'] = '1'

HERE = os.path.dirname(os.path.realpath(__file__))
PROJECT_ROOT = os.path.dirname(HERE)
sys.path.insert(0, PROJECT_ROOT)

project = 'pymccusb'
copyright = '2017, Zhiming Wang'
author = 'Zhiming Wang'
version = release = '0.1dev'

source_suffix = '.rst'
master_doc = 'index'
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']
pygments_style = 'sphinx'

extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.viewcode',
    'sphinx.ext.githubpages',
]

# sphinx_rtd_theme
html_theme = 'sphinx_rtd_theme'
html_theme_path = [sphinx_rtd_theme.get_html_theme_path()]

# autodoc
autodoc_member_order = 'bysource'

def autodoc_skip_attributes(app, what, name, obj, skip, options):
    return skip or not (inspect.isclass(obj) or inspect.isfunction(obj) or inspect.ismethod(obj))

def setup(app):
    app.connect('autodoc-skip-member', autodoc_skip_attributes)
