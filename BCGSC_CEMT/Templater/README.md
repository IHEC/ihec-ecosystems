json data sharing specification and visualization templating
============================================================
usage:

    python __main__.py -ucsc -config:./examples/PrimaryTissue.tracks.json -hub:./Config/centre.json -annotations:./Config/annotations.json -www:$WWW -settings:./Config/settings.json -by-centre

examples:

    python  __main__.py -ucsc -config:./examples/exampleWithMultipleTypes.json -hub:./Config/centre.json -annotations:./Config/annotations.json -www:$WWW -settings:./Config/settings.json -by-centre

writes:
    $WWW/CEMT.Mar-19-2015-21.33.01.hub
    $WWW/genomes.Mar-19-2015-21.33.01.gs
    $WWW/hg19/tracks.Mar-19-2015-21.33.01.db

generated hub:
http://genome.ucsc.edu/cgi-bin/hgTracks?db=hg19&hubUrl=http://www.epigenomes.ca/data/CEMT/temp/hubs/examples/CEMT.byCentre.hub

    python  __main__.py -ucsc -config:./examples/exampleWithMultipleTypes.json -hub:./Config/centre.json -annotations:./Config/annotations.json -www:$WWW -settings:./Config/settings.json

writes:
    $WWW/CEMT.Mar-19-2015-21.37.40.hub
    $WWW/genomes.Mar-19-2015-21.37.40.gs
    $WWW/hg19/tracks.Mar-19-2015-21.37.40.db

generated hub:
http://genome.ucsc.edu/cgi-bin/hgTracks?db=hg19&hubUrl=http://www.epigenomes.ca/data/CEMT/temp/hubs/examples/CEMT.byAssay.hub

Developed on Python 2.7.7 :: Anaconda 2.0.1

$WWW: The the path to http accessible directory where hub will be written. Must have hg19 subdirectory (or appropriate genome db) as neeeded by UCSC track hub specification.

    -settings:<json> is the visualization settings.
    -hub:<json> is used to specify hub labels etc. 
    -annotations:<json> is a list of attributes that are retained for metadata in UCSC.
    -by-centre flag creates hub organized by centre. no -by-centre creates hub organized by assays

UCSCTemplate.customizable method controls subgroups and metadata annotations.










