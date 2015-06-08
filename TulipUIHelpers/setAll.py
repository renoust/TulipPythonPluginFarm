from tulip import *
import tulipplugins
try:
	import json
	json_available = True
except ImportError:
	json_available = False


class PropertyManipulation(tlp.Algorithm):
	def __init__(self, context):
		tlp.Algorithm.__init__(self, context)
		self.addPropertyParameter("property by list",\
										   "the property to set the value of<br>"\
										   "if nothing is specified, takes the 'property by name' value",\
										   "", False, True, True)
		self.addStringParameter("value",\
										 "the value to set, empty means default value relative to the given property type<br>"\
										 "<b>StringProperty</b>: default is <b>''</b><br>"\
										 "<b>BooleanProperty</b>: default is <b>false</b>, <i>any</i> value is <b>true</b>, false can set by <b>''</b>, <b>0</b>, <b>no</b>, <b>none</b>, <b>null</b> - not case sensitive<br>"\
										 "<b>IntegerProperty</b>: default is <b>0</b>, the string of value must parse int or else it will be default<br>"\
										 "<b>DoubleProperty</b>: default is <b>0.0</b>, the string of value must parse double or else it will be default<br>"\
										 "<b>ColorProperty</b>: default is <b>'(0,0,0,255)'</b>, list values parsing explained below, or else default<br>"\
										 "<b>SizeProperty</b>: default is <b>'(1,1,0)'</b>, list values parsing explained below, or else default<br>"\
										 "<b>LayoutProperty</b>: default is <b>'(0,0,0)'</b>, list values parsing explained below, or else default<br>"\
										 "<b>List values</b> can be expressed with any brackets <b>[]{}()</b>, or none<br>"\
										 "<b>numerical values</b> can be separated space or <b>,</b> or <b>;</b>, or none<br>"\
										 "list <b>size</b> does not matter only what is given is parsed and applied <br>"\
										 "<i>(1,2,3)</i>, <i>[1;2;3]</i>, <i>1 2 3</i> are equivalent, <i>(1)</i> and <i>(1,2,3,4,5)</i> are also valid",
										 "",False, True, False)
		self.addStringCollectionParameter("target", 
													  "the target of the property to set<br>"\
													  "it can be <i>nodes</i>, <i>edges</i>, or <i>both</i> (nodes and edges)", 
													  "nodes;edges;both", False, True, True)
		self.addStringParameter("property by name",
										 "if this parameter is set, it has priority over <i>property by list</i><br>"\
										 "if the name corresponds to a property, then the given property is set<br>"\
										 "otherwise it tries to create a new property under the given <i>type</i> and <i>scope</i>", 
										 "", False, True, False)		
		self.addStringCollectionParameter("creation type", 
											       "the type of property to create, it can be <i>string</i>, <i>boolean</i>, <i>integer</i>, <i>double</i>, <i>layout</i>, <i>size</i>, or <i>color</i>", 
											       "string;boolean;integer;double;layout;size;color", False, True, False)		
		self.addStringCollectionParameter("creation scope", "the scope of property to create (<i>global</i> or <i>local</i>)", "global;local", False, True, False)		

	def check(self):
		if not json_available:
			return (False, "This plugins requires the 'json' python package")

		prop = self.dataSet["property by list"]
		create = self.dataSet["property by name"]
		if prop == None and create == "":
			return (False, "You need to set at least one of the two properties 'create' or 'property'")

		return (True, "")

	#simplyfing the access to the property interface
	def getProp(self, _name, _type, _scope):

			if _type.lower() in ["boolean", "bool"]:
				if _scope == "global":
					return self.graph.getBooleanProperty(_name)
				else:
					return self.graph.getLocalBooleanProperty(_name)

			elif _type.lower() in ["string", "str", "unicode"]:
				if _scope == "global":
					return self.graph.getStringProperty(_name)
				else:
					return self.graph.getLocalStringProperty(_name)

			elif _type.lower() in ["integer", "int", "unsigned int", "long"]:
				if _scope == "global":
					return self.graph.getIntegerProperty(_name)
				else:
					return self.graph.getLocalIntegerProperty(_name)

			elif _type.lower() in ["double", "float"]:
				if _scope == "global":
					return self.graph.getDoubleProperty(_name)
				else:
					return self.graph.getLocalDoubleProperty(_name)

			elif _type.lower() in ["layout", "coord"]:
				if _scope == "global":
					return self.graph.getLayoutProperty(_name)
				else:
					return self.graph.getLocalLayoutProperty(_name)

			elif _type.lower() in ["color"]:
				if _scope == "global":
					return self.graph.getColorProperty(_name)
				else:
					return self.graph.getLocalColorProperty(_name)
					
			elif _type.lower() in ["size"]:
				if _scope == "global":
					return self.graph.getSizeProperty(_name)
				else:
					return self.graph.getLocalSizeProperty(_name)
		

	def run(self):
		prop = self.dataSet["property by list"]
		create = self.dataSet["property by name"]
		scope = self.dataSet["creation scope"].getCurrentString()
		val = self.dataSet["value"]
		newType = self.dataSet["creation type"].getCurrentString()
		target = self.dataSet["target"].getCurrentString()

		toSet = None
		value = None
		
		# if a name in 'property by namee' is specified,
		# we either access it directly or try to create it
		if create != "":
			if self.graph.existProperty(create):
				toSet = self.graph.getProperty(create)
					
			else:	
				try:
					toSet = self.getProp(create,newType,scope)
				except ValueError:
					return False
		# using directly the given property object in 'property by list'
		else:
			toSet = prop
		
		if toSet:

			typeF = toSet.getTypename()
			# setting/parsing the value from the type of the given property
			# if error, set to default values
			
			# for StringProperty
			# sets only the content of the given value
			if typeF == "string":
				value = val
			
			# for BooleanProperty
			# if value is set "", 0, none, false, null, no - not case sensitive
			# sets to False
			# otherwise, sets to True
			elif typeF == "bool":
				value = True
				if val.lower() in ["","0","none", "false", "null", "no"]:
					value = False
			
			# for Integer property
			# if value does not parse to int, sets to 0
			elif typeF == "int":
				value = 0
				try :
					value = int(val)
				except ValueError:
					pass
				 
			# for DoubleProperty
			# if value does not parse to float, sets to0
			elif typeF == "double":
				value = 0.0
				try :
					value = float(val)
				except ValueError:
					pass
			else:

				# List values can be specified in the following formats:
				# '('..')', '['..']', '{'..'}', or without any brackets etc. '..'
				# elements can be separated by ';', ',' or ' '
				# values should be numerical
				# only the min given size is treated (does not if smaller or bigger)
				# [1 2 3], (1;2;3), {1,2,3}, or 1 2 3 are equivalent expressions
				
				if val != "":

					# correcting/converting to json list format				
					# so it can be easily set/parsed, default
					
					val = list(val)
					if val[0] == "(" or val[0] == "{":
						val[0] = "["
					
					if val[0] != "[":
						val.insert(0, "[")
						
					if val[len(val)-1] == ")" or val[len(val)-1] == "}":
						val[len(val)-1] = "]"
					
					if val[len(val)-1] != "]":
						val.append("]")
					
					content = "".join(val[1:len(val)-1])
					content = content.replace(";",",")
					
					if "," not in content:
						content = ",".join(content.split())
						
					val = "["+content+"]"
					val = "".join(val)
				
				# for ColorProperty
				# default is (0, 0, 0, 255)
				# min and max boundaries to [0, 255] are tested	
				if typeF == "color":
					value = [0,0,0,255]
					if val == "":
						val = "[0,0,0,255]"
	
					try:
						color = json.loads(val)
						if type(color) != list:
							raise ValueError
						
						for i in range(min([len(color), 4])):
							c = color[i]
							try:
								value[i] = int(c)
								if value[i] < 0:
									value[i] = 0
								if value[i] > 255:
									value[i] = 255
							except ValueError:
								pass
								
					except ValueError:
						pass
					value = tlp.Color(value[0], value[1], value[2], value[3])
	
		
				# for LayoutProperty
				# default is (0, 0, 0)	
				elif typeF == "layout":
					value = [0,0,0]
					if val == "":
						val = "[0,0,0]"
	
					try:
						coord = json.loads(val)
						if type(coord) != list:
							raise ValueError
						
						for i in range(min([len(coord), 3])):
							c = coord[i]
							try:
								value[i] = float(c)
							except ValueError:
								pass
								
					except ValueError:
						pass
					value = tlp.Coord(value[0], value[1], value[2])
	
				# for SizeProperty
				# default is (1, 1, 0)	
				elif typeF == "size":
					value = [1,1,0]
					if val == "":
						val = "[1,1,0]"
	
					try:
						size = json.loads(val)
						if type(size) != list:
							raise ValueError
						
						for i in range(min([len(size), 3])):
							c = size[i]
							try:
								value[i] = float(c)
							except ValueError:
								pass
						
					except ValueError:
						pass
					
					value = tlp.Size(value[0], value[1], value[2])

		if target in ["nodes", "both"]:
			#print "setting all nodes of ",toSet.getName()," : (",toSet.getTypename(),")",value
			toSet.setAllNodeValue(value)
		if target in ["edges", "both"]:
			#print "setting all edges of ",toSet.getName()," : (",toSet.getTypename(),")",value
			toSet.setAllEdgeValue(value)
			
		return True

tulipplugins.registerPluginOfGroup("PropertyManipulation", "Set all", "Benjamin Renoust", "01/05/2015", "Set values for all nodes/edges of a given property", "1.0", "Property Manipulation")
