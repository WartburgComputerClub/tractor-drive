from PyQt4.QtGui import *
from PyQt4.QtCore import *
from ui_mainwindow import Ui_MainWindow
from calibration_widget import CalibrationWidget
from update_widget import UpdateWidget
from settings_widget import SettingsWidget
from subprocess import call
from os.path import dirname,realpath
import ConfigParser

class Launcher(QThread):
    
    def run(self):
        proj_home = dirname(realpath(__file__))
        proj_home = proj_home[0:proj_home.rfind('/')]
        conf = ConfigParser.ConfigParser()
        conf.read(proj_home + '/global.cfg')
        call([conf.get('system','blenderplayer'),proj_home + '/levels/portal_world.blend'])
    
class MainWindow(QMainWindow, Ui_MainWindow):
    
    launchSignal = pyqtSignal()

    def __init__(self, parent = None):
    
        QMainWindow.__init__(self, parent)
        self.setupUi(self)
        self.countdown = QTimer();
        self.startTimer()
        self.countdown.timeout.connect(self.decrement)
        self.launchSignal.connect(self.launchButton.click)
        self.launchButton.clicked.connect(self.launch)
        self.tabWidget.currentChanged.connect(self.tabChange)
        self.calibrationWidget = CalibrationWidget()
        self.tabWidget.addTab(self.calibrationWidget,"Calibration")
        self.updateWidget = UpdateWidget()
        self.updateWidget.setStatusbar(self.statusbar)
        self.tabWidget.addTab(self.updateWidget,"Update")
        self.settingsWidget = SettingsWidget(self)
        self.settingsWidget.statusBar = self.statusbar
        self.tabWidget.addTab(self.settingsWidget,"Global Settings")
        self.statusbar.showMessage("Ready")
        
    def decrement(self):
        self.lcdNumber.display(self.lcdNumber.intValue() - 1)
        if self.lcdNumber.intValue() == 0:
            self.launchSignal.emit()
            self.countdown.stop()
        
    def startTimer(self):
        self.countdown.start(1000)
        self.lcdNumber.display(10)
        
    def tabChange(self,tab):
        self.countdown.stop()

        if self.tabWidget.tabText(tab) == 'Global Settings':
            self.settingsWidget.updateImage()
            self.settingsWidget.updateImage()
        
    def gameStop(self):
        self.statusbar.showMessage("Ready")
        self.startTimer()
        
    def launch(self):
        self.countdown.stop()
        self.statusbar.showMessage("Launching Simulation...")
        launcher = Launcher()
        launcher.finished.connect(self.gameStop)
        launcher.start()
        self.launcher = launcher
        
