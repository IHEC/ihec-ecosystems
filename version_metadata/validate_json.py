from .utils import json2, cmn, logger
import jsonschema
import os
import string
import json
import sys
import random
from .prevalidate import Prevalidate
from . import egautils
from . import io_adaptor 

def verbose_error(schema, obj, tag):
	error_log = list()
	v = jsonschema.Draft7Validator(schema, format_checker=jsonschema.FormatChecker())
	errors = [e for e in v.iter_errors(obj)]
	#error_log.append('__total_errors__:{}'.format(len(errors)))
    
	for error in sorted(errors, key=str):
		#error_log.append('#__validation_error_in__: {2} \n\n# {0}: {1}'.format('.'.join(str(v) for v in error.path), error.message, tag))
		error_log.append('{0} {1}'.format('.'.join(str(v) for v in error.path), error.message, tag))
		if len(error.context) > 0:
			#error_log.append('Multiple sub-schemas can apply. This is the errors for each:')
			prev_schema = -1
			for suberror in sorted(error.context, key=lambda e: e.schema_path):
				schema_index = suberror.schema_path[0]
				if prev_schema < schema_index:
					#error_log.append('{}'.format(schema_index + 1))
					prev_schema = schema_index
				#error_log.append('{}'.format(suberror.message))
		#error_log.append("--------------------------------------------------")
	return error_log





class Sanitizer:
	def __init__(self):
		pass
	def filter_alphan(self, t, additional):
		return ''.join(filter(lambda x: x.lower() in string.ascii_lowercase or x in additional, t))
	


class JsonSchema:
	def fixfilebase(self, f):
		if not f.startswith(self.expectedpath):
			utils.sanity_check_fail('__malformed_jsonschema__')
		f = self.newpath + f[len(self.expectedpath):]
		schemafile = f.split(':')[-1].split('#')[0]
		if not cmn.fexists(schemafile):
			 logger('#err ...schema file {0} not found\n'.format(schemafile))
		return f

	def obj_id(self, e):
		return egautils.obj_id(e)



	def __init__(self, schema_file, config, version, tag = None, verbose = True, draft4schema=False):
		self.version = version
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
		self.schema = io_adaptor.load_schema(self.f) 
		self.base = os.path.dirname(os.path.abspath(__file__))
		self.cwd = os.getcwd()
		if draft4schema:
			raise Exception("__v4_schema_no_longer_supported__")
		else:
			self.schema = io_adaptor.load_schema(self.f)  
		print('#__initialized: {0} {1}\n'.format(self.f, self.version))	
		self.prevalidation = Prevalidate([ json2.copyobj(self.schema)   ],   version) 

	def errlog(self, i, tag):
		if not tag:
			f = '{3}/errs.{2}.{0}.{1}.log'.format(i, self.now, self.tag, self.errdir)
		else:
			f = '{4}/errs.{3}.{0}.{1}.{2}.log'.format(i, tag, self.now, self.tag, self.errdir)
		if not cmn.fexists(f): return f
		for i in range(1000):
			g = f + '.' + ''.join(random.choice(string.ascii_lowercase) for i in range(10)) + '.log'
			if not cmn.fexists(g):
				return g
		raise Exception('__cannot_file_nonexistent_file_starting_with:' +  f)
				
		

	def validate(self, jsonObj, details, schema_version):
		tag = self.obj_id(details)
		prevalidate, errors =  self.prevalidation.prevalidate(jsonObj, tag)
		if prevalidate:
			print('#__prevalidation_passed__', tag, schema_version)
			ok, status =  self.validate_draft7logging(jsonObj, details, schema_version)
		else:
			print('#__prevalidation_failed__', tag, schema_version, '__validation_skipped__')
			ok = False 
			status = {tag : {'error_type' : '__prevalidation__', 'errors' : errors, 'version' : schema_version, "ok":False}}
		#### 
		
		#status[tag]['ok'] = ok
		return ok, status
				


		#return self.validate_defaultlogging(jsonObj, details)

	def validate_draft7logging(self, jsonObj, details, schema_version):
		try:
			#logger.entry('#__errors__')
			jsonschema.Draft7Validator(self.schema, format_checker=jsonschema.FormatChecker()).validate(jsonObj)
			jsonschema.validate(jsonObj, self.schema, format_checker=jsonschema.FormatChecker())
			tag = self.obj_id(details)
			print('#__validates__', tag, schema_version)
			return True, {tag: {'errors' : [], 'ok' : True, 'version' : schema_version}   }
		except jsonschema.ValidationError as err:
			tag = self.obj_id(details)
			errors = verbose_error(self.schema, jsonObj, tag) 
			return False, {tag : {'errors' :  errors,  'error_type' : 'jsonschema',  'ok' : False, 'version': schema_version}}
			
				






