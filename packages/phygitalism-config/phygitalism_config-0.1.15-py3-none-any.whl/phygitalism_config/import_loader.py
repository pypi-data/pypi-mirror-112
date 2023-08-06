import importlib.abc
import types
import os

from .config import Config


class MagicEnv:
    def __init__(self, name):
        self._name = name

    def __getattribute__(self, item):
        if item == '__name__':
            return super(MagicEnv, self).__getattribute__('__name__')
        name = super().__getattribute__('_name')
        env_var = name.split('.')[-1]
        return os.environ.get(env_var, '')


class ImportLoader(importlib.abc.Loader):
    name: str = 'env'

    def __init__(self):
        self._dummy_module = types.ModuleType(self.name)
        self._dummy_module.__path__ = []

    def is_provided(self, name: str):
        return name.startswith(self.name)

    def create_module(self, spec):
        if '.' in spec.name:
            return MagicEnv(spec.name)
        return self._dummy_module

    def exec_module(self, module):
        """Execute the given module in its own namespace
        This method is required to be present by importlib.abc.Loader,
        but since we know our module object is already fully-formed,
        this method merely no-ops.
        """
        pass
