from .sraparse import SRAParseObjSet, SRAParseObj,  XMLValidator
from .utils import cmn, json2, logger
from .validate_json import JsonSchema
from .ihec_validator_base import  IHECJsonValidator
from . import exp_semantic_rules
from . import validate_main
from . import utils


class ExperimentValidator(IHECJsonValidator):
	def normalize_tags(self, hashed):
		return { self.normalize(k) :v for k, v in hashed.items()}

	def __init__(self, sra, validators):
		super(ExperimentValidator, self).__init__(validators)	
		self.validators = validators
		self.normalize = lambda t: t.lower().replace(' ', '_')
		self.sra = sra
		self.xmljson = self.sra.obj_xmljson()
		for (xml, attrs) in self.xmljson:
			#print('xxxxxxx', 'jsons')
			attrs['attributes'] = self.normalize_tags(attrs['attributes'])
	
		self.semantic_rules = [e for e in dir(exp_semantic_rules) if e.startswith('rule_')]
		


	def validate_semantics(self, attrs):
		failed = list()
		try:
			attributes = attrs['attributes']
			status = True
			for rule_name in self.semantic_rules:
				f = getattr(exp_semantic_rules, rule_name)
				ok = f(attributes)
				status = status and ok
				if not ok:
					failed.append('semantic_rule:' + rule_name + '=failed')
					print('__semantic_validation_failure__', rule_name)
			return status, failed
		except KeyError as e:
			logger.warn('#warn keyerror in validate_semantics, probably is not even syntactically valid\n')
			return False, failed

# to do: refactor this code along with validate_sample into one module
def main(args):
	print (args['-config'])
	outfile = args['-out']
	config = json2.loadf(args['-config'])
	xml_validator = XMLValidator(config["sra"]["experiment"])
	ihec_validators = cmn.safedict([(schema["version"] ,  JsonSchema(schema["schema"], args, version=schema["version"])) for schema in config["ihec"]["experiment"]])

	objtype = 'EXPERIMENT'
	objset = 'EXPERIMENT_SET'

	validated = list()
	xmllist = args.args()
	nObjs = 0
	expvalidator = dict()
	
	print('\n\n') 
	for e in xmllist:
		sra = SRAParseObjSet.from_file(e)
		nObjs += sra.nOffspring()
		if not sra.xml.getroot().tag == objset:
			utils.sanity_check_fail('__unexpected_xmltype:' + e)
		if not sra.is_valid__xml(xml_validator) or args.has("-not-sra-xml-but-try"):
			utils.sanity_check_fail('__invalid_xml:' + e)
		v = ExperimentValidator(sra, ihec_validators)
		validated.extend(v.is_valid_ihec())
		expvalidator[e] = v

	versioned_xml = ['<{0}>'.format(objset) ]
	for e in validated:
		(version, xml, tag) = e
		sra_versioned = SRAParseObj(xml)
		sra_versioned.add_attribute("VALIDATED_AGAINST_METADATA_SPEC", "{0}/{1}".format(version, objtype))
		versioned_xml.append(sra_versioned.tostring())
	versioned_xml.append('</{0}>'.format(objset))

	

	return validate_main.main(args, versioned_xml, validated, nObjs, expvalidator, xml_validator)
