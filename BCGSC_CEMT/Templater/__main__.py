from DataHub import DataHub
from MinimalPyUtils import Clargs, Cmn

def main(args):
	if args.has('-h'):
		home = Cmn.home() 
		print 'home:{0}'.format(home)
		for l in Cmn.contents('{0}/README.md'.format(home)):
			print l.strip()
	else:
		print DataHub.main(args)



if __name__ == '__main__':
	main(Clargs.sys())
	
