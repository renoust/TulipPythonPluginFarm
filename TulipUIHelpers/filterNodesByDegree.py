from tulip import *
import tulipplugins

class FilterNodesByDegree(tlp.Algorithm):
	def __init__(self, context):
		tlp.Algorithm.__init__(self, context)
		self.addIntegerParameter("degree", "the degree we want to compare with", "0", True)
		self.addBooleanParameter("delete", "delete the nodes", "false", False)
		self.addStringCollectionParameter("operator", "the comparison operator (d op length)", "==;!=;>;>=;<;<=",True)

	def check(self):
		# This method is called before applying the algorithm on the input graph.
		# You can perform some precondition checks here.
		# See comments in the run method to know how to access to the input graph.

		# Must return a tuple (boolean, string). First member indicates if the algorithm can be applied
		# and the second one can be used to provide an error message
		return (True, "")

	def run(self):
		degree = self.dataSet["degree"]
		delete = self.dataSet["delete"]
		operator = self.dataSet["operator"].getCurrentString()
		
		selectedNodes = []
		for n in self.graph.getNodes():
			
			d = self.graph.deg(n)

			if operator == ">":
				if d > degree:
					selectedNodes.append(n)

			if operator == ">=":
				if d >= degree:
					selectedNodes.append(n)
				
			if operator == "<":
				if d < degree:
					selectedNodes.append(n)

			if operator == "<=":
				if d <= degree:
					selectedNodes.append(n)

			if operator == "==":
				if d == degree:
					selectedNodes.append(n)

			if operator == "!=":
				if d != degree:
					selectedNodes.append(n)
					
		if delete:
			graph.delNodes(selectedNodes)
		else:
			vS = self.graph["viewSelection"]
			for n in selectedNodes:
				vS[n] = True
		return True

# The line below does the magic to register the plugin to the plugin database
# and updates the GUI to make it accessible through the menus.
tulipplugins.registerPluginOfGroup("FilterNodesByDegree", "Filter nodes by degree", "Benjamin Renoust", "27/05/2015", "Filter nodes by degree", "1.0", "Filter")
