json data sharing specification and visualization templating
============================================================
See ./examples to see examples of json hubs by assay

run `./generateExamples $WWW` to generate example hubs. WWW is path to where hubs should be written.

./examples/example.DNA_Methylation.json  is an example of using lists for `big_data_url` field

General usage is like:

    apy __main__.py -ucsc -config:./examples/example.ChIP.json -hub:./Config/centre.json -annotations:./Config/annotations.json -www:$WWW -settings:./Config/settings_nohide.json -by-centre -randomize:ChIP

    apy __main__.py -ucsc -config:./examples/example.mRNA.json -hub:./Config/centre.json -annotations:./Config/annotations.json -www:$WWW -settings:./Config/settings_nohide.json -by-centre -randomize:mRNA

    apy __main__.py -ucsc -config:./examples/example.smRNA.json -hub:./Config/centre.json -annotations:./Config/annotations.json -www:$WWW -settings:./Config/settings_nohide.json -by-centre -randomize:smRNA

    apy __main__.py -ucsc -config:./examples/example.WGS.json -hub:./Config/centre.json -annotations:./Config/annotations.json -www:$WWW -settings:./Config/settings_nohide.json -by-centre -randomize:WGS

    apy __main__.py -ucsc -config:./examples/example.DNA_Methylation.json -hub:./Config/centre.json -annotations:./Config/annotations.json -www:$WWW -settings:./Config/settings_nohide.json -by-centre -randomize:DNA_Meth

`-settings`:<json> is the visualization settings.

`-hub`:<json> is used to specify hub labels etc.

`-config`:<json hub>

`-annotations`:<json> is a list of attributes that are retained for metadata in UCSC.

`-by-centre` flag creates hub organized by centre. no -by-centre creates hub organized by assays

`-randomize` adds a tag with a random string to name of the hub


Recommended Python 2.7.7 :: Anaconda 2.0.1

UCSCTemplate.customizable method controls subgroups and metadata annotations.

