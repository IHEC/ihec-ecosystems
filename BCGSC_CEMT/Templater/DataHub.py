from MinimalPyUtils import *
from Config import Config, Parser
#from UCSCTemplate import UCSCTemplate

class DataHub:
	def __init__(self, config, hubTag, byCentre, annotations, settings, selected=None):
		db = Json.loadf(config)
		self.annotations = annotations
		self.config = db if not selected else {experiment : db[experiment] for experiment in db if experiment in selected}
		self.hubTag = hubTag
		self.settings = settings
		if not byCentre:
			self.byExperimentType = Cmn.groupby(self.config.keys(), lambda x: Config.assays[self.config[x]['experiment']])
			self.byCentre = dict()
		else:
			self.experimentType = dict()
			self.byCentre = Cmn.groupby(self.config.keys(), lambda x: self.config[x]['analysis_group'])

		#self.templateManager = UCSCTemplate(annotations, settings)



	def ucsc(self):
		from UCSCTemplate import UCSCTemplate
		self.templateManager = UCSCTemplate(self.annotations, self.settings)
		tracks = list()
		groupedTracks = self.byCentre if self.byCentre else self.byExperimentType
		for key in groupedTracks:
			containerConfig = {
				'root' : key,
				'label' : key,
				'group' : self.hubTag,
				'visibility' : 'hide', 
			}
			subtracks = list()
			for library in groupedTracks[key]:
				subtracks.extend(self.templateManager.subtrackBlocks(self.config, library, parent = containerConfig['root']))
			tracks.append(self.templateManager.container(containerConfig))
			tracks.extend(subtracks)
		return tracks


		
	@staticmethod
	def main(args):
		verbose = False
		if args.has('-h'):
			return Cmn.contents('README.md')
		else:
			annotations = Json.loadf(args['-annotations'])
			hubAttributes = Json.loadf(args['-hub'])
			settings = Json.loadf(args['-settings'])
			if verbose: Cmn.log(annotations)
			hub = DataHub(args['-config'], hubAttributes['tag'], args.has('-by-centre'), annotations, settings, args.args())
			if args.has('-ucsc'):
				tracks = hub.ucsc()
				if args.has('-www'):
					import UCSC
					hubConfig = UCSC.UCSC.defaultConfig(hubAttributes)
					ucsc = UCSC.UCSC(hubConfig, randomize = args.has('-randomize'))
					ucsc.write(args['-www'], tracks)
				return ucsc
			elif args.has('-washu'):
				if args.has('-www'):
					import WashU
					washu = WashU.WashU(hub.washu())
					washu.write()
				return washu
			elif args.has('-tracklist'):
				pass
			else:
				Cmn.log('..unknown option..')
	

if __name__ == '__main__':
	DataHub.main(Clargs.sys())
