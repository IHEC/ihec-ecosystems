from config import Config
from utils import cmn, json2, logger

import validate_sample
import validate_experiment



def main(args):
	if not args.has('-config'):
		args.add_key('-config',  "./config.json")

	logger(str([args.keys, args.args()]) + '\n')
	
	if not args.has('-out'):
		logger('#__noOutFileGiven___\n')
		return

	if cmn.fexists(args['-out']) and not args.has('-overwrite-outfile'):
		logger('#__outfile:{0} exists\n'.format(args['-out']))
		return

	try:
		if args.has("-test-sample"):
			testargs = ["./examples/samples.xml", "-config:{0}".format(args['-config']), "-out:./examples/samples.versioned.xml"]
			validate_sample.main(Config(testargs))
		elif args.has("-sample"):
			validate_sample.main(args)
		elif args.has("-experiment"):
			raise NotImplementedError("__ExperimentSchemasUnavailable__")
		else:
			raise NotImplementedError("#__unknownArguments__")
	except Exception as err:
		logger('#__unexpected__\n')
		logger(str(err.message) + '\n')



if __name__ == '__main__':
	main(Config.sys())


