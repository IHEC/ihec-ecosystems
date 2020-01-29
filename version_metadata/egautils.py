def obj_id(e):
	def filter_alphan(t, additional):
		return ''.join(filter(lambda x: x.lower() in string.ascii_lowercase or x in additional, t))
	try:
		idblock = e.get('@idblock', dict())
		tags = sorted(list(set([idblock[k]  for k in ['alias', 'refname', 'accession'] if k in idblock])))
		return 'unknown' if not tags else filter_alphan('.'.join(tags), '.-_1234567890')
	except Exception as e:
		logger('#__couldNotExactId__:{0}\n'.format(e ))
		return '__unknown'
