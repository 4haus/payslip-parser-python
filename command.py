import os
import argparse
from processing import Processor

parser = argparse.ArgumentParser(
    prog='4Haus Payslip Parser Python',
    description='A simple helper tool to parse DATEV issued payslips from PDF file format to json',
    epilog='Text at the bottom of help'
)

parser.add_argument('-v', '--verbose',
                    help="This flag will enable the outputting of the coordinated parsing result.",
                    action='store_true')
parser.add_argument('-i', '--input',
                    help='The relative or absolute path to the file to be parsed',
                    required=True)
parser.add_argument('-o', '--output',
                    help='The relative or absolute path of the outputted file to write to')
parser.add_argument('-m', '--mapping',
                    help='The relative or absolute path to a custom yaml mapping file',
                    required=False)

if __name__ == '__main__':
    args = parser.parse_args()
    if args.input is None or not os.path.exists(args.input):
        print(f'The input file "{args.input}" does either not exist, '
              f'is inaccessible to this system or hasn\'t been provided!')
        exit(0)
    try:
        custom_mapping = args.mapping
        processor = Processor(args.input, custom_mapping)
        processor.process()
        result = processor.get_result()

        if args.output:
            # @todo normalize relative input and output paths
            if args.output.startswith('.'):
                exit(1)
            output_file = open(args.output, 'w')
            output_file.write(result.mapper.json())
            output_file.close()
        else:
            print(result.mapper.json())
        if args.verbose:
            print(processor.get_parser().debug())

    except FileNotFoundError as exception:
        print(exception)

