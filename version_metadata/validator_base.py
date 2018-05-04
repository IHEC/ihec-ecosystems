from lxml import etree

class XMLValidator:
	def __init__(self, xsd):
		self.parsed_xsd = etree.parse(xsd)
		self.xsd = etree.XMLSchema(self.parsed_xsd)
	def validate(self, xml):
		return self.xsd.validate(xml)

