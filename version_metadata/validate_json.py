from utils import json2, cmn, logger
import jsonschema
import os
import string


class Sanitizer:
	def __init__(self):
		pass
	def filter_alphan(self, t, additional):
		return filter(lambda x: x.lower() in string.ascii_lowercase or x in additional, t)
	


class JsonSchema:
	def fixfilebase(self, f):
		assert f.startswith(self.expectedpath), [f, self.expectedpath]
		f = self.newpath + f[len(self.expectedpath):]
		schemafile = f.split(':')[-1].split('#')[0]
		if not cmn.fexists(schemafile):
			 logger('#err ...schema file {0} not found\n'.format(schemafile))
		return f

	def obj_id(self, e):
		try:
			idblock = e.get('@idblock', dict())
			tags = [idblock[k]  for k in ['alias', 'refname', 'accession'] if k in idblock]
			return 'unknown' if not tags else self.sanitizer.filter_alphan('.'.join(tags), '.-_') 
		except Exception as e:
			logger('#__couldNotExactId__:{0}\n'.format(e ))
			return 'unknown'

	def __init__(self, schema_file, config, tag = None, verbose = True):
		self.sanitizer = Sanitizer()
		if not tag:
			tag = cmn.basename(schema_file).split('.')[0]
		self.tag = tag
		self.errdir = '.'
		#if not config.has('-dbg'):
		#	try: os.mkdir("./errlog")
		#	except: pass
		#	self.errdir = "./errlog"
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
					e['$ref'] = self.fixfilebase(e['$ref'])



	def errlog(self, i, tag):
		if not tag:
			return '{3}/errs.{2}.{0}.{1}.log'.format(i, self.now, self.tag, self.errdir)
		else:
			return '{4}/errs.{3}.{0}.{1}.{2}.log'.format(i, tag, self.now, self.tag, self.errdir)


	def validate(self, jsonObj, details):
		try:
			jsonschema.validate(jsonObj, self.schema, format_checker=jsonschema.FormatChecker())
			return True
		except jsonschema.ValidationError as err:
			if self.verbose:
				self.errs.append(err)
				logfile = self.errlog(len(self.errs),  self.obj_id(details))
				with open(logfile, "w") as errs:
					context_size = len(err.context)
					if context_size > 0:
						errs.write('Multiple sub-schemas can apply. This is what prevents successful validation in each:\n')
						prev_schema = -1
						for suberror in sorted(err.context, key=lambda e: e.schema_path):
							schema_index = suberror.schema_path[0]
							if prev_schema < schema_index:
								errs.write('Schema %d:\n' % (schema_index + 1))
								prev_schema = schema_index
							errs.write('  %s\n' % (suberror.message))
					else:
						errs.write(err.message)

				logger('#__validationFailuresFound: see {0}\n'.format(logfile))
			return False
				


