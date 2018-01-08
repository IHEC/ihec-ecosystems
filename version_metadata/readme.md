Based on:

    $ apy -V
    Python 2.7.12 :: Anaconda 2.3.0 (64-bit)

Usage:

    $ apy __main__.py -sample -out:./examples/samples.versioned.xml ./examples/samples.xml
    {'-config': './config.json', '-out': './examples/samples.versioned.xml'}
    ./config.json
    # xml validates [against:./schemas/SRA.sample.xsd]... True [./examples/samples.xml]
    # is valid ihec spec:True version:1.0 [Primary Tissue from Some Donor]
    # is valid ihec spec:True version:1.0 [Primary Tissue from Some Other Donor]
    written:./examples/samples.versioned.xml

    
Diffs:

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

    
Check updated xml still validates against SRA:
    
    $ xmllint ./examples/samples.versioned.xml --schema ./schemas/SRA.sample.xsd > /dev/null
    ./examples/samples.versioned.xml validates



Note that example xml given validates against SRA XML schema, and conforms to IHEC schema, but EGA will not accept this as it does not include "gender", "subject_id" and "phenotype" attributes. This should be included. 
