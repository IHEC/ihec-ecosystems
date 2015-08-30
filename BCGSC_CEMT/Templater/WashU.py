from MinimalPyUtils import Cmn, Json

class WashU:
	def __init__(self, randomize=True):
		self.tag = (Cmn.random_tag() + '.'+ Cmn.now()) if randomize else Cmn.now()
		self.hub = None

	def write(self, home, tracks):
		Cmn.log('#[WashU] ignoring bb tracks..' ) 
		bigwigs = [e for e in tracks if not e['url'].strip().split('.')[-1] in ['bb'] ]
		self.hub = Cmn.write('{0}/CEMT.washu{1}.json'.format(home, self.tag), [Json.pretty(bigwigs)])

	def __str__(self):
		return Json.pretty({ 'tag' : self.tag, 'hub' : self.hub }) 
