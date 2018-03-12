# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'run.ui'
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

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName(_fromUtf8("Dialog"))
        Dialog.resize(804, 655)
        self.gridLayout_9 = QtGui.QGridLayout(Dialog)
        self.gridLayout_9.setObjectName(_fromUtf8("gridLayout_9"))
        self.gridLayout_8 = QtGui.QGridLayout()
        self.gridLayout_8.setObjectName(_fromUtf8("gridLayout_8"))
        self.gridLayout_5 = QtGui.QGridLayout()
        self.gridLayout_5.setObjectName(_fromUtf8("gridLayout_5"))
        self.gridLayout_4 = QtGui.QGridLayout()
        self.gridLayout_4.setObjectName(_fromUtf8("gridLayout_4"))
        self.groupBox = QtGui.QGroupBox(Dialog)
        self.groupBox.setObjectName(_fromUtf8("groupBox"))
        self.gridLayout_3 = QtGui.QGridLayout(self.groupBox)
        self.gridLayout_3.setObjectName(_fromUtf8("gridLayout_3"))
        self.resultandEventTableView = QtGui.QTableView(self.groupBox)
        self.resultandEventTableView.setObjectName(_fromUtf8("resultandEventTableView"))
        self.gridLayout_3.addWidget(self.resultandEventTableView, 0, 0, 1, 1)
        self.gridLayout_4.addWidget(self.groupBox, 0, 0, 1, 1)
        self.groupBox_2 = QtGui.QGroupBox(Dialog)
        self.groupBox_2.setObjectName(_fromUtf8("groupBox_2"))
        self.gridLayout = QtGui.QGridLayout(self.groupBox_2)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.stdTextEditor = QtGui.QTextEdit(self.groupBox_2)
        self.stdTextEditor.setObjectName(_fromUtf8("stdTextEditor"))
        self.gridLayout.addWidget(self.stdTextEditor, 0, 0, 1, 1)
        self.gridLayout_4.addWidget(self.groupBox_2, 1, 0, 1, 1)
        self.gridLayout_5.addLayout(self.gridLayout_4, 0, 0, 1, 1)
        self.groupBox_3 = QtGui.QGroupBox(Dialog)
        self.groupBox_3.setObjectName(_fromUtf8("groupBox_3"))
        self.gridLayout_2 = QtGui.QGridLayout(self.groupBox_3)
        self.gridLayout_2.setObjectName(_fromUtf8("gridLayout_2"))
        self.errorLogTextEdit = QtGui.QTextEdit(self.groupBox_3)
        self.errorLogTextEdit.setObjectName(_fromUtf8("errorLogTextEdit"))
        self.gridLayout_2.addWidget(self.errorLogTextEdit, 0, 0, 1, 1)
        self.gridLayout_5.addWidget(self.groupBox_3, 0, 1, 1, 1)
        self.gridLayout_8.addLayout(self.gridLayout_5, 0, 0, 1, 1)
        self.gridLayout_7 = QtGui.QGridLayout()
        self.gridLayout_7.setObjectName(_fromUtf8("gridLayout_7"))
        self.groupBox_4 = QtGui.QGroupBox(Dialog)
        self.groupBox_4.setObjectName(_fromUtf8("groupBox_4"))
        self.gridLayout_6 = QtGui.QGridLayout(self.groupBox_4)
        self.gridLayout_6.setObjectName(_fromUtf8("gridLayout_6"))
        self.RemarkLineEdit = QtGui.QLineEdit(self.groupBox_4)
        self.RemarkLineEdit.setObjectName(_fromUtf8("RemarkLineEdit"))
        self.gridLayout_6.addWidget(self.RemarkLineEdit, 0, 0, 1, 1)
        self.runResultcomboBox = QtGui.QComboBox(self.groupBox_4)
        self.runResultcomboBox.setObjectName(_fromUtf8("runResultcomboBox"))
        self.gridLayout_6.addWidget(self.runResultcomboBox, 0, 1, 1, 1)
        self.gridLayout_7.addWidget(self.groupBox_4, 0, 0, 1, 1)
        self.buttonBox = QtGui.QDialogButtonBox(Dialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.gridLayout_7.addWidget(self.buttonBox, 0, 1, 1, 1)
        self.gridLayout_8.addLayout(self.gridLayout_7, 1, 0, 1, 1)
        self.gridLayout_9.addLayout(self.gridLayout_8, 0, 0, 1, 1)

        self.retranslateUi(Dialog)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), Dialog.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), Dialog.reject)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(_translate("Dialog", "Run Status Window", None))
        self.groupBox.setTitle(_translate("Dialog", "Result & Event", None))
        self.groupBox_2.setTitle(_translate("Dialog", "Std Info", None))
        self.groupBox_3.setTitle(_translate("Dialog", "Error Logs", None))
        self.groupBox_4.setTitle(_translate("Dialog", "Remark", None))

