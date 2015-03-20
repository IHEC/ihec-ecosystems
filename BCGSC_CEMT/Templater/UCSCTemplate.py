from MinimalPyUtils import *
from Config import Config, Parser
from collections import defaultdict

class UCSCTemplate:
	none = ['none', 'na', 'n/a']
	def customizable(self, arg, track_type):
		Cmn.log(arg)
		if arg['sample_attributes']['biomaterial_type'].lower().replace(' ', '_') in ['cell_line']:
			description = UCSCTemplate.sanitize(arg['sample_attributes']['line'])
		elif arg['sample_attributes']['biomaterial_type'].lower().replace(' ', '_') in ['primary_tissue']:
			if arg['sample_attributes']['disease'].lower() in UCSCTemplate.none:
				description = UCSCTemplate.sanitize('{tissue_depot}'.format(**arg['sample_attributes']))
			else:
				description = UCSCTemplate.sanitize('{tissue_depot}:{disease}'.format(**arg['sample_attributes']))
		elif arg['sample_attributes']['biomaterial_type'].lower().replace(' ', '_') in ['primary_cell']:
			if arg['sample_attributes']['disease'] in UCSCTemplate.none:
				description = UCSCTemplate.sanitize('{cell_type}'.format(**arg['sample_attributes']))
			else:
				description = UCSCTemplate.sanitize('{cell_type}:{disease}'.format(**arg['sample_attributes']))
		else:
			raise NotImplementedError(arg['sample_attributes']['biomaterial_type'])
		return {
				'description' : description,
				'assay' : Config.assays[arg['experiment']],
				'attributes' : {k: UCSCTemplate.sanitize(arg['sample_attributes'][k]) for k in arg['sample_attributes'] if k in self.annotations},
				'subgroups' : {
					'analysis_group' : UCSCTemplate.sanitize(arg['analysis_group']),
					'track_type' : UCSCTemplate.sanitize(track_type),
					'source' : description,
					'sample_id' : UCSCTemplate.sanitize(arg['sample_attributes']['sample_id']),
					'assay' : UCSCTemplate.sanitize(Config.assays[arg['experiment']]),
				}
			}


	def container(self, arg):
		template = Cmn.stripTo('''	|track {root}
						|compositeTrack on
						|visibility {visibility}
						|priority 1.0
						|shortLabel {root}
						|longLabel {group}:{label}
						|{subgroupSoup}
						|dimensions dimX=assay dimY=source dimA=track_type dimB=analysis_group dimC=sample_id
						|sortOrder analysis_group=+ track_type=+ assay=+ source=+
						|filterComposite dimA dimB dimC
						|dragAndDrop subTracks
						|type bigWig\n''')
		#Cmn.log(arg)
		arg['subgroupSoup'] = self.subgroup_soup(arg['root'])
		#Cmn.log(str(arg['subgroupSoup']))
		return template.format(**arg)

	@staticmethod
	def sanitize(arg):
		return arg.replace(' ', '_')

	def annotate(self, arg):
		self.additional_metadata[arg['parent']].append(arg['attributes']) 
		return ' '.join(['{0}={1}'.format(k, arg['attributes'][k]) for k in arg['attributes']])

	def subgroups(self, arg):
		Cmn.log(arg)
		self.subgroupSoup[arg['parent']].append(arg['subgroups'])
		return ' '.join([ '{0}={1}'.format(k, v) for k, v in arg['subgroups'].items()])

	def subgroup_soup(self, container_id):
		flattened = [(k, v) for subgroups in self.subgroupSoup[container_id] for (k, v) in subgroups.items()]
		keyed = Cmn.groupby(flattened, key = lambda x: x[0], transform = lambda x: x[1]) 
		subgroups = ['subGroup{0} {1} {2} {3}'.format(i + 1, k, k.capitalize(), ' '.join('{0}={0}'.format(v) for v in list(set(keyed[k])) ))
			for i, k in enumerate(keyed)]
		return '\n'.join(subgroups) 

	def subtrackTemplate(self, arg, subgroups = None, tab = '\t'):
		tags = '\n'.join([tab + l  for l in filter(lambda x: x.strip(), [
			'track {experimentId}:{trackTag}',
			'parent {parent} on' if 'parent' in arg else '', 
			'shortLabel {experimentId}:{trackTag}', 
			'longLabel {experimentId}:{sampleId}:{description}:{assay}:{trackTag}', 
			'type {filetype}', 
			'itemRgb on', 
			'visibility {visibility}',
			'maxHeightPixels {maxHeightPixels}',
			'bigDataUrl {bigDataUrl}', 
			'configurable on', 
			'alwaysZero on', 
			'priority 1.0', 
			'autoScale on', 
			'color {color}', 
			'subGroups  {0}'.format(self.subgroups(arg)) if 'parent' in arg else '',
			'metadata {0}'.format(self.annotate(arg)) if 'parent' in arg else ''
		])]) + '\n\n'
		
		return tags.format(**arg)

	
	def __init__(self, annotations, view):
		self.annotations = annotations
		self.subgroupSoup = defaultdict(list)
		self.additional_metadata = defaultdict(list)
		self.settings = Config(view)


	def subtrackBlocks(self, db, library, parent = None):
		tracks = db[library]
		subtracks = list()
		for track_type in tracks['browser']:
			customizable = self.customizable(tracks, track_type)
			metadata = { 
						'experimentId' : library,
						'trackType' : track_type,
						'trackTag' : tracks['browser'][track_type]['tag'],
						'bigDataUrl' : tracks['browser'][track_type]['big_data_url'],
						'sampleId' : tracks['sample_attributes']['sample_id'],
						'description' : customizable['description'],
						'assay' : customizable['assay'],
						'attributes' : customizable['attributes'],
						'subgroups' : customizable['subgroups']
			}
			if parent: metadata['parent'] = parent
			metadata.update(self.settings.view(metadata['assay'], metadata['trackType']))
			subtracks.append(self.subtrackTemplate(metadata))
		return subtracks 

