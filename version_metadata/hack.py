from .utils import json2, cmn
import os
import json 

def load_schema(f):
	base = os.path.dirname(os.path.abspath(__file__))
	cwd = os.getcwd()
	expectedpath = 'file:./schemas/json/' 
	newpath = 'file:{0}/../schemas/json/'.format(base)
	schema_json = cmn.fread(f)
	schema_json_fixed = schema_json.replace(expectedpath, newpath)
	return json.loads(schema_json_fixed)
