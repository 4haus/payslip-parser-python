from .value_mapper import ValueMapper


class StringMapper(ValueMapper):

    defaults = {}

    def map_value(self, value: any) -> str:
        self.options = self.defaults
        return str(value)
