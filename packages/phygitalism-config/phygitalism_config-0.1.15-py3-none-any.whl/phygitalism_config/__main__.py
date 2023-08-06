import argparse
import importlib
import os
import sys

from .config import Config
from .generator import generate_ini, generate_json, generate_toml

args_parser = argparse.ArgumentParser()
group = args_parser.add_argument_group('generate')
group.add_argument('package', type=str)
group.add_argument('name', type=str, )
group.add_argument('path', type=str)
group.add_argument('--rewrite', action='store_true')


def find_by_name(name: str):
    for c in Config.find_all_subclasses():
        if c.__name__ == name:
            return c


def main():
    args = args_parser.parse_args()
    sys.path.extend([os.getcwd()])
    try:
        importlib.import_module(args.package)
    except Exception as e:
        print(e)
        return

    klass = find_by_name(args.name)
    if not klass:
        print('Class not found')
        return

    path = os.path.abspath(args.path)
    if not os.path.exists(os.path.dirname(path)):
        print(f"Not found {path}")
        return

    params = {k: klass.__dict__.get(k) for k in klass.__annotations__.keys()}

    if '.ini' in args.path:
        generate_ini(args.path, args.name, params, override=args.rewrite)
    elif '.json' in args.path:
        generate_json(args.path, args.name, params, override=args.rewrite)
    elif '.toml' in args.path:
        generate_toml(args.path, args.name, params, override=args.rewrite)
    else:
        print('Not valid file name')
        return


if __name__ == "__main__":
    main()
