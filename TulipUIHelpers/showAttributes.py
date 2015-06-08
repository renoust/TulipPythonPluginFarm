from tulip import *
import tulipplugins

try:
	from PyQt4.Qt import *
	pyqt_available = True
	
	class MyPopup(QWidget):
		def __init__(self):
			QWidget.__init__(self)
		
		def paintEvent(self, e):
			dc = QPainter(self)
			dc.drawLine(0, 0, 100, 100)
			dc.drawLine(100, 0, 0, 100)
			
	class MainWindow(QMainWindow):
	    def __init__(self, *args):
	        QMainWindow.__init__(self, *args)
	        self.cw = QWidget(self)
	        self.setCentralWidget(self.cw)
	        self.btn1 = QPushButton("Click me", self.cw)
	        self.btn1.setGeometry(QRect(0, 0, 100, 30))
	        self.connect(self.btn1, SIGNAL("clicked()"), self.doit)
	        self.w = None
	
	    def doit(self):
	        print "Opening a new popup window..."
	        self.w = MyPopup()
	        self.w.setGeometry(QRect(100, 100, 400, 200))
	        self.w.show()
	
	class App(QApplication):
	    def __init__(self, *args):
	        QApplication.__init__(self, *args)
	        self.main = MainWindow()
	        self.connect(self, SIGNAL("lastWindowClosed()"), self.byebye )
	        self.main.show()
	
	    def byebye( self ):
	        self.exit(0)
	
	
except ImportError:
	pyqt_available = False
	


class ShowGraphAttributes(tlp.Algorithm):
	def __init__(self, context):
		tlp.Algorithm.__init__(self, context)

	def check(self):
		#if not pyqt_available:
		#	return (False, "This plugins requires the PyQt4.Qt python package")
		return (True, "")

	def run(self):
		if pyqt_available:
			myApp = MyForm()
			myApp.show()
		else:
			att = self.graph.getAttributes()
			for a in att.getKeys():
				try:
					val = str(att[a])
					print a, ": ",val
				except AttributeError:
					pass
		return True


def cbc(id, tex):
    return lambda : callback(id, tex)

def callback(id, tex):
    s = 'At {} f is {}\n'.format(id, id**id/0.987)
    tex.insert(tk.END, s)
    tex.see(tk.END)             # Scroll if necessary

# The line below does the magic to register the plugin to the plugin database
# and updates the GUI to make it accessible through the menus.
tulipplugins.registerPluginOfGroup("ShowGraphAttributes", "Display graph attributes in Python Output", "Benjamin Renoust", "03/05/2015", "Displays the different attributes of a graph in a python output (use of print)", "1.0", "Attribute Manipulation")
