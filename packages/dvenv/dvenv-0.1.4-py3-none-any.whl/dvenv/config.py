import yaml
import os

from dvenv.exceptions import NoConfigurationFound, InvalidConfiguration


def _validate_configuration(cfg):
    return True


def load_configuration(path="dvenv.yml"):
    if not os.path.exists(path):
        raise NoConfigurationFound

    with open(path, "r") as f:
        try:
            cfg = yaml.safe_load(f.read())
        except yaml.YAMLError:
            raise InvalidConfiguration

    is_valid_config = _validate_configuration(cfg)
    if not is_valid_config:
        raise InvalidConfiguration

    return cfg
