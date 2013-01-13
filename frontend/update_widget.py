from PyQt4.QtCore import *
from PyQt4.QtGui import *
from ui_update import Ui_Update
import ConfigParser
from subprocess import Popen,PIPE,call
from os.path import dirname,realpath
#import git

class Updater(QThread):
    finished = pyqtSignal()
    updateMessage = pyqtSignal(str)
    
    def __init__(self,loc):
        QObject.__init__(self)
        self.loc = loc
        proj_home = dirname(realpath(__file__))
        proj_home = proj_home[0:proj_home.rfind('/')]
        self.proj_home = proj_home
    
    def run(self):
        print "updating"
        # TODO: Use self.proj_home for these calls
        call(["git","stash"])
        p = Popen(["git","pull",self.loc],stdout=PIPE)
        output = p.communicate()[0]
        self.updateMessage.emit(output)
        call(["git","stash","pop"])
        self.finished.emit()
        
    

class UpdateWidget(QWidget,Ui_Update):
    
    def __init__(self,parent = None):
        QWidget.__init__(self,parent)
        proj_home = dirname(realpath(__file__))
        proj_home = proj_home[0:proj_home.rfind('/')]
        self.proj_home = proj_home
        self.setupUi(self)
        conf = ConfigParser.ConfigParser()
        conf.read(self.proj_home + '/global.cfg')
        self.conf = conf
        self.lineEdit.setText(conf.get('support','update_location'))
        self.updateButton.clicked.connect(self.updateProject)
        self.saveButton.clicked.connect(self.saveLocation)
        self.browseButton.clicked.connect(self.fileBrowse)
        self.statusbar = None
        
    def setStatusbar(self,statusbar):
        self.statusbar = statusbar
        
    def outputMessage(self,message):
        self.textBrowser.append(message)
        
    def doneUpdating(self):
        if self.statusbar != None:
            self.statusbar.showMessage("Ready")
        
    def updateProject(self):
        loc = self.lineEdit.text()
        if self.statusbar != None:
            self.statusbar.showMessage("Updating")
            
        updater = Updater(loc)
        updater.finished.connect(self.doneUpdating)
        updater.updateMessage.connect(self.outputMessage)
        updater.start()
        self.updater = updater
            
    def saveLocation(self):
        self.conf.set("support","update_location",self.lineEdit.text())
        fp = open(self.proj_home + '/global.cfg','w')
        self.conf.write(fp)
        
    def fileBrowse(self):
        fname = QFileDialog.getOpenFileName(self, "Update Location")
        self.lineEdit.setText(fname)
        