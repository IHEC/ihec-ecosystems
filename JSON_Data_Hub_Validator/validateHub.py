from __future__ import print_function
from jsonschema import validate, exceptions, FormatChecker
from sys import argv
import json
import os
import getopt
# import sys


def main(argv):
    """Command line way to valide a data hub"""

    opts, args = getopt.getopt(argv, "", ["json=", "loose-validation", "verbose"])

    json_filename = ''
    is_loose_validation = False
    is_verbose = False

    for opt, arg in opts:
        if opt == '--json':
            json_filename = arg
        elif opt == '--loose-validation':
            is_loose_validation = True
        elif opt == '--verbose':
            is_verbose = True

    #JSON to be validated is mandatory, otherwise, display options
    if json_filename == '':
        printHelp()
        exit()

    #If loose validation, use loose JSON Schema
    if is_loose_validation:
        schema_file = os.path.dirname(os.path.realpath(__file__)) + '/data_hub_schema_loose.json'
    else:
        schema_file = os.path.dirname(os.path.realpath(__file__)) + '/data_hub_schema.json'

    with open(json_filename) as json_file:
        jsonObj = json.load(json_file)

    try:
        validateJson(jsonObj, schema_file)
        print("Data hub is valid.")

    except exceptions.ValidationError as e:
        print("--------------------------------------------------")
        print("- Validation error")
        print("--------------------------------------------------")
        if is_verbose:
            print(e)
        else:
            try:
                c = e.context.pop()
                print(c.message)
            except IndexError as ie:
                print(e.message)


def printHelp():
    print("Usage: python validateHub.py --json=doc.json [--loose-validation --verbose]")


def validateJson(jsonObj, schema_file):
    """Validate a data hub against the IHEC Data Hub Schema"""

    with open(schema_file) as jsonStr:
        json_schema = json.load(jsonStr)

    return validate(jsonObj, json_schema, format_checker=FormatChecker())


if __name__ == "__main__":
    main(argv[1:])