json data sharing specification and visualization templating
============================================================
usage:

    python __main__.py -ucsc -config:./examples/hub.ChIP.json -hub:./Config/centre.json -annotations:./Config/annotations.json -www:$WWW -settings:./Config/settingsNoHide.json -by-centre

examples:

See ./examples to see examples of json hubs by assay


    python __main__.py -ucsc -config:./examples/ChIP_examples.json -hub:./Config/centre.json -annotations:./Config/annotations.json -www:$WWW -settings:./Config/settings_hide.json -by-centre

http://genome.ucsc.edu/cgi-bin/hgTracks?db=hg19&hubUrl=http://www.epigenomes.ca/data/CEMT/temp/hubs/CEMT.Oct-2-2015-23.22.21

    python __main__.py -ucsc -config:./examples/smRNA_example.json -hub:./Config/centre.json -annotations:./Config/annotations.json -www:$WWW -settings:./Config/settings_hide.json -by-centre

http://genome.ucsc.edu/cgi-bin/hgTracks?db=hg19&hubUrl=http://www.epigenomes.ca/data/CEMT/temp/hubs/CEMT.Oct-2-2015-23.24.21

    python __main__.py -ucsc -config:./examples/WGBS_example.json -hub:./Config/centre.json -annotations:./Config/annotations.json -www:$WWW -settings:./Config/settings_hide.json -by-centre

http://genome.ucsc.edu/cgi-bin/hgTracks?db=hg19&hubUrl=http://www.epigenomes.ca/data/CEMT/temp/hubs//CEMT.Oct-2-2015-23.25.57


    python __main__.py -ucsc -config:./examples/mRNA_example.json -hub:./Config/centre.json -annotations:./Config/annotations.json -www:$WWW -settings:./Config/settings_hide.json -by-centre

http://genome.ucsc.edu/cgi-bin/hgTracks?db=hg19&hubUrl=http://www.epigenomes.ca/data/CEMT/temp/hubs//CEMT.Oct-2-2015-23.29.11


Recommended Python 2.7.7 :: Anaconda 2.0.1

$WWW: The the path to http accessible directory where hub will be written. Must have hg19 subdirectory (or appropriate genome db) as neeeded by UCSC track hub specification.

    -settings:<json> is the visualization settings.
    -hub:<json> is used to specify hub labels etc. 
    -annotations:<json> is a list of attributes that are retained for metadata in UCSC.
    -by-centre flag creates hub organized by centre. no -by-centre creates hub organized by assays

UCSCTemplate.customizable method controls subgroups and metadata annotations.
