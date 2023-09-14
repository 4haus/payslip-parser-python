# Vierhaus - Python Payslip Parser
## Description
A simple tool to convert/transform ordinary <a href="https://apps.datev.de/ano/">DATEV</a> compliant payslips from PDF
format to JSON documents.<br>
Originally designed for <a href="https://www.vierhaus-kanzlei.de">Vierhaus Steuerberatungsgesellschaft mbH</a> and their
subsidiaries.
## Requirements
This package facilitates **libmagic-dev** and **locales** for MIME type determination of incoming streams and proper
reading of German umlauts.

`Python~=3.11` and `Pip~=23.2`

Running `apt install libmagic-dev locales ; dpkg-reconfigure` seems like a good preparation before going ahead.

## Installation
### Python

This package is originally designed to be run in python's virtual environment, however it might also be run within a
global python installation.

In order to install all the required packages within its own virtual environment, which is the recommended approach,
the procedure goes as follows:

1. `git clone https://github.com/4haus/payslip-parser-python.git`
2. `cd payslip-parser-python`
3. `python3 -m venv venv`
4. `pip install -r requirements.txt`

### Docker

Building the Docker image, which will create a standalone Docker based service:

`docker build -t 4haus/payslip_parser:latest .`

Running the Docker container as http service listening on port 8000 to serve as an interconnected microservice withing 
the local infrastructure:

`docker run -p 8000:8000 4haus/payslip_parser`

This will start a docker container listening on port "*8000*" and serving the transformation of PDF inputs to JSON
documents as http service(Perhaps the desired way within an orchestration).



Running the parser directly by invoking the docker run command:

`docker run -it -v "$(pwd)"/data:/data 4haus/payslip_parser python command.py -i input.pdf -o /data/output.json`

## Configuration

**Configure the basic mappings of a PDF input file to the json output by adjusting using the following convention to
the `configuration/mappings.yaml`:**

  ```yaml
mappings:
  -
    property: nested.dictionary.to_be_mapped_to.using_dot_notation
    # location is the position of the text element to be read out of the provided PDF document based on
    # LTR(left to right) and RTL(right to left) and their corresponding positions within the document.
    # see cli "-v" or "--verbose" to examine the accurate position of a value within the document
    location: LTR.310.716 # referring to "the left to right" order, the horizontal point "310" and the vertical distance "716" 
    # default is the default value in case that no value could be extracted through reaching into the location
    default: null
    # pre array|list is a list of methods or functions to apply to the value before setting it to the "property" path
    pre: [ '.strip()', '.replace(" ", "")']
    # post array|list is a list of methods or functions to apply to the value after setting it to the "property" path
    post: [ '.split("|")' ]
    # types are defined as follows: string, datetime, number, currency, percentage, integer
    type: integer
    # a dictionary of arguments to be passed to the corresponding mapping function
    arguments:
      # "format" for datetime to use to map the string value into a datetime object
      format: '%d%m%y'

  -
    property: employee.id
    location: LTR.42.767
    pre: [ '.split(" ")[0]', '.strip()' ]
    type: string
  ```
### Usage

**Server**

1. In order to initialize the http server there's two options available to run it.<br>
Primarily and also recommended is to run it as a Docker container by issuing the following command after completing the 
initial installation process above:<br><br>
    `docker run -p 8000:8000 4haus/payslip_parser`<br><br>
2. As a second option the service can be invoked directly via python using the embedded server:<br><br>
    `./server` or `python ./server.py`<br><br>
3. The server can then be accessed at http://localhost:8000 for example via the **curl** library by sending a binary stream "application/octet-stream" request using the "POST" request method:<br><br>
    `curl --data-binary @input.pdf http://localhost:8000`<br><br>
The server then should reply with an "application/json" response. 

**Command**

1. `./cli` While issuing the required executable permission byte might be required(`chmod +x ./cli`)
which will take at least one "`-i`", or "`--input`" argument that needs to point to an accessible "PDF" file location within the system.<br>Further the `./cli` or `python3 command.py` commands support the following additional arguments:<br><br>
`-o` or `--output` to specify a relative or absolute, accessible and writable path on the local file system to write the JSON document. e.g.<br><br>`./cli --input ./input.pdf --output /var/app/output.json`<br><br>
`-m` or `--mapping` to override the configuration/mappings.yaml file with a custom yaml file on the local file system. e.g.<br><br>
`./cli --input ./input.pdf --mapping ./custom_mapping.yaml`<br><br>
2. In addition to the previous deployment, the service may be invoked by forwarding the previously explained `./server`
concept to a Docker `docker run` command which<br>This will start a simple http server listening to "POST" requests containing binary "POST" request data streams and 
responding with a "JSON" document.<br><br>
3. In order to avoid dependencies to be installed locally the commands can be executed within to docker container by calling:<br><br>
`docker run -it -v "$(pwd)"/data:/data 4haus/payslip_parser python command.py -i input.pdf -o /data/output.json[ --mapping /data/my_mapping.yaml]`

This will return a JSON document containing the result of the parsing process directly to the console/terminal

**Debugging/Analysing**

Debugging or analysing of the PDF input is available only via command line interface. In order to receive a list of all
values and their corresponding locations issue the flag `-v` or `--verbose` to the command, e.g.

`./cli --input ./input.pdf --verbose`

### Output
Amongst the expected output after parsing and applying the given mappings configuration a examplifying output should look similar to the one beneath: 
```json
{
    "bookings": {
        "0": {
            "GB": "J",
            "SV": "L",
            "St": "L",
            "amount": 2080.0,
            "description": "Stundenlohn",
            "quantity": "104,00",
            "unit": "Std"
        },
        "1": {
            "GB": "J",
            "SV": "F",
            "St": "P",
            "amount": 104.0,
            "description": "Verpflegungs.pauschalSt",
            "type": "205"
        },
        "2": {
            "description": "Urlaubsentg. KJ / VJ KJ",
            "type": "508"
        },
        "3": {
            "description": "Url. Geld",
            "type": "508"
        },
        "4": {
            "type": "004"
        }
    },
    "date": "2021-12-27T00:00:00",
    "employee": {
        "address": {
            "locality": "CITY",
            "post_code": "POST CODE",
            "street": "STREET AND HOUSE NUMBER"
        },
        "bank_name": "BANK NAME",
        "confession": "rk",
        "date_of_birth": "1965-01-01T00:00:00",
        "full_name": "FIRST NAME LAST NAME",
        "iban": "DE6350XXXXXXXX71199100",
        "id": "00014",
        "social_security_number": "520******010",
        "tax_bracket": 1,
        "tax_id": 87400000054
    },
    "employer": "COMPANY NAME*STREET AND HOUSE NUMBER*POST CODE AND CITY",
    "file_hash": "SHA 512 FILE DIGEST OF THE SUBMITTED FILE",
    "hash": "SHA 512 DOCUMENT DIGEST AFTER PARSING",
    "income": {
        "brut": 4627.35,
        "net": 2866.91,
        "payout": 3012.92,
        "statement": {
            "brut_tax": 39389.98,
            "brut_total": 40781.08,
            "income_tax": 5676.22
        }
    },
    "ulid": "01HA7VQSKTBJ49J5KS5PQJK95N",
    "uuid": "b54ea291-be95-4788-9ae9-91ab112fb5b4"
}

```

# Todo

- Probably move the hardcoded mappers to a centralized registry and allow custom mappers to be dynamically discovered and added through configurations.
- 
