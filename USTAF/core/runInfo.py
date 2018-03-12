#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      yuboli
#
# Created:     08/05/2017
# Copyright:   (c) yuboli 2017
# Licence:     <your licence>
#-------------------------------------------------------------------------------
from USTAF.ui import run_ui
from PyQt4 import QtGui, QtCore
from USTAF.core.run import Run
import os, sys
from logger import LOGGER

class runInfoWindow(QtGui.QDialog, run_ui.Ui_Dialog):
    def __init__(self, run):
        QtGui.QDialog.__init__(self)
        self.setupUi(self)
        self.run = run

        self.RunResultEventModel = QtGui.QStandardItemModel(self.resultandEventTableView)
        self.resultandEventTableView.setModel(self.RunResultEventModel)

        name_item = QtGui.QStandardItem(QtCore.QString("%0").arg("Run Result:"))
        _t = ''
        for key, value in Run.Results.items():
            if type(key) == int and run.result & key > 0:
                _t += '[{}]'.format(value)
        value_item = QtGui.QStandardItem(QtCore.QString("%0").arg(_t))
        self.RunResultEventModel.appendRow([name_item, value_item])

        name_item = QtGui.QStandardItem(QtCore.QString("%0").arg("Run Event:"))
        _t = ''
        for key, value in Run.Event.items():
            if type(key) == int and run.event & key > 0:
                _t += '[{}]'.format(value)
        value_item = QtGui.QStandardItem(QtCore.QString("%0").arg(_t))
        self.RunResultEventModel.appendRow([name_item, value_item])

        #get std logs
        self.stdTextEditor.setText(self.run.std_out_err)

        _l = ''
        for _ in self.run.error_log:
            _l += '-*' * 30 + '\r\n' + repr(_) + '\r\n'

        self.errorLogTextEdit.setText(_l)








