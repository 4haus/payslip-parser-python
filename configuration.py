from enum import Enum
from yaml import load, Loader


class ConfigurationType(Enum):
    MAPPINGS = 'configuration/mappings.yaml'
    CUSTOM_MAPPINGS = ''


class Configuration:

    def __init__(self, custom_mappings=None):
        self.configuration = {}
        self.custom_mappings = '' if custom_mappings is None else custom_mappings

    def load(self, configuration_type: ConfigurationType) -> dict:
        with open(self.custom_mappings + configuration_type.value, 'r') as stream:
            self.configuration = load(stream, Loader=Loader)
        return self.configuration
