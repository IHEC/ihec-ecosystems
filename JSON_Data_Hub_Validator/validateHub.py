from jsonschema import validate, exceptions, FormatChecker
from sys import argv
import json


def validateJson(jsonObj):
    """Validate a data hub against the IHEC Data Hub Schema"""

    with open('data_hub_schema.json') as jsonStr:
        data = json.load(jsonStr)

    return validate(jsonObj, data, format_checker=FormatChecker())


def main():
    """Command line way to valide a data hub"""
    script, jsonFilename = argv

    with open(jsonFilename) as jsonFile:
        jsonObj = json.load(jsonFile)

    try:
        validateJson(jsonObj)
        print "Data hub is valid."

    except exceptions.ValidationError as e:
        print "--------------------------------------------------"
        print "- Validation error"
        print "--------------------------------------------------"
        print e

if __name__ == "__main__":
    main()