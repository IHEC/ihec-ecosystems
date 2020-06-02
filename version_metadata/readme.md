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
	cd ihec-ecosystem # IMPORTANT: Currently you have to run the validator from this directory
	git checkout feb2020 # To be merged

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
	
There is a lot of output, the part to pay attention to is at the end (json not redirected):

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

In versioned.xml, a new attribute has been added at the end of the attributes (no new line):

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

### SRA Schema Definition
It is simple to test any XML file against SRA:

	xmllint versioned.xml --schema schemas/xml/SRA.sample.xsd >/dev/null
	versioned.xml validates


## Old documentation


### Examples of validating sample xml.

`-sample` indicates the object to validate is a sample xml. `-out:<filename>` is the updated xml that is written containing all valid objects. 


Here's an example of `SAMPLE_SET` xml containing two objects both of which validate. 

    $ python -m version_metadata -sample -out:./version_metadata/examples/samples.versioned.xml ./version_metadata/examples/samples.xml
    {'-config': './config.json', '-out': './version_metadata/examples/samples.versioned.xml'}
    ./config.json
    # xml validates [against:../schemas/xml/SRA.sample.xsd]... True [./version_metadata/examples/samples.xml]
    # is valid ihec spec:True version:1.0 [Primary Tissue from Some Donor]
    # is valid ihec spec:True version:1.0 [Primary Tissue from Some Other Donor]
    written:./version_metadata/examples/samples.versioned.xml

Similarly to run the above example using pipenv 
    
    `$ pipenv run python main.py -sample -out:./version_metadata/examples/samples.versioned.xml ./version_metadata/examples/samples.xml`


Note if you are running from a different directory then you may need to modify paths in `config.json`. 

### Diffs

In case all object validate, and only one xml was given for validation, then the only difference between the xmls should be the version tag. This should *always* be verified.

    $ diff ./version_metadata/examples/samples.xml ./version_metadata/examples/samples.versioned.xml
    27c27
    <         <SAMPLE_ATTRIBUTE><TAG>DONOR_SEX</TAG><VALUE>Male</VALUE></SAMPLE_ATTRIBUTE>
    ---
    >         <SAMPLE_ATTRIBUTE><TAG>DONOR_SEX</TAG><VALUE>Male</VALUE></SAMPLE_ATTRIBUTE><SAMPLE_ATTRIBUTE><TAG>VALIDATED_AGAINST_METADATA_SPEC</TAG><VALUE>1.0/SAMPLE</VALUE></SAMPLE_ATTRIBUTE>
    30a31,32
    >
    >
    56c58
    <         <SAMPLE_ATTRIBUTE><TAG>DONOR_SEX</TAG><VALUE>Female</VALUE></SAMPLE_ATTRIBUTE>
    ---
    >         <SAMPLE_ATTRIBUTE><TAG>DONOR_SEX</TAG><VALUE>Female</VALUE></SAMPLE_ATTRIBUTE><SAMPLE_ATTRIBUTE><TAG>VALIDATED_AGAINST_METADATA_SPEC</TAG><VALUE>1.0/SAMPLE</VALUE></SAMPLE_ATTRIBUTE>
    60d61
    < </SAMPLE_SET>
    61a63,64
    >
    > </SAMPLE_SET>
    \ No newline at end of file



Finally check versioned xml still validates against SRA:
    
    $ xmllint ./version_metadata/examples/samples.versioned.xml --schema .../schemas/xml/xml/SRA.sample.xsd > /dev/null
    ./version_metadata/examples/samples.versioned.xml validates

Note that example xml given validates against SRA XML schema, and conforms to IHEC schema, but EGA will not accept this as it does not include "gender", "subject_id" and "phenotype" attributes. This should be included. 

### Example where one of the objects doesn't validate. 

    python -m version_metadata -sample -out:./version_metadata/examples/samples.with_one_invalid.versioned.xml ./version_metadata/examples/samples.with_one_invalid.xml -overwrite-outfile
    [{'-config': './config.json', '-out': './version_metadata/examples/samples.with_one_invalid.versioned.xml'}, ['./version_metadata/examples/samples.with_one_invalid.xml']]
    # xml validates [against:../schemas/xml/SRA.sample.xsd]... True [./version_metadata/examples/samples.with_one_invalid.xml]
    #__normalizingTags:Primary Tissue from Some Donor
    #__normalizingTags:Primary Tissue from Some Other Donor
    # is valid ihec spec:True version:0.9 [Primary Tissue from Some Donor]
    #__validationFailuresFound: see ./errs.Jan-8-2018-15.25.54.log.1
    # is valid ihec spec:False version:__invalid__ [Primary Tissue from Some Other Donor]
    written:./version_metadata/examples/samples.with_one_invalid.versioned.xml

### With multiple invalids/valids

    python -m version_metadata -sample -out:./version_metadata/examples/samples.with_multiple_valid_invalid.versioned.xml ./version_metadata/examples/samples.with_multiple_valid_invalid.xml -overwrite-outfile
    [{'-config': './config.json', '-out': './version_metadata/examples/samples.with_multiple_valid_invalid.versioned.xml'}, ['./version_metadata/examples/samples.with_multiple_valid_invalid.xml']]
    # xml validates [against:../schemas/xml/SRA.sample.xsd]... True [./version_metadata/examples/samples.with_multiple_valid_invalid.xml]
    #__normalizingTags:Primary Tissue from Some Donor A
    #__normalizingTags:Primary Tissue from Some Donor B
    #__normalizingTags:Primary Tissue from Some Donor D
    #__normalizingTags:Primary Tissue from Some Donor C
    #__warning: failed to cast donor age to number
    {'collection_method': 'Flash Frozen', 'donor_sex': 'Female', 'donor_health_status': 'Donor_Health_Condition', 'donor_age_unit': 'year', 'molecule': 'genomic DNA', 'disease': 'None', 'biomaterial_type': 'Primary Tissue', 'sample_id': 'CEMTXX', 'tissue_depot': 'Some_Tissue', 'tissue_type': 'Some_Tissue', 'donor_id': 'Some_Other_Donor', 'donor_life_stage': 'adult', 'biomaterial_provider': 'Some Lab', 'donor_age': '49 years', 'sample_ontology_uri': ' http://purl.obolibrary.org/obo/UBERON____', 'donor_ethnicity': 'Some_Ethnicity'}
    # is valid ihec spec:True version:0.9 [Primary Tissue from Some Donor A]
    # is valid ihec spec:True version:0.9 [Primary Tissue from Some Donor B]
    #__validationFailuresFound: see ./errs.Jan-8-2018-15.23.55.log.1
    # is valid ihec spec:False version:__invalid__ [Primary Tissue from Some Donor D]
    #__validationFailuresFound: see ./errs.Jan-8-2018-15.23.55.log.2
    # is valid ihec spec:False version:__invalid__ [Primary Tissue from Some Donor C]
    written:./version_metadata/examples/samples.with_multiple_valid_invalid.versioned.xml


### Examples of validating experimnet xml

An example where all experiments in the set validate.

    python -m version_metadata -experiment ./version_metadata/examples/experiment.xml -out:./version_metadata/examples/experiment.validated.xml -overwrite-outfile
    [{'-config': './config.json', '-out': './version_metadata/examples/experiment.validated.xml'}, ['./version_metadata/examples/experiment.xml']]
    ./config.json
    # xml validates [against:../schemas/xml/SRA.experiment.xsd]... True [./version_metadata/examples/experiment.xml]
    # is valid ihec spec:True 1.0 [WGBS (whole genome bisulfite sequencing) analysis of SomeSampleA (library: SomeLibraryA).]
    # is valid ihec spec:True 1.0 [WGBS (whole genome bisulfite sequencing) analysis of SomeSampleB (library: SomeLibraryB).]
    written:./version_metadata/examples/experiment.validated.xml
    # xml validates [against:../schemas/xml/SRA.experiment.xsd]... True [./version_metadata/examples/experiment.validated.xml]
    ok

An example where some only experiments in the set validate.

    $ python -m version_metadata -experiment ./version_metadata/examples/experiment.some_invalid.xml -out:./version_metadata/examples/experiment.some_invalid.validated.xml -overwrite-outfile
    [{'-config': './config.json', '-out': 'examples/experiment.some_invalid.validated.xml'}, ['./version_metadata/examples/experiment.some_invalid.xml']]
    ./config.json
    # xml validates [against:../schemas/xml/SRA.experiment.xsd]... True [./version_metadata/examples/experiment.some_invalid.xml]
    # is valid ihec spec:True 1.0 [RNA-Seq (strand specific) analysis of SomeSampleC (library: SomeLibrary).]
    # is valid ihec spec:True 1.0 [RNA-Seq (strand specific) analysis of SomeSampleB (library: SomeLibrary).]
    # is valid ihec spec:True 1.0 [RNA-Seq (strand specific) analysis of SomeSampleA (library: SomeLibrary).]
    written:./version_metadata/examples/experiment.some_invalid.validated.xml
    # xml validates [against:../schemas/xml/SRA.experiment.xsd]... True [./version_metadata/examples/experiment.some_invalid.validated.xml]
    ok


