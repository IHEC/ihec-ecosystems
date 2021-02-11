### General
The validator tests if a given Experiment or Sample XML validates against SRA XML Schema Definitions and IHEC Schema specifications.

The validation is broken down in 3 Steps:
1. SRA XML XSD validation
2. Prevalidation
3. JSON schema validation

If SRA validation fails, Prevalidation and JSON schema validation will not run.
If Prevalidation fails, JSON schema validation will not run.


### Tested with:

    $ python
	Python 3.6.8 |Anaconda, Inc.| (default, Dec 30 2018, 01:22:34)
	Python 3.8.2 | packaged by conda-forge | (default, Apr 24 2020, 07:56:27) 

Note that python 2 is no longer supported.

### Installation
The easiest way is to use Conda. Installation guides for Conda on various systems can be found here:
https://docs.conda.io/projects/conda/en/latest/user-guide/install

	conda create --name ihec python=3.8 lxml jsonschema
	conda activate ihec
	git clone https://github.com/IHEC/ihec-ecosystems
	cd ihec-ecosystem # IMPORTANT: Currently you have to run the validator from this directory

### SRA Schema Definition
It is simple to test any XML file against SRA once the conda environment is installed.

	xmllint versioned.xml --schema schemas/xml/SRA.sample.xsd >/dev/null
	versioned.xml validates

### Usage

Note that there are no space in arguments like `-out:./version_metadata/examples/samples.versioned.xml`.

	python -m version_metadata -jsonlog:log.json -overwrite-outfile -out:versioned.xml -sample sample.xml
	python -m version_metadata -jsonlog:log.json -overwrite-outfile -out:versioned.xml -experiment experiment.xml

Options explained:

	-out:<filename> All validated objects from the input file will added here. An additional attribute showing the highest IHEC version that the object validates against is added (Remember no space). 
	<SAMPLE_ATTRIBUTE><TAG>VALIDATED_AGAINST_METADATA_SPEC</TAG><VALUE>1.0/SAMPLE</VALUE></SAMPLE_ATTRIBUTE>
	-overwrite-outfile If the file  specified above already exists, overwrite it
	-sample | -experiment: Which JSON schema and SRA XSD's to apply.	
	-jsonlog:<filename> Optional, redirects the JSON output to file (Remember no space)

### Successful run

	python -m version_metadata  -overwrite-outfile -out:versioned.xml -sample version_metadata/examples/sample-Primary_Cell-pass_all.xml
	
There is a lot of output, the part to pay attention to is at the end (json is not redirected with the -jsonlog option):

	__checking_against_schema: 2.0 schemas/json/2.0/sample.json
	sample-Primary_Cell-pass_all.xml:prevalidates
	#__prevalidation_passed__ sample-Primary_Cell-pass_all.xml 2.0
	#__validates__ sample-Primary_Cell-pass_all.xml 2.0
	# is valid ihec spec:True version:2.0 [sample-Primary_Cell-pass_all.xml]
	written:versioned.xml
	validated: 1
	failed: 0
	# xml validates [against:schemas/xml/SRA.sample.xsd]... True [versioned.xml]
	ok
	{
	    "version_metadata/examples/sample-Primary_Cell-pass_all.xml": [
		{
		    "sample-Primary_Cell-pass_all.xml": {
			"errors": [],
			"ok": true,
			"version": "2.0"
		    }
		}
	    ]
	}

In versioned.xml, a new attribute has been added at the end of the attributes (no new line is added):

	<SAMPLE_ATTRIBUTE><TAG>TREATMENT</TAG><VALUE>NA</VALUE></SAMPLE_ATTRIBUTE><SAMPLE_ATTRIBUTE><TAG>VALIDATED_AGAINST_METADATA_SPEC</TAG><VALUE>2.0/SAMPLE</VALUE></SAMPLE_ATTRIBUTE>

Aside from indentations, that should be the only change (ignore whitespace:

	diff --ignore-all-space versioned.xml version_metadata/examples/sample-Primary_Cell-pass_all.xml
	33c33
	<       <SAMPLE_ATTRIBUTE><TAG>TREATMENT</TAG><VALUE>NA</VALUE></SAMPLE_ATTRIBUTE><SAMPLE_ATTRIBUTE><TAG>VALIDATED_AGAINST_METADATA_SPEC</TAG><VALUE>2.0/SAMPLE</VALUE></SAMPLE_ATTRIBUTE>
	---
	>       <SAMPLE_ATTRIBUTE><TAG>TREATMENT</TAG><VALUE>NA</VALUE></SAMPLE_ATTRIBUTE>
	36,37d35
	< 
	< 

	 
### Unsuccessful run
Several test files showing various error messages are available in `version_metadata/examples/`.

	python -m version_metadata  -overwrite-outfile -out:versioned.xml -sample version_metadata/examples/sample-Primary_Cell-BIOMATERIAL_TYPE_only.xml
	
Again, the important information is at the end:

	__checking_against_schema: 2.0 schemas/json/2.0/sample.json
	sample-Primary_Cell-BIOMATERIAL_TYPE_only.xml: missing attributes for biomaterial_type: Primary Cell , ['cell_type', 'markers', 'origin_sample', 'origin_sample_ontology_curie', 'passage_if_expanded']
	#__prevalidation_failed__ sample-Primary_Cell-BIOMATERIAL_TYPE_only.xml 2.0 __validation_skipped__
	__checking_against_schema: 1.0 schemas/json/1.0/sample.json
	sample-Primary_Cell-BIOMATERIAL_TYPE_only.xml: missing attributes for biomaterial_type: Primary Cell , ['cell_type', 'markers', 'origin_sample', 'origin_sample_ontology_uri', 'passage_if_expanded']
	#__prevalidation_failed__ sample-Primary_Cell-BIOMATERIAL_TYPE_only.xml 1.0 __validation_skipped__
	# is valid ihec spec:False version:__invalid__ [None]
	written:versioned.xml
	validated: 0
	failed: 1
	..no valid objects found
	{
	    "version_metadata/examples/sample-Primary_Cell-BIOMATERIAL_TYPE_only.xml": [
		{
		    "sample-Primary_Cell-BIOMATERIAL_TYPE_only.xml": {
			"error_type": "__prevalidation__",
			"errors": [
			    "missing : cell_type",
			    "missing : markers",
			    "missing : origin_sample",
			    "missing : origin_sample_ontology_curie",
			    "missing : passage_if_expanded"
			],
			"ok": false,
			"version": "2.0"
		    }
		},
		{
		    "sample-Primary_Cell-BIOMATERIAL_TYPE_only.xml": {
			"error_type": "__prevalidation__",
			"errors": [
			    "missing : cell_type",
			    "missing : markers",
			    "missing : origin_sample",
			    "missing : origin_sample_ontology_uri",
			    "missing : passage_if_expanded"
			],
			"ok": false,
			"version": "1.0"
		    }
		}
	    ]
	}
