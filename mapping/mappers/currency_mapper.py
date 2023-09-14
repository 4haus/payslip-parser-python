import locale

from .value_mapper import ValueMapper


class CurrencyMapper(ValueMapper):

    defaults = {
        'locale': False
    }

    def map_value(self, value: any) -> str | float:
        value = value.replace('.', '').replace(',', '')
        if self.options['locale']:
            return locale.currency(float(format(int(value) / 100, '.02f')), grouping=True)
        return float(format(int(value) / 100, '.02f'))
