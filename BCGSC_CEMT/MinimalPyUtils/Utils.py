import sys
import types
import time 
import os
import subprocess
import hashlib
import re
import textwrap
import json
from collections import namedtuple, defaultdict
import threading

class Cmn:
	@staticmethod
	def stripTo(text, tag='|'):
		stripped = [l.lstrip() for l in text.split('\n')]
		return '\n'.join(map(lambda x: (x[1:] if x[0] == tag else x) if x else '', stripped))
			


	@staticmethod
	def executionHome():
		return os.path.dirname(os.path.realpath(sys.argv[0]))

	@staticmethod
	def tuple2hash(e):
		return {field : getattr(e, field) for field in e._fields} 



	@staticmethod
	def tag(arg, tag, delimit='.'):
		oldTags = arg.split(delimit) 
		return delimit.join(oldTags[0:-1] +[tag, oldTags[-1]])

	@staticmethod
	def changeType(arg, newType, delimit='.'):
		oldTags = arg.split(delimit)
		if len(oldTags) == 1: return arg + '.' + newType
		else: return delimit.join(oldTags[0:-1] +[newType])       

	@staticmethod
	def listcontents(f):
		return [x.strip() for x in Cmn.contents(f) if x.strip()]

	@staticmethod
	def wait(debug = True, msg='enter to continue...'):
		Cmn.log(msg, None, None)
		return raw_input('...') if debug else None

	@staticmethod
	def getOrElse(alist, i, orElse=None):
		return alist[i] if len(alist) > i else orElse

	@staticmethod
	def makedir(home, verbose=True):
		try: os.makedirs(home)
		except Exception as err: 
			if verbose: Cmn.log(err)
		return home

	@staticmethod
	def makelink(link, verbose=False):
		ok = True
		home = Cmn.makedir(os.path.dirname(link.linkname), verbose)
		try: 
			os.symlink(link.source, link.linkname)
			if verbose: Cmn.log("#MSG.. {0} >> {1}".format(link.linkname, link.source)) 
		except Exception as e:
			ok = False 
			Cmn.log("#ERR.. {0} >> {1}... {2}".format(link.linkname, link.source, e))
		return ok


	@staticmethod
	def demanduniq(arg):
		if len(arg) == 1: return arg[0]
		elif len(list(set(arg))) != 1: raise Exception('ambiguous: ' + str(arg))
		else: return arg[0]
		raise Exception('unmatched cases (demanduniq): ' + str(arg))


	@staticmethod
	def dirname(arg):
		return os.path.dirname(arg)

	@staticmethod
	def filename(arg):
		return arg.split('/')[-1]
	
	@staticmethod
	def entries(filename, comments=True, comments_tag='#'):
		with open(filename) as readfile:
			if comments: 
				lines = [x for x in map(lambda x: x.strip(), readfile.readlines()) if x]
			else:
				lines = [x for x in map(lambda x: x.strip(), readfile.readlines()) if x and x[0] != comments_tag]
		return lines


	@staticmethod	
	def contents(source, ignore_head=0):
		with open(source, 'r') as readfile:
			for i in range(ignore_head):
				readfile.readline()	
			lines = readfile.readlines()
		return lines 

	@staticmethod	
	def write(target, rows, delimit='\n'):
		with open(target, 'w') as outfile:
			for row in rows:
				outfile.write(str(row) + delimit)
		return target


	@staticmethod
	def file_list(path, keep=lambda x: True, descend=False, verbose=False):
		if verbose:  Cmn.log('in: ' + path, None, False)
		files = ['{0}/{1}'.format(path, filename) for filename in os.listdir(path) if keep('{0}/{1}'.format(path, filename))]
		if not descend: return files
		else: return files + reduce( lambda x, y: x+y, [Cmn.file_list(afile, keep, True, verbose) for afile in files if os.path.isdir(afile)], []) 


	@staticmethod
	def groupby(source, key, transform = None):
		target = defaultdict(list)
		if transform:
			for element in source:
				target[key(element)].append(transform(element))
		else:
			for element in source:
				target[key(element)].append(element)
		
		return dict(target)			

	@staticmethod
	def exists(filename):
		if os.path.exists(filename): return True
		try:
			with open(filename) as test:
				return True
		except IOError: return False

	@staticmethod
	def now():
		current = time.ctime().split()
		return ('-'.join(current[1:3] + [current[-1], current[-2]])).replace(':', '.')	

	@staticmethod
	def groupInto(lines, n):
		pieces = [list() for i in range(n)]
		for i, l in enumerate(lines):
			pieces[i%n].append(l)
		tupled = tuple(pieces)
		assert sum([len(tupled[k]) for k in range(n)]) == len(lines)
		return tupled



