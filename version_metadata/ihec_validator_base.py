from  .utils import logger
from . import egautils

class IHECJsonValidator(object):
	def __init__(self, validators):
		self.validators = validators
		self.errorlog = list()

	def is_valid_ihec(self):
		validated = list()
		invalid = list()
		for (xml, attrs) in self.xmljson:
			(version, title_sanitized)  = self.latest_valid_spec(attrs)
			try:
				semantics_ok = self.validate_semantics(attrs)
			except Exception as err:
				semantics_ok = False
			if version and semantics_ok:
				validated.append((version, xml, egautils.obj_id(attrs)   ))
				logger("# is valid ihec spec:{0} version:{1} [{2}]\n".format('True', version, title_sanitized))
			else:
				logger("# is valid ihec spec:{0} version:{1} [{2}]\n".format('False', '__invalid__', title_sanitized))
			if version and not semantics_ok:
				logger("# found a valid spec version but failed semantic validation:{2}\n".format('', '', title_sanitized))
			

				
		return validated

	def validate_semantics(self, attrs):
		raise NotImplementedError('__mustOverride__')

	def latest_valid_spec(self, attributes):
		attrs = attributes['attributes']
		all_valid_versions = list()
		for version in self.validators:
			validator = self.validators[version]
			print('__checking_against_schema:', version, self.validators[version].f, self.validators[version].newpath)
			valid, errlog = validator.validate(attrs, details=attributes, schema_version=version)
			title_sanitized =  egautils.obj_id(attributes)  #logger.trystr(attributes['title'])  # .decode('ascii', 'ignore')
			#logger("# is valid ihec spec:{0} version:{1} [{2}]\n".format(valid, version if valid else '__invalid__', title_sanitized  ))
			self.errorlog.append(errlog)
			if valid:
				all_valid_versions.append((version, title_sanitized))
		return (None, None) if not all_valid_versions else all_valid_versions
		 




def validate():
	return False
