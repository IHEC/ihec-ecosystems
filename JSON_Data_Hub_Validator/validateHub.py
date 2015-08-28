from jsonschema import validate

schema = {
    "$schema": "http://json-schema.org/draft-04/schema#",
    "title": "IHEC Data Hub Schema 0.1",
    "type" : "object",

    "definitions": {
        "track": {
            "type" : "object",
            "properties" : {
                "track_type" : {"type" : "string", "enum": ["signal", "peak_calls", "rpkm", "methylation_profile"]},
                "strand" : {"type" : "string", "enum": ["forward", "reverse", "unstranded"]},
                "format" : {"type" : "string", "enum": ["bigWig", "bigBed", "bam"]},
            },
            "required": ["strand"]
        }
    },

    "properties": {
        "browser": { "$ref": "#/definitions/track" },
    }
}

validate({"browser":{"track_type" : "signal", "strand": "forward"}}, schema)