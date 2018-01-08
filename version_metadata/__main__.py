from config import Config
from utils import cmn, json2

import validate_sample
import validate_experiment


def main(args):
	if not args.has('-config'):
		args.add_key('-config',  "./config.json")
	print args.keys
	if args.has("-test-sample"):
		testargs = ["./examples/samples.xml", "-config:{0}".format(args['-config']), "-out:./examples/samples.versioned.xml"]
		validate_sample.main(Config(testargs))
	elif args.has("-sample"):
		validate_sample.main(args)
	elif args.has("-experiment"):
		raise NotImplementedError("__ExperimentSchemasUnavailable__")
	else:
		raise NotImplementedError("...")
	
if __name__ == '__main__':
	main(Config.sys())


