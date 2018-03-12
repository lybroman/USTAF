#-------------------------------------------------------------------------------
# Name:        groupEditor.py
# Purpose:
#
# Author:      yuboli
#
# Created:     04/05/2017
# Copyright:   (c) yuboli 2017
# Licence:     <your licence>
#-------------------------------------------------------------------------------

from USTAF.ui import groupEditor_ui
from PyQt4 import QtGui, QtCore
from group import Group

class GroupEditor(QtGui.QDialog, groupEditor_ui.Ui_GroupEditorDialog):
    def __init__(self, parent, server, group=None):
        QtGui.QDialog.__init__(self)
        self.parent = parent
        if not group:
            self.group = Group(server)
        else:
             self.group = group

        self.setupUi(self)
        self.GroupNamelineEdit.setText(self.group.group_name)
        self.GroupNameTextBrowser.setText(repr(self.group.group_info))

    def accept(self):
        if self.parent.server.hasGroup(self.group.group_id):
            pass
        else:
            self.parent.server.addGroup(self.group)
        self.group.group_name = str(self.GroupNamelineEdit.text())
        self.group.group_info = eval(str(self.GroupNameTextBrowser.toPlainText()))
        QtGui.QDialog.accept(self)

    def reject(self):
        QtGui.QDialog.reject(self)
