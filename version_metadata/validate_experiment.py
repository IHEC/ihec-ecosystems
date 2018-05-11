from sraparse import SRAParseObjSet, SRAParseObj,  XMLValidator
from utils import cmn, json2, logger
from validate_json import JsonSchema
from ihec_validator_base import  IHECJsonValidator



class ExperimentValidator(IHECJsonValidator):
	def normalize_tags(self, hashed):
		fix_tag_names =  { self.normalize(k) :v for k, v in hashed.items()}
		return {k :cmn.tryuniq(v) for k, v in fix_tag_names.items()}

	def __init__(self, sra, validators):
		super(ExperimentValidator, self).__init__(validators)	
		self.validators = validators
		self.normalize = lambda t: t.lower().replace(' ', '_')
		self.sra = sra
		self.xmljson = self.sra.obj_xmljson()
		for (xml, attrs) in self.xmljson:
			attrs['attributes'] = self.normalize_tags(attrs['attributes'])
	

			

# to do: refactor this code along with validate_sample into one module
def main(args):
	print args['-config']
	outfile = args['-out']
	config = json2.loadf(args['-config'])
	xml_validator = XMLValidator(config["sra"]["experiment"])
	ihec_validators = cmn.safedict([(schema["version"] ,  JsonSchema(schema["schema"])) for schema in config["ihec"]["experiment"]])

	objtype = 'EXPERIMENT'
	objset = 'EXPERIMENT_SET'

	validated = list()
	xmllist = args.args()
	nObjs = 0
	for e in xmllist:
		sra = SRAParseObjSet.from_file(e)
		nObjs += sra.nOffspring()
		assert sra.xml.getroot().tag == objset, [sra.xml.getroot().tag , objset] 
		assert sra.is_valid__xml(xml_validator)
		v = ExperimentValidator(sra, ihec_validators)
		validated.extend(v.is_valid_ihec())

	versioned_xml = ['<{0}>'.format(objset) ]
	for e in validated:
		(version, xml) = e
		sra_versioned = SRAParseObj(xml)
		sra_versioned.add_attribute("VALIDATED_AGAINST_METADATA_SPEC", "{0}/{1}".format(version, objtype))
		versioned_xml.append(sra_versioned.tostring())
	versioned_xml.append('</{0}>'.format(objset))


	validated_xml_file = cmn.writel(outfile, versioned_xml)
	print 'written:' + validated_xml_file
	print 'validated:', len(validated)
	print 'failed:', nObjs - len(validated)
	if validated:
		validated_xml_set = SRAParseObjSet.from_file(validated_xml_file)
		assert validated_xml_set.is_valid__xml(xml_validator)
		logger('ok\n')
	else:
		logger('..no valid objects found\n')

