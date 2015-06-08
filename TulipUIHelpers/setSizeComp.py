from tulip import *
import tulipplugins

class SetSizeComponent(tlp.SizeAlgorithm):
	def __init__(self, context):
		tlp.SizeAlgorithm.__init__(self, context)
		self.addSizePropertyParameter("Size property","The size property to modify",
										   "viewSize", True, True, False)
										   
		self.addStringCollectionParameter("Component", 
													  "the component of the property to set (<i>width</i>, <i>height</i>, or <i>depth</i>)",
													  "width;height;depth", False, True, False)
		self.addFloatParameter("Value",\
										 "the value to set, empty means default is 0.0",
										 "0.0",False, True, False)
										 
		self.addStringCollectionParameter("Target", 
													  "the target of the property to set<br>"\
													  "it can be <i>nodes</i>, <i>edges</i>, or <i>both</i> (nodes and edges)", 
													  "nodes;edges;both", False, True, False)

	def check(self):
		return (True, "")

	def run(self):
		sP = self.dataSet["Size property"] 
		componentCoord = self.dataSet["Component"].getCurrentString()

		comp = 0
		if componentCoord == "height":
			comp = 1
		if componentCoord == "depth":
			comp = 2
			
		val = self.dataSet["Value"]
		target = self.dataSet["Target"].getCurrentString()
		
		for n in self.graph.getNodes():
			if target in ["nodes", "both"]:
				c = sP[n]
				c[comp] = val
				self.result[n] = c
			else:
				self.result[n] = sP[n]

		for e in self.graph.getEdges():
			if target in ["edges", "both"]:
				c = sP[e]
				c[comp] = val
				self.result[e] = c
			else:
				self.result[e] = sP[e]
				
		return True

#tulipplugins.registerPlugin("SetSizeComponent", "Set size component", "", "03/05/2015", "", "1.0")
tulipplugins.registerPluginOfGroup("SetSizeComponent", "Set size component", "Benjamin Renoust", "01/05/2015", "Set values on a component (width, height or depth) for all nodes/edges of a given size property", "1.0", "")
