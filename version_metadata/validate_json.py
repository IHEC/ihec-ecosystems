from utils import json2, cmn, logger
import jsonschema
import os

class JsonSchema:
	def __init__(self, schema_file, verbose = True):
		self.f = schema_file
		self.errs = list()
		self.now  = cmn.now()
		self.verbose = verbose
		self.schema = json2.loadf(self.f)
		self.base = os.path.dirname(os.path.abspath(__file__))
		expectedpath = 'file:schema/'
		newpath = 'file:{0}/json_schema/'.format(self.base) 
		for x in self.schema['allOf']:
			for e in x['anyOf']:
				if '$ref' in e:
					assert e['$ref'].startswith(expectedpath)
					e['$ref'] = newpath +  e['$ref'][len(expectedpath):]
					schemafile = e['$ref'].split(':')[-1].split('#')[0]
					if not cmn.fexists(schemafile):
						logger('#err ...schema file {0} not found\n'.format(schemafile))
				#else:
				#	logger('#using: {0}\n'.format(schemafile))

	def errlog(self, i, tag):
		if not tag:
			return './errs.{0}.{1}.log'.format(i, self.now)
		else:
			return './errs.{0}.{1}.{2}.log'.format(i, tag, self.now)


	def validate(self, jsonObj, tag=None):
		try:
			# jsonschema.validate(jsonObj, self.schema, format_checker=jsonschema.FormatChecker())
			jsonschema.validate(jsonObj, self.schema, format_checker=jsonschema.FormatChecker())
			return True
		except jsonschema.ValidationError as err:
			if self.verbose:
				self.errs.append(err)
				logfile = self.errlog(len(self.errs), tag)
				with open(logfile, "w") as errs:
					errs.write(str(err))
				logger('#__validationFailuresFound: see {0}\n'.format(logfile))
			return False
				


