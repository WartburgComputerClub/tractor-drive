from PyQt4.QtCore import *
from PyQt4.QtGui import *
from PyQt4.uic.Compiler.qtproxies import QtCore
import sys

class PictureItem(QObject):
    
    def __init__(self,pix):
        super(PictureItem,self).__init__()
        self.pix = pix
        self.rot = 0
        
    def getRot(self):
        return self.rot
    
    def setRot(self,angle):
        print angle
        self.rot = angle
        #if self.rot != angle:
        #    self.rot = angle
        #    c = self.pix.boundingRect().center()
        #    t = QTransform
        #    t.translate(c.x(),c.y())
        #    t.rotate(self.rot,Qt.YAxis)
        ##    t.translate(-c.x(),-c.y())
        #    self.pix.setTransform(t)
            
    rot = pyqtProperty(float,getRot,setRot)
    
    def animateAngle(self,start,end):
        self.anim = QPropertyAnimation(self,"rot")
        self.anim.setDuration(20)
        self.anim.setStartValue(start)
        self.anim.setEndValue(end)
        self.anim.setEasingCurve(QEasingCurve.InOutBack)
        self.anim.finished.connect(self.anim.deleteLater)
        QTimer.singleShot(1000, self.anim, SLOT("start()"))
    
    
        