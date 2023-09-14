from mapping.mapper import Mapper
from parsing.parser import Parser


class Result:

    parser = None
    mapper = None

    def __init__(self, parser: Parser, mapper: Mapper):
        self.parser = parser
        self.mapper = mapper

    def json(self) -> str:
        return self.mapper.json()
