from tulip import *
import tulipplugins

class CreateMetaGraph(tlp.Algorithm):
	def __init__(self, context):
		tlp.Algorithm.__init__(self, context)

	def check(self):
		return (True, "")

	def run(self):
		
		def createGraphTree(sGraph):
			nodeObject = {}
			nodeObject["graph_id"] = sGraph.getId()
			nodeObject["number_of_nodes"] = sGraph.numberOfNodes()
			nodeObject["number_of_edges"] = sGraph.numberOfEdges()
			attDS = sGraph.getAttributes()
			for k in attDS.getKeys():
				val = attDS[k]
				if type(val) in [str, bool, long, float, tlp.Size, tlp.Coord, tlp.Color]:
					nodeObject[k] = attDS[k]
			
			if sGraph.numberOfSubGraphs() > 0:	
				nodeObject["subgraphs"] = []
				for s in sGraph.getSubGraphs():
					nodeObject["subgraphs"].append(createGraphTree(s))

			return nodeObject
		
		def addNodeFromTreeNode(sGraph, treeNode, parentNode):
			n = sGraph.addNode()
			if parentNode:
				sGraph.addEdge(parentNode, n)
				# I guess it would be useful to include some edge metric computation here
			for k in treeNode:
				if k == "subgraphs":
					continue
				val = treeNode[k]
				if not sGraph.existProperty("att_"+k):
					typeVal = type(val)
					if typeVal == str:
						sGraph.getStringProperty("att_"+k)
					if typeVal == bool:
						sGraph.getBooleanProperty("att_"+k)
					if typeVal == long:
						sGraph.getIntegerProperty("att_"+k)
					if typeVal == float:
						sGraph.getDoubleProperty("att_"+k)
					if typeVal == tlp.Size:
						sGraph.getSizeProperty("att_"+k)
					if typeVal == tlp.Coord:
						sGraph.getLayoutProperty("att_"+k)
					if typeVal == tlp.Color:
						sGraph.getColorProperty("att_"+k)
				
				prop = sGraph.getProperty("att_"+k)
				# we should test the adequation of property types but...
				prop[n] = val
			if 'subgraphs' in treeNode	:
				for g in treeNode["subgraphs"]:
					print "adding a node"
					addNodeFromTreeNode(sGraph, g, n)

				
		#hierarchy = ["subgraphs":createGraphTree(self.graph)]
		hierarchy = createGraphTree(self.graph)
		
		sg = self.graph.getSuperGraph().addSubGraph()
		sg.setName("meta graph of "+self.graph.getName())
		addNodeFromTreeNode(sg, hierarchy, None)
		
		return True

tulipplugins.registerPluginOfGroup("CreateMetaGraph", "Create meta graph", "Benjamin Renoust", "03/05/2015", "Creates a meta graph of a hierarchy starting from the current graph", "1.0", "Misc")
