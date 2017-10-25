from DataHub import DataHub
from MinimalPyUtils import Clargs, Cmn

def path():
	import os
	return os.path.dirname(os.path.abspath(__file__))

def readme(home):
	readmeFile = '{0}/README.md'.format(home)
	for l in Cmn.contents(readmeFile):
		print l.strip()
	print '#__HOME__:{0}\n\n\n\n'.format(home) 
	

def main(args):
	home = path()
	if not args.has('-hub'):
		args.keys['-hub'] = home + '/Config/centre.json'
	if not args.has('-settings'):
		args.keys['-settings'] = home + '/Config/settings_new_spec.json'
	if not args.has('-annotations'):
		args.keys['-annotations'] = home + '/Config/annotations.json'
	if args.has('-debug'):
		print args
		print '#__HOME__:{0}\n\n\n\n'.format(home)
	elif args.has('-h') or ( not args.has('-ucsc') and not args.has('-washu') ):
		readme(home)
	else:
		print DataHub.main(args)

if __name__ == '__main__':
	main(Clargs.sys())
	
