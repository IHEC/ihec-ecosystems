from jsonschema import validate, exceptions, FormatChecker

schema = {
    "$schema": "http://json-schema.org/draft-04/schema#",
    "id": "http://epigenomesportal.ca/schemas/datahub.json",
    "title": "IHEC Data Hub Schema 0.1",
    "description": "Structural validation of IHEC data hubs.",
    "type" : "object",

    "definitions": {
        "hub_description": {
            "type": "object",
            "properties": {
                "taxon_id": {"type": "integer"},                #Such as "9606" for human
                "assembly": {"type": "string"},                 #hg19, hg38, mm10...
                "publishing_group": {"type": "string"},         #BluePrint, ENCODE, CEEHRC...
                "email": {"type": "string", "format": "email"}  #Write-to address for enquiries about the hub
            },
            "required": ["taxon_id", "assembly", "analysis_group", "email"]
        },

        "sample_attributes": {
            "type" : "object",
            "properties": {
                "sample_id" : {"type": "string"},
                "sample_ontology_uri" : {"type": "string", "format": "uri"},
                "molecule" : {"type": "string"},
                "disease" : {"type": "string"},
                "disease_ontology_uri" : {"type": "string", "format": "uri"},
                "biomaterial_type" : {"type": "string", "enum":["Cell Line", "Primary Cell", "Primary Cell Culture", "Primary Tissue"]},
            },
            "anyOf": [
                { "$ref": "#/definitions/SA_cell_line" },
                { "$ref": "#/definitions/SA_primary_cell" },
                { "$ref": "#/definitions/SA_primary_cell_culture" },
                { "$ref": "#/definitions/SA_primary_tissue" },
            ],
            "required": ["sample_id", "sample_ontology_uri", "molecule", "disease", "disease_ontology_uri", "biomaterial_type"]
        },

        "SA_with_donor": {
            "type": "object",
            "properties": {
                "donor_id" : {"type": "string"},
                "donor_age" : {"type": "number", "minimum": 0, "exclusiveMinimum": True},
                "donor_age_unit" : {"type": "string", "enum": ["year", "month", "week", "day", "hour", "minute", "second"]},
                "donor_health_status" : {"type": "string"},
                "donor_sex" : {"type": "string", "enum": ["Male", "Female", "Unknown"]},
                "donor_ethnicity" : {"type": "string"},
            },
            "required": ["donor_id", "donor_age", "donor_age_unit", "donor_health_status", "donor_sex", "donor_ethnicity"],
        },

        "SA_cell_line": {
            "type": "object",
            "properties": {
                "biomaterial_type" : {"type": "string", "enum":["Cell Line"]},
                "line" : {"type": "string"},
                "lineage" : {"type": "string"},
                "differenciate_stage" : {"type": "string"},
                "medium" : {"type": "string"},
                "sex" : {"type": "string", "enum": ["Male", "Female", "Unknown"]},
            },
            "required": ["biomaterial_type", "line", "lineage", "differenciate_stage", "medium", "sex"],
        },

        "SA_primary_cell": {
            "type": "object",
            "properties": {
                "biomaterial_type" : {"type": "string", "enum":["Primary Cell"]},
                "cell_type" : {"type": "string"},
            },
            "required": ["biomaterial_type", "cell_type"],
            "allOf": [{ "$ref": "#/definitions/SA_with_donor" }],
        },

        "SA_primary_cell_culture": {
            "type": "object",
            "properties": {
                "biomaterial_type" : {"type": "string", "enum":["Primary Cell Culture"]},
                "cell_type" : {"type": "string"},
                "culture_conditions" : {"type": "string"},
            },
            "required": ["biomaterial_type", "cell_type", "culture_conditions"],
            "allOf": [{ "$ref": "#/definitions/SA_with_donor" }],
        },

        "SA_primary_tissue": {
            "type": "object",
            "properties": {
                "biomaterial_type" : {"type": "string", "enum":["Primary Tissue"]},
                "tissue_type" : {"type": "string"},
                "tissue_depot" : {"type": "string"},
            },
            "required": ["biomaterial_type", "tissue_type", "tissue_depot"],
            "allOf": [{ "$ref": "#/definitions/SA_with_donor" }],
        },


        "experiment_attributes": {
            "type": "object",
            "properties": {
                "experiment_type": {"type": "string"},      #DNA Methylation, mRNA-Seq, ChIP-Seq Input...
                "assay_type": {"type": "string"},           #As described in the experiment_ontology_uri term, e.g. "DNA Methylation"...
                "experiment_ontology_uri": {"type": "string", "format": "uri"},
                "reference_registry_id": {"type": "string"},    #Assigned after submitting to EpiRR
            },
            "required": ["experiment_type", "assay_type", "experiment_ontology_uri"],
        },


        "analysis_attributes": {
            "type": "object",
            "properties": {
                "analysis_group": {"type": "string"},
                "alignment_software": {"type": "string"},
                "alignment_software_version": {"type": "string"},
                "analysis_software": {"type": "string", "format": "uri"},
                "analysis_software_version": {"type": "string"},
            },
        },


        "track": {
            "type" : "object",
            "properties" : {
                "big_data_url" : {"type" : "string", "format": "uri"},
                "track_type" : {"type" : "string", "enum": ["signal", "peak_calls", "methylation_profile", "contigs", "rpkm"]},
                "strand" : {"type" : "string", "enum": ["forward", "reverse", "unstranded"]},
                "format" : {"type" : "string", "enum": ["bigWig", "bigBed", "bam"]},
            },
            "required": ["big_data_url", "track_type", "strand", "format"]
        },
    },

    "properties": {
        "hub_description": { "$ref": "#/definitions/hub_description" },
        "sample_attributes": { "$ref": "#/definitions/sample_attributes" },
        "experiment_attributes": { "$ref": "#/definitions/experiment_attributes" },
        "analysis_attributes": { "$ref": "#/definitions/experiment_attributes" },
        "browser": {
            "type": "object",
            "additionalProperties": { "$ref": "#/definitions/track" }
        },
    },

    "required": ["hub_description", "sample_attributes", "experiment_attributes", "browser"]
}


try:
    validate({
        "sample_attributes": {
            "biomaterial_type": "Cell Line",
            "line": "unknown",
            "sample_id": "123",

            "sample_ontology_uri": "uri2://123",
            "molecule": "gDNA",
            "disease": "Healthy",
            "disease_ontology_uri": "http://a.com",
            "line": "unknown",
            "lineage": "unknown",
            "differenciate_stage": "unknown",
            "medium": "unknown",
            "sex": "Male",

        },
        "experiment_attributes": {
            "experiment_type": "DNA Methylation",
            "assay_type": "WGB-Seq",
            "experiment_ontology_uri": "http://a.com",
        },
        "browser": {
            "my_dataset_1": {
                "track_type" : "signal",
                "strand": "forward",
                "big_data_url": "http://myurl",
                "format": "bigBed"
            },
            "my_dataset_2": {
                "track_type" : "signal",
                "strand": "reverse",
                "big_data_url": "http://myurl",
                "format": "bigBed"
            }
        },

        "hub_description": {
            "taxon_id": 9606,
            "assembly": "hg19",
            "analysis_group": "McGill",
            "email": "info@epigenomesportal.ca"
        }
    }, schema, format_checker=FormatChecker())
except exceptions.ValidationError as e:
    print "Error in " + "/".join(e.path) + ": " + e.message
