Based on:

    $ apy -V
    Python 2.7.12 :: Anaconda 2.3.0 (64-bit)

Note that you can also use plain Python 2 and install required packages:
* either by using pip directly (if you have root privileges)

    `$ pip install -r requirements.txt`

* or by using pipenv

    `$ pipenv install --two -r requirements.txt`


### Usage

Note that there are no space in arguments like `-out:./examples/samples.versioned.xml`.

`-sample` indicates the object to validate is a sample xml. `-out:<filename>` is the updated xml that is written containing all valid objects. 


Here's an example of `SAMPLE_SET` xml containing two objects both of which validate. 

    $ apy __main__.py -sample -out:./examples/samples.versioned.xml ./examples/samples.xml
    {'-config': './config.json', '-out': './examples/samples.versioned.xml'}
    ./config.json
    # xml validates [against:./schemas/SRA.sample.xsd]... True [./examples/samples.xml]
    # is valid ihec spec:True version:1.0 [Primary Tissue from Some Donor]
    # is valid ihec spec:True version:1.0 [Primary Tissue from Some Other Donor]
    written:./examples/samples.versioned.xml

Similarly to run the above example using pipenv 
    $ pipenv run __main__.py -sample -out:./examples/samples.versioned.xml ./examples/samples.xml

### Diffs

In case all object validate, and only one xml was given for validation, then the only difference between the xmls should be the version tag. This should *always* be verified.

    $ diff ./examples/samples.xml ./examples/samples.versioned.xml
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
    
    $ xmllint ./examples/samples.versioned.xml --schema ./schemas/SRA.sample.xsd > /dev/null
    ./examples/samples.versioned.xml validates

Note that example xml given validates against SRA XML schema, and conforms to IHEC schema, but EGA will not accept this as it does not include "gender", "subject_id" and "phenotype" attributes. This should be included. 

### Example where one of the objects doesn't validate. 

    apy __main__.py -sample -out:./examples/samples.with_one_invalid.versioned.xml ./examples/samples.with_one_invalid.xml -overwrite-outfile
    [{'-config': './config.json', '-out': './examples/samples.with_one_invalid.versioned.xml'}, ['./examples/samples.with_one_invalid.xml']]
    # xml validates [against:./schemas/SRA.sample.xsd]... True [./examples/samples.with_one_invalid.xml]
    #__normalizingTags:Primary Tissue from Some Donor
    #__normalizingTags:Primary Tissue from Some Other Donor
    # is valid ihec spec:True version:0.9 [Primary Tissue from Some Donor]
    #__validationFailuresFound: see ./errs.Jan-8-2018-15.25.54.log.1
    # is valid ihec spec:False version:__invalid__ [Primary Tissue from Some Other Donor]
    written:./examples/samples.with_one_invalid.versioned.xml

### With multiple invalids/valids

    apy __main__.py -sample -out:./examples/samples.with_multiple_valid_invalid.versioned.xml ./examples/samples.with_multiple_valid_invalid.xml -overwrite-outfile
    [{'-config': './config.json', '-out': './examples/samples.with_multiple_valid_invalid.versioned.xml'}, ['./examples/samples.with_multiple_valid_invalid.xml']]
    # xml validates [against:./schemas/SRA.sample.xsd]... True [./examples/samples.with_multiple_valid_invalid.xml]
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
    written:./examples/samples.with_multiple_valid_invalid.versioned.xml



