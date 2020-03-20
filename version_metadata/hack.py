from .utils import json2, cmn
import os, sys
import json 

def load_schema(f, ):
	base = os.path.dirname(os.path.abspath(__file__))
	cwd = os.getcwd()
	expectedpath = 'file:./schemas/json/' 
	newpath = 'file:{0}/../schemas/json/'.format(base)
	schema_json = cmn.fread(f)
	schema_json_fixed = schema_json.replace(expectedpath, newpath)
	print(newpath, expectedpath)
	assert schema_json_fixed.find(newpath) != -1
	return json.loads(schema_json_fixed)
