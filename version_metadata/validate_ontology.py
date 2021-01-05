import requests
import json



def logger(*args):
	print(*args)




class OntologyValidation:
	ontology_rules = {
    'sample_ontology_curie': {
        'Cell Line': 'efo',
        'Primary Cell': 'cl',
        'Primary Tissue': 'uberon'
    },
		'origin_sample_ontology_curie' : 'uberon',
    	'experiment_ontology_curie': 'obi',
    	'molecule_ontology_curie': 'so',
    	# leaving out these two for now
    	'disease_ontology_curie': 'ncim',
    	'donor_health_status_ontology_curie': 'ncim'
	}

	def __init__(self):
		self.verbose = False
		self.mock = False
		self.base_url = 'https://www.ebi.ac.uk/ols/api/search'
		self.cache = dict()

	def parse_curie(self, curie):
		[ontology_name, term] = curie.split(':')
		return {'ontology_name':ontology_name, 'curie': term}

	def payload(self, curie):
		try:
			raw = self.parse_curie(curie)
			q = raw['ontology_name'].upper() + '_' + raw['curie']
			ontology = raw['ontology_name']
			return {'q': q, 'ontology': ontology}
		except Exception as err:
			return {'err': str(err), 'term':term}

	def accepteddb(self, term, ontology_type, subparam=None):
		rule_ontology = OntologyValidation.ontology_rules[ontology_type]
		current_ontology = self.parse_curie(term)['ontology_name'].lower()
		termdata = self.parse_curie(term)
		if subparam and isinstance(rule_ontology, dict):
			rule_ontology = rule_ontology[subparam]
		if not current_ontology == rule_ontology:
			err = '#__invalid_ontology_db__: "' + current_ontology +  '" is not valid for ' + ontology_type + '/' + str(subparam) + ', expected ' + str(rule_ontology) 
			return {'ok':False, 'err':err}
		else:
			return {'ok':True}

	def __call__(self, term, refresh=False):
		if term in self.cache and not refresh:
			return self.cache[term]
		if self.mock: return { 'ok' : True, 'mocked':True}
		
		payload = self.payload(term)
		if 'err' in payload:
			logger("#__could_not_parse__:", payload)
			payload['ok'] = False
			return payload

		

		try:
			r = requests.get(self.base_url, headers={'accept': 'application/json'}, params=payload)
			response = json.loads(r.content.decode('utf-8'))
			response = response.get('response')
			if response.get('numFound') > 0:
				if self.verbose: logger('#__validated_curie__: {0}'.format(term))
				r = {'ok': True}
			else:
				if self.verbose: logger('#__does_not_validate__: {0}'.format(term))
				r =  {'ok':False, 'err': '__notfound__'}
			self.cache[term] = r
			return r
		except Exception as err:
			return {'ok': False, 'err':str(err)}
			
validate_ontology = OntologyValidation()
#validate_ontology.mock = True



def check_term(term, termtype, subparam=None):
	ok = True
	for e in term:
		ok1 = validate_ontology.accepteddb(e, ontology_type = termtype, subparam=subparam)
		ok2 = {'ok':False}
		if ok1['ok']:
			ok2 = validate_ontology(e)
		ok = ok and ok1['ok'] and ok2['ok']
		print(e, ok1, ok2)
	return ok

def tests():
	print(validate_ontology('obi:000185812'))
	print(validate_ontology('obi:0001858'))
	print(validate_ontology('ncit:C115935xxxxxxxxx'))
	check_term(['ncit:C115935xxxxxxxxx'], 'disease_ontology_curie')
	
	for e in [("molecule_ontology_curie", ["so:0000991"]), ("experiment_ontology_curie", ["obi:OBI_0001863"]), ('disease_ontology_curie', ['ncit:C115935']), ('sample_ontology_curie', ['cl:0001054']), ('donor_health_status_ontology_curie', ['ncit:C0277545'])]:
		print(e, check_term(e[1], e[0], 'Primary Cell'))



	print(validate_ontology.accepteddb('obi:000185812', ontology_type='sample_ontology_curie'))
	print(validate_ontology.accepteddb('obi:000185812', ontology_type='experiment_ontology_curie'))
	print(validate_ontology.accepteddb('obi:0001858',ontology_type='sample_ontology_curie', subparam='Cell Line'))


if __name__ == '__main__':
	tests()
