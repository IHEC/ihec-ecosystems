from DataHub import DataHub
from MinimalPyUtils import Clargs, Cmn

def main(args):
	if args.has('-h'):
		for l in Cmn.contents(Cmn.home() + '/README.md'):
			print l.strip()
	else:
		print DataHub.main(args)



if __name__ == '__main__':
	main(Clargs.sys())
	
