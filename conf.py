
# Configuration du projet Sphinx

project = "vehicule2"
copyright = "2026, nico"
author = "nico"

# Extensions Sphinx
extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.autosummary",
]

autosummary_generate = True

# Configuration générale
templates_path = ["_templates"]

exclude_patterns = [
    "_build",
    ".venv",
    "venv",
    "build",
    "Thumbs.db",
    ".DS_Store",
]

language = "fr"

# Sortie HTML
html_theme = "alabaster"
html_static_path = ["_static"]
