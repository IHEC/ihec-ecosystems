from DataHub import DataHub
from MinimalPyUtils import Clargs, Cmn

def path():
	import os
	return os.path.dirname(os.path.abspath(__file__))

def readme():
	readmeFile = path() + '/README.md'
	for l in Cmn.contents(readmeFile):
		print l.strip()
	

def main(args):
	if args.has('-h') or ( not args.has('-ucsc') and not args.has('-washu') ):
		readme()
	else:
		home = path()
		if not args.has('-hub'):
			args.keys['-hub'] = home + '/Config/centre.json'
		if not args.has('-settings'):
			args.keys['-settings'] = home + '/Config/settings.json'
		if not args.has('-annotations'):
			args.keys['-annotations'] = home + '/Config/annotations.json'
		
		print DataHub.main(args)

if __name__ == '__main__':
	main(Clargs.sys())
	
