# IHEC Data Hub validator

## Files description

**validateHub.py** can be used as a standalone tool to validate an IHEC data hub JSON document. You'll need Python with the dependencies in requirements.txt in order to use it.

**requirements.txt** can be used with pip to install mandatory pacakges.

**example1.json** is a simple example the validator can be used on.


## Setup
Make sure you have the required dependencies. If you have ```pip``` on your machine, you can do:
```
pip install
```


## Usage
To validate in strict mode (make sure only predefined track types are included):
```
python validateHub.py --json='./example1.json' --epirr
```

To validate in loose mode (allow any kind of track types):

## Switches:
* --json : The IHEC Data Hub to be validated. Mandatory.
* --loose-validation : Allow for other track types than the ones listed in the controlled vocabulary. If you use this, please make sure that you don't create a track type that is already in the list using another name.
* --epirr : Validate that the IHEC Data Hub metadata matches the one provided in EpiRR. This is useful to identify data entry mistakes.
* --verbose : Output more information on screen. Sometimes useful to understand why an error is displayed.


 
## Future Plans:
* Minimum set of tracks is provided for a given assay, as described here: https://github.com/IHEC/ihec-ecosystems/blob/master/minimum_required_track_types.md
* Ontology term at a given URI matches term explicitely given in the JSON hub. (e.g. if `disease_ontology_uri` == `http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C115935`, then `disease` == `Healthy`) 
 
