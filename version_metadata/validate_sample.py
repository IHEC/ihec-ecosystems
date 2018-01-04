from sraparse import SRAParseObjSet, SRAParseObj,  XMLValidator
from utils import cmn, json2, logger
from validate_json import JsonSchema


class Validator:
	def normalize_tags(self, hashed):
		fix_tag_names =  { self.normalize(k) :v for k, v in hashed.items()}	
		uniq_values = {k :cmn.demanduniq(v) for k, v in fix_tag_names.items()}
		#uniq_values['biomaterial_type'] = uniq_values['biomaterial_type'].lower().replace(' ', '_')
		try:
			age = int(uniq_values['donor_age'])
			age = min(age, 89)
			uniq_values['donor_age'] = age
			
		except Exception as err:
			print '{0}!!!'.format(err) + json2.pretty(uniq_values)
		return uniq_values

	def __init__(self, sra, validators):
		self.validators = validators
		self.normalize = lambda t: t.lower().replace(' ', '_')
		self.sra = sra
		self.xmljson = self.sra.obj_xmljson()
		for (xml, attrs) in self.xmljson:
			attrs['attributes'] = self.normalize_tags(attrs['attributes'])
	
	def is_valid_ihec(self):
		validated = list()
		for (xml, attrs) in self.xmljson:
			version = self.latest_valid_version(attrs)
			if version:
				validated.append((version, xml))
				print '#', version
		return validated

	def latest_valid_version(self, attributes):
		attrs = attributes['attributes']
		for version in self.validators:
			validator = self.validators[version]
			valid = validator.validate(attrs)
			print attrs.keys()
			logger("# is valid ihec spec:{0} {1} [{2}]".format(valid, version, attributes['title']))
			if valid:
				return version
		return None

				
def main(args):
	print args['-config']
	config = json2.loadf(args['-config'])
	xml_validator = XMLValidator(config["sra"]["sample"])
	ihec_validators = {version :  JsonSchema(config["ihec"]["sample"][version]) for version in config["ihec"]["sample"]}
	
	validated = list()
	xmllist = args.args()
	for e in xmllist:
		sra = SRAParseObjSet.from_file(e)
		assert sra.is_valid__xml(xml_validator)
		v = Validator(sra, ihec_validators)
		validated.extend(v.is_valid_ihec())

	

	(version, xml) = validated[0]
	s = SRAParseObj(xml)
	s.add_attribute("whoa", "meh")
	#print xml.text, dir(xml), type(xml)
	print 'ok'
	print s.tostring()



