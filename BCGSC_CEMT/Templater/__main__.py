from MinimalPyUtils import *
from Config import Config, Parser
from Hub import Hub
from UCSCTemplate import UCSCTemplate

class DataHub:
	defaultAnnotationJson = './Config/annotations.json'
	defaultHubAttributes = './Config/centre.json'
	defaultSettings = './Config/settings.json'

	def __init__(self, config, hubTag, byCentre, annotations, settings):
		self.config = Json.loadf(config)
		self.hubTag = hubTag
		if not byCentre:
			self.byExperimentType = Cmn.groupby(self.config.keys(), lambda x: Config.assays[self.config[x]['experiment']])
			self.byCentre = dict()
		else:
			self.experimentType = dict()
			self.byCentre = Cmn.groupby(self.config.keys(), lambda x: self.config[x]['analysis_group'])

		self.templateManager = UCSCTemplate(annotations, settings)


	def ucsc(self):
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


		


def main(args):
	if args.has('-h'):
		Cmn.log(Cmn.stripTo(
			'''	|usage: ./Templater  -config:<json_hub> -hub-tag:<hub_name_tag> -www:<www_home>
				|	example: ./Templater -config:test.tracks.json -hub:CEMT -www:$WWW
				|	PYTHONPATH must have PyUtils package'''))
	else:
		annotations = Json.loadf(args.get('-annotations', DataHub.defaultAnnotationJson))
		hubAttributes = Json.loadf(args.get('-hub', DataHub.defaultHubAttributes))
		settings = Json.loadf(args.get('-settings', DataHub.defaultSettings))
		Cmn.log(annotations)
		hub = DataHub(args['-config'], hubAttributes['tag'], args.has('-by-centre'), annotations, settings)
		hubConfig = Hub.defaultConfig(hubAttributes)
		tracks = hub.ucsc()
		if args.has('-www'):
			Hub(hubConfig).write(args['-www'], tracks) 
		else:
			for track in tracks:
				Cmn.log(track)

		
		#Cmn.log(hub.templateManager.subgroupSoup)
	

if __name__ == '__main__':
	main(Clargs.sys())