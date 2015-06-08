from tulip import *
import tulipplugins

class DuplicateProperty(tlp.Algorithm):
	def __init__(self, context):
		tlp.Algorithm.__init__(self, context)
		self.addPropertyParameter("input property",
										 "copy from this property",
										 "", True, True, False)		

		self.addStringParameter("output property name",
										 "to this property name"\
										 "the target has to be of same type, or creates it if it does not exist",
										 "", True, True, False)		

		self.addStringCollectionParameter("target", 
													  "the target of the property to set<br>"\
													  "it can be <i>nodes</i>, <i>edges</i>, or <i>both</i> (nodes and edges)", 
													  "nodes;edges;both", False, True, False)

		#self.addIntegerParameter("graph source id",
		#								 "to this property name"\
		#								 "the target has to be of same type, or creates it if it does not exist",
		#								 "", True, True, False)	

		self.addIntegerParameter("output graph id",
										 "hte id of the output graph "\
										 "(if not set'-1', the current graph is the output graph)",
										 "-1", False, True, False)	

		self.addStringCollectionParameter("output scope", "the scope of property to copy (<i>global</i> or <i>local</i>)", "global;local", False, True, False)		


	def check(self):
		#source_id = self.dataSet["graph source id"]
		#if source_id == "":
		#	source_id = self.graph.getId()
		#if source_id > 0:
		#	source_graph = self.graph.getRoot().getDescendantGraph(source_id)
		
		#if source_graph == "None":
		#	return (False, "Please specify a valid source graph ID (empty means current graph)")

		target_id = self.dataSet["output graph id"]
		if target_id == -1:
			target_id = self.graph.getId()
		target_graph = self.graph.getRoot()

		if target_id > 0:
			target_graph = self.graph.getRoot().getDescendantGraph(target_id)
		
		
		if target_graph == "None":
			return (False, "Please specify a valid target graph ID (empty means current graph)")

		source_property = self.dataSet["input property"]
		target_property_name = self.dataSet["output property name"]
		
		if target_graph.existProperty(target_property_name):
			target_property = self.graph.getProperty(target_property_name)
			if source_property.getTypename() != target_property.getTypename():
				return (False, "source and target properties have different types: '"+source_property.getTypename()+"' and '"+target_property.getTypename()+"' \nplease change the output property name")
		
		return (True, "")
	
		#simplyfing the access to the property interface
	def getProp(self, _graph, _name, _type, _scope):

			if _type.lower() in ["boolean", "bool"]:
				if _scope == "global":
					return _graph.getBooleanProperty(_name)
				else:
					return _graph.getLocalBooleanProperty(_name)

			elif _type.lower() in ["string", "str", "unicode"]:
				if _scope == "global":
					return _graph.getStringProperty(_name)
				else:
					return _graph.getLocalStringProperty(_name)

			elif _type.lower() in ["integer", "int", "unsigned int", "long"]:
				if _scope == "global":
					return _graph.getIntegerProperty(_name)
				else:
					return _graph.getLocalIntegerProperty(_name)

			elif _type.lower() in ["double", "float"]:
				if _scope == "global":
					return _graph.getDoubleProperty(_name)
				else:
					return _graph.getLocalDoubleProperty(_name)

			elif _type.lower() in ["layout", "coord"]:
				if _scope == "global":
					return _graph.getLayoutProperty(_name)
				else:
					return _graph.getLocalLayoutProperty(_name)

			elif _type.lower() in ["color"]:
				if _scope == "global":
					return _graph.getColorProperty(_name)
				else:
					return _graph.getLocalColorProperty(_name)
					
			elif _type.lower() in ["size"]:
				if _scope == "global":
					return _graph.getSizeProperty(_name)
				else:
					return _graph.getLocalSizeProperty(_name)

	def run(self):
		#source_id = self.dataSet["graph source id"]
		#if source_id == -1:
		#	source_id = self.graph.getId()
		#source_graph = self.graph.getRoot().getDescendantGraph(source_id)

		source_id = self.graph.getId()
		source_graph = self.graph.getRoot()
		if source_id > 0:
			source_graph = self.graph.getRoot().getDescendantGraph(source_id)
		
		target_id = self.dataSet["output graph id"]
		if target_id == -1:
			target_id = self.graph.getId()
		target_graph = self.graph.getRoot()
		if target_id > 0:
			target_graph = self.graph.getRoot().getDescendantGraph(target_id)

		source_property = self.dataSet["input property"]
		#if source_graph.getId() != self.graph.getId():
		#	check for the right property in the right graph
		
		target_property_name = self.dataSet["output property name"]
		target_scope = self.dataSet["output scope"].getCurrentString()
		apply_on = self.dataSet["target"].getCurrentString()
	
		source_type = source_property.getTypename()
		target_property = None
		target_property = self.getProp(target_graph, target_property_name, source_type, target_scope)
		
		#print "the target property: "	,target_property
		
		if apply_on in ["both", "nodes"]:
			for n in target_graph.getNodes():
				if self.graph.isElement(n):
					target_property[n] = source_property[n]
					
		if apply_on in ["both", "edges"]:
			for e in target_graph.getEdges():
				if self.graph.isElement(e):
					target_property[e] = source_property[e]
					
			
		return True

# The line below does the magic to register the plugin to the plugin database
# and updates the GUI to make it accessible through the menus.
tulipplugins.registerPluginOfGroup("DuplicateProperty", "Copy/duplicate Property", "Benjamin Renoust", "05/05/2015", "Duplicate or copy a graph property (also to another graph)", "1.0", "Property Manipulation")
