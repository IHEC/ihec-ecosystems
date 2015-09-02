from jsonschema import validate, exceptions, FormatChecker
from sys import argv
import json


def validateJson(jsonObj):
    """Validate a data hub against the IHEC Data Hub Schema."""

    with open('data_hub_schema.json') as jsonFile:
        data = json.load(jsonFile)

    return validate(jsonObj, data, format_checker=FormatChecker())


def main():
    """Validates a data hub from the command line"""
    script, jsonFile = argv
    jsonStr = open(jsonFile).read()
    jsonObj = json.loads(jsonStr)
    try:
        validateJson(jsonObj)
    except exceptions.ValidationError as e:
        print "Error in " + "/".join(e.path) + ": " + e.message



if __name__ == "__main__":
    main()