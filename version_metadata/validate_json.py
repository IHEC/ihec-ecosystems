from utils import json2, cmn, logger
import jsonschema
import os

class JsonSchema:
	def fixfilebase(self, f):
		assert f.startswith(self.expectedpath)
		f = self.newpath + f[len(self.expectedpath):]
		schemafile = f.split(':')[-1].split('#')[0]
		if not cmn.fexists(schemafile):
			 logger('#err ...schema file {0} not found\n'.format(schemafile))
		return f

	def obj_id(self, e):
		try:
			idblock = e.get('@idblock', dict())
			tags = [idblock[k]  for k in ['alias', 'refname', 'accession'] if k in idblock]
			return 'unknown' if not tags else '.'.join(tags)
		except Exception as e:
			logger('#__couldNotExactId__:{0}\n'.format(e ))
			return 'unknown'

	def __init__(self, schema_file, tag = None, verbose = True):
		if not tag:
			tag = cmn.basename(schema_file).split('.')[0]
		self.tag = tag
		self.errdir = '.'
		self.f = schema_file
		self.errs = list()
		self.now  = cmn.now()
		self.verbose = verbose
		self.schema = json2.loadf(self.f)
		self.base = os.path.dirname(os.path.abspath(__file__))
		self.expectedpath = 'file:schema/'
		self.newpath = 'file:{0}/json_schema/'.format(self.base) 
		for e in self.schema.get('anyOf', list()):
			if '$ref' in e:
				e['$ref'] = self.fixfilebase(e['$ref'])

		for x in self.schema.get('allOf', dict()):
			for e in x['anyOf']:
				if '$ref' in e:
					e['$ref'] = self.fixfilebase('$ref')



	def errlog(self, i, tag):
		if not tag:
			return '{3}/errs.{2}.{0}.{1}.log'.format(i, self.now, self.tag, self.errdir)
		else:
			return '{4}/errs.{3}.{0}.{1}.{2}.log'.format(i, tag, self.now, self.tag, self.errdir)


	def validate(self, jsonObj, details):
		try:
			# jsonschema.validate(jsonObj, self.schema, format_checker=jsonschema.FormatChecker())
			jsonschema.validate(jsonObj, self.schema, format_checker=jsonschema.FormatChecker())
			return True
		except jsonschema.ValidationError as err:
			if self.verbose:
				self.errs.append(err)
				logfile = self.errlog(len(self.errs),  self.obj_id(details))
				with open(logfile, "w") as errs:
					errs.write(str(err))
				logger('#__validationFailuresFound: see {0}\n'.format(logfile))
			return False
				


