from MinimalPyUtils import *
from Config import Config, Parser
from collections import defaultdict

class Template:
	@staticmethod
	def extractUrl(m, track_type):
		url_or_urllist = m['browser'][track_type]['big_data_url']
		if isinstance(url_or_urllist, list):
			return url_or_urllist[0]
		else:
			return url_or_urllist

	@staticmethod
	def rgb2hex(arg):
		Cmn.log(arg)
		return '#%02x%02x%02x' % (int(arg[0]), int(arg[1]), int(arg[2]))

	none = ['none', 'na', 'n/a']
	@staticmethod
	def sanitize(arg):
		if not isinstance(arg, basestring):
			arg = str(arg)
			print '#__WARN__:' + arg
		return arg.replace(' ', '_')

	@staticmethod
	def customizable(arg, track_type, sample, sample_source, annotations):
		biomaterial_type = sample['biomaterial_type'].lower().replace(' ', '_')
		if biomaterial_type in ['cell_line']:
			description = Template.sanitize(sample['line'])
		else:
			disease_tag = '' if sample['disease'].lower() in Template.none else ':{0}'.format(sample['disease'])
			if biomaterial_type in ['primary_tissue']:
				description = '{tissue_depot}'.format(**sample) + disease_tag
			elif biomaterial_type in ['primary_cell', 'primary_cell_culture']:
				description = '{cell_type}'.format(**sample) + disease_tag
			else:
				raise NotImplementedError(biomaterial_type)

		description_sanitized = Template.sanitize(description)
		assay = Config.assays[arg['experiment_attributes']['experiment_type']]
		return {
				'analysis_group' : arg['analysis_group'],
				'description' : description_sanitized,
				'assay' : assay,
				'attributes' : {k: Template.sanitize(sample[k]) for k in sample if k in annotations},
				'subgroups' : {
					'analysis_group' : Template.sanitize(arg['analysis_group']),
					'track_type' : Template.sanitize(track_type),
					'source' : description_sanitized,
					'sample_id' : Template.sanitize(sample_source),
					'assay' : Template.sanitize(assay),
				}
			}


class WashUTemplate:
	hubline = '''{filetype}	{bigDataUrl}	{experimentId}__{sampleId}__{description}__{assay}__{trackType}	show	center:{center},sample:{sampleId},assay:{assay}	colorpositive:{color_positive},colornegative:{color_negative},height:{pixels}'''
	def __init__(self, annotations, view):
		self.browser_name = 'washu'
		self.annotations = annotations
		self.tagSoup = defaultdict(list)
		self.additional_metadata = defaultdict(list)
		self.settings = Config(view)
		self.typesToTags = view['tags']
		self.ignore = view['ignore'][self.browser_name]

	def hotpatch(self, arg):
		""" hook for any last minute edits... """
		return arg 


	def subtrackTemplate(self, arg):
		return self.hotpatch(WashUTemplate.hubline.format(**arg))

	def tags(self):
		return {
			"type" : "metadata", "vocabulary_set" : {
				"sample" : sorted(list(set(self.tagSoup["sample"]))),
				"assay" : sorted(list(set(self.tagSoup["assay"]))),
				"center" : sorted(list(set(self.tagSoup["center"]))),
			},
			"show_terms": {"sample": sorted(list(set(self.tagSoup["sample"]))), "assay": sorted(list(set(self.tagSoup["assay"]))), "center" : sorted(list(set(self.tagSoup["center"])))}
		}

	def subtrackBlocks(self, datahub, library, parent = None):
		tracks = datahub.config[library]
		sample_id = tracks['sample_id']
		sample_attributes = datahub.samples[sample_id] 
		subtracks = list()
		for track_type_0 in tracks['browser']:
			if not track_type_0 in self.ignore:
				primary = [e for e in tracks['browser'][track_type_0] if e['primary']][0]
				subtype = primary.get('subtype', '').strip()
				track_type = None # '{0}_{1}'.format(track_type_0, subtype) if subtype else track_type_0
				track_tag = '{0}_{1}'.format(self.typesToTags[track_type_0], subtype) if subtype else self.typesToTags[track_type_0]
				sample_source = '{0}_{1}'.format(sample_id, primary['sample_source']) if primary['sample_source'] != sample_id else sample_id
				customizable = Template.customizable(tracks, track_type_0, sample_attributes, sample_source, self.annotations)
				metadata = { 
							'experimentId' : library,
							'trackType' : track_type_0,
							'trackTag' : track_tag,
							'bigDataUrl' : primary['big_data_url'],
							'sampleId' : sample_source,
							'description' : customizable['description'],
							'assay' : customizable['assay'],
							'attributes' : customizable['attributes'],
							'subgroups' : customizable['subgroups'],
							'analysis_group' : customizable['analysis_group'],
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
				})
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
		arg['subgroupSoup'] = self.subgroup_soup(arg['root'], subgroupKeys)
		arg['sortOrder'] = ' '.join('{0}={1}'.format(k, self.sortOrderBySubgroup.get(k, '-')) for k in subgroupKeys) 
		return self.hotpatch(template.format(**arg))

	def annotate(self, arg):
		self.additional_metadata[arg['parent']].append(arg['attributes']) 
		return ' '.join(['{0}={1}'.format(k, arg['attributes'][k]) for k in arg['attributes']])

	def subgroups(self, arg):
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
			'longLabel {experimentId}:{sampleId}:{description}:{assay}:{trackTag}:{analysis_group}', 
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
			'subGroups {0}'.format(self.subgroups(arg)) if 'parent' in arg else '',
			'metadata {0}'.format(self.annotate(arg)) if 'parent' in arg else ''
		])]) + '\n\n'
		
		return self.hotpatch(tags.format(**arg))
	
	def __init__(self, annotations, view):
		self.browser_name = 'ucsc'
		self.annotations = annotations
		self.subgroupSoup = defaultdict(list)
		self.additional_metadata = defaultdict(list)
		self.settings = Config(view)
		self.typesToTags = view['tags']
		self.ignore = view['ignore'][self.browser_name]
		self.sortOrderBySubgroup = view.get("sorting", dict())

	def subtrackBlocks(self, datahub, library, parent = None):
		tracks = datahub.config[library]
		sample_id = tracks['sample_id']
		sample_attributes = datahub.samples[sample_id] 
		subtracks = list()
		for track_type_0 in tracks['browser']:
			if not track_type_0 in self.ignore:
				primary = [e for e in tracks['browser'][track_type_0] if e['primary']][0]
				subtype = primary.get('subtype', '').strip()
				track_type = None # '{0}_{1}'.format(track_type_0, subtype) if subtype else track_type_0
				#print self.typesToTags
				track_tag = '{0}_{1}'.format(self.typesToTags[track_type_0], subtype) if subtype else self.typesToTags[track_type_0]
				sample_source = '{0}_{1}'.format(sample_id, primary['sample_source']) if not sample_id.startswith(primary['sample_source'])  else sample_id
				customizable = Template.customizable(tracks, track_type_0, sample_attributes, sample_source, self.annotations)
				metadata = { 
							'experimentId' : library,
							'trackType' : track_type_0,
							'trackTag' : track_tag,
							'bigDataUrl' : primary['big_data_url'],
							'sampleId' : sample_source,
							'description' : customizable['description'],
							'assay' : customizable['assay'],
							'attributes' : customizable['attributes'],
							'subgroups' : customizable['subgroups'],
							'analysis_group' : customizable['analysis_group'],
				}
				if parent: metadata['parent'] = parent
				metadata.update(self.settings.view(metadata['assay'], metadata['trackType']))
				subtracks.append(self.subtrackTemplate(metadata))
		return subtracks

	def hotpatch(self, arg):
		""" hook for any last minute edits... """
		return arg 

