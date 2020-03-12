from .sraparse import SRAParseObjSet, SRAParseObj,  XMLValidator
from .utils import cmn, json2, logger

class ValidatorTemplate:
	def __init__(self, objtype):
		self.nObj = 0
		self.validated = list()
		self.objtype = objtype
		self.objset = self.objtype + '_SET'
		self.validator_log = dict()
		self.versioned_xml = list()
		self.validated = list()


def main(args, versioned_xml, validated, nObjs, validator, xml_validator):
	validated_xml_file = cmn.writel(args['-out'], versioned_xml)
	print ('written:' + validated_xml_file)
	print ('validated:', len(validated))
	print ('failed:', nObjs - len(validated))
	if validated:
		validated_xml_set = SRAParseObjSet.from_file(validated_xml_file)
		assert validated_xml_set.is_valid__xml(xml_validator) or args.has("-skip-updated-xml-validation")
		logger('ok\n')
	else:
		logger('..no valid objects found\n')

	errlog = { e : v.errorlog  for e, v in validator.items()}

	if args.has('-jsonlog'):
		print(json2.dumpf(args['-jsonlog'], errlog))
	else:
		json2.pp(errlog)
	return 
