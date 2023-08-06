from functools import wraps
from dvenv import log
from dvenv.client import Client
from dvenv.config import load_configuration
from dvenv.exceptions import NoConfigurationFound, InvalidConfiguration


def with_client(callback):
    @wraps(callback)
    def wrapper(*args, **kwargs):

        try:
            cfg = load_configuration()
        except NoConfigurationFound:
            log.die("No configuration found.")
        except InvalidConfiguration:
            log.die("Invalid configuration.")

        client = Client(cfg=cfg)
        client.initialize_channel()

        return callback(client, *args, **kwargs)

    return wrapper


def with_config(callback):
    @wraps(callback)
    def wrapper(*args, **kwargs):

        try:
            cfg = load_configuration()
        except NoConfigurationFound:
            log.die("No configuration found.")
        except InvalidConfiguration:
            log.die("Invalid configuration.")

        return callback(cfg, *args, **kwargs)

    return wrapper
