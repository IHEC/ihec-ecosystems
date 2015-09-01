#Data hub validation

**validateHub.py** can be used as a standalone tool to validate an IHEC data hub JSON document.

**data_hub_schema.json** can be used with other external JSON validation tools.
 
###To Do:
The following things are not supported by the JSON-schema, and will be implemented in a semantic validator:

* Minimum set of tracks is provided for a given assay, as described here: https://github.com/IHEC/ihec-ecosystems/blob/master/minimum_required_track_types.md

* Ontology term at a given URI matches term explicitely given in the JSON hub. (e.g. if `disease_ontology_uri` == `http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C115935`, then `disease` == `Healthy`)

* Metadata matches what's in EpiRR if dataset is registered there 
 
