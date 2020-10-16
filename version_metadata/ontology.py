import requests
import json

# refactor ../IHEC_Data_Hub/ontology_lookup.py


class Ontology:
	"""
	Class to handle validation of accepted ontologies
	"""

	def __init__(self):
		self.base_url = 'https://www.ebi.ac.uk/ols/api/search'
		self.ontology_rules = {
			'sample_ontology_curie': {
   			 'Cell Line': 'efo',
   			 'Primary Cell': 'cl',
   			 'Primary Tissue': 'uberon'
   			},
			'experiment_ontology_curie': 'obi',                                                                                                                                     'molecule_ontology_curie': 'so',
	# leaving out these two for now
	# 'disease_ontology_curie': 'ncim',
	# 'donor_health_status_ontology_curie': 'ncim'
		}	



	def parse_curie(self, curie):
		[db, term] = curie.split(':')
		return {'ontology_name': db, 'curie':term}


	def check_ontology_rules(self, curie, ontology_type, schema_object, subparam=None, msg=None):
		"""
		:param curie'
		:param ontology_type: E.g. 'sample_ontology_curie', 'molecule_ontology_curie'
		:param schema_object: Schema object where ontology term is located. Needed for an error message.
		:param subparam: Used to handle complex validation when accepted ontology depends on value of another property,
		e.g. if 'biomaterial_type': 'Cell Line' then accepted ontology for 'sample_ontology_curie' is EFO
		:param msg: custom error message is term is not accepted
		:return: True if validation passed. False if not.
		"""

		# check what ontology must be applied by rule
		rule_ontology = ontology_rules[ontology_type] # e.g 'so' or {'Cell Line': 'efo'}
		# the given ontology by input
		current_ontology = self.parse_curie(curie)['ontology_name']
		# check if rule is a dict, then unpack rule ontology based on subparam value
		if subparam:
			rule_ontology = rule_ontology[subparam]

		ok = current_ontology == rule_ontology
		return ok

	def api_payload(self, curie):
		"""
		Payload for GET e.g. q=EFO_0001639&ontology=efo
		:return: Returns params to query according to API spec
		"""
		# Note: ontology lookup service's curie is case sensitive
		parsed_curie = self.parse_curie(curie)
		q = parsed_curie['ontology_name'].upper() + '_' + parsed_curie['curie']
		ontology = parsed_curie['ontology_name']
		return {'q': q, 'ontology': ontology}

	def validate(self, curie):
		"""
		Calls ontology lookup API to check if curie is valid
		:return: Returns True if response is not empty
		"""
		r = requests.get(self.base_url, headers={'accept': 'application/json'}, params=self.api_payload(curie))
		response = json.loads(r.content.decode('utf-8'))
		response = response.get('response')
		ok = response.get('numFound') > 0
		return ok



