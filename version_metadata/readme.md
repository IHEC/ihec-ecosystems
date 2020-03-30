### Tested with:

    $ python
	Python 3.6.8 |Anaconda, Inc.| (default, Dec 30 2018, 01:22:34)

Note that python 2 is no longer supported.


### Usage

Note that there are no space in arguments like `-out:./version_metadata/examples/samples.versioned.xml`.


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


