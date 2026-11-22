# Sphinx configuration for the pitmap documentation.
import importlib.metadata
import os
import sys

# the package is installed (pip install -e ./src in CI, or pip install pitmap locally)

project = "pitmap"
author = "Leonid Shpaner"
copyright = "2026, Data Science Dynamics"
release = importlib.metadata.version("pitmap")
version = release

extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.napoleon",
    "sphinx.ext.mathjax",
    "sphinx.ext.viewcode",
    "sphinx.ext.intersphinx",
    "myst_parser",
]
source_suffix = {".rst": "restructuredtext", ".md": "markdown"}
templates_path = ["_templates"]
exclude_patterns = ["_build", "Thumbs.db", ".DS_Store"]

intersphinx_mapping = {
    "python": ("https://docs.python.org/3", None),
    "numpy": ("https://numpy.org/doc/stable/", None),
    "scipy": ("https://docs.scipy.org/doc/scipy/", None),
}

autodoc_member_order = "bysource"
autodoc_typehints = "description"
napoleon_numpy_docstring = True

html_theme = "sphinx_rtd_theme"
html_static_path = ["_static"]
html_logo = "_static/logo.svg"
html_favicon = "_static/favicon.svg"
html_theme_options = {
    "logo_only": True,
    "collapse_navigation": False,
    "navigation_depth": 3,
}
html_css_files = ["custom.css"]
