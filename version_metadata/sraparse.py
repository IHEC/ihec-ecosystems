from lxml import etree
from collections import defaultdict
from .utils import cmn, json2, logger, NonUniqException

class XMLValidator:
	def __init__(self, xsd):
		self.source = xsd
		self.parsed_xsd = etree.parse(xsd)
		self.xsd = etree.XMLSchema(self.parsed_xsd)
	def validate(self, xml):
		return self.xsd.validate(xml)




class SRAParseObj:
	def __init__(self, xml):
		self.xml = xml
		self.pretty = True
	def add_attribute(self, tag, value):
		obj = self.xml
		objtype = obj.tag
		if not objtype in ['SAMPLE', 'EXPERIMENT']:
			utils.sanity_check_fail('__xml_is_unknown_type:' + objtype)
		attrtag = '{0}_ATTRIBUTES'.format(objtype)
		attribute_list = obj.findall(attrtag)
		attrs = cmn.demanduniq(list(obj.findall(attrtag)))
		attribute_list = attrs.getchildren()
		attribute_list[-1].addnext(self.new_tag_value(objtype, tag, value))

	def new_tag_value(self, objtype, tag, value):
		name = '{0}_ATTRIBUTE'.format(objtype)
		new_attr = etree.Element(name)
		t = etree.SubElement(new_attr, 'TAG')
		v = etree.SubElement(new_attr, 'VALUE')
		t.text = tag
		v.text = value
		return new_attr

	def tostring(self):
		return etree.tostring(self.xml, pretty_print=self.pretty )


class SRAParseObjSet:
	@staticmethod
	def from_file(f):
		xml = etree.parse(f)
		return SRAParseObjSet(xml, f)
	@staticmethod
	def extract_attributes_to_json(args, outfile):
		extracted = list()
		for arg in args:
			attrs = SRAParseObjSet.from_file(arg).attributes()
			print (json2.dumpf( arg + '.extracted.json', attrs))
			extracted.extend(attrs)
		print(json2.dumpf(outfile, extracted))
	def __init__(self, xml, tag):
		self.tag = tag
		self.xml = xml
		self.optional_core_fields = {
			"SAMPLE" :  ['TITLE', './/PRIMARY_ID', './/SUBMITTER_ID', './/TAXON_ID', './/SCIENTIFIC_NAME', './/COMMON_NAME', 'DESCRIPTION'],
			"EXPERIMENT": ['TITLE', './/PRIMARY_ID', './/SUBMITTER_ID',  'DESCRIPTION',  './/LIBRARY_STRATEGY']
		}
		self.expected_root_tags = ['SAMPLE_SET', 'EXPERIMENT_SET']
		self.expected_obj_tags = list(map(lambda x: x[0:-4], self.expected_root_tags))
	def is_valid__xml(self, validator):
		valid = validator.validate(self.xml)
		logger("# xml validates [against:{2}]... {0} [{1}]\n".format(valid, self.tag, validator.source))
		return valid
	def extract_optional(self, obj, tag):
		tag_found = list(obj.findall(tag))	
		if len(tag_found) == 0:
			return []
		else:
			return tag_found
		#tag = cmn.demanduniq(tag_found) if tag_found else default
		return tag
	def extract_additional_experiment_attributes(self, obj, hashed):
		strategy = hashed.get("library_strategy", "" ).strip()
		if not strategy:
			strategy = self.extract_optional(obj, ".//SEQUENCING_LIBRARY_STRATEGY")
			if not strategy or len(strategy) > 1:
				logger("#warn__: cannot parse 'library_strategy' or 'library_sequencing_strategy'..  {0}\n ".format(str(strategy)))
			else:
				logger("#warn__: updated 'library_strategy' with 'library_sequencing_strategy'..  {0}\n ".format(str(strategy[0].text)))
				hashed["library_strategy"] = strategy[0].text.strip()
		return hashed

		
	def extract_from_sra_body(self, obj):
		hashed = dict()
		object_type = obj.tag
		optional_core_fields =  self.optional_core_fields[object_type]
		for k in optional_core_fields:   
			found = self.extract_optional(obj,k)
			key = k.lower().split('/')[-1]
			hashed[key] = cmn.tryuniq(list(map(lambda x: x.text, found))) if found else  "__missing__:{0}/{1}".format(k, found)
		hashed['@idblock'] = {k: obj.attrib[k] for k in obj.attrib}
		if object_type in ['EXPERIMENT']:
			hashed = self.extract_additional_experiment_attributes(obj, hashed)
		return hashed
	def from_sra_main_to_attributes(self, hashed):
		if 'library_strategy' in hashed:
			if 'LIBRARY_STRATEGY' in hashed['attributes'] or 'library_strategy' in hashed['attributes']:
				lib_strat_attr = 'LIBRARY_STRATEGY' if 'LIBRARY_STRATEGY' in hashed['attributes'] else 'library_strategy'
				hashed['attributes']['LIBRARY_STRATEGY_IHEC'] = hashed['attributes'][lib_strat_attr]
				old_lib_start = hashed['attributes'].pop(lib_strat_attr)
				logger("#warn:__library_strategy__ defined in both SRA block and as IHEC attribute:{0}, value pushed into 'LIBRARY_STRATEGY_IHEC'\n".format(old_lib_start))
			hashed['attributes']['LIBRARY_STRATEGY'] = [hashed['library_strategy']]
		#hashed['attributes']['@idblock'] = hashed['@idblock']	
		return hashed
	def parse_attributes_block(self, obj, objtype):
		if not objtype in self.expected_obj_tags: # [objtype, self.expected_obj_tags]
			utils.sanity_check_fail('__unexpected_object_type__:' + objtype)
		attrtag = '{0}_ATTRIBUTES'.format(objtype)
		attributes_found = list(obj.findall(attrtag))
		if len(attributes_found) == 0:
			logger.warn("#__warn__... no attributes block found...\n")
			return dict()
		attrs = cmn.demanduniq(attributes_found)
		attrhash = defaultdict(list)
		for e in attrs.getchildren():
			try:
				tag = cmn.demanduniq(e.findall('TAG')).text
				value = cmn.demanduniq(e.findall('VALUE')).text
				attrhash[tag].append(value)
			except NonUniqException as err:
				logger.warn("#warn... malformed tag value block {0}\n".format(str([e.findall('TAG'), e.findall('VALUE')])) )

		return dict(attrhash)
	def parse(self, obj):
		hashed =  self.extract_from_sra_body(obj)
		logger.debugonly(hashed, obj)
		hashed['attributes'] = self.parse_attributes_block(obj, obj.tag)
		return self.from_sra_main_to_attributes(hashed)
	def obj_xmljson(self):
		root = self.xml.getroot()
		offspring = list(root.getchildren())
		return [(e, self.parse(e)) for e in offspring]
	def attributes(self):
		root = self.xml.getroot()
		root_tag = root.tag
		if not root_tag in self.expected_root_tags:
			utils.sanity_check_fail('__root_tag_not_as_expected__:' + root_tag)
		objtype = root_tag[0:-4]
		offspring = root.getchildren()
		objs = [self.parse(e) for e in offspring]
		return objs
	def nOffspring(self):
		root = self.xml.getroot()
		return len(root.getchildren())


if __name__ == '__main__':
	x = SRAParseObjSet.from_file('samples.092015.xml')
	json2.pp(x.attributes())
