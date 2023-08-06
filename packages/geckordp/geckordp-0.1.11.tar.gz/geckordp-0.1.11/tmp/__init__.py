import os
from geckordp.about import __version__
from geckordp.logger import *
from geckordp.settings import *
import geckordp.settings

""" config = [[k, v] for k, v in globals().items() if str(k).startswith("GECKORDP_")]
for name, value in config:
    print(name)
    setattr(geckordp.settings, name, 1)
    break

#geckordp.settings.GECKORDP_DEBUG_EVENTS = 1

print(geckordp.settings.GECKORDP_DEBUG_EVENTS) """



#geckordp.DEBUG_EVENTS = 1
#geckordp.__dict__["_Settings__XDEBUG_EVENTS"] = 2


VAR_ID = "_Settings__X"
for name, value in geckordp.__dict__.items():
    if (not name.startswith(VAR_ID)):
        continue

    func_name = name.replace(VAR_ID, "")
    env_name = name.replace(VAR_ID, "GECKORDP_")
    env_value = os.environ.get(env_name, None)
    func = getattr(Settings, func_name)
    
    if (env_value == None):
        continue
    try:
        env_value = type(value)(env_value)
    except Exception as ex:
        print(f"invalid type for environment variable '{env_name}':\n{ex}")
        continue

    func.fset(geckordp, env_value)


print(geckordp.DEBUG_EVENTS)
print(geckordp.__dict__)



#for k, v in GECKORDP_VARIABLES.items():
#    print(k)
#print(settings)
#geckordp.config.init_config()
#init_logger()
#dlog(f"name={__name__}")
#dlog(f"version={__version__}")
