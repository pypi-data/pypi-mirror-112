import configparser
import json
import toml


def generate_toml(path: str, name: str, params: dict, override: bool = False):
    try:
        f = open(path, 'r')
        file_data = toml.load(f)
        f.close()
    except:
        file_data = {}
    if override:
        file_data = {}
    file_data[name] = params
    with open(path, "w") as f:
        toml.dump(file_data, f)


def generate_json(path: str, name: str, params: dict, override: bool = False):
    try:
        f = open(path, 'r')
        file_data = json.load(f)
        f.close()
    except:
        file_data = {}
    if override:
        file_data = {}
    file_data[name] = params
    with open(path, "w") as f:
        json.dump(file_data, f, indent=2)


def generate_ini(path: str, name: str, params: dict, override: bool = False):
    cfgp = configparser.ConfigParser()
    try:
        if not override:
            f = open(path, 'r')
            cfgp.read_file(f)
            f.close()
    except:
        pass
    cfgp[name] = params
    with open(path, 'w') as f:
        cfgp.write(f)
