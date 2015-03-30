from MinimalPyUtils import *
from Config import Config, Parser
from collections import defaultdict

class Template:
	@staticmethod
	def rgb2hex(arg):
		Cmn.log(arg)
		return '#%02x%02x%02x' % (int(arg[0]), int(arg[1]), int(arg[2]))

	none = ['none', 'na', 'n/a']
	@staticmethod
	def sanitize(arg):
		return arg.replace(' ', '_')

	@staticmethod
	def customizable(arg, track_type, annotations):
		biomaterial_type = arg['sample_attributes']['biomaterial_type'].lower().replace(' ', '_')
		if biomaterial_type in ['cell_line']:
			description = Template.sanitize(arg['sample_attributes']['line'])
		else:
			disease_tag = '' if arg['sample_attributes']['disease'].lower() in Template.none else ':{0}'.format(arg['sample_attributes']['disease'])
			if biomaterial_type in ['primary_tissue']:
				description = '{tissue_depot}'.format(**arg['sample_attributes']) + disease_tag
			elif biomaterial_type in ['primary_cell', 'primary_cell_culture']:
				description = '{cell_type}'.format(**arg['sample_attributes']) + disease_tag
			else:
				raise NotImplementedError(biomaterial_type)

		description_sanitized = Template.sanitize(description)

		return {
				'description' : description_sanitized,
				'assay' : Config.assays[arg['experiment']],
				'attributes' : {k: Template.sanitize(arg['sample_attributes'][k]) for k in arg['sample_attributes'] if k in annotations},
				'subgroups' : {
					'analysis_group' : Template.sanitize(arg['analysis_group']),
					'track_type' : Template.sanitize(track_type),
					'source' : description_sanitized,
					'sample_id' : Template.sanitize(arg['sample_attributes']['sample_id']),
					'assay' : Template.sanitize(Config.assays[arg['experiment']]),
				}
			}


class WashUTemplate:
	hubline = '''{filetype}	{bigDataUrl}	{experimentId}__{sampleId}__{description}__{assay}__{trackType}	show	center:{center},sample:{sampleId},assay:{assay}	colorpositive:{color_positive},colornegative:{color_negative},height:{pixels}'''
	def __init__(self, annotations, view):
		self.annotations = annotations
		self.tagSoup = defaultdict(list)
		self.additional_metadata = defaultdict(list)
		self.settings = Config(view)

	def subtrackTemplate(self, arg):
		return WashUTemplate.hubline.format(**arg)

	def tags(self):
		return {
			"type" : "metadata", "vocabulary_set" : {
				"sample" : sorted(list(set(self.tagSoup["sample"]))),
				"assay" : sorted(list(set(self.tagSoup["assay"]))),
				"center" : sorted(list(set(self.tagSoup["center"]))),
			},
			"show_terms": {"sample": sorted(list(set(self.tagSoup["sample"]))), "assay": sorted(list(set(self.tagSoup["assay"]))), "center" : sorted(list(set(self.tagSoup["center"])))}
		}
		#return '\n'.join(['metadata\t{0}\t{1}'.format(k, ','.join(sorted(list(set(self.tagSoup[k]))))) for k in self.tagSoup])

	def subtrackBlocks(self, db, library, parent = None):
		tracks = db[library]
		subtracks = list()
		for track_type in tracks['browser']:
			customizable = Template.customizable(tracks, track_type, self.annotations)
			metadata = { 
						'experimentId' : library,
						'trackType' : track_type,
						'trackTag' : tracks['browser'][track_type]['tag'],
						'bigDataUrl' : tracks['browser'][track_type]['big_data_url'],
						'sampleId' : tracks['sample_attributes']['sample_id'],
						'description' : customizable['description'].replace(':','__'),
						'assay' : customizable['assay'],
						'attributes' : customizable['attributes'],
						'subgroups' : customizable['subgroups'],
						'center' : customizable['subgroups']['analysis_group'],
			}
			if parent: metadata['parent'] = parent
			metadata.update(self.settings.view(metadata['assay'], metadata['trackType']))
			metadata['color_positive'] = Template.rgb2hex(metadata['color'].split(','))
			metadata['color_negative'] = Template.rgb2hex(metadata['color'].split(','))
			metadata['pixels'] = metadata['maxHeightPixels'].split(':')[0]
			self.tagSoup['center'].append(metadata['center'])
			self.tagSoup['sample'].append(metadata['sampleId'])
			self.tagSoup['assay'].append(metadata['assay'])

			subtracks.append({
			    'type':metadata['filetype'],
			    'url':metadata['bigDataUrl'],
			    'name':'{experimentId}__{sampleId}__{description}__{assay}__{trackType}'.format(**metadata),
			    'mode':"show",
			    'colorpositive':Template.rgb2hex(metadata['color'].split(',')),
			    'colornegative':Template.rgb2hex(metadata['color'].split(',')),
			    'height':50,
			    #"metadata" : {"sample":["Sample"],"assay":["Assay"], "center":["Center"]},
			})

			#subtracks.append(self.subtrackTemplate(metadata))
		return subtracks 



class UCSCTemplate(Template):
	def container(self, arg,  ordered_subgroup_keys = None):
		if not  ordered_subgroup_keys: 
			subgroupKeys = ['source', 'sample_id', 'assay', 'track_type', 'analysis_group']
		else: 
			subgroupKeys =  ordered_subgroup_keys
		template = Cmn.stripTo('''	|track {root}
						|compositeTrack on
						|visibility {visibility}
						|priority 1.0
						|shortLabel {root}
						|longLabel {group}:{label}
						|{subgroupSoup}
						|dimensions dimX=assay dimY=source dimA=track_type dimB=analysis_group dimC=sample_id
						|sortOrder {sortOrder}
						|filterComposite dimA dimB dimC
						|dragAndDrop subTracks
						|type bigWig\n''')
		#Cmn.log(arg)
		arg['subgroupSoup'] = self.subgroup_soup(arg['root'], subgroupKeys)
		arg['sortOrder'] = ' '.join('{0}=+'.format(k) for k in subgroupKeys) 
		#Cmn.log(str(arg['subgroupSoup']))
		return template.format(**arg)



	def annotate(self, arg):
		self.additional_metadata[arg['parent']].append(arg['attributes']) 
		return ' '.join(['{0}={1}'.format(k, arg['attributes'][k]) for k in arg['attributes']])

	def subgroups(self, arg):
		#Cmn.log(arg)
		self.subgroupSoup[arg['parent']].append(arg['subgroups'])
		return ' '.join([ '{0}={1}'.format(k, v) for k, v in arg['subgroups'].items()])

	def subgroup_soup(self, container_id, subgroupKeys):
		flattened = [(k, v) for subgroups in self.subgroupSoup[container_id] for (k, v) in subgroups.items()]
		keyed = Cmn.groupby(flattened, key = lambda x: x[0], transform = lambda x: x[1]) 
		assert all(k in keyed for k in subgroupKeys)
		subgroups = ['subGroup{0} {1} {2} {3}'.format(i + 1, k, k.capitalize(), ' '.join('{0}={0}'.format(v) for v in list(set(keyed[k])) ))
			for i, k in enumerate(subgroupKeys)]
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
			customizable = Template.customizable(tracks, track_type, self.annotations)
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

