from tulip import *
import tulipplugins

class DuplicateAttribute(tlp.Algorithm):
	def __init__(self, context):
		tlp.Algorithm.__init__(self, context)
		self.addStringParameter("attribute source",
										 "copy from this attribute",
										 "", True, True, False)		

		self.addStringParameter("attribute target",
										 "to this attribute"\
										 "the target has to be of same type, or creates it if it does not exist",
										 "", True, True, False)		

	def check(self):
		source = self.dataSet["attribute source"]
		target = self.dataSet["attribute target"]

		attList = self.graph.getAttributes().getKeys()

		if not source:
			return (False, "'Attribute source' should be set! Possible values are:\n  "+"; ".join(attList))

		if not target:
			return (False, "'Attribute target' should be set! Possible values are:\n  "+"; ".join(attList))

		if not self.graph.attributeExist(source):
			return (False, "Attribute: '"+source+"' does not exist! Possible values are:\n  "+"; ".join(attList))
		
		if self.graph.attributeExist(target):
			if type(self.graph.getAttribute(source)) != type(self.graph.getAttribute(target)):
				return (False, "Source: '"+source+"' and target: '"+target+"' must be of the same type, or target must be a new attribute")
				
		return (True, "")

	def run(self):
		source = self.dataSet["attribute source"]
		target = self.dataSet["attribute target"]

		sourceA = self.graph.getAttribute(source)
		if self.graph.attributeExist(target):
			if type(self.graph.getAttribute(source)) != type(self.graph.getAttribute(target)):
				return False
		self.graph.setAttribute(target, sourceA)
		return True

tulipplugins.registerPluginOfGroup("DuplicateAttribute", "Copy/duplicate Attribute", "Benjamin Renoust", "03/05/2015", "Duplicate or copy a graph attribute", "1.0", "Attribute Manipulation")
