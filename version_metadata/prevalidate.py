from .config import Config
from .utils import cmn, json2, logger

from . import egautils
from . import markdown
from . import exp_semantic_rules



class SchemaParser:
	def __init__(self, jsonschema, cfg=None): 
		getprop = lambda h, k: (k, h.get(k, "__undef__"))		
		property_attrs = ["type" , "minItems", "maxItems"]
		bytype = dict()
		for defn in jsonschema['definitions']:
			assert not defn in bytype
			if not cfg:
				bytype[defn] = list(jsonschema['definitions'][defn]['properties'].keys())
			else:
				properties = jsonschema['definitions'][defn]['properties']
				bytype[defn] = {p :   cmn.safedict([ getprop(properties[p], e) for e in property_attrs]) for p in properties}
				for p in properties:
					item_attr = properties[p].get("items", {})
					bytype[defn][p]["description"] = item_attr.get("description", "_undef_")
					bytype[defn][p]["enum"] = item_attr.get("enum", "")

		self.rules = self.semantic_rules() 
		self.bytype = bytype
		
	def definitions(self):
		return self.bytype
		
	def semantic_rules(self):
		data = dict()
		rules = [e for e in dir(exp_semantic_rules) if e.startswith('rule_')]
		for r in rules:
			f = getattr(exp_semantic_rules, r)
			data[r] = json2.loads(f.__doc__)
		ruleshash = dict()
		for r in data.values():
			print(r)
			[e1, e2] = r["applies"]
			if not e1 in ruleshash: ruleshash[e1] = dict()
			if not e2 in ruleshash[e1]: ruleshash[e1][e2] = list()
			ruleshash[e1][e2].append(r["description"])
		return ruleshash

	def md(self):
		txt = []
		print(self.rules)
		for k in sorted(self.bytype.keys()):
			txt.append(markdown.markdown(k, self.bytype[k], self.rules.get(k, {})))
			print(k, self.rules, 'XX')
		return '\n'.join(txt) + '\n\n'



class Prevalidate:
	def __init__(self, jsonschemas, version):
		self.jsonschemas = [j for j in jsonschemas]
		assert len(jsonschemas) == 1 # no more lists here
		#for jsonschema in self.jsonschemas:
		jsonschema = jsonschemas[0]
		self.schema_id = jsonschema['$id'].split('/')[-1].replace('.json', '')
		assert self.schema_id in ['experiment', 'sample']
		self.bytype = SchemaParser(jsonschema).definitions()
		self.version = version

	def attributes(self, obj):
		return {k.lower():v for k, v in obj['attributes'].items()}
	
	def check_sample_properties(self, obj):
		raise NotImplementedError('sample')
		attrs = obj

		if not 'biomaterial_type' in attrs:
			print(objid(obj) + ': missing biomaterial_type: cannot determine schema to use')
			return False

		biomaterial_type = attrs['biomaterial_type'][0]
		if not biomaterial_type in self.bytype:
			print(objid(obj) + ': invalid biomaterial_type: ' + biomaterial_type)
			return False
			
		keys = self.bytype[biomaterial_type]
		missing = [k for k in keys if not k in attrs]
		if missing:
			print(objid(obj) + ': missing attributes for biomaterial_type: {0} , {1}'.format(biomaterial_type, missing))
			return False
		print(objid(obj) + ':prevalidates')
		return True
			
			
	def check_experiment_properties(self, obj, tag):
		attrs = obj
		if not 'experiment_type' in attrs:
			print('__prevalidate_fail', tag , ': missing experiment_type: cannot determine schema to use')
			return False, ['missing experiment_type']
		if not 'library_strategy' in attrs:
			print('__prevalidate_fail', tag ,': missing library strategy: cannot determine schema to use')
			return False, ['missing library strategy']

		exp_type =  egautils.strategy2schema(attrs['library_strategy'])
		if not exp_type in self.bytype:
			print('__prevalidate_fail', tag , ': invalid experiment_type: ' + exp_type)
			return False, ['invalid experiment_type']
	
		if self.version in ["1.1"]:
			keys = self.bytype[exp_type]
			missing = [k for k in keys if not k in attrs]
			if missing:
				print('__prevalidate_fail', tag , ': missing attributes for experiment_type: {0} , {1}'.format(exp_type, missing))
			return (False, ['missing', missing]) if missing else (True, [])
		#print(objid(obj) + ':prevalidates') 
		elif self.version in ["1.0"]:
			assert 'library_strategy' in attrs # this is known from above
			if not "experiment_ontology_uri" in attrs and not "experiment_type" in attrs:
				return (False, "__mising_both__:__experiment_ontology_uri+experiment_type__")
			else:
				return (True, [])
		else:
			raise Exception("unknown version:" + self.version)



	def prevalidate(self, obj, tag):
		if  self.schema_id in ['experiment']:
			return self.check_experiment_properties(obj, tag)
		else:
			print('#__warn:__no_prevalidation_available_for_sample_schema_yet__')
			return True, {'__warn__' : 'prevalidation ignored'}


if __name__ == '__main__':
	schemafile = '../schemas/json/1.1/experiment.json'
	parser = SchemaParser(json2.loadf(schemafile) , True)
	#json2.pp([parser.bytype, parser.rules])
	print(cmn.dumpf('experiment_attributes.md', parser.md()))

	




