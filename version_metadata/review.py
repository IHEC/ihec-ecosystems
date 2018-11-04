from utils import json2, cmn
import config
import sraparse

def objtype(e):
	if 'BIOMATERIAL_TYPE' in e['attributes']:
		return cmn.demanduniq(e['attributes']['BIOMATERIAL_TYPE']).lower().replace(' ', '_')
	elif 'EXPERIMENT_TYPE' in e['attributes']:
		return cmn.demanduniq(e['attributes']['EXPERIMENT_TYPE']).lower().replace(' ', '_')	
	else:
		return None
def main(args):
	#assert args.has('-sample')
	xmls = args.args()
	ihec = json2.loadf('./json_spec/ihec_spec.json')
	if args.has('-isxml'):
		loader = lambda x: sraparse.SRAParseObjSet.from_file(x).attributes()	
	else:
		loader = lambda x: json2.loadf(x)

	for arg in xmls:
		db = loader(arg)
		for e in db:
			ot = objtype(e)
			alias = e.get('title', '__missing_title__')
			required = ihec.get(ot, None)
			if required:
				missing = [x for x in required if not x in e['attributes']]
				print alias, missing, ot
			else:
				print alias, '__unknown_object_type__', ot

if __name__ == '__main__':
	main(config.Config.sys())