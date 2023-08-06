import sys
import os
from pathlib import Path
#sys.path.insert(0, str(Path().absolute()))
#sys.path.insert(0, str(Path(".").absolute().joinpath("geckordp")))
sys.path.append(os.path.abspath('..'))

extensions = [
    'myst_parser',
    'sphinx.ext.autodoc',
    'sphinx.ext.napoleon',
    #'sphinx.ext.autosummary',
]


#autodoc_default_flags = ['members']
#autosummary_generate = True
html_sidebars = {'**': [
                         'searchbox.html']}
#sys.setrecursionlimit(10000)

