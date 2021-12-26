# WIP

import importlib
from sys import modules
import pkgutil
import os

PRELOADED_MODULES = set()

result_pkg_list = []
def reload_pkg(module_path:str, top_pkg_name=None):
    global result_pkg_list
    print(module_path)
    for i in pkgutil.iter_modules([module_path]):
        result_pkg_list.append(i)
        if i.ispkg:
            subpkg_path = os.path.join(module_path, i.name)
#             subpkg_name =
            result_pkg_list.append(subpkg_path)
            reload_pkg(subpkg_path)


def reload():
    import importlib
    from sys import modules
    for module in set(modules.values()) - PRELOADED_MODULES:
        try:
            importlib.reload(module)
        except:
            # there are some problems that are swept under the rug here
            pass
