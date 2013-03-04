# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui/calibration.ui'
#
# Created: Fri Mar  1 09:29:04 2013
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

class Ui_Calibration(object):
    def setupUi(self, Calibration):
        Calibration.setObjectName(_fromUtf8("Calibration"))
        Calibration.resize(524, 436)
        self.verticalLayout = QtGui.QVBoxLayout(Calibration)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.stepLabel = QtGui.QLabel(Calibration)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.stepLabel.sizePolicy().hasHeightForWidth())
        self.stepLabel.setSizePolicy(sizePolicy)
        self.stepLabel.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.stepLabel.setObjectName(_fromUtf8("stepLabel"))
        self.verticalLayout.addWidget(self.stepLabel)
        self.instructionLabel = QtGui.QLabel(Calibration)
        self.instructionLabel.setObjectName(_fromUtf8("instructionLabel"))
        self.verticalLayout.addWidget(self.instructionLabel)
        self.graphicsView = QtGui.QGraphicsView(Calibration)
        self.graphicsView.setObjectName(_fromUtf8("graphicsView"))
        self.verticalLayout.addWidget(self.graphicsView)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.label = QtGui.QLabel(Calibration)
        self.label.setObjectName(_fromUtf8("label"))
        self.horizontalLayout.addWidget(self.label)
        self.valueLabel = QtGui.QLabel(Calibration)
        self.valueLabel.setObjectName(_fromUtf8("valueLabel"))
        self.horizontalLayout.addWidget(self.valueLabel)
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.nextButton = QtGui.QPushButton(Calibration)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.nextButton.sizePolicy().hasHeightForWidth())
        self.nextButton.setSizePolicy(sizePolicy)
        self.nextButton.setObjectName(_fromUtf8("nextButton"))
        self.horizontalLayout.addWidget(self.nextButton)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        self.label_2 = QtGui.QLabel(Calibration)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.horizontalLayout_2.addWidget(self.label_2)
        self.portEdit = QtGui.QLineEdit(Calibration)
        self.portEdit.setObjectName(_fromUtf8("portEdit"))
        self.horizontalLayout_2.addWidget(self.portEdit)
        self.connectButton = QtGui.QPushButton(Calibration)
        self.connectButton.setObjectName(_fromUtf8("connectButton"))
        self.horizontalLayout_2.addWidget(self.connectButton)
        self.verticalLayout.addLayout(self.horizontalLayout_2)

        self.retranslateUi(Calibration)
        QtCore.QMetaObject.connectSlotsByName(Calibration)

    def retranslateUi(self, Calibration):
        Calibration.setWindowTitle(_translate("Calibration", "Form", None))
        self.stepLabel.setText(_translate("Calibration", "<html><head/><body><p><span style=\" font-size:28pt; font-weight:600;\">MidPoint</span></p></body></html>", None))
        self.instructionLabel.setText(_translate("Calibration", "Make sure wheel is centered and press Next to begin calibration", None))
        self.label.setText(_translate("Calibration", "Current Value:", None))
        self.valueLabel.setText(_translate("Calibration", "0", None))
        self.nextButton.setText(_translate("Calibration", "Next", None))
        self.label_2.setText(_translate("Calibration", "Port:", None))
        self.connectButton.setText(_translate("Calibration", "Connect", None))

