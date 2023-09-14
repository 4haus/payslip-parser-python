

class ValueMapper:

    defaults = {}

    def __init__(self, options: dict) -> None:
        self.options = self.defaults
        self.options.update(options)
