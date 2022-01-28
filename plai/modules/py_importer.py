import sys
import importlib


class PyImporter:
    def __init__(self, path="", module=None):
        self._path = path
        self._module = module

    def __getattr__(self, attr):
        full_path = attr if self._module is None else self._path + f".{attr}"

        if full_path in sys.modules:
            return PyImporter(full_path, sys.modules[full_path])
        elif hasattr(self._module, attr):
            return getattr(self._module, attr)
        else:
            mod = importlib.import_module(full_path)
            return PyImporter(full_path, mod)

    def __repr__(self):
        cls = type(self).__name__
        if self._module:
            return f"{cls}({self._path!r}, {self._module})"
        else:
            return f"{cls}({self._path!r})"
