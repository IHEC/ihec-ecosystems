from .utils import json2, cmn
import os
import json 


def warn(*msg):
	print(*msg)

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
			list_get =  lambda a, i : a[i] if i < len(a) else ['prevalidation']
			#assert len(v['errors']) == 2, v['errors']
			error = v['errors'][0]
			return [error + " : " + error_instance for error_instance in list_get(v['errors'],1)]
			
		
	
	for xml in errlog:
		for e in errlog[xml]:
			for k, v in e.items():
				if v.get('error_type', '') in ['__prevalidation__']:
					v['errors'] = clean_prevalidate(v)
				else:
					v['errors'] = [clean_error(x) for x in v['errors']]
	return errlog

def patch_curie_uri(attrs):
	attr_names = list(attrs.keys())
	for e in attr_names:
		
		e_new = ''
		if e.endswith('_uri'):
			e_new = e[0:-len('_uri')]  + '_curie'
		elif e.endswith('_curie'):
			e_new = e[0:-len('_curie')]  + '_uri' 
		
		if e_new:
			if e_new in attrs:
				warn('# __curie_uri_not_patched_as_patch_attr_exists__', e, e_new, attrs[e], attrs[e_new])
			else:
				attrs[e_new] = attrs[e]
	return attrs

			





