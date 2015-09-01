from jsonschema import validate, exceptions, FormatChecker
from sys import argv
import json

schema = {
    "$schema": "http://json-schema.org/draft-04/schema#",
    "id": "http://epigenomesportal.ca/schemas/data_hub_schema.json",
    "title": "IHEC Data Hub Schema 0.1",
    "description": "Structural validation of IHEC data hubs.",
    "type" : "object",

    "definitions": {
        "hub_description": {
            "type": "object",
            "properties": {
                "taxon_id": {"type": "integer", "description": "Such as '9606' for human"},
                "assembly": {"type": "string", "description": "hg19, hg38, mm10..."},
                "publishing_group": {"type": "string", "description": "BluePrint, ENCODE, CEEHRC..."},
                "email": {"type": "string", "format": "email", "description": "Write-to address for enquiries about the hub"}
            },
            "required": ["taxon_id", "assembly", "publishing_group", "email"]
        },

        "datasets": {
            "type": "object",
            "properties": {
                "sample_attributes": { "$ref": "#/definitions/sample_attributes" },
                "experiment_attributes": { "$ref": "#/definitions/experiment_attributes" },
                "analysis_attributes": { "$ref": "#/definitions/analysis_attributes" },
                "browser": {
                    "type": "object",
                    "properties": {
                        "signal": {"$ref": "#/definitions/track"},
                        "signal_forward": {"$ref": "#/definitions/track"},
                        "signal_reverse": {"$ref": "#/definitions/track"},
                        "peak_calls": {"$ref": "#/definitions/track"},
                        "methylation_profile":  {"$ref": "#/definitions/track"},
                        "contigs":  {"$ref": "#/definitions/track"},
                        "rpkm_forward": {"$ref": "#/definitions/track"},
                        "rpkm_reverse": {"$ref": "#/definitions/track"},
                    },
                    "additionalProperties": False,
                    "dependencies": {
                        "signal_forward": ["signal_reverse"],
                        "signal_reverse": ["signal_forward"],
                        "rpkm_forward": ["rpkm_reverse"],
                        "rpkm_reverse": ["rpkm_forward"],
                    }
                }
            },

            "required": ["sample_attributes", "experiment_attributes", "analysis_attributes", "browser"]
        },

        "sample_attributes": {
            "type" : "object",
            "properties": {
                "sample_id" : {"type": "string"},
                "sample_ontology_uri" : {"type": "string", "format": "uri"},
                "molecule" : {"type": "string", "enum": ["total RNA", "polyA RNA", "cytoplasmic RNA", "nuclear RNA", "genomic DNA", "protein", "other"]},
                "disease" : {"type": "string"},
                "disease_ontology_uri" : {"type": "string", "format": "uri"},
                "biomaterial_type" : {"type": "string", "enum":["Cell Line", "Primary Cell", "Primary Cell Culture", "Primary Tissue"]}
            },
            "anyOf": [
                { "$ref": "#/definitions/SA_cell_line" },
                { "$ref": "#/definitions/SA_primary_cell" },
                { "$ref": "#/definitions/SA_primary_cell_culture" },
                { "$ref": "#/definitions/SA_primary_tissue" }
            ],
            "required": ["sample_id", "sample_ontology_uri", "molecule", "disease", "disease_ontology_uri", "biomaterial_type"]
        },

        "SA_with_donor": {
            "type": "object",
            "properties": {
                "donor_id" : {"type": "string"},
                "donor_age" : {
                    "oneOf": [
                        {
                            "type": "number",
                            "minimum": 0,
                            "exclusiveMinimum": True,
                            "maximum": 90
                        },
                        { "type": "string", "enum": ["90+"] },
                        { "type": "string", "pattern": "^\d+-\d+$" },
                    ]
                },
                "donor_age_unit" : {"type": "string", "enum": ["year", "month", "week", "day"]},
                "donor_life_stage": {"type": "string", "enum": ["fetal", "newborn", "child", "adult", "unknown", "embryonic", "postnatal"]},
                "donor_health_status" : {"type": "string"},
                "donor_sex" : {"type": "string", "enum": ["Male", "Female", "Unknown", "Mixed"]},
                "donor_ethnicity" : {"type": "string"}
            },
            "required": ["donor_id", "donor_age", "donor_age_unit", "donor_life_stage", "donor_health_status", "donor_sex", "donor_ethnicity"]
        },

        "SA_cell_line": {
            "type": "object",
            "properties": {
                "biomaterial_type" : {"type": "string", "enum":["Cell Line"]},
                "line" : {"type": "string"},
                "lineage" : {"type": "string"},
                "differenciate_stage" : {"type": "string"},
                "medium" : {"type": "string"},
                "sex" : {"type": "string", "enum": ["Male", "Female", "Unknown", "Mixed"]}
            },
            "required": ["biomaterial_type", "line", "lineage", "differenciate_stage", "medium", "sex"]
        },

        "SA_primary_cell": {
            "type": "object",
            "properties": {
                "biomaterial_type" : {"type": "string", "enum":["Primary Cell"]},
                "cell_type" : {"type": "string"}
            },
            "required": ["biomaterial_type", "cell_type"],
            "allOf": [{ "$ref": "#/definitions/SA_with_donor" }]
        },

        "SA_primary_cell_culture": {
            "type": "object",
            "properties": {
                "biomaterial_type" : {"type": "string", "enum":["Primary Cell Culture"]},
                "cell_type" : {"type": "string"},
                "culture_conditions" : {"type": "string"}
            },
            "required": ["biomaterial_type", "cell_type", "culture_conditions"],
            "allOf": [{ "$ref": "#/definitions/SA_with_donor" }]
        },

        "SA_primary_tissue": {
            "type": "object",
            "properties": {
                "biomaterial_type" : {"type": "string", "enum":["Primary Tissue"]},
                "tissue_type" : {"type": "string"},
                "tissue_depot" : {"type": "string"}
            },
            "required": ["biomaterial_type", "tissue_type", "tissue_depot"],
            "allOf": [{ "$ref": "#/definitions/SA_with_donor" }]
        },

        "experiment_attributes": {
            "type": "object",
            "properties": {
                "experiment_type": {"type": "string", "description": "DNA Methylation, mRNA-Seq, ChIP-Seq Input..."},
                "assay_type": {"type": "string", "description": "As described in the experiment_ontology_uri term, e.g. 'DNA Methylation'..."},
                "experiment_ontology_uri": {"type": "string", "format": "uri"},
                "reference_registry_id": {"type": "string", "description": "Assigned after submitting to EpiRR"}
            },
            "required": ["experiment_type", "assay_type", "experiment_ontology_uri"]
        },

        "analysis_attributes": {
            "type": "object",
            "properties": {
                "analysis_group": {"type": "string"},
                "alignment_software": {"type": "string"},
                "alignment_software_version": {"type": "string"},
                "analysis_software": {"type": "string"},
                "analysis_software_version": {"type": "string"}
            },
            "required": ["analysis_group", "alignment_software", "alignment_software_version", "analysis_software", "analysis_software_version"]
        },

        "track": {
            "type" : "object",
            "properties" : {
                "big_data_url" : {"type" : "string", "format": "uri"},
                "description_url" : {"type": "string", "format": "uri"}
            },
            "required": ["big_data_url"]
        }
    },

    "properties": {
        "hub_description": { "$ref": "#/definitions/hub_description" },
        "datasets": { "type": "object", "additionalProperties": {"$ref": "#/definitions/datasets"} }
    },
    "required": ["hub_description", "datasets"]

}


def validateJson(jsonObj):
    """Validate a data hub against the IHEC Data Hub Schema."""
    return validate(jsonObj, schema, format_checker=FormatChecker())


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