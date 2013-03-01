# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui/update.ui'
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

class Ui_Update(object):
    def setupUi(self, Update):
        Update.setObjectName(_fromUtf8("Update"))
        Update.resize(520, 421)
        self.verticalLayout = QtGui.QVBoxLayout(Update)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.label = QtGui.QLabel(Update)
        self.label.setObjectName(_fromUtf8("label"))
        self.verticalLayout.addWidget(self.label)
        self.textBrowser = QtGui.QTextBrowser(Update)
        self.textBrowser.setObjectName(_fromUtf8("textBrowser"))
        self.verticalLayout.addWidget(self.textBrowser)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.label_2 = QtGui.QLabel(Update)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.horizontalLayout.addWidget(self.label_2)
        self.lineEdit = QtGui.QLineEdit(Update)
        self.lineEdit.setObjectName(_fromUtf8("lineEdit"))
        self.horizontalLayout.addWidget(self.lineEdit)
        self.browseButton = QtGui.QPushButton(Update)
        self.browseButton.setObjectName(_fromUtf8("browseButton"))
        self.horizontalLayout.addWidget(self.browseButton)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        spacerItem = QtGui.QSpacerItem(65, 20, QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem)
        self.saveButton = QtGui.QPushButton(Update)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.saveButton.sizePolicy().hasHeightForWidth())
        self.saveButton.setSizePolicy(sizePolicy)
        self.saveButton.setObjectName(_fromUtf8("saveButton"))
        self.horizontalLayout_2.addWidget(self.saveButton)
        self.updateButton = QtGui.QPushButton(Update)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.updateButton.sizePolicy().hasHeightForWidth())
        self.updateButton.setSizePolicy(sizePolicy)
        self.updateButton.setObjectName(_fromUtf8("updateButton"))
        self.horizontalLayout_2.addWidget(self.updateButton)
        spacerItem1 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem1)
        self.verticalLayout.addLayout(self.horizontalLayout_2)

        self.retranslateUi(Update)
        QtCore.QMetaObject.connectSlotsByName(Update)

    def retranslateUi(self, Update):
        Update.setWindowTitle(_translate("Update", "Form", None))
        self.label.setText(_translate("Update", "<html><head/><body><p><span style=\" font-size:26pt; font-weight:600;\">Updates</span></p></body></html>", None))
        self.label_2.setText(_translate("Update", "Location:", None))
        self.browseButton.setText(_translate("Update", "Browse", None))
        self.saveButton.setText(_translate("Update", "Save Location", None))
        self.updateButton.setText(_translate("Update", "Update", None))

