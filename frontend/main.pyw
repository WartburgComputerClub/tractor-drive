#!/usr/bin/env python
#import sip
#sip.setapi('QString',2)    
#sip.setapi('QVariant',2)  
import sys
#import icons_rc
from PyQt4.QtGui import QApplication
from mainwindow import MainWindow

__version__ = "1.0"

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
