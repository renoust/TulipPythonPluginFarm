from tulip import *
import tulipplugins
import math

class FilterEdgesByLength(tlp.Algorithm):
	def __init__(self, context):
		tlp.Algorithm.__init__(self, context)
		self.addFloatParameter("length", "the length in the layout we want to compare with", "10", True)
		self.addBooleanParameter("delete", "delete the edges", "false", False)
		self.addStringCollectionParameter("operator", "the comparison operator (d op length)", ">;>=;<;<=;==;!=",True)
		# you can add parameters to the plugin here through the following syntax
		# self.add<Type>Parameter("<paramName>", "<paramDoc>", "<paramDefaultValue>")
		# (see documentation of class tlp.WithParameter to see what types of parameters are supported)

	def check(self):
		# This method is called before applying the algorithm on the input graph.
		# You can perform some precondition checks here.
		# See comments in the run method to know how to access to the input graph.

		# Must return a tuple (boolean, string). First member indicates if the algorithm can be applied
		# and the second one can be used to provide an error message
		return (True, "")

	def run(self):
		length = self.dataSet["length"]
		delete = self.dataSet["delete"]
		operator = self.dataSet["operator"].getCurrentString()
		
		vL = self.graph["viewLayout"]
		
		
		selectedEdges = []
		for e in self.graph.getEdges():
			pS = vL[self.graph.source(e)]
			pT = vL[self.graph.target(e)]
			
			d = math.sqrt(sum([(pS[x]-pT[x])*(pS[x]-pT[x]) for x in range(3)]))

			if operator == ">":
				if d > length:
					selectedEdges.append(e)

			if operator == ">=":
				if d >= length:
					selectedEdges.append(e)
				
			if operator == "<":
				if d < length:
					selectedEdges.append(e)

			if operator == "<=":
				if d <= length:
					selectedEdges.append(e)

			if operator == "==":
				if d == length:
					selectedEdges.append(e)

			if operator == "!=":
				if d != length:
					selectedEdges.append(e)
					
		if delete:
			graph.delEdges(selectedEdges)
		else:
			vS = self.graph["viewSelection"]
			for e in selectedEdges:
				vS[e] = True

			
		return True

# The line below does the magic to register the plugin to the plugin database
# and updates the GUI to make it accessible through the menus.
tulipplugins.registerPluginOfGroup("FilterEdgesByLength", "Filter Edges by Euclidian Distance", "Benjamin Renoust", "27/05/2015", "Filter edges by length", "1.0", "Filter")
