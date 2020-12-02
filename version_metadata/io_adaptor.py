from .utils import json2, cmn
import os
import json 

def load_schema(f):
	base = os.path.dirname(os.path.abspath(__file__))
	cwd = os.getcwd()
	expectedpath = 'file:../schemas/json/' 
	newpath = 'file:{0}/../schemas/json/'.format(base)
	schema_json = cmn.fread(f, encoding = 'utf-8')
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
			
	
	print(errlog)
	for xml in errlog:
		for e in errlog[xml]:
			for k, v in e.items():
				if v.get('error_type', '') in ['__prevalidation__']:
					v['errors'] = clean_prevalidate(v)
				else:
					v['errors'] = [clean_error(x) for x in v['errors']]
	return errlog








def collectreports(reports):
	collected = dict()
	
	uniqkey = lambda x: cmn.demanduniq(list(x.keys()))
	expectedxmls = None

	for name, report in reports.items():
		if not expectedxmls: expectedxmls = set(list(report.keys()))
		else:
			assert set(list(report.keys())) == expectedxmls, 'cannot collect reports'
		for xml in report:
			if not xml in collected: collected[xml] = dict()
			hashed = cmn.safedict([( uniqkey(record), record[uniqkey(record)] )  for record in report[xml]])
			for k in hashed:
				if not k in collected[xml]: collected[xml][k] = dict()
				assert not name in collected[xml][k]
				collected[xml][k][name] = hashed[k]
	return collected



