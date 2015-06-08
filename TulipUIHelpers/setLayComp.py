from tulip import *
import tulipplugins

class SetLayoutComponent(tlp.LayoutAlgorithm):
	def __init__(self, context):
		tlp.LayoutAlgorithm.__init__(self, context)
		self.addLayoutPropertyParameter("Layout property","The layout property to modify",
										   "viewLayout", True, True, False)
										   
		self.addStringCollectionParameter("Component", 
													  "the component of the property to set (<i>x</i>, <i>y</i>, or <i>z</i>)",
													  "x;y;z", False, True, False)
		self.addFloatParameter("Value",\
										 "the value to set, empty means default is 0.0",
										 "0.0",False, True, False)
										 
		self.addStringCollectionParameter("Target", 
													  "the target of the property to set<br>"\
													  "it can be <i>nodes</i>, <i>edges</i>, or <i>both</i> (nodes and edges)", 
													  "nodes;edges;both", False, True, False)

	def check(self):
		#lP = self.dataSet["Layout property"] 
		#if not lP \
		#   or not lP.getTypename() == "layout" \
		#   or not self.graph.existProperty(lP.getName()):
		#	return (False, lP.getName()+" is not a valid property (a layout property is required)") 
		return (True, "")

	def run(self):
		lP = self.dataSet["Layout property"] 
		componentCoord = self.dataSet["Component"].getCurrentString()

		comp = 0
		if componentCoord == "y":
			comp = 1
		if componentCoord == "z":
			comp = 2
			
		val = self.dataSet["Value"]
		target = self.dataSet["Target"].getCurrentString()
		
		
		
		for n in self.graph.getNodes():
			if target in ["nodes", "both"]:
				c = lP[n]
				c[comp] = val
				self.result[n] = c
			else:
				self.result[n] = lP[n]

		for e in self.graph.getEdges():
			if target in ["edges", "both"]:
				cList = lP[e]
				if len(cList) > 0:
					for c in cList:
						c[comp] = val
					self.result[e] = cList
				else:
					self.result[e] = lP[e]

				
		return True

tulipplugins.registerPluginOfGroup("SetLayoutComponent", "Set layout component", "Benjamin Renoust", "01/05/2015", "Set values on a component (x, y or z) for all nodes/edges of a given layout property", "1.0", "Misc")
