from tulip import *
import tulipplugins

class RemoveProperty(tlp.Algorithm):
	def __init__(self, context):
		tlp.Algorithm.__init__(self, context)
		self.addPropertyParameter("property by list",
										 "if the name corresponds to an exisiting property, deletes it",
										 "", False, True, False)		
		self.addStringParameter("property by name",
										 "if the name corresponds to an exisiting property, deletes it",
										 "", False, True, False)	


	def check(self):
		prop = self.dataSet["property by list"]
		name = self.dataSet["property by name"]

		if prop == None and name == "":
			return (False, "At least one of the two properties need to be set")
			
		if name != "":
			if not self.graph.existLocalProperty(name):
				return (False, "Property '"+name+"' does not exist locally")

		if prop != None:
			name = prop.getName()
			if not self.graph.existLocalProperty(name):
				return (False, "Property '"+name+"' does not exist locally")
			
		return (True, "")

	def run(self):
		name = self.dataSet["property by name"]
		if name != "":
			self.graph.delLocalProperty(name)

		else:
			prop = self.dataSet["property by list"]
			self.graph.delLocalProperty(prop.getName())

		return True

tulipplugins.registerPluginOfGroup("RemoveProperty", "Remove local property", "Benjamin Renoust", "05/05/2015", "Removes a property", "1.0", "Property Manipulation")
