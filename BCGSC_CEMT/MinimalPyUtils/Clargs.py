from collections import namedtuple
from Utils import Cmn

class Clargs:
	def __init__(self, args=None, system=False):
		if not args: args = list()
		if system:
			import sys
			args = sys.argv[1:]

		keyargs = dict()
		def argtype(x):
			if x.strip()[0] != '-': return 'values'
			else:
				tokens = x.split(':')
				t = len(tokens)
				if t == 2:
					if tokens[0] in keyargs: raise Exception('malformed arguments '+ str(args) )
					else: keyargs[tokens[0]] = tokens[1]
				elif t == 1: return 'flags'
				else: raise Exception('malformed arguments '+ str(x))
		Clarg = namedtuple('Clarg',  ['values', 'keys', 'flags'])
		parsed = Cmn.groupby(args, lambda x: argtype(x))
		self.values, self.keys, self.flags = parsed.get('values', []), keyargs, parsed.get('flags', [])

	def __getitem__(self, k):
		if k in self.keys: return self.keys[k]
		elif k in self.flags: return True
		else:
			raise Exception('__MISSING__')

	
	def get(self, k, defaultValue = None):
		if not defaultValue: return self.keys[k]
		else: return self.keys.get(k, defaultValue)

	def has(self, flag):
		return flag in self.flags or flag in self.keys.keys()

	def opt(self, field):
		return self.keys[field] 

	def filelist(self, field='-file'):
		return self.args("-file")		

	def args(self, field='-args'):
		if field in self.keys: return Cmn.listcontents(self.keys[field])
		else: return self.values

	def contents(self):
		return self.args('-contents')

	def targets(self):
		return self.args('-targets')

	def __str__(self):
		return '\n\t-flags:{0}\n\t-keys:{1}\n\t values:{2}'.format(self.flags, self.keys, self.values)


	def config(self):
		return Clargs.New(keys = self.keys, flags = self.flags) 	

	@staticmethod
	def New(keys=None, values=None, flags=None):
		if not keys: keys ={} 
		if not values: values=[]
		if not flags: flags=[]
		newClarg = Clargs()
		if flags: newClarg.flags.extend(flags)
		if values: newClarg.values.extend(values)
		if keys: newClarg.keys.update(keys)
		return newClarg

	@staticmethod
	def sys():
		return Clargs(system=True) 
