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
from USTAF.ui import case_ui
from PyQt4 import QtGui, QtCore
import os, sys
from logger import LOGGER

class casePropertyWindow(QtGui.QDialog, case_ui.Ui_Dialog):
    def __init__(self, testcase):
        QtGui.QDialog.__init__(self)
        self.setupUi(self)
        self.testcase = testcase
        self.testInfoModel = QtGui.QStandardItemModel(self.casePropertyTableView)
        self.casePropertyTableView.setModel(self.testInfoModel)

        # -------------------------------------------------------------- display case properties
        name_item = QtGui.QStandardItem(QtCore.QString("%0").arg("Test Case ID:"))
        value_item = QtGui.QStandardItem(QtCore.QString("%0").arg(testcase.name))
        self.testInfoModel.appendRow([name_item, value_item])
        name_item = QtGui.QStandardItem(QtCore.QString("%0").arg("Parameters:"))
        value_item = QtGui.QStandardItem(QtCore.QString("%0").arg(testcase.parameters))
        self.testInfoModel.appendRow([name_item, value_item])
        name_item = QtGui.QStandardItem(QtCore.QString("%0").arg("Command Line:"))
        value_item = QtGui.QStandardItem(QtCore.QString("%0").arg(testcase.cmd))
        self.testInfoModel.appendRow([name_item, value_item])
        name_item = QtGui.QStandardItem(QtCore.QString("%0").arg("Dependencies:"))
        value_item = QtGui.QStandardItem(QtCore.QString("%0").arg(repr(testcase.pass_bypass)))
        self.testInfoModel.appendRow([name_item, value_item])
        name_item = QtGui.QStandardItem(QtCore.QString("%0").arg("Critical:"))
        value_item = QtGui.QStandardItem(QtCore.QString("%0").arg(testcase.critical))
        self.testInfoModel.appendRow([name_item, value_item])
        name_item = QtGui.QStandardItem(QtCore.QString("%0").arg("Fail Rerun Count:"))
        value_item = QtGui.QStandardItem(QtCore.QString("%0").arg(testcase.failrerun))
        self.testInfoModel.appendRow([name_item, value_item])
        name_item = QtGui.QStandardItem(QtCore.QString("%0").arg("Repetition Count:"))
        value_item = QtGui.QStandardItem(QtCore.QString("%0").arg(testcase.repetition))
        self.testInfoModel.appendRow([name_item, value_item])
        name_item = QtGui.QStandardItem(QtCore.QString("%0").arg("Sleep Time:"))
        value_item = QtGui.QStandardItem(QtCore.QString("%0").arg(testcase.sleep_time))
        self.testInfoModel.appendRow([name_item, value_item])
        name_item = QtGui.QStandardItem(QtCore.QString("%0").arg("Reboot after Execution:"))
        value_item = QtGui.QStandardItem(QtCore.QString("%0").arg(testcase.reboot))
        self.testInfoModel.appendRow([name_item, value_item])
        name_item = QtGui.QStandardItem(QtCore.QString("%0").arg("Always Pass:"))
        value_item = QtGui.QStandardItem(QtCore.QString("%0").arg(testcase.always_pass))
        self.testInfoModel.appendRow([name_item, value_item])
        name_item = QtGui.QStandardItem(QtCore.QString("%0").arg("Must Run:"))
        value_item = QtGui.QStandardItem(QtCore.QString("%0").arg(testcase.mustrun))
        self.testInfoModel.appendRow([name_item, value_item])
        name_item = QtGui.QStandardItem(QtCore.QString("%0").arg("env cases:"))
        value_item = QtGui.QStandardItem(QtCore.QString("%0").arg(testcase.bEnv))
        self.testInfoModel.appendRow([name_item, value_item])






