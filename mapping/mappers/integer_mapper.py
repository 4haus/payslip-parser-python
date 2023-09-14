from .value_mapper import ValueMapper


class IntegerMapper(ValueMapper):

    defaults = {}

    def map_value(self, value: any) -> int:
        return int(value)
