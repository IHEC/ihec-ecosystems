import json
import os 
import sys
import time
from collections import defaultdict

class Utils:
	def __init__(self):
		self.config = dict()
	def fread(self, f):
		with open(f) as infile:
			return infile.read()
	def fentries(self, f):
		with open(f) as infile:
			return [e.strip() for e in infile]
	def writel(self, f, entries, sep='\n'):
		with open(f, "w") as outfile:
			outfile.write(sep.join(entries))
		return f
	def fexists(self, filename):
		if os.path.exists(filename): return True
		try:
			with open(filename) as test:
				return True
		except IOError: return False
	def demanduniq(self, iterable):
		if len(iterable) == 1:
			return iterable[0]
		uniq = set()
		for e in iterable:
			uniq.add(e)
			if size(uniq) > 1:
				raise Exception('#__nonUniqInDemandUniq:' + str(uniq))
		if size(uniq) != 1:
			raise Exception('#__nonUniqInDemandUniq:' + str(uniq))
		return iterable[0]
	def safedict(self, tuples):
		hashed = dict()
		for k, v in tuples:
			assert not k in hashed, '#__repeated__:{0} old:{1} new:{2}'.format(k, hashed[k], v)
			hashed[k] = v
		return hashed
	def now(self):
		current = time.ctime().split()
		return ('-'.join(current[1:3] + [current[-1], current[-2]])).replace(':', '.')




class Json:
	def __init__(self):
		self.multidict = True
		self.sort_keys = True
		self.indent = 4
		self.separators = (',', ': ')
	def loadf(self, f):
		if self.multidict:
			return self.multidictLoadf(f)
		else:
			with open(f) as target:
				return json.load(target)
	def multidictLoadf(self, f):
		with open(f) as target:
			return self.multidictLoadStr(target.read())
	def multidictLoadStr(self, data):
		def multidictParser(pairs):
			d = defaultdict(list)
			for k, v in pairs:
				d[k].append(v)
			return { k: v[0] if len(v) == 1 else v for k, v in d.items()} 
		return json.JSONDecoder(object_pairs_hook=multidictParser).decode(data)
	def pretty(self, arg):
		return json.dumps(arg, sort_keys=self.sort_keys, indent=self.indent, separators=self.separators)
	def pp(self, arg):
		print self.pretty(arg)
		


class Logger:
	def __init__(self):
		pass
	def __call__(self, m):
		sys.stderr.write('{0}'.format(m))
	def warn(self, m):
		self.__call__(m)



logger = Logger()
json2 = Json()
cmn = Utils()






