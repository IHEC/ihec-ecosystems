from utils import json2, cmn
import config
import sraparse
import os 

def objtype(e):
	if 'BIOMATERIAL_TYPE' in e['attributes']:
		return cmn.demanduniq(e['attributes']['BIOMATERIAL_TYPE']).lower().replace(' ', '_')
	elif 'EXPERIMENT_TYPE' in e['attributes']:
		et = cmn.demanduniq(e['attributes']['EXPERIMENT_TYPE']).lower().replace(' ', '_')	
		if et.startswith('histone'):
			et = 'chip-seq'
		elif et.find('input') != -1:
			et = 'chip-seq_input'
		return et
	else:
		return None
def main(args):
	#assert args.has('-sample')
	xmls = args.args()
	schome = os.path.dirname(os.path.realpath(__file__))
	ihec = json2.loadf('{0}/json_spec/ihec_spec.json'.format(schome))
	if args.has('-isxml'):
		loader = lambda x: sraparse.SRAParseObjSet.from_file(x).attributes()	
	else:
		loader = lambda x: json2.loadf(x)

	patches = ihec["patches"]
	for arg in xmls:
		db = loader(arg)
		for e in db:
			ot = objtype(e)
			alias = e.get('title', '__missing_title__')
			required = ihec.get(ot, None)
			if required:
				missing = [x for x in required if not x in e['attributes']]
				missing2 = [x for x in missing if not patches.get(x, '-')  in e['attributes']]
				print alias, ot, missing2, 'XXXX', missing
			else:
				print alias, '__unknown_object_type__', ot

if __name__ == '__main__':
	main(config.Config.sys())
