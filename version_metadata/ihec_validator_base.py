from  .utils import logger
from . import egautils

class IHECJsonValidator(object):
	def __init__(self, validators):
		self.validators = validators
		self.errorlog = list()
		self.semanticlog = list()

	def is_valid_ihec(self):
		validated = list()
		invalid = list()
		for (xml, attrs) in self.xmljson:
			(version, title_sanitized)  = self.latest_valid_spec(attrs)
			try:
				semantics_ok, failed_rules = self.validate_semantics(attrs)
			except Exception as err:
				semantics_ok, failed_rules = False, ['__exception_in_semantic_validation__:' +  str(err)]
			
			if version and semantics_ok:
				validated.append((version, xml, egautils.obj_id(attrs)   ))
				logger("# is valid ihec spec:{0} version:{1} [{2}]\n".format('True', version, title_sanitized))
			else:
				logger("# is valid ihec spec:{0} version:{1} [{2}]\n".format('False', '__invalid__', title_sanitized))
			if version and not semantics_ok:
				logger("# found a valid spec version but failed semantic validation:{2}\n".format('', '', title_sanitized))
			
			self.semanticlog.append({title_sanitized : {'semantics_ok' : semantics_ok, "failed_rules": failed_rules}})

		


		return validated

	def validate_semantics(self, attrs):
		raise NotImplementedError('__mustOverride__')

	def latest_valid_spec(self, attributes):
		attrs = attributes['attributes']
		all_valid_versions = list()
		for version in self.validators:
			validator = self.validators[version]
			print('__checking_against_schema:', version, self.validators[version].f)
			valid, errlog = validator.validate(attrs, details=attributes, schema_version=version)
			title_sanitized =  egautils.obj_id(attributes)  #logger.trystr(attributes['title'])  # .decode('ascii', 'ignore')
			#logger("# is valid ihec spec:{0} version:{1} [{2}]\n".format(valid, version if valid else '__invalid__', title_sanitized  ))
			self.errorlog.append(errlog)
			if valid:
				all_valid_versions.append((version, title_sanitized))
				return (version, title_sanitized)
		return (None, None) if len(all_valid_versions) == 0 else all_valid_versions[0]
		 




def validate():
	return False
