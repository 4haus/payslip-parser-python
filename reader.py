import ulid
import json
import hashlib
import uuid
import locale
from py_pdf_parser.loaders import load_file
from py_pdf_parser.components import ElementOrdering
from pdfminer.layout import LTTextContainer, LTTextLineHorizontal, LTChar
from dict_deep import deep_set, deep_get

from configuration import Configuration, ConfigurationType
from mapping.mapper import Mapper

locale.setlocale(locale.LC_ALL, 'de_DE.UTF-8')
file_path = 'resources/documents/Dezember_2021_Part1.pdf'
document = load_file(
    file_path,
    element_ordering=ElementOrdering.LEFT_TO_RIGHT_TOP_TO_BOTTOM
)

output = {
    'LTR': {},
    'RTL': {}
}
reference = {
}
for element in document.elements:
    digits = 1
    key = '.'.join([
        str(round(element.bounding_box.x0)),
        str(round(element.bounding_box.y1))
    ])
    # output['ltr'][key] = element.text()
    for line in element.original_element:
        if isinstance(line, LTTextLineHorizontal):
            reference['LTR' + '.' + str(round(line.x0)) + '.' + str(round(line.y0))] = line.get_text().strip()
            deep_set(output['LTR'], str(round(line.x0)) + '.' + str(round(line.y0)), line.get_text().strip())
            # output['ltr'][str(round(line.x0)) + '__' + str(round(line.y0))] = line.get_text()

    # print(element.original_element)
    # print(f'X0: {element.bounding_box.x0}, X1: {element.bounding_box.x1}, Y0: {element.bounding_box.y0}, Y1: {element.bounding_box.y1}')
    # print(element.text())


# Preset - right to left, top to bottom
document = load_file(
    file_path,
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
            reference['RTL' + '.' + str(round(line.y1)) + '.' + str(round(line.x1))] = line.get_text().strip()
            deep_set(output['RTL'], str(round(line.y1)) + '.' + str(round(line.x1)), line.get_text().strip())
    # output['rtl'][key] = element.text()

# for element in document.elements:
#     print(f'X0: {element.bounding_box.x0}, X1: {element.bounding_box.x1}, Y0: {element.bounding_box.y0}, Y1: {element.bounding_box.y1}')
#     print(element.text())
# print([element.text() for element in document.elements])

output['uuid'] = str(uuid.uuid4())
output['ulid'] = str(ulid.ulid())
hash_base = json.dumps(
    output,
    sort_keys=True,
    indent=4,
    separators=(',', ': ')
)
output['hash'] = hashlib.sha512(hash_base.encode('utf-8')).hexdigest()


# for k, direction in output.items():
#     for key, value in dict(direction).items():
#         print(f'\n{k.upper()} - {key}:\n{value}\n----------------\n')



# print(json.dumps(
#     output,
#     sort_keys=True,
#     indent=4,
#     separators=(',', ': ')
# ))


print(deep_get(output, 'ltr.42.767'))
print('CONFIG')
configuration = Configuration()
config = configuration.load(ConfigurationType.MAPPINGS)
print('CONFIG', config['mappings'])
for mapping in config['mappings']:
    print(mapping)

mapper = Mapper(config['mappings'], output)
mapper.start()
for key, value in reference.items():
    print(f'{key} = {value}')
print(mapper.json())
