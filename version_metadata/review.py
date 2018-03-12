from utils import json2, cmn
import config

def objtype(e):
	return cmn.demanduniq(e['attributes']['BIOMATERIAL_TYPE']).lower().replace(' ', '_')

def main(args):
	assert args.has('-sample')
	xmls = args.args()
	ihec = json2.loadf('./json_spec/ihec_spec.json')
	for arg in xmls:
		db = json2.loadf(arg)
		for e in db:
			ot = objtype(e)
			required = ihec[ot]
			missing = [x for x in required if not x in e['attributes']]
			print e['attributes'].get('SAMPLE_ID', '*'), missing
			

if __name__ == '__main__':
	main(config.Config.sys())
