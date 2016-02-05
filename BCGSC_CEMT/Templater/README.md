json data sharing specification and visualization templating
============================================================
usage:

    python __main__.py -ucsc -config:./examples/hub.ChIP.json -hub:./Config/centre.json -annotations:./Config/annotations.json -www:$WWW -settings:./Config/settingsNoHide.json -by-centre

examples:

See ./examples to see examples of json hubs by assay
Run ./generateExamples <web_accessible_location> to generate example assay specific hubs:

http://www.epigenomes.ca/data/CEMT/IHEC/hubs/CEMT.Aug-29-2015-18.56.29.5G19WJG268H8.ChIP
http://www.epigenomes.ca/data/CEMT/IHEC/hubs/CEMT.Aug-29-2015-18.56.29.E4KZ4ACBVYSK.mRNA
http://www.epigenomes.ca/data/CEMT/IHEC/hubs/CEMT.Aug-29-2015-18.56.29.KISU5KG8MFEF.WGS
http://www.epigenomes.ca/data/CEMT/IHEC/hubs/CEMT.Aug-29-2015-18.56.29.NZDSR31ZLLMM.smRNA
http://www.epigenomes.ca/data/CEMT/IHEC/hubs/CEMT.Aug-29-2015-18.56.29.Y6EVR30JO7EE.WGBS


Recommended Python 2.7.7 :: Anaconda 2.0.1

$WWW: The the path to http accessible directory where hub will be written. Must have hg19 subdirectory (or appropriate genome db) as neeeded by UCSC track hub specification.

    -settings:<json> is the visualization settings.
    -hub:<json> is used to specify hub labels etc. 
    -annotations:<json> is a list of attributes that are retained for metadata in UCSC.
    -by-centre flag creates hub organized by centre. no -by-centre creates hub organized by assays

UCSCTemplate.customizable method controls subgroups and metadata annotations.










