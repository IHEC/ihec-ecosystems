from lxml import etree
from collections import defaultdict
from utils import cmn, json2, logger

class XMLValidator:
	def __init__(self, xsd):
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
		assert objtype in ['SAMPLE', 'EXPERIMENT']
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
	def __init__(self, xml, tag):
		self.tag = tag
		self.xml = xml
		self.expected_root_tags = ['SAMPLE_SET']
		self.expected_obj_tags = map(lambda x: x[0:-4], self.expected_root_tags)
	def is_valid__xml(self, validator):
		valid = validator.validate(self.xml)
		logger("# xml validates... {0} [{1}] ".format(valid, self.tag))
		return valid
	def parse(self, obj):
		objtype = obj.tag
		assert objtype in self.expected_obj_tags
		attrtag = '{0}_ATTRIBUTES'.format(objtype)
		title = cmn.demanduniq(list(obj.findall('TITLE')))
		hashed = {'title' : title.text}
		attrs = cmn.demanduniq(list(obj.findall(attrtag)))
		attrhash = defaultdict(list)
		for e in attrs.getchildren():
			tag = cmn.demanduniq(e.findall('TAG')).text
			value = cmn.demanduniq(e.findall('VALUE')).text
			attrhash[tag].append(value)
		hashed['attributes'] = dict(attrhash)
		return hashed
	def obj_xmljson(self):
		root = self.xml.getroot()
		offspring = root.getchildren()
		return [(e, self.parse(e)) for e in offspring]
	def attributes(self):
		root = self.xml.getroot()
		root_tag = root.tag
		assert root_tag in self.expected_root_tags
		objtype = root_tag[0:-4]
		offspring = root.getchildren()
		objs = [self.parse(e) for e in offspring]
		return objs


if __name__ == '__main__':
	x = SRAParseObjSet.from_file('samples.092015.xml')
	json2.pp(x.attributes())
