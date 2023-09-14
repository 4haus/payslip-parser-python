from .value_mapper import ValueMapper
from datetime import datetime


class DatetimeMapper(ValueMapper):

    defaults = {
        'format': '%d%m%y'
    }

    def map_value(self, value: any) -> str:
        return datetime.strptime(value, self.options['format']).isoformat()
