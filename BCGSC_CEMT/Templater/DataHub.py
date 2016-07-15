from MinimalPyUtils import *
from Config import Config, Parser
#from UCSCTemplate import UCSCTemplate

class DataHub:
	header = ['__header__']
	def __init__(self, config, hubTag, byCentre, annotations, settings, selected=None):
		db = Json.loadf(config)
		datasets = db['datasets']
		self.annotations = annotations
		self.config = {experiment : datasets[experiment] for experiment in datasets if  experiment in selected } if selected else datasets 
		self.samples = db['samples']
		self.empty = not self.config.keys()
		self.hubDescription = db['hub_description']
		self.hubTag = hubTag
		self.settings = settings
		#Cmn.log(settings)
		if not byCentre:
			self.byExperimentType = Cmn.groupby(self.config.keys(), lambda x: Config.assays[self.config[x]["experiment_attributes"]["experiment_type"]])
			self.byCentre = dict()
		else:
			self.experimentType = dict()
			self.byCentre = Cmn.groupby(self.config.keys(), lambda x: self.config[x]['analysis_group'])

	def expandedConfig(self):
		data = dict()
		for exp in self.config:
			data[exp] = self.config[exp]	
			data[exp]['sample_attributes'] = self.samples[data[exp]['sample_id']]
		return data


	def ucsc(self):
		if self.empty: return list()
		else:
			from Template import UCSCTemplate
			templateManager = UCSCTemplate(self.annotations, self.settings)
			tracks = list()
			groupedTracks = self.byCentre if self.byCentre else self.byExperimentType
			for key in groupedTracks:
				containerConfig = {
					'root' : key,
					'label' : key,
					'group' : self.hubTag,
					'visibility' : self.settings['__visibility__'], 
				}
				subtracks = list()
				for library in groupedTracks[key]:
					subtracks.extend(templateManager.subtrackBlocks(self, library, parent = containerConfig['root']))
				tracks.append(templateManager.container(containerConfig))
				tracks.extend(subtracks)
			return tracks




	def washu(self):
		if self.empty: return list()
		else:
			from Template import WashUTemplate
			templateManager = WashUTemplate(self.annotations, self.settings)
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
					subtracks.extend(templateManager.subtrackBlocks(self, library, parent = containerConfig['root']))
				tracks.extend(subtracks)
			#tracks.append(templateManager.tags())
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
			if args.has('-hide'):
				settings['__visibility__'] = 'hide'
			if verbose:
				Cmn.log(annotations)
			hub = DataHub(args['-config'], hubAttributes['tag'], args.has('-by-centre'), annotations, settings, args.args())
			if args.has('-ucsc'):
				tracks = hub.ucsc()
				if args.has('-www'):
					import UCSC
					hubConfig = UCSC.UCSC.defaultConfig(hubAttributes)
					ucsc = UCSC.UCSC(hubConfig, args)
					ucsc.write(args['-www'], tracks)
					return ucsc
				else:
					raise Exception('missing:www')
			elif args.has('-washu'):
				tracks = hub.washu()
				if args.has('-www'):
					import WashU
					washu = WashU.WashU()
					washu.write(args['-www'], tracks)
				return washu
			elif args.has('-tracklist'):
				return hub.expandedConfig()
			else:
				Cmn.log('..unknown option..')
	

if __name__ == '__main__':
	DataHub.main(Clargs.sys())
