# Submitting an update PR

Before submitting a PR check that you have done the following:
- updated the JSON schema (`schemas/json/#.#*/*.json`)
- updated the Markdown specification (`../docs/metadata/#.#/Ihec_metadata_specification.md`)
- updated the example files (`version_metadata/examples/*`)
- tested the metadata validator on the examples in `version_metadata/readme.md`
- tested the hub validator on the examples in `IHEC_Data_Hub/using_validator.md`

# Updating schema versions
- Schema updates:
	- The schema stored in `schemas/json/dev` is considered to be work in development, and modifications are always made to that copy.
	- On a roughly yearly basis (typically at the IHEC annual meeting, when it happens):
		- The dev schema is reviewed (both on the JSON and MarkDown) and made official. 
		- This schema is thus given a version number:
			- Schemas are numbered with two numbers, a major followed by a minor release number, e.g. `V1.2`.
			- The minor number is incremented each time changes are made official.
			- The major number is incremented at each major change, i.e. when submissions compliant with the latest schema are no longer compliant with the previous schema. 
		- The `dev` directory is duplicated into a new directory with the appropriate number.
