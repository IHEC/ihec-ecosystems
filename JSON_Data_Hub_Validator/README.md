#Data hub validation

**validateHub.py** can be used as a standalone tool to validate an IHEC data hub JSON document. You'll need Python with the dependencies in requirements.txt in order to use it.

**data_hub_schema.json** can be used with other external JSON validation tools.
 
###Switches:
* --json : The IHEC Data Hub to be validated. Mandatory.
* --loose-validation : Allow for other track types than the ones listed in the controlled vocabulary. If you use this, please make sure that you don't create a track type that is already in the list using another name.
* --epirr : Validate that the IHEC Data Hub metadata matches the one provided in EpiRR. This is useful to identify data entry mistakes.
* --verbose : Output more information on screen. Sometimes useful to understand why an error is displayed.


 
###To Do:
* Minimum set of tracks is provided for a given assay, as described here: https://github.com/IHEC/ihec-ecosystems/blob/master/minimum_required_track_types.md
* Ontology term at a given URI matches term explicitely given in the JSON hub. (e.g. if `disease_ontology_uri` == `http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C115935`, then `disease` == `Healthy`) 
 
