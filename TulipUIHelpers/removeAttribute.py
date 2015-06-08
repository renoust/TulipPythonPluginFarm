from tulip import *
import tulipplugins

class RemoveAttribute(tlp.Algorithm):
	def __init__(self, context):
		tlp.Algorithm.__init__(self, context)
		self.addStringParameter("attribute name",
										 "if the name corresponds to an exisiting attribute, deletes it",
										 "", True, True, False)		

	def check(self):
		name = self.dataSet["attribute name"]
		attList = self.graph.getAttributes().getKeys()
		if not name:
			return (False, "'Attribute name' should be set! Possible values are:\n  "+"; ".join(attList))
		if not self.graph.attributeExist(name):
			return (False, "Attribute: '"+name+"' does not exist! Possible values are:\n  "+"; ".join(attList))

		return (True, "")

	def run(self):
		name = self.dataSet["attribute name"]
		self.graph.removeAttribute(name)
		return True

tulipplugins.registerPluginOfGroup("RemoveAttribute", "Remove attribute", "Benjamin Renoust", "03/05/2015", "Remove a graph attribute", "1.0", "Attribute Manipulation")
