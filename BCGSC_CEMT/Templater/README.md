json data sharing specification and visualization templating
============================================================

usage:

    python __main__.py -ucsc -config:./examples/hub.ChIP.json -hub:./Config/centre.json -annotations:./Config/annotations.json -www:$WWW -settings:./Config/settings_new_spec.json -by-centre


Recommended Python 2.7.10 | Anaconda 2.3.0

$WWW: The the path to http accessible directory where hub will be written. Must have hg19 subdirectory. 

    -settings:<json> is the visualization settings.
    -hub:<json> is used to specify hub labels etc.
    -annotations:<json> is a list of attributes that are retained for metadata in UCSC.
    -by-centre flag creates hub organized by centre. no -by-centre creates hub organized by assays

## Examples

### ChIP-Seq

python __main__.py -ucsc -www:$EPIWWW/temp/hubs -config:./examples/CEMT0007.ChIP.json -settings:./Config/settings_new_spec.json -hub:./Config/centre.json -annotations:./Config/annotations.json

http://genome.ucsc.edu/cgi-bin/hgTracks?db=hg19&hubUrl=http://www.epigenomes.ca/data/CEMT/temp/hubs/CEMT.Jul-30-2016-23.56.43

### DNA Methylation

python __main__.py -ucsc -www:$EPIWWW/temp/hubs -config:./examples/CEMT0007.DNA_Methylation.json -settings:./Config/settings_new_spec.json -hub:./Config/centre.json -annotations:./Config/annotations.json

http://genome.ucsc.edu/cgi-bin/hgTracks?db=hg19&hubUrl=http://www.epigenomes.ca/data/CEMT/temp/hubs/CEMT.Jul-30-2016-23.53.29

### mRNA

python __main__.py -ucsc -www:$EPIWWW/temp/hubs -config:./examples/CEMT0007.mRNA-Seq.json -settings:./Config/settings_new_spec.json -hub:./Config/centre.json -annotations:./Config/annotations.json

http://genome.ucsc.edu/cgi-bin/hgTracks?db=hg19&hubUrl=http://www.epigenomes.ca/data/CEMT/temp/hubs/CEMT.Jul-30-2016-23.52.02

### smRNA

python __main__.py -ucsc -www:$EPIWWW/temp/hubs -config:./examples/CEMT0007.smRNA-Seq.json -settings:./Config/settings_new_spec.json -hub:./Config/centre.json -annotations:./Config/annotations.json

http://genome.ucsc.edu/cgi-bin/hgTracks?db=hg19&hubUrl=http://www.epigenomes.ca/data/CEMT/temp/hubs/CEMT.Jul-30-2016-23.50.28












