import json
import locale
from py_pdf_parser.loaders import load
from py_pdf_parser.components import ElementOrdering
from pdfminer.layout import LTTextLineHorizontal
from utilities import objects


class Parser:

    def __init__(self):
        locale.setlocale(locale.LC_ALL, 'de_DE.UTF-8')
        self.output = {
            'LTR': {},
            'RTL': {},
            'TTB': {}
        }
        self.reference = {}
        self.parsed = {}

    def parse_file(self, file_path: str) -> None:
        file = open(file_path, 'rb')
        self.parse_stream(file)

    def parse_stream(self, file: str) -> any:
        document = load(
            file,
            element_ordering=ElementOrdering.LEFT_TO_RIGHT_TOP_TO_BOTTOM
        )
        for element in document.elements:
            digits = 1
            key = '.'.join([
                str(round(element.bounding_box.x0)),
                str(round(element.bounding_box.y1))
            ])
            for line in element.original_element:
                if isinstance(line, LTTextLineHorizontal):
                    self.reference[
                        'LTR' + '.' + str(round(line.x0)) + '.' + str(round(line.y0))
                    ] = line.get_text().strip()
                    ttb_key = 'TTB' + '.' + str(round(line.y0))
                    if ttb_key not in self.reference:
                        self.reference[ttb_key] = ''

                    self.reference[ttb_key] += line.get_text().strip()

                    objects.set_property(
                        self.output['LTR'],
                        str(round(line.x0)) + '.' + str(round(line.y0)),
                        line.get_text().strip()
                    )

        document = load(
            file,
            element_ordering=ElementOrdering.RIGHT_TO_LEFT_TOP_TO_BOTTOM
        )
        for element in document.elements:
            key = '.'.join([
                str(round(element.bounding_box.y1)),
                str(round(element.bounding_box.y0)),
                str(round(element.bounding_box.x1)),
                str(round(element.bounding_box.x0))
            ])
            for line in element.original_element:
                if isinstance(line, LTTextLineHorizontal):
                    self.reference[
                        'RTL' + '.' + str(round(line.y1)) + '.' + str(round(line.x1))] = line.get_text().strip()
                    ttb_key = str(round(line.y0))
                    if ttb_key not in self.output['TTB']:
                        self.output['TTB'][ttb_key] = ''

                    self.output['TTB'][ttb_key] += line.get_text().strip()
                    objects.set_property(
                        self.output['RTL'],
                        str(round(line.y1)) + '.' + str(round(line.x1)),
                        line.get_text().strip()
                    )

    def dictionary(self) -> dict:
        return self.output

    def debug(self) -> str:
        debug = []
        for key, value in self.reference.items():
            debug.append(f'{key} = {value}')

        return '\n'.join(debug)

    def json(self) -> str:

        return json.dumps(
            self.output,
            sort_keys=True,
            indent=4,
            separators=(',', ': ')
        )
