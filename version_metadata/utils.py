import json
import os 
import sys
import time
from collections import defaultdict


def sanity_check_fail(msg):
	print(msg)
	sys.exit(1)


class NonUniqException(Exception):
	def __init__(self, message, iterable):
		self.message = message
		self.iterable = iterable

class Logger:
	def __init__(self):
		self.debug = False # just wrap logging
	def __call__(self, m):
		sys.stderr.write(u'{0}'.format(m))
	def entry(self, m): 
		self.__call__(m)
		self.__call__('\n')
	def warn(self, m):
		self.__call__(m)
	def debugonly(self, *args):
		if self.debug: print(args) 
	def trystr(self, x):
		try:
			# does nothing for python 3 and we no longer support 2...
			return x #unicode(x).encode('utf-8', errors='ignore').strip().decode('ascii', 'ignore')
		except Exception as e:
			self.__call__('#warn... unicode issue... ' + str(e))
			return x


logger = Logger()


class Utils:
	def __init__(self):
		self.config = dict()
		self.encoding = 'utf-8'
	def fread(self, f):
		with open(f) as infile:
			return infile.read()
	def fentries(self, f):
		with open(f) as infile:
			return [e.strip() for e in infile]
	def writel(self, f, entries, sep=b'\n', encoding=None):
		if not encoding: encoding = self.encoding
		assert isinstance(entries, list), ['expected list, found:' , type(entries)]
		with open(f, "wb") as outfile:
			# handle mixed string, unicode lists
			for e in entries:
				if isinstance(e, str):
					outfile.write(e.encode(encoding))
				else:
					outfile.write(e)  #sep.join(entries))
				outfile.write(sep)
		return f
	def dumpf(self, f, data):
		with open(f, "w") as out:
			out.write(data)
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
			if len(uniq) > 1:
				raise NonUniqException('#__nonUniqInDemandUniq:', uniq)
		if len(uniq) != 1:
			raise NonUniqException('#__nonUniqInDemandUniq:' , uniq)
		return iterable[0]
	def tryuniq(self, iterable):
		if len(iterable) == 1:
			return iterable[0]
		uniq = set()
		for e in iterable:
			uniq.add(e)
		uniqlist = list(uniq)
		if len(uniqlist) == 1:
			return uniqlist[0]
		else:
			logger('#__warn__ ... repeated values found where unique expeced... {0}\n'.format(str(uniqlist)))
			return uniqlist
	def safedict(self, tuples):
		hashed = dict()
		for k, v in tuples:
			assert not k in hashed, '#__repeated__:{0} old:{1} new:{2}'.format(k, hashed[k], v)
			hashed[k] = v
		return hashed
	def now(self):
		current = time.ctime().split()
		return ('-'.join(current[1:3] + [current[-1], current[-2]])).replace(':', '.')
	def basename(self, f):
		return os.path.basename(f)

	def getpath(data, ifmissing, *args):
		d = data
		path = list()
		try:
			for e in args:
				path.append(e)
				d = d[e]
			return d
		except Exception as err:
			return ifmissing

class Json:
	def __init__(self):
		self.multidict = True
		self.sort_keys = True
		self.indent = 4
		self.separators = (',', ': ')
	def loadf(self, f):
		try:
			if self.multidict:
				return self.multidictLoadf(f)
			else:
				with open(f) as target:
					return json.load(target)
		except Exception as e:
			print('__failed_at:' , f)
			raise e
	def dumpf(self, f, data):
		stringed = self.pretty(data)
		with open(f, 'w') as outfile:
			outfile.write(stringed)
		return f
	def multidictLoadf(self, f):
		with open(f) as target:
			return self.multidictLoadStr(target.read())
	def loads(self, data):
		return self.multidictLoadStr(data)
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
		print(self.pretty(arg))
		
	def copyobj(self, x):
		return self.multidictLoadStr(self.pretty(x))


json2 = Json()
cmn = Utils()






