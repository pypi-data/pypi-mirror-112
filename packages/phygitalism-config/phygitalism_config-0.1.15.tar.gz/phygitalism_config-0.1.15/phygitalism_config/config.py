import configparser
import json
import os
import typing
from distutils.util import strtobool

import toml

from phygitalism_config.exceptions import MissingException
from phygitalism_config.special_types import Realtime, Required
from phygitalism_config.type_caster import TypeCaster

is_testing = os.environ.get('ENVIRONMENT') == 'testing'


class MetaclassConfig(type):
    def __new__(cls, *args, **kwargs):
        name, bases, dct = args
        annotations = dct.get('__annotations__', {})
        defaults = {k: dct.get(k) for k in annotations.keys() if dct.get(k)}
        for base in bases:
            hook = getattr(base, '__subclasshook__', None)
            if hook:
                values = hook(name, annotations, defaults, dct.get('_load_from', ''))
                dct.update(values)
        return super().__new__(cls, *args, **kwargs)

    def __getattribute__(self, item):
        try:
            __name__ = super(MetaclassConfig, self).__getattribute__('__name__')
            _is_real_time = super(MetaclassConfig, self).__getattribute__('_is_real_time')
            _is_required = super(MetaclassConfig, self).__getattribute__('_is_required')
            __annotations__ = super(MetaclassConfig, self).__getattribute__('__annotations__')
            _load_from = super(MetaclassConfig, self).__getattribute__('_load_from')
            try:
                defaults = {
                    k: super(MetaclassConfig, self).__getattribute__(k) for k in __annotations__.keys()
                }
            except AttributeError:
                defaults = {}
            if item in __annotations__:
                if _is_real_time or isinstance(__annotations__[item], Realtime):
                    return super(MetaclassConfig, self).__getattribute__('__subclasshook__')(__name__,
                                                                                             __annotations__,
                                                                                             defaults,
                                                                                             _load_from)[item]
                if _is_required or isinstance(__annotations__[item], Required):
                    return super(MetaclassConfig, self).__getattribute__('__subclasshook__')(__name__,
                                                                                             __annotations__,
                                                                                             defaults,
                                                                                             _load_from,
                                                                                             _is_required)[item]
        except AttributeError:
            pass
        return super(MetaclassConfig, self).__getattribute__(item)

    # def __getattr__(self, item):
    #     return super(MetaclassConfig, self).__setattr__(item, None)


class Config(metaclass=MetaclassConfig):
    _load_from = ''
    _is_real_time = False
    _is_required = False
    
    @classmethod
    def __subclasshook__(cls,
                         name: str,
                         annotations: dict,
                         defaults: dict,
                         load_from: str,
                         _is_required: bool = False) -> dict:
        get_values = {}
        values = cls._load_default(annotations, defaults)
        file_values: dict = dict()
        if '.ini' in load_from:
            file_values = cls._load_from_ini(name, annotations, load_from)
        elif '.toml' in load_from:
            file_values = cls._load_from_toml(name, annotations, load_from)
        elif '.json' in load_from:
            file_values = cls._load_from_json(name, annotations, load_from)
        env_values = cls._load_from_env(name, annotations)

        get_values.update(file_values)
        get_values.update(env_values)

        for key, val in annotations.items():
            if (
                    key not in get_values
                    and not is_testing
                    and (
                        _is_required
                        or isinstance(val, Required)
                    )
            ):
                raise MissingException(name, key)

        values.update(get_values)

        return values

    @staticmethod
    def _cast_type(value_type, value):
        if isinstance(value_type, Realtime) or isinstance(value_type, Required):
            return Config._cast_type(value_type.get_type(), value)
        if type(value) == str:
            return TypeCaster[value_type](value)
        else:
            return value_type(value)

    @classmethod
    def _load_default(cls, annotations: typing.Optional[dict] = None, defaults: typing.Optional[dict] = None) -> dict:
        default = {}
        for attr_name, attr_type in annotations.items():
            if not defaults or attr_name not in defaults:
                value = TypeCaster[attr_type]()
                default[attr_name] = value
            else:
                default[attr_name] = defaults.get(attr_name)
        return default

    @classmethod
    def _load_from_env(cls, name: str, annotations: typing.Optional[dict] = None, ) -> dict:
        env = {}
        for k in annotations.keys():
            v = os.environ.get("{}_{}".format(name.upper(), k.upper()))
            if v:
                v = cls._cast_type(annotations[k], v)
                env[k] = v
        return env

    @classmethod
    def _load_from_toml(cls, name: str, annotations: typing.Optional[dict] = None, path: str = '') -> dict:
        with open(path, 'r') as toml_file:
            toml_file_data = toml.load(toml_file)
            return cls._load_from_dict(name, annotations, toml_file_data)

    @classmethod
    def _load_from_json(cls, name: str, annotations: typing.Optional[dict] = None, path: str = '') -> dict:
        with open(path, 'r') as json_file:
            json_file_data = json.load(json_file)
            return cls._load_from_dict(name, annotations, json_file_data)

    @classmethod
    def _load_from_ini(cls, name: str, annotations: typing.Optional[dict] = None, path: str = '') -> dict:
        cfg_parser = configparser.ConfigParser()
        cfg_parser.read_file(open(path, 'r'))
        return cls._load_from_dict(name, annotations, cfg_parser)

    @classmethod
    def _load_from_dict(cls, name: str, annotations: dict, config_dict: dict) -> dict:
        dict_values = {}
        if name in config_dict:
            for attribute_name, attribute_type in annotations.items():
                if attribute_name in config_dict[name]:
                    v = cls._cast_type(attribute_type, config_dict[name][attribute_name])
                    dict_values[attribute_name] = v
        for attribute_name, attribute_type in annotations.items():
            if attribute_name in config_dict:
                v = cls._cast_type(attribute_type, config_dict[attribute_name])
                dict_values[attribute_name] = v
        return dict_values

    @classmethod
    def find_all_subclasses(cls) -> list:
        subclasses = []
        for s in cls.__subclasses__():
            subclasses.append(s)
            subclasses += s.find_all_subclasses()
        return subclasses
