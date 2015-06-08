from tulip import *
import tulipplugins
try:
	import json
	json_available = True
except ImportError:
	json_available = False

class AddAttribute(tlp.Algorithm):
	def __init__(self, context):
		tlp.Algorithm.__init__(self, context)
				
		self.addStringParameter("attribute name",
										 "if this parameter is set,"\
										 "and if the name corresponds to an exisiting attribute, then the given attribute is set with its own type<br>"\
										 "otherwise it tries to create a new attribute under the given <i>attribute type</i>", 
										 "", True, True, False)		

		self.addStringParameter("attribute value",\
										 "the value to set, empty means default value relative to the given attribute type<br>"\
										 "<b>string</b>: default is <b>''</b><br>"\
										 "<b>boolean</b>: default is <b>false</b>, <i>any</i> value is <b>true</b>, false can set by <b>''</b>, <b>0</b>, <b>no</b>, <b>none</b>, <b>null</b> - not case sensitive<br>"\
										 "<b>integer</b>: default is <b>0</b>, the string of value must parse int or else it will be default<br>"\
										 "<b>double</b>: default is <b>0.0</b>, the string of value must parse double or else it will be default<br>"\
										 "<b>color</b>: default is <b>'(0,0,0,255)'</b>, list values parsing explained below, or else default<br>"\
										 "<b>size</b>: default is <b>'(1,1,0)'</b>, list values parsing explained below, or else default<br>"\
										 "<b>coord</b>: default is <b>'(0,0,0)'</b>, list values parsing explained below, or else default<br>"\
										 "<b>List values</b> can be expressed with any brackets <b>[]{}()</b>, or none<br>"\
										 "<b>numerical values</b> can be separated space or <b>,</b> or <b>;</b>, or none<br>"\
										 "list <b>size</b> does not matter only what is given is parsed and applied <br>"\
										 "<i>(1,2,3)</i>, <i>[1;2;3]</i>, <i>1 2 3</i> are equivalent, <i>(1)</i> and <i>(1,2,3,4,5)</i> are also valid",
										 "",False, True, False)
										 
		self.addStringCollectionParameter("attribute type", 
											       "the type of property to create, it can be <i>string</i>, <i>boolean</i>, <i>integer</i>, <i>double</i>, <i>coord</i>, <i>size</i>, or <i>color</i>"\
											       " warning, <i>size</i> and <i>coord</i> may not be supported", 
											       "string;boolean;integer;double;coord;size;color", False, True, False)		


	def check(self):
		if not json_available:
			return (False, "This plugins requires the 'json' python package")

		if self.dataSet["attribute name"] == "":
			return (False, "you need to set the attribute's name")

		return (True, "")

	def run(self):
		name = self.dataSet["attribute name"]
		val = self.dataSet["attribute value"]
		aType = self.dataSet["attribute type"].getCurrentString()
		
		if not self.graph.attributeExist(name):
			#print "adding a attribute"
			
			default = None
			if aType == "boolean":
				default = False
			elif aType == "integer":
				default = 0
			elif aType == "string":
				default = ""
			elif aType == "double":
				default = 0.0
			elif aType == "coord":
				default = tlp.Coord(0,0,0)
			elif aType == "size":
				default = tlp.Size(1,1,0)
			elif aType == "color":
				default = tlp.Color(0,0,0,255)
				
			#print "default value ",default
			
			if default != None:
				#print "attribute ",name," of type ",aType," with value ",default
				self.graph.setAttribute(name, default)
		
		attList = self.graph.getAttributes()
		#print attList.getKeys()
		try:
			att = attList[name]
		except AttributeError:
			return False
			
			
		typeF = type(att)
		
		#print typeF
		
	
		# setting/parsing the value from the type of the given property
		# if error, set to default values
		
		# for StringProperty
		# sets only the content of the given value
		if typeF == str:
			#print "type is str"
			value = val
		
		# for BooleanProperty
		# if value is set "", 0, none, false, null, no - not case sensitive
		# sets to False
		# otherwise, sets to True
		elif typeF == bool:
			#print "type is bool"
			
			value = True
			if val.lower() in ["","0","none", "false", "null", "no"]:
				value = False
		
		# for Integer property
		# if value does not parse to int, sets to 0
		elif typeF == long:
			#print "type is int"
			value = 0
			try :
				value = int(val)
			except ValueError:
				pass
			 
		# for DoubleProperty
		# if value does not parse to float, sets to0
		elif typeF == float:
			#print "type is float"
			
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
				if typeF == tlp.Color:
					#print "type is color"
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
				elif typeF == tlp.Coord:
					#print "type is coord"
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
				elif typeF == tlp.Size:
					#print "type is Size"
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
				
				#unmanaged type	
				else:
					return False

		self.graph.setAttribute(name, value)
		return True

# The line below does the magic to register the plugin to the plugin database
# and updates the GUI to make it accessible through the menus.
tulipplugins.registerPluginOfGroup("AddAttribute", "Add/edit graph attribute", "Benjamin Renoust", "03/05/2015", "Adds/edit a global attribute of the graph", "1.0", "Attribute Manipulation")
