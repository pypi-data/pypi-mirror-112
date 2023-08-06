import sys

from typing import Generic, TypeVar, Optional
from .special_types import Realtime, Required

if sys.version_info.major == 3 and sys.version_info.minor >= 8:
    from typing import get_origin, get_args
else:
    from typing_inspect import get_origin, get_args
from distutils.util import strtobool

T = TypeVar('T')


def _get_valid_type(base_types, string_value):
    for _type in base_types:
        try:
            return _type(string_value)
        except ValueError:
            pass


class TypeCaster(Generic[T]):
    __slots__ = (
        '_type'
    )

    def __init__(self, _type: T):
        self._type = _type

    @classmethod
    def __class_getitem__(cls, item: T) -> 'TypeCaster':
        return TypeCaster(item)

    def _cast(self, _type: T, string_value: str):
        origin = get_origin(_type)
        if not origin:
            if _type == bool:
                return strtobool(string_value)
            return _type(string_value)
        args = get_args(_type)
        if origin == list or origin == tuple:
            if '[' in string_value:
                string_value = string_value.replace('[', '')
            if ']' in string_value:
                string_value = string_value.replace(']', '')
            res = []
            for value in string_value.split(','):
                res.append(_get_valid_type(args, value))
            return origin(res)
        if origin == dict:
            if '{' in string_value:
                string_value = string_value.replace('{', '')
            if '}' in string_value:
                string_value = string_value.replace('}', '')
            d = dict()
            for value in string_value.split(','):
                key, val = value.split(':')
                d[args[0](key)] = args[1](val)
            return d
        return string_value

    def _init_type(self, _type: T) -> T:
        if isinstance(_type, Realtime) or isinstance(_type, Required):
            return self._init_type(_type.get_type())
        origin = get_origin(_type)
        if not origin:
            return _type()
        args = get_args(_type)
        if origin == list or origin == tuple:
            if args:
                arg_origin = get_origin(args[0])
                if not arg_origin:
                    return origin([args[0]()])
                return origin([arg_origin()])
            return origin()
        if origin == dict:
            return origin()
        return str()

    def __call__(self, string_value: Optional[str] = None) -> T:
        if string_value:
            return self._cast(self._type, string_value)
        return self._init_type(self._type)
