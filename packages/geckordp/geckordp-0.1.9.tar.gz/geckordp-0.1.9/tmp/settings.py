import sys
import types
GECKORDP_DEBUG_EVENTS = 0
GECKORDP_DEBUG_RESPONSE = 0
GECKORDP_CREATE_LOG_FILE = ""



""" def module_property(func):
    module = sys.modules[func.__module__]

    def base_getattr(name):
        raise AttributeError(
            f"module '{module.__name__}' has no attribute '{name}'")

    old_getattr = getattr(module, '__getattr__', base_getattr)

    def new_getattr(name):
        if f'_{name}' == func.__name__:
            return func()
        else:
            return old_getattr(name)

    module.__getattr__ = new_getattr
    return func


@module_property
def GECKORDP_DEBUG_EVENTS():
    return 0 """


""" def __getattr__(name):
    if name == "GECKORDP_DEBUG_EVENTS":
        return 0
    raise AttributeError(f"module '{__name__}' has no attribute '{name}'") """


#globals()["GECKORDP_DEBUG_EVENTS"] = 0
