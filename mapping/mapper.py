import json
from utilities import objects
from mapping.mappers import StringMapper, IntegerMapper, DatetimeMapper, CurrencyMapper


class Mapper:

    mappers = {
        'string': StringMapper,
        'datetime': DatetimeMapper,
        'integer': IntegerMapper,
        'currency': CurrencyMapper
    }

    def __init__(self, configuration: dict, elements: dict):
        self.configuration = configuration
        self.elements = elements
        self.output = {}

    def start(self):

        for mapping in self.configuration:

            if 'default' in mapping:
                objects.set_property(self.output, mapping['property'], mapping['default'])

            value = objects.get_property(self.elements, mapping['location'])

            if value is not None:

                if 'pre' in mapping:
                    for pre_processing in mapping['pre']:
                        value = self.__process(value, pre_processing)

                objects.set_property(self.output, mapping['property'], self.__map_value(value, mapping))

                if 'post' in mapping:
                    for pre_processing in mapping['post']:
                        value = self.__process(value, pre_processing)

    def json(self) -> str:
        return json.dumps(
            self.output,
            sort_keys=True,
            indent=4,
            separators=(',', ': ')
        )

    def dictionary(self) -> dict:
        return self.output

    def __process(self, value: any, processing: any) -> any:
        evaluation = '"' + str(value) + '"' + processing
        evaluated = eval(evaluation)
        return evaluated

    def __map_value(self, value: any, mapping: str) -> any:
        mapping_type = 'string' if 'type' not in mapping else mapping['type']
        mapping_arguments = {} if 'arguments' not in mapping else mapping['arguments']
        try:
            return self.mappers[mapping_type](mapping_arguments).map_value(value)
        except KeyError as exception:
            return value
        except ValueError as exception:
            return value
