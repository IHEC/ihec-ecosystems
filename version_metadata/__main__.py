from config import Config
from utils import cmn, json2

import validate_sample
#import validate_experiment


def main(args):
	if not args.has('-config'):
		args.add_key('-config',  "./config.json")
	print args.keys
	if args.has("-test-sample"):
		testargs = ["./examples/samples.092015.xml", "-config:{0}".format(args['-config'])]
		validate_sample.main(Config(testargs))
	else:
		raise NotImplementedError("...")
	

if __name__ == '__main__':
	main(Config.sys())


