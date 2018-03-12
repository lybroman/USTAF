# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'groupEditor.ui'
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

class Ui_GroupEditorDialog(object):
    def setupUi(self, GroupEditorDialog):
        GroupEditorDialog.setObjectName(_fromUtf8("GroupEditorDialog"))
        GroupEditorDialog.resize(470, 236)
        self.groupBox = QtGui.QGroupBox(GroupEditorDialog)
        self.groupBox.setGeometry(QtCore.QRect(20, 10, 441, 221))
        self.groupBox.setMinimumSize(QtCore.QSize(441, 221))
        self.groupBox.setMaximumSize(QtCore.QSize(441, 221))
        self.groupBox.setObjectName(_fromUtf8("groupBox"))
        self.GroupNamelineEdit = QtGui.QLineEdit(self.groupBox)
        self.GroupNamelineEdit.setGeometry(QtCore.QRect(90, 30, 251, 20))
        self.GroupNamelineEdit.setMinimumSize(QtCore.QSize(251, 20))
        self.GroupNamelineEdit.setMaximumSize(QtCore.QSize(251, 20))
        self.GroupNamelineEdit.setObjectName(_fromUtf8("GroupNamelineEdit"))
        self.label = QtGui.QLabel(self.groupBox)
        self.label.setGeometry(QtCore.QRect(11, 31, 56, 16))
        self.label.setMinimumSize(QtCore.QSize(56, 16))
        self.label.setMaximumSize(QtCore.QSize(56, 16))
        self.label.setObjectName(_fromUtf8("label"))
        self.buttonBox = QtGui.QDialogButtonBox(self.groupBox)
        self.buttonBox.setGeometry(QtCore.QRect(290, 190, 151, 32))
        self.buttonBox.setMinimumSize(QtCore.QSize(151, 32))
        self.buttonBox.setMaximumSize(QtCore.QSize(151, 32))
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.GroupNameTextBrowser = QtGui.QTextBrowser(self.groupBox)
        self.GroupNameTextBrowser.setGeometry(QtCore.QRect(90, 55, 251, 121))
        self.GroupNameTextBrowser.setMinimumSize(QtCore.QSize(251, 121))
        self.GroupNameTextBrowser.setMaximumSize(QtCore.QSize(251, 121))
        self.GroupNameTextBrowser.setReadOnly(False)
        self.GroupNameTextBrowser.setObjectName(_fromUtf8("GroupNameTextBrowser"))
        self.label_2 = QtGui.QLabel(self.groupBox)
        self.label_2.setGeometry(QtCore.QRect(10, 70, 46, 13))
        self.label_2.setMinimumSize(QtCore.QSize(46, 13))
        self.label_2.setMaximumSize(QtCore.QSize(46, 13))
        self.label_2.setObjectName(_fromUtf8("label_2"))

        self.retranslateUi(GroupEditorDialog)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), GroupEditorDialog.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), GroupEditorDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(GroupEditorDialog)

    def retranslateUi(self, GroupEditorDialog):
        GroupEditorDialog.setWindowTitle(_translate("GroupEditorDialog", "GroupEditor", None))
        self.groupBox.setTitle(_translate("GroupEditorDialog", "Edit Group Info", None))
        self.label.setText(_translate("GroupEditorDialog", "GroupName", None))
        self.label_2.setText(_translate("GroupEditorDialog", "Info", None))


if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    GroupEditorDialog = QtGui.QDialog()
    ui = Ui_GroupEditorDialog()
    ui.setupUi(GroupEditorDialog)
    GroupEditorDialog.show()
    sys.exit(app.exec_())

