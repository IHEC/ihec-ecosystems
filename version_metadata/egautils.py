import string
import logging
import string
import random

logger = logging.getLogger()



class ObjectID:
	def __init__(self):
		self.index = 1

	def __call__(self, e):
		def filter_alphan(t, additional):
			return ''.join(filter(lambda x: x.lower() in string.ascii_lowercase or x in additional, t))
		try:
			idblock = e.get('@idblock', dict())
			tags = sorted(list(set([idblock[k]  for k in ['alias', 'refname', 'accession'] if k in idblock])))
			if tags:
				return filter_alphan('.'.join(tags), '.-_1234567890')
			else:
				#random_tag = ''.join(random.choice(string.ascii_lowercase) for i in range(10))
				#assigned = '__unknown:{0}.{1}__'.format(random_tag, str(self.index))
				#self.index = self.index + 1
				# really should just err out here.. 
				return "unknown"
		except Exception as e:
			logger.info('#__could_not_exact_id__:{0}\n'.format(e ))
			return '__cannot_understand_id_block__'



obj_id = ObjectID()


def strategy2schema(s):
	def found(x, alist):
		if x in alist: return True
		else:
			return x.lower() in [e.lower() for e in alist]
			
	if found(s, ["DNase-Hypersensitivity", "ATAC-seq", "NOME-Seq"]): return "chromatin_accessibility"
	elif found(s, ["Bisulfite-Seq"]): return "bisulfite-seq"
	elif found(s, ["MeDIP-Seq"]): return "medip-seq"
	elif found(s, ["MRE-Seq"]): return "mre-seq"
	elif found(s, ["RNA-Seq", "miRNA-Seq"]): return "rna-seq"
	elif found(s, ["WGS"]): return "wgs"
	elif s[0:4].lower() in ['chip', 'hist']: return 'chip-seq'
	else:
		return s.lower()

