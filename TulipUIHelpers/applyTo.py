from tulip import *
import tulipplugins

class ApplyTo(tlp.Algorithm):
	def __init__(self, context):
		tlp.Algorithm.__init__(self, context)
		self.addPropertyParameter("property by list",
										 "if the name corresponds to an exisiting property, deletes it",
										 "", False, True, False)		

		self.addStringParameter("apply(x)",
										 "the code to apply, current element is 'x' and current prop is 'prop'",
										 "", False, True, False)	
	
		self.addStringCollectionParameter("target", 
													  "the target of the property to set<br>"\
													  "it can be <i>nodes</i>, <i>edges</i>, or <i>both</i> (nodes and edges)", 
													  "nodes;edges;both", False, True, False)

		self.addStringCollectionParameter("mode", 
													  "Simple mode automatically sets for each element 'prop[x]='"\
													  "Complex mode only launch code, with 'prop' and 'x' set"\
													  "it can be <i>simple</i>, <i>complex</i>", 
													  "simple;complex", False, True, False)

	def check(self):
		return (True, "")

	def run(self):
		prop = self.dataSet["property by list"]
		code = self.dataSet["apply(x)"]
		target = self.dataSet["target"].getCurrentString()
		mode = self.dataSet["mode"].getCurrentString()
		
		if target in ["both", "nodes"]:
			 for x in self.graph.getNodes():
			 	if mode == "simple":
			 		prop[x] = eval(code)
				elif mode == "complex":
					eval(code)
				print prop[x]

		if target in ["both", "edges"]:
			 for x in self.graph.getNodes():
			 	if mode == "simple":
			 		prop[x] = eval(code)
				elif mode == "complex":
					eval(code)
			 	print prop[x]

		return True

# The line below does the magic to register the plugin to the plugin database
# and updates the GUI to make it accessible through the menus.
tulipplugins.registerPluginOfGroup("ApplyTo", "Apply to each...", "Benjamin", "05/05/2015", "Apply python code to each element", "1.0", "Property Manipulation")
