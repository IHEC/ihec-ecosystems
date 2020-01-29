from config import Config
from utils import cmn, json2, logger



import egautils






class Prevalidate:
	def __init__(self, jsonschemas, version):
		self.jsonschemas = [j for j in jsonschemas]
		for jsonschema in self.jsonschemas:
			self.schema_id = jsonschema['$id'].split('/')[-1].replace('.json', '')
			assert self.schema_id in ['experiment', 'sample']
			self.bytype = dict()
			for defn in jsonschema['definitions']:
				assert not defn in self.bytype
				self.bytype[defn] = list(jsonschema['definitions'][defn]['properties'].keys())
	
	def attributes(self, obj):
		return {k.lower():v for k, v in obj['attributes'].items()}
	
	def check_sample_properties(self, obj):
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
			return False
		if not 'library_strategy' in attrs:
			print('__prevalidate_fail', tag ,': missing library strategy: cannot determine schema to use')
			return False

		exp_type =  egautils.strategy2schema(attrs['library_strategy'])
		if not exp_type in self.bytype:
			print('__prevalidate_fail', tag , ': invalid experiment_type: ' + exp_type)
			return False
			
		keys = self.bytype[exp_type]
		missing = [k for k in keys if not k in attrs]
		if missing:
			print('__prevalidate_fail', tag , ': missing attributes for experiment_type: {0} , {1}'.format(exp_type, missing))
			return False
		#print(objid(obj) + ':prevalidates') 
		return True


	def prevalidate(self, obj, tag):
		if  self.schema_id in ['experiment']:
			return self.check_experiment_properties(obj, tag)
		else:
			print('#__warn:__no_prevalidation_available_for_sample_schema_yet__')
			return True


if __name__ == '__main__':
	schemafiles = ['../schemas/json/1.1/experiment.json', '../schemas/json/1.1/sample.json']
	prevalidate = Prevalidate([json2.loadf(f) for f in schemafiles] , '1.1')
	for example in ['./examples/experiment.some_invalid.validated.xml.extracted.json']:
		for e in json2.loadf(example):
			prevalidate.check_experiment_properties(e)


