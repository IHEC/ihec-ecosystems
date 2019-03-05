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
	
	def validate_semantics_stub(self, attrs):
		# flip this switch based on miRNA/smRNA end result
		raise NotImplementedError("__thisShouldBeUnreachable__")
		attributes = attrs['attributes']
		RNA_experiment_types = ["RNA-Seq", "mRNA-Seq", "smRNA-Seq", "total-RNA-Seq"]
		miRNA_experiment_types = ["smRNA-Seq"]
		miRNA_experiment_type =  attributes['experiment_type'] in miRNA_experiment_types
		miRNA_strategy = attributes['library_strategy'] in ['miRNA-Seq']
		if miRNA_experiment_type:
			print miRNA_strategy, [attributes['experiment_type'], attributes['library_strategy'] ] 
			return miRNA_strategy
		else:
			# allow miRNA-Seq library strategy for any RNA-Seq experiment type 
			if miRNA_strategy:
				logger.warn("#warn... experiment type not 'smRNA-Seq', but library strategy is 'miRNA-Seq'\n".format(miRNA_experiment_types))
				if  attributes['experiment_type'] in RNA_experiment_types:
					logger.warn("#warn... semantically okay as experiment_type:{1} is in {0}\n".format(RNA_experiment_types,  attributes['experiment_type']))
				else:
					logger.warn("#warn... will not accept as experiment_type:{1} is not in {0}\n".format(RNA_experiment_types, RNA_experiment_types ))
					return False
			return True

	def validate_semantics(self, attrs):
		attributes = attrs['attributes']
		miRNA_experiment_type =  attributes['experiment_type'] in ['smRNA-Seq'] # abstract all this using a Rule interface... another day
		miRNA_strategy = attributes['library_strategy'] in ['miRNA-Seq']
		validation_status = miRNA_strategy 	if miRNA_experiment_type else not miRNA_strategy
		if not validation_status:
			logger.warn('#warn: __semantic_validation_failed__: smRNA-Seq library strategy if and only if miRNA-Seq experiment type')
		return validation_status
		

# to do: refactor this code along with validate_sample into one module
def main(args):
	print args['-config']
	outfile = args['-out']
	config = json2.loadf(args['-config'])
	xml_validator = XMLValidator(config["sra"]["experiment"])
	ihec_validators = cmn.safedict([(schema["version"] ,  JsonSchema(schema["schema"], args)) for schema in config["ihec"]["experiment"]])

	objtype = 'EXPERIMENT'
	objset = 'EXPERIMENT_SET'

	validated = list()
	xmllist = args.args()
	nObjs = 0
	for e in xmllist:
		sra = SRAParseObjSet.from_file(e)
		nObjs += sra.nOffspring()
		assert sra.xml.getroot().tag == objset, [sra.xml.getroot().tag , objset] 
		assert sra.is_valid__xml(xml_validator) or args.has("-not-sra-xml-but-try")
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
		assert validated_xml_set.is_valid__xml(xml_validator) or args.has("-skip-updated-xml-validation")
		logger('ok\n')
	else:
		logger('..no valid objects found\n')

