from .utils import json2, cmn
import os
import json 

def load_schema(f):
	base = os.path.dirname(os.path.abspath(__file__))
	cwd = os.getcwd()
	expectedpath = 'file:../schemas/json/' 
	newpath = 'file:{0}/../schemas/json/'.format(base)
	schema_json = cmn.fread(f)
	schema_json_fixed = schema_json.replace(expectedpath, newpath)
	return json.loads(schema_json_fixed)


def format_errlog(errlog):
	# change errlog here
	def clean_error(e):
		if isinstance(e, list):
			return e
		else:
			return e.strip()

	def clean_prevalidate(v):
		if not isinstance(v['errors'], list): return [v['errors']]
		else:
			assert len(v['errors']) == 2, v['errors']
			error = v['errors'][0]
			return [error + " : " + error_instance for error_instance in v['errors'][1]]
			
		
	
	for xml in errlog:
		for e in errlog[xml]:
			for k, v in e.items():
				if v.get('error_type', '') in ['__prevalidation__']:
					v['errors'] = clean_prevalidate(v)
				else:
					v['errors'] = [clean_error(x) for x in v['errors']]
	return errlog
