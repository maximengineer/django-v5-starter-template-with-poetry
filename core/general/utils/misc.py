import yaml


def yaml_coerce(value):
    # converts value (stringified dict) to python dict
    # yaml.loa returns a python object
    if isinstance(value, str):
        return yaml.load(f"dummy: {value}", Loader=yaml.SafeLoader)["dummy"]
    return value
