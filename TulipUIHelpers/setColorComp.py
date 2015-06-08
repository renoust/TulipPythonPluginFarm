from tulip import *
import tulipplugins

class SetColorComponent(tlp.ColorAlgorithm):
	def __init__(self, context):
		tlp.ColorAlgorithm.__init__(self, context)
		self.addColorPropertyParameter("Color property","The color property to modify",
										   "viewColor", True, True, False)
										   
		self.addStringCollectionParameter("Component", 
													  "the component of the property to set (<i>alpha</i>, <i>red</i>, <i>green</i>, or <i>blue</i>)",
													  "alpha;red;green;blue", False, True, False)
		self.addIntegerParameter("Value",\
										 "the value to set in [0-255], empty means default is 0",
										 "0",False, True, False)
										 
		self.addStringCollectionParameter("Target", 
													  "the target of the property to set<br>"\
													  "it can be <i>nodes</i>, <i>edges</i>, or <i>both</i> (nodes and edges)", 
													  "nodes;edges;both", False, True, False)

	def check(self):
		return (True, "")

	def run(self):
		cP = self.dataSet["Color property"] 
		componentCoord = self.dataSet["Component"].getCurrentString()

		comp = 3
		if componentCoord == "red":
			comp = 0
		if componentCoord == "green":
			comp = 1
		if componentCoord == "blue":
			comp = 2
			
		val = self.dataSet["Value"]
		if val < 0:
			val = 0
		if val > 255:
			val = 255
			
		target = self.dataSet["Target"].getCurrentString()
		
		for n in self.graph.getNodes():
			if target in ["nodes", "both"]:
				c = cP[n]
				c[comp] = val
				self.result[n] = c
			else:
				self.result[n] = cP[n]

		for e in self.graph.getEdges():
			if target in ["edges", "both"]:
				c = cP[e]
				c[comp] = val
				self.result[e] = c
			else:
				self.result[e] = cP[e]
				
		return True

tulipplugins.registerPluginOfGroup("SetColorComponent", "Set color component", "Benjamin Renoust", "01/05/2015", "Set values on a component (alpha, red, green or blue) for all nodes/edges of a given color property", "1.0", "")
