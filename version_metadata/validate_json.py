from utils import json2
import jsonschema
import os

class JsonSchema:
	def __init__(self, schema_file, verbose = True):
		self.f = schema_file
		self.verbose = verbose
		self.schema = json2.loadf(self.f)
		self.base = os.path.dirname(os.path.abspath(__file__))
		for e in self.schema['anyOf']:
			e['$ref'] = e['$ref'].format(self.base)




	def validate(self, jsonObj):
		try:
			#return jsonschema.validate(jsonObj, self.schema, format_checker=jsonschema.FormatChecker())
			jsonschema.validate(jsonObj, self.schema)
			return True
		except jsonschema.ValidationError as err:
			if self.verbose:
				print err
			return False
				


