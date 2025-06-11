import importlib
import sys
import types

def reload_package(package):
    package_name = package.__name__

    modules_to_reload = [
        name for name in sys.modules
        if name.startswith(package_name)
    ]

    for module_name in sorted(modules_to_reload, reverse=True):
        module = sys.modules.get(module_name)
        if isinstance(module, types.ModuleType):
            try:
                importlib.reload(module)
                print(f"Reloaded: {module_name}")
            except Exception as e:
                print(f"Failed to reload {module_name}: {e}")
