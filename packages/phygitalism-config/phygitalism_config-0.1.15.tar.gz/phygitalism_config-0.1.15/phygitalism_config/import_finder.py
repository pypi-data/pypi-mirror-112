import importlib.abc
import importlib.machinery
import types

from . import ImportLoader
from .config import Config


class ImportFinder(importlib.abc.MetaPathFinder):
    def __init__(self, loader: ImportLoader):
        self._loader = loader

    def find_spec(self, fullname, path, target):
        if self._loader.is_provided(fullname):
            return self._gen_spec(fullname)

    def _gen_spec(self, fullname):
        return importlib.machinery.ModuleSpec(fullname, self._loader)
