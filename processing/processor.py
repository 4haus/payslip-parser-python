import ulid
import json
import hashlib
import uuid
from parsing.parser import Parser
from mapping.mapper import Mapper
from processing.result import Result
from configuration import Configuration, ConfigurationType


class Processor:

    result = None

    def __init__(self, file: str, mappings=None):
        configurator = Configuration(mappings)
        configuration_type = ConfigurationType.MAPPINGS if mappings is None else ConfigurationType.CUSTOM_MAPPINGS
        configuration = configurator.load(configuration_type)
        self.file = file
        self.objects = {}
        self.parser = Parser()
        self.parser.parse_file(file)
        self.objects = self.parser.dictionary()
        self.mapper = Mapper(configuration['mappings'], self.objects)

    def process(self) -> Result:
        self.parser.parse_file(self.file)
        self.mapper.start()
        self.mapper.output['uuid'] = str(uuid.uuid4())
        self.mapper.output['ulid'] = str(ulid.ulid())
        document = json.dumps(
            self.mapper.output,
            sort_keys=True,
            indent=4,
            separators=(',', ': ')
        )
        self.mapper.output['hash'] = hashlib.sha512(document.encode('utf-8')).hexdigest()
        with open(self.file, "rb") as file:
            self.mapper.output['file_hash'] = hashlib.file_digest(file, 'sha512').hexdigest()
        self.result = Result(self.parser, self.mapper)
        return self.result

    def get_result(self) -> Result:
        return self.result

    def get_parser(self) -> Parser:
        return self.result.parser
