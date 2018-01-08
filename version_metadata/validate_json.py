from utils import json2, cmn, logger
import jsonschema
import os

class JsonSchema:
	def __init__(self, schema_file, verbose = True):
		self.f = schema_file
		self.errs = list()
		self.errfile = './errs.{0}.log'.format(cmn.now())
		self.verbose = verbose
		self.schema = json2.loadf(self.f)
		self.base = os.path.dirname(os.path.abspath(__file__))
		for e in self.schema['anyOf']:
			e['$ref'] = e['$ref'].format(self.base)


	def validate(self, jsonObj):
		try:
			# jsonschema.validate(jsonObj, self.schema, format_checker=jsonschema.FormatChecker())
			jsonschema.validate(jsonObj, self.schema, format_checker=jsonschema.FormatChecker())
			return True
		except jsonschema.ValidationError as err:
			if self.verbose:
				self.errs.append(err)
				logfile = '{0}.{1}'.format(self.errfile, len(self.errs))
				with open(logfile, "w") as errs:
					errs.write(str(err))
				logger('#__validationFailuresFound: see {0}\n'.format(logfile))
			return False
				


