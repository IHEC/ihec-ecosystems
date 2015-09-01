#Json hub decription 

A formal definition is at: https://github.com/IHEC/ihec-ecosystems/blob/master/JSON_Data_Hub_Validator/data_hub_schema.json

##Informal description

A json hub is a hash keyed by experiment identifier.

* Each experiment key in the hash refers to a hash with following required keys:
	'analysis_attributes', 'analysis_group', 'browser', 'experiment', 'experiment_attributes', 'sample_attributes'

* Each of keys 'analysis_attributes', 'experiment_attributes', 'sample_attributes' points to hash containing attrubutes specified by IHEC Metadata Working group at https://docs.google.com/document/d/1F8RUNGtKMr2lBqMc6pvSyAlZmmtwZxMB3I3u7f7xIbg , with required attributes defined in https://github.com/IHEC/ihec-ecosystems/blob/master/docs/trackhub_specification.md

* 'analysis_group' is a string identifier for the centre processing the data referenced from the hub. 

* 'experiment' is the experiment type. It must be one of the experiment types defined in the Metadata Standards document.


###Tracks:

* The 'browser' key points to a hash of each data track for the experiment. This hash is keyed by a description for the track (the 'type'). Any key is supported, however, only keys corresponding to required track types as defined in https://github.com/IHEC/ihec-ecosystems/blob/master/minimum_required_track_types.md are read. 

* For each 'type' key under 'browser', the following keys are required:
	  'tag' : a short tag for the 'type' which is used in the UCSC hub description 
	  'description_url' : a url with description of methods used to generate the track 
	  'type' : the type key itself
	  'big_data_url' : the actual data url

* A key corresponding to strand maybe required for strand specific data.

* If a track is stranded (forward or reverse), the opposite strand track also needs to be provided.

* For one experiment, a track should be unique for a type/strand combination. (e.g. not having two peak files, or two coverage tracks on the forward strand)


###Notes:

* Note that the the format is extensible. You can annotate your data, and include data way beyond the specification.   

* For complete examples (possibly not up to date with latest developments on the spec) see: https://github.com/IHEC/ihec-ecosystems/tree/master/BCGSC_CEMT/Templater/examples and https://github.com/IHEC/ihec-ecosystems/blob/master/JSON_Data_Hub_Validator/example1.json
