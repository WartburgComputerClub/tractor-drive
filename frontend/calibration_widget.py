from PyQt4.QtCore import *
from PyQt4.QtGui import *
from ui_calibration import Ui_Calibration
import Image
import ImageQt
from pictureitem import PictureItem
from ConfigParser import ConfigParser
from serial import Serial
from os.path import dirname,realpath

class CalibrationWidget(QWidget,Ui_Calibration):
    
    def __init__(self,parent = None):
        proj_home = dirname(realpath(__file__))
        proj_home = proj_home[0:proj_home.rfind('/')]
        QWidget.__init__(self,parent)
        self.setupUi(self)
        self.step = 0
        self.rot = 0
        self.scene = QGraphicsScene()
        #self.graphicsView.setRenderHints(QPainter.Antialiasing | QPainter.SmoothPixmapTransform | QPainter.TextAntialiasing)
        self.graphicsView.setScene(self.scene)
        self.anim = QTimer()
        self.anim.setInterval(30)
        self.anim.timeout.connect(self.rotateCallback)
        self.showImage()
        self.nextButton.clicked.connect(self.nextStep)
        self.conf = ConfigParser()
        self.conf.read(proj_home + '/global.cfg')
        self.portEdit.setText(self.conf.get('wheel','port'))
        self.timer = QTimer()
        self.timer.setInterval(100)
        self.timer.timeout.connect(self.updateValue)
        self.nextButton.setDisabled(True)
        self.connectButton.clicked.connect(self.connectWheel)
        
        self.midpoint = 0
        self.right_max = 0
        self.left_max = 0
        
    def connectWheel(self):
        try:
            txt = str(self.portEdit.text())
            self.ser = Serial(txt)
            print 'success'
            self.timer.start()
            self.nextButton.setDisabled(False)
            self.connectButton.setDisabled(True)
        except:
            pass
        
    def updateValue(self):
        if (self.ser.inWaiting() > 100):
            self.ser.flushInput()
        if (self.ser.inWaiting()):
            curr_val = float(self.ser.readline()[0:-2])
            if self.step == 1:
                if abs(self.midpoint - curr_val) > abs(self.midpoint - self.left_max):
                    self.valueLabel.setNum(curr_val)
            elif self.step == 2:
                if (self.midpoint - self.left_max) > 0:
                    if curr_val > self.right_max:
                        self.right_max = curr_val
                        self.valueLabel.setNum(curr_val)
                else:
                    if curr_val < self.right_max:
                        self.right_max = curr_val
                        self.valueLabel.setNum(curr_val)
            else:
                self.valueLabel.setNum(curr_val)
            self.update()
       
    def nextStep(self):
        proj_home = dirname(realpath(__file__))
        proj_home = proj_home[0:proj_home.rfind('/')]
        self.step += 1
        self.anim.stop()
        if self.step == 0:
            self.stepLabel.setText('<html><head/><body><p><span style=" font-size:28pt; font-weight:600;">MidPoint</span></p></body></html>')
            self.instructionLabel.setText('Make sure wheel is centered and press Next to begin calibration')
        elif self.step == 1:
            self.midpoint = float(self.valueLabel.text())
            self.left_max = self.midpoint
            self.stepLabel.setText('<html><head/><body><p><span style=" font-size:28pt; font-weight:600;">Left Max</span></p></body></html>')
            self.instructionLabel.setText("Rotate the wheel as far left as possible, then return to center and press Next to continue.")
            self.anim.start()
        elif self.step == 2:
            self.left_max = float(self.valueLabel.text())
            self.right_max = self.midpoint
            self.stepLabel.setText('<html><head/><body><p><span style=" font-size:28pt; font-weight:600;">Right Max</span></p></body></html>')
            self.instructionLabel.setText("Rotate the wheel as far right as possible, then return to center and press Next to continue.")
            self.rot = 0
            self.anim.start()
        elif self.step == 3:
            self.rotateImage(0)
            self.step = -1
            self.conf.set('wheel','port',self.portEdit.text())
            self.conf.set('wheel','midpoint',self.midpoint)
            self.conf.set('wheel','left_max',self.left_max)
            self.conf.set('wheel','right_max',self.right_max)
            fp = open(proj_home + '/global.cfg','w')
            self.conf.write(fp)
            fp.close()
            self.midpoint = 0
            self.left_max = 0
            self.right_max = 0
            self.stepLabel.setText('<html><head/><body><p><span style=" font-size:28pt; font-weight:600;">Settings Saved</span></p></body></html>')
            self.instructionLabel.setText('Your settings have been saved.  Click next to recalibrate.')
            
    def rotateImage(self,angle):
        c = self.pitem.boundingRect().center()
        t = QTransform()
        t.translate(c.x(),c.y())
        t.rotate(angle,Qt.ZAxis)
        t.translate(-c.x(),-c.y())
        self.pitem.setTransform(t)
        
    def rotateCallback(self):
        if self.step == 1:
            self.rot -= .6
        elif self.step == 2:
            self.rot += .6
            
        self.rotateImage(self.rot)
        if (self.rot < -90 and self.step == 1) \
        or (self.rot > 90 and self.step == 2):
            self.anim.stop()
            
    def displayImage(self,img):
        self.scene.clear()
        self.imgQ = ImageQt.ImageQt(img)
        pixMap = QPixmap.fromImage(self.imgQ)
        self.pitem = self.scene.addPixmap(pixMap)
        # put one of following in rotate callback
        #self.graphicsView.fitInView(QRectF(0,0,w,h),Qt.KeepAspectRatio)
        #self.graphicsView.fitInView(self.scene.itemsBoundingRect(),Qt.KeepAspectRatio)
        #self.graphicsView.fitInView(self.scene.itemsBoundingRect(),Qt.KeepAspectRatio)
        self.scene.update()
        
    def showImage(self):
        proj_home = dirname(realpath(__file__))
        proj_home = proj_home[0:proj_home.rfind('/')]
        img = Image.open(proj_home + "/frontend/img/wheel.png")
        self.displayImage(img)
