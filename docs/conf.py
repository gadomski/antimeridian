import importlib.metadata
import os

os.environ["PYDEVD_DISABLE_FILE_VALIDATION"] = "1"

project = "antimeridian"
copyright = "2023, Pete Gadomski"
author = "Pete Gadomski"
version = importlib.metadata.version("antimeridian")
release = importlib.metadata.version("antimeridian")

extensions = [
    "nbsphinx",
    "sphinx.ext.autodoc",
    "sphinx.ext.intersphinx",
    "sphinx.ext.napoleon",
    "sphinx_click",
]

templates_path = ["_templates"]
exclude_patterns = ["_build", "Thumbs.db", ".DS_Store"]

html_theme = "pydata_sphinx_theme"
html_static_path = ["_static"]
html_theme_options = {"github_url": "https://github.com/gadomski/antimeridian"}

intersphinx_mapping = {"shapely": ("https://shapely.readthedocs.io/en/stable", None)}

nbsphinx_custom_formats = {".md": "jupytext.reads"}
