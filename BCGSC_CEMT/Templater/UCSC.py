from MinimalPyUtils import *

class UCSC:
	def __init__(self, config, randomize=True):
		self.config = config
		if randomize:
			randomized = Cmn.random_tag()
			now = Cmn.now()
			self.config['base'] = self.config['base'] + randomized
			self.config['genomes'] = self.config['genomes'] + randomized	
			self.config['tracks'] = self.config['tracks'] + randomized
			self.config['longLabel'] = '{0}.{1}'.format(self.config['longLabel'], now)	
			self.config['shortLabel'] = '{0} T{1}'.format(self.config['shortLabel'], now.split('-')[-1])

		self.hub = Cmn.stripTo('''	|hub {hub}
									|shortLabel {shortLabel}
									|longLabel {longLabel}
									|genomesFile {genomes}
									|email {contact}'''.format(**config))
		self.genomes = 'genome {db}\ntrackDb {tracks}'.format(**config)

	def __str__(self):
		return Json.pretty([self.basefile, self.genomesfile, self.tracksfile, self.config])

	def write(self, home, tracks):
		self.basefile = Cmn.write('{0}/{1}'.format(home, self.config['base']), [self.hub])
		self.genomesfile = Cmn.write('{0}/{1}'.format(home, self.config['genomes']), [self.genomes])
		self.tracksfile = Cmn.write('{0}/{1}'.format(home, self.config['tracks']), tracks)
		return self.basefile

	@staticmethod
	def defaultConfig(config, db = 'hg19'):
		timeTag = Cmn.now()
		config.update({
			'genomes' : 'genomes.{0}'.format(timeTag),
			'tracks' : '{1}/tracks.{0}'.format(timeTag, db),
			'base' : 'CEMT.{0}'.format(timeTag),
		})
		return config
