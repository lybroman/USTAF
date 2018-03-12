# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'configEditor.ui'
#
# Created by: PyQt4 UI code generator 4.11.4
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

class Ui_ServerConfigDialog(object):
    def setupUi(self, ServerConfigDialog):
        ServerConfigDialog.setObjectName(_fromUtf8("ServerConfigDialog"))
        ServerConfigDialog.resize(496, 428)
        self.groupBox = QtGui.QGroupBox(ServerConfigDialog)
        self.groupBox.setGeometry(QtCore.QRect(10, 20, 471, 231))
        self.groupBox.setObjectName(_fromUtf8("groupBox"))
        self.layoutWidget = QtGui.QWidget(self.groupBox)
        self.layoutWidget.setGeometry(QtCore.QRect(11, 24, 431, 207))
        self.layoutWidget.setObjectName(_fromUtf8("layoutWidget"))
        self.gridLayout_3 = QtGui.QGridLayout(self.layoutWidget)
        self.gridLayout_3.setObjectName(_fromUtf8("gridLayout_3"))
        self.gridLayout = QtGui.QGridLayout()
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.label_2 = QtGui.QLabel(self.layoutWidget)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.gridLayout.addWidget(self.label_2, 1, 0, 1, 1)
        self.label_4 = QtGui.QLabel(self.layoutWidget)
        self.label_4.setObjectName(_fromUtf8("label_4"))
        self.gridLayout.addWidget(self.label_4, 3, 0, 1, 1)
        self.label_3 = QtGui.QLabel(self.layoutWidget)
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.gridLayout.addWidget(self.label_3, 2, 0, 1, 1)
        self.label = QtGui.QLabel(self.layoutWidget)
        self.label.setObjectName(_fromUtf8("label"))
        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)
        self.label_6 = QtGui.QLabel(self.layoutWidget)
        self.label_6.setObjectName(_fromUtf8("label_6"))
        self.gridLayout.addWidget(self.label_6, 5, 0, 1, 1)
        self.label_5 = QtGui.QLabel(self.layoutWidget)
        self.label_5.setObjectName(_fromUtf8("label_5"))
        self.gridLayout.addWidget(self.label_5, 4, 0, 1, 1)
        self.label_10 = QtGui.QLabel(self.layoutWidget)
        self.label_10.setObjectName(_fromUtf8("label_10"))
        self.gridLayout.addWidget(self.label_10, 6, 0, 1, 1)
        self.gridLayout_3.addLayout(self.gridLayout, 0, 0, 1, 1)
        self.gridLayout_2 = QtGui.QGridLayout()
        self.gridLayout_2.setObjectName(_fromUtf8("gridLayout_2"))
        self.AddresslineEdit = QtGui.QLineEdit(self.layoutWidget)
        self.AddresslineEdit.setObjectName(_fromUtf8("AddresslineEdit"))
        self.gridLayout_2.addWidget(self.AddresslineEdit, 0, 0, 1, 1)
        self.PortlineEdit = QtGui.QLineEdit(self.layoutWidget)
        self.PortlineEdit.setObjectName(_fromUtf8("PortlineEdit"))
        self.gridLayout_2.addWidget(self.PortlineEdit, 1, 0, 1, 1)
        self.BaseSharePathlineEdit = QtGui.QLineEdit(self.layoutWidget)
        self.BaseSharePathlineEdit.setObjectName(_fromUtf8("BaseSharePathlineEdit"))
        self.gridLayout_2.addWidget(self.BaseSharePathlineEdit, 4, 0, 1, 1)
        self.ColdRebootAddressLineEditor = QtGui.QLineEdit(self.layoutWidget)
        self.ColdRebootAddressLineEditor.setObjectName(_fromUtf8("ColdRebootAddressLineEditor"))
        self.gridLayout_2.addWidget(self.ColdRebootAddressLineEditor, 2, 0, 1, 1)
        self.StdLoglineEdit = QtGui.QLineEdit(self.layoutWidget)
        self.StdLoglineEdit.setObjectName(_fromUtf8("StdLoglineEdit"))
        self.gridLayout_2.addWidget(self.StdLoglineEdit, 5, 0, 1, 1)
        self.ColdRebootPortLineEditor = QtGui.QLineEdit(self.layoutWidget)
        self.ColdRebootPortLineEditor.setObjectName(_fromUtf8("ColdRebootPortLineEditor"))
        self.gridLayout_2.addWidget(self.ColdRebootPortLineEditor, 3, 0, 1, 1)
        self.SocketPortLineEdit = QtGui.QLineEdit(self.layoutWidget)
        self.SocketPortLineEdit.setObjectName(_fromUtf8("SocketPortLineEdit"))
        self.gridLayout_2.addWidget(self.SocketPortLineEdit, 6, 0, 1, 1)
        self.gridLayout_3.addLayout(self.gridLayout_2, 0, 1, 1, 1)
        self.buttonBox = QtGui.QDialogButtonBox(ServerConfigDialog)
        self.buttonBox.setGeometry(QtCore.QRect(20, 390, 156, 23))
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.groupBox_2 = QtGui.QGroupBox(ServerConfigDialog)
        self.groupBox_2.setGeometry(QtCore.QRect(10, 260, 471, 111))
        self.groupBox_2.setObjectName(_fromUtf8("groupBox_2"))
        self.layoutWidget1 = QtGui.QWidget(self.groupBox_2)
        self.layoutWidget1.setGeometry(QtCore.QRect(10, 20, 211, 87))
        self.layoutWidget1.setObjectName(_fromUtf8("layoutWidget1"))
        self.gridLayout_6 = QtGui.QGridLayout(self.layoutWidget1)
        self.gridLayout_6.setObjectName(_fromUtf8("gridLayout_6"))
        self.gridLayout_4 = QtGui.QGridLayout()
        self.gridLayout_4.setObjectName(_fromUtf8("gridLayout_4"))
        self.label_7 = QtGui.QLabel(self.layoutWidget1)
        self.label_7.setObjectName(_fromUtf8("label_7"))
        self.gridLayout_4.addWidget(self.label_7, 0, 0, 1, 1)
        self.label_8 = QtGui.QLabel(self.layoutWidget1)
        self.label_8.setObjectName(_fromUtf8("label_8"))
        self.gridLayout_4.addWidget(self.label_8, 1, 0, 1, 1)
        self.label_9 = QtGui.QLabel(self.layoutWidget1)
        self.label_9.setObjectName(_fromUtf8("label_9"))
        self.gridLayout_4.addWidget(self.label_9, 2, 0, 1, 1)
        self.gridLayout_6.addLayout(self.gridLayout_4, 0, 0, 1, 1)
        self.gridLayout_5 = QtGui.QGridLayout()
        self.gridLayout_5.setObjectName(_fromUtf8("gridLayout_5"))
        self.LogFilecomboBox = QtGui.QComboBox(self.layoutWidget1)
        self.LogFilecomboBox.setObjectName(_fromUtf8("LogFilecomboBox"))
        self.gridLayout_5.addWidget(self.LogFilecomboBox, 0, 0, 1, 1)
        self.LogStreamcomboBox = QtGui.QComboBox(self.layoutWidget1)
        self.LogStreamcomboBox.setObjectName(_fromUtf8("LogStreamcomboBox"))
        self.gridLayout_5.addWidget(self.LogStreamcomboBox, 1, 0, 1, 1)
        self.LogPathlineEdit = QtGui.QLineEdit(self.layoutWidget1)
        self.LogPathlineEdit.setObjectName(_fromUtf8("LogPathlineEdit"))
        self.gridLayout_5.addWidget(self.LogPathlineEdit, 2, 0, 1, 1)
        self.gridLayout_6.addLayout(self.gridLayout_5, 0, 1, 1, 1)

        self.retranslateUi(ServerConfigDialog)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), ServerConfigDialog.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), ServerConfigDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(ServerConfigDialog)

    def retranslateUi(self, ServerConfigDialog):
        ServerConfigDialog.setWindowTitle(_translate("ServerConfigDialog", "Server Configuration", None))
        self.groupBox.setTitle(_translate("ServerConfigDialog", "Execution Configuration", None))
        self.label_2.setText(_translate("ServerConfigDialog", "Task Queue Server Port", None))
        self.label_4.setText(_translate("ServerConfigDialog", "Cold Reboot Server Port", None))
        self.label_3.setText(_translate("ServerConfigDialog", "Cold Reboot Server Address", None))
        self.label.setText(_translate("ServerConfigDialog", "Task Queue Server Address", None))
        self.label_6.setText(_translate("ServerConfigDialog", "Std out/err Log Path", None))
        self.label_5.setText(_translate("ServerConfigDialog", "Base Share Path", None))
        self.label_10.setText(_translate("ServerConfigDialog", "Socket Server Port", None))
        self.groupBox_2.setTitle(_translate("ServerConfigDialog", "Log Configuration", None))
        self.label_7.setText(_translate("ServerConfigDialog", "Log File Level", None))
        self.label_8.setText(_translate("ServerConfigDialog", "Log Stream Level", None))
        self.label_9.setText(_translate("ServerConfigDialog", "Log File Path", None))

