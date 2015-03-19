import json
from collections import defaultdict

class Json:
	@staticmethod
	def loadf(f):
		with open(f) as target:
			return json.load(target)

	@staticmethod
	def multidictLoadf(target):
		with open(target) as f:
			data = f.read()
		return Json.multidictLoadStr(data)


	@staticmethod
	def multidictLoadStr(data):
		def multidict(ordered_pairs):
			"""Convert duplicate keys values to lists."""
			# read all values into lists
			d = defaultdict(list)
			for k, v in ordered_pairs:
				d[k].append(v)

			# unpack lists that have only 1 item
			for k, v in d.items():
				if len(v) == 1:
					d[k] = v[0]
			return dict(d)

		return json.JSONDecoder(object_pairs_hook=multidict).decode(data)

	@staticmethod
	def pretty(arg):
		return json.dumps(arg, sort_keys=True, indent=4, separators=(',', ': '))

	@staticmethod
	def compact(arg):
		return json.dumps(arg, sort_keys=True)

