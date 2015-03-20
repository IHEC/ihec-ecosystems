json data sharing specification and visualization templating
============================================================


    python __main__.py -config:./examples/PrimaryTissue.tracks.json -hub:./Config/centre.json -annotations:./Config/annotations.json -www:$WWW -settings:./Config/settings.json -by-centre


$WWW: The the path to http accessible directory where hub will be written. Must have hg19 subdirectory (or appropriate genome db) as neeeded by UCSC track hub specification.

