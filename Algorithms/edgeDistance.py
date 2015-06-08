from tulip import *
import tulipplugins
import math

class EdgeDistance(tlp.DoubleAlgorithm):
	def __init__(self, context):
		tlp.DoubleAlgorithm.__init__(self, context)

	def check(self):
		return (True, "")

	def run(self):
		vL = self.graph["viewLayout"]
		for e in self.graph.getEdges():
			pS = vL[self.graph.source(e)]
			pT = vL[self.graph.target(e)]
			
			d = math.sqrt(sum([(pS[x]-pT[x])*(pS[x]-pT[x]) for x in range(3)]))
			
			self.result[e] = d

		return True

# The line below does the magic to register the plugin to the plugin database
# and updates the GUI to make it accessible through the menus.
tulipplugins.registerPluginOfGroup("EdgeDistance", "Edge Euclidian Distance", "Benjamin Renoust", "27/05/2015", "Computes the edge's Euclidian distance", "1.0", "Edges")
