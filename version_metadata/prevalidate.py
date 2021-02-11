from .config import Config
from .utils import cmn, json2, logger

from . import egautils
from . import markdown
from . import semantic
from . import io_adaptor

from collections import namedtuple

#from . import exp_semantic_rules

from . import utils

Constraint = namedtuple('Constraint', ['rules', 'required', 'dependencies', 'properties'])

class SchemaParser:
	@staticmethod
	def schema_id(jsonschema):
		return jsonschema['$id'].split('/')[-1].replace('.json', '')

	@staticmethod
	def dependencies(js):
		return [e["$ref"].split('/')[-1] for e in js.get("allOf", {}   )]


	def __init__(self, jsonschema, cfg=None): 
		self.schema_id = SchemaParser.schema_id(jsonschema)
		self.rules = self.semantic_rules() 
		self.cfg = cfg

		if self.schema_id in ['experiment']:
			self.constraints  =  self.experiment(jsonschema)
		elif self.schema_id in ['sample']:
			self.constraints  = self.sample(jsonschema)
		else:
			raise Exception(self.schema_id)

		self.bytype = {k: self.constraints[k].properties for k in self.constraints}


	@staticmethod
	def properties(properties):
		property_attrs = ["type" , "minItems", "maxItems"]
		getprop = lambda h, k: (k, h.get(k, "__undef__"))
		parsed = {p :   cmn.safedict([ getprop(properties[p], e) for e in property_attrs]) for p in properties}
		for p in properties:
			if properties[p].get("type", "").lower() != "array": 
				parsed[p]["description"] = "__malformed-schema__"
				parsed[p]["enum"] = ""
			else:
				item_attr = properties[p].get("items", {})
				parsed[p]["description"] = item_attr.get("description", "<strong>_undef_</strong>")
				parsed[p]["enum"] = item_attr.get("enum", "")
		return parsed

	def sample(self, js):
		rules = self.semantic_rules()
		bytype, required, dependencies = dict(), dict(), dict()
		
		if list(js['definitions'].keys()) != ['donor']:
			utils.sanity_check_fail('__malformed-schema__:defnitions as not expected [1]') 

		for defn in js['definitions']:
			properties = js['definitions'][defn]['properties']
			bytype[defn] =  SchemaParser.properties(properties)   
			required[defn] = js['definitions'][defn]['required']
			dependencies[defn] = SchemaParser.dependencies(js['definitions'][defn])

		for subtype in js["allOf"]:
			biomaterial_type = subtype['if']['properties']['biomaterial_type']["const"][0]
			if not biomaterial_type in ["Cell Line",  "Primary Cell", "Primary Cell Culture", "Primary Tissue"]:
				utils.sanity_check_fail('__malformed-schema__:defnitions as not expected [2]')
			properties = subtype["then"]["properties"]
			bytype[biomaterial_type] = SchemaParser.properties(properties) 
			required[biomaterial_type] = subtype["then"]["required"]
			dependencies[biomaterial_type] = SchemaParser.dependencies(subtype["then"])
	
		return { k: Constraint(rules.get(k, {}), required.get(k, {}), dependencies.get(k, {}), bytype[k] )  for k in bytype}

		
	

	def experiment(self, jsonschema):
		rules = self.semantic_rules()
		bytype, required, dependencies = dict(), dict(), dict()
		for defn in jsonschema['definitions']:
			if defn in bytype:
				utils.sanity_check_fail('__malformed-schema__:defnitions as not expected [3]:' + defn)
			if not self.cfg:
				bytype[defn] = list(jsonschema['definitions'][defn]['properties'].keys())
			else:
				properties = jsonschema['definitions'][defn]['properties']
				bytype[defn] =  SchemaParser.properties(properties)   #  {p :   cmn.safedict([ getprop(properties[p], e) for e in property_attrs]) for p in properties}

		common = {e : jsonschema['properties'][e] for e in jsonschema['properties']}
		common_required = jsonschema['required']
		preval= { k: Constraint(rules.get(k, {}), required.get(k, []) + common_required, dependencies.get(k, {}), bytype[k] )  for k in bytype}
		
		#print(preval)
		return preval

	def definitions(self):
		return {k: self.constraints[k].properties  for k in self.constraints}
		
	def semantic_rules(self):
		data = dict()
		rules =  semantic.rules(self.schema_id) #  [e for e in dir(exp_semantic_rules) if e.startswith('rule_')]
		for r in rules:
			data[r] = semantic.experiment_rule_desc(r)
		
		ruleshash = dict()
		for r in data.values():
			[e1, e2] = r["applies"]
			if not e1 in ruleshash: ruleshash[e1] = dict()
			if not e2 in ruleshash[e1]: ruleshash[e1][e2] = list()
			ruleshash[e1][e2].append(r["description"])
		return ruleshash

	def md(self):
		txt = []
		print(self.rules)
		for k in sorted(self.bytype.keys()):
			txt.append(markdown.markdown(k, self.bytype[k], self.constraints[k], self.schema_id))
		return '\n'.join(txt) + '\n\n'



class Prevalidate:
	def __init__(self, jsonschemas, version):
		self.jsonschemas = [j for j in jsonschemas]
		if not len(jsonschemas) == 1: # no more lists here
			utils.sanity_check_fail('__malformed-schema__:defnitions as not expected [4]')
		#for jsonschema in self.jsonschemas:
		jsonschema = jsonschemas[0]
		self.schema_id = SchemaParser.schema_id(jsonschema)   #jsonschema['$id'].split('/')[-1].replace('.json', '')
		if not self.schema_id in ['experiment', 'sample']:
			utils.sanity_check_fail('__malformed-schema__:defnitions as not expected [5]')
		self.bytype = SchemaParser(jsonschema).definitions()
		self.version = version

	def attributes(self, obj):
		return {k.lower():v for k, v in obj['attributes'].items()}
	
	def check_sample_properties(self, obj, tag):
		#raise NotImplementedError('sample')
		attrs = obj

		if not 'biomaterial_type' in attrs:
			print(tag + ': missing biomaterial_type: cannot determine schema to use')
			return False, ['missing biomaterial_type']

		biomaterial_type = attrs['biomaterial_type'][0]
		if not biomaterial_type in self.bytype:
			print(tag + ': invalid biomaterial_type: ' + biomaterial_type)
			return False, ['unknown biomaterial tyoe:' + biomaterial_type ]
			
		keys = self.bytype[biomaterial_type]
		missing = [k for k in keys if not k in attrs]
		if missing:
			print(tag + ': missing attributes for biomaterial_type: {0} , {1}'.format(biomaterial_type, missing))
			return False, ['missing', missing]
		print(tag + ':prevalidates')
		return True, []
			
			
	def check_experiment_properties(self, obj, tag):
		attrs = obj
		
		if not 'library_strategy' in attrs:
			print('__prevalidate_fail', tag ,': missing library strategy: cannot determine schema to use')
			return False, ['missing library strategy']


		if len(attrs['library_strategy']) > 1:
			return False, ['unique library strategy expected:' + str(attrs['library_strategy']) ]
		
		strategy = cmn.demanduniq(attrs['library_strategy'])
		exp_type =  egautils.strategy2schema(strategy)
			
	
		if not exp_type in self.bytype:
			print('__prevalidate_fail', tag , ': invalid experiment_type: ' + exp_type)
			return False, ['invalid experiment_type']
		
		if self.version in ["1.0"]:
			if not "experiment_ontology_uri" in attrs and not "experiment_type" in attrs:
				return (False, "__mising_both__:__experiment_ontology_uri+experiment_type__")
			else:
				return (True, [])
		elif self.version in ["1.1", "2.0", "2.1-dev"]:
			if strategy in ['ChIP-Seq'] and not "experiment_target_histone" in attrs and not "experiment_target_tf" in attrs and self.version in ["2.0"]:
				return (False, "1 is required : experiment_target_histone  or  experiment_target_tf")
			if not "experiment_ontology_curie" in attrs and not "experiment_type" in attrs:
				return (False, "__mising_both__:__experiment_ontology_curie+experiment_type__")
			required = ['library_strategy', 'experiment_type', 'experiment_ontology_curie', 'molecule', 'molecule_ontology_curie']
			missing = [e for e in required if not e in attrs]
			if missing:
				return (False, ['missing at prevalidate', missing])
			else:
				return (True, [])
			
	

		if not 'experiment_type' in attrs:
			print('__prevalidate_fail', tag , ': missing experiment_type: cannot determine schema to use')
			return False, ['missing experiment_type']


		raise Exception("__unreachable__")




	def prevalidate(self, obj, tag):
		if  self.schema_id in ['experiment']:
			return self.check_experiment_properties(obj, tag)
		else:
			return self.check_sample_properties(obj, tag)
			print('#__warn:__no_prevalidation_available_for_sample_schema_yet__')
			return True, {'__warn__' : 'prevalidation ignored'}


def main(args):
	schemas = {
		'1.0':  ['./schemas/json/1.0/experiment.json', './schemas/json/1.0/sample.json'],
		'2.0':  ['./schemas/json/2.0/experiment.json', './schemas/json/2.0/sample.json']
	}
	for version, schemafiles in schemas.items():
		for schemafile in schemafiles:	
			parser = SchemaParser(io_adaptor.load_schema(schemafile), True)
			outfile = cmn.basename(schemafile) 
			outfile = './autodocs/' + outfile.replace('.json', '_' + version + '.md')
			print("outfile:", outfile)
			print(cmn.dumpf(outfile, parser.md()))

	

if __name__ == '__main__':
	main()



