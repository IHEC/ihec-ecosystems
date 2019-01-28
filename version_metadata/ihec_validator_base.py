from utils import logger


class IHECJsonValidator(object):
	def __init__(self, validators):
		self.validators = validators

	def is_valid_ihec(self):
		validated = list()
		for (xml, attrs) in self.xmljson:
			version = self.latest_valid_version(attrs)
			if version and self.validate_semantics(attrs):
				validated.append((version, xml))
		return validated

	def validate_semantics(self, attrs):
		raise NotImplementedError('__mustOverride__')

	def latest_valid_version(self, attributes):
		attrs = attributes['attributes']
		for version in self.validators:
			validator = self.validators[version]
			valid = validator.validate(attrs, details=attributes)
			title_sanitized = logger.trystr(attributes['title'])  # .decode('ascii', 'ignore')
			logger("# is valid ihec spec:{0} version:{1} [{2}]\n".format(valid, version if valid else '__invalid__', title_sanitized  ))
			if valid:
				return version
		return None




def validate():
	return False
