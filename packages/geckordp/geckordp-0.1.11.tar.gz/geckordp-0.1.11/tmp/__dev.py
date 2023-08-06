from geckordp.about import __version__
""" import geckordp.settings
print(f"test{geckordp.settings.GECKORDP_DEBUG_EVENTS}")


from geckordp.settings import *
print(f"test{GECKORDP_DEBUG_EVENTS}") """


#from geckordp.settings import GECKORDP_DEBUG_EVENTS
#print(f"test{GECKORDP_DEBUG_EVENTS}")

import geckordp.settings
from geckordp.settings import *

GECKORDP.DEBUG_EVENTS = 5
print(f"test{GECKORDP.DEBUG_EVENTS}")
print(f"test{geckordp.settings.GECKORDP.DEBUG_EVENTS}")
