# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui/mainwindow.ui'
#
# Created: Fri Mar  1 09:29:03 2013
#      by: PyQt4 UI code generator 4.9.6
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName(_fromUtf8("MainWindow"))
        MainWindow.resize(800, 600)
        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.verticalLayout = QtGui.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.tabWidget = QtGui.QTabWidget(self.centralwidget)
        self.tabWidget.setObjectName(_fromUtf8("tabWidget"))
        self.launchTab = QtGui.QWidget()
        self.launchTab.setObjectName(_fromUtf8("launchTab"))
        self.verticalLayout_2 = QtGui.QVBoxLayout(self.launchTab)
        self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))
        self.label_3 = QtGui.QLabel(self.launchTab)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_3.sizePolicy().hasHeightForWidth())
        self.label_3.setSizePolicy(sizePolicy)
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.verticalLayout_2.addWidget(self.label_3)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.label = QtGui.QLabel(self.launchTab)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label.sizePolicy().hasHeightForWidth())
        self.label.setSizePolicy(sizePolicy)
        self.label.setObjectName(_fromUtf8("label"))
        self.horizontalLayout.addWidget(self.label)
        self.lcdNumber = QtGui.QLCDNumber(self.launchTab)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lcdNumber.sizePolicy().hasHeightForWidth())
        self.lcdNumber.setSizePolicy(sizePolicy)
        self.lcdNumber.setAutoFillBackground(False)
        self.lcdNumber.setStyleSheet(_fromUtf8("QLCDNumber{\n"
"color:  rgb(0, 255, 0);\n"
"background-color: rgb(0,0,0);\n"
"}"))
        self.lcdNumber.setObjectName(_fromUtf8("lcdNumber"))
        self.horizontalLayout.addWidget(self.lcdNumber)
        self.label_2 = QtGui.QLabel(self.launchTab)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_2.sizePolicy().hasHeightForWidth())
        self.label_2.setSizePolicy(sizePolicy)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.horizontalLayout.addWidget(self.label_2)
        self.verticalLayout_2.addLayout(self.horizontalLayout)
        self.launchButton = QtGui.QPushButton(self.launchTab)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.launchButton.sizePolicy().hasHeightForWidth())
        self.launchButton.setSizePolicy(sizePolicy)
        self.launchButton.setObjectName(_fromUtf8("launchButton"))
        self.verticalLayout_2.addWidget(self.launchButton)
        self.tabWidget.addTab(self.launchTab, _fromUtf8(""))
        self.verticalLayout.addWidget(self.tabWidget)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtGui.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 25))
        self.menubar.setObjectName(_fromUtf8("menubar"))
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtGui.QStatusBar(MainWindow)
        self.statusbar.setObjectName(_fromUtf8("statusbar"))
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        self.tabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(_translate("MainWindow", "Grant Wood Tractor Drive", None))
        self.label_3.setText(_translate("MainWindow", "<html><head/><body><p><span style=\" font-size:26pt; font-weight:600;\">Launch Grant Wood Tractor Drive</span></p></body></html>", None))
        self.label.setText(_translate("MainWindow", "Autostart in ", None))
        self.label_2.setText(_translate("MainWindow", "Seconds", None))
        self.launchButton.setText(_translate("MainWindow", "Launch", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.launchTab), _translate("MainWindow", "Launch", None))

