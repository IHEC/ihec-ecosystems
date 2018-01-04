from utils import json2
import jsonschema

class JsonSchema:
	def __init__(self, schema_file, verbose = True):
		self.f = schema_file
		self.verbose = verbose
		self.schema = json2.loadf(self.f)
	def validate(self, jsonObj):
		try:
			#return jsonschema.validate(jsonObj, self.schema, format_checker=jsonschema.FormatChecker())
			jsonschema.validate(jsonObj, self.schema)
			return True
		except ValidationError as err:
			if self.verbose:
				print err
			return False
				


