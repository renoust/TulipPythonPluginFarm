from tulip import *
import tulipplugins

class FilterCCbySize(tlp.Algorithm):
	def __init__(self, context):
		tlp.Algorithm.__init__(self, context)
		self.addIntegerParameter("size", "the degree we want to compare with", "5", True)
		self.addBooleanParameter("delete", "delete the nodes", "false", False)
		self.addStringCollectionParameter("operator", "the comparison operator (d op length)", "<;<=;==;!=;>;>=;",True)

	def check(self):
		return (True, "")

	def run(self):
		size = self.dataSet["size"]
		delete = self.dataSet["delete"]
		operator = self.dataSet["operator"].getCurrentString()
		
		selectedCC = []
		ccList = tlp.ConnectedTest.computeConnectedComponents(self.graph)
		for cc in ccList:
			
			d = len(cc)

			if operator == ">":
				if d > size:
					selectedCC.append(cc)

			if operator == ">=":
				if d >= size:
					selectedCC.append(cc)
				
			if operator == "<":
				if d < size:
					selectedCC.append(cc)

			if operator == "<=":
				if d <= size:
					selectedCC.append(cc)

			if operator == "==":
				if d == size:
					selectedCC.append(cc)

			if operator == "!=":
				if d != size:
					selectedCC.append(cc)
					
		if delete:
			for cc in selectedCC:
				graph.delNodes(cc)
		else:
			vS = self.graph["viewSelection"]
			for cc in selectedCC:
				for n in cc:
					vS[n] = True
		return True

# The line below does the magic to register the plugin to the plugin database
# and updates the GUI to make it accessible through the menus.
tulipplugins.registerPluginOfGroup("FilterCCbySize", "Filter Connected Components by Size", "Benjamin Renoust", "27/05/2015", "Filter Connected Components by Size", "1.0", "Filter")
