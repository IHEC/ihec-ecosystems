from MinimalPyUtils import Cmn, Json

class WashU:
	def __init__(self, randomize=True):
		self.tag = (Cmn.random_tag() + '.'+ Cmn.now()) if randomize else Cmn.now()

	def write(self, home, tracks):
		return Cmn.write('{0}/CEMT.washu{1}.json'.format(home, self.tag), [Json.pretty(tracks)])