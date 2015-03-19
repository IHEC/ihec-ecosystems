from MinimalPyUtils import *

class Hub:
	def __init__(self, config):
		self.config = config
		self.hub = Cmn.stripTo('''	|hub {hub}
									|shortLabel {shortLabel}
									|longLabel {longLabel}
									|genomesFile {genomes}
									|email {contact}'''.format(**config))
		self.genomes = 'genome {db}\ntrackDb {tracks}'.format(**config)

	def write(self, home, tracks):
		print 'written:' + Cmn.write('{0}/{1}'.format(home, self.config['base']), [self.hub])
		print 'written:' + Cmn.write('{0}/{1}'.format(home, self.config['genomes']), [self.genomes])
		print 'written:' + Cmn.write('{0}/{1}'.format(home, self.config['tracks']), tracks)


	@staticmethod
	def defaultConfig(config, db = 'hg19'):
		timeTag = Cmn.now()
		config.update({
			'genomes' : 'genomes.{0}.gs'.format(timeTag),
			'tracks' : '{1}/tracks.{0}.db'.format(timeTag, db),
			'base' : 'CEMT.{0}.hub'.format(timeTag),
		})
		return config