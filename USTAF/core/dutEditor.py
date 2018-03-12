#-------------------------------------------------------------------------------
# Name:        dutEditor
# Purpose:
#
# Author:      yuboli
#
# Created:     05/05/2017
# Copyright:   (c) yuboli 2017
# Licence:     <your licence>
#-------------------------------------------------------------------------------

from USTAF.ui import dut_ui
from PyQt4 import QtGui, QtCore
from dut import DUT


class DutEditor(QtGui.QDialog, dut_ui.Ui_Dialog):
    def __init__(self, parent):
        QtGui.QDialog.__init__(self)
        self.parent = parent

        _selected_index = self.parent.groupTreeView.selectedIndexes()[0]
        _item = self.parent.groupTreeModel.itemFromIndex(_selected_index)

        if not _item.parent():
            '''
            Add new Dut
            '''
            _group_id = str(_item.data().toString())
            _group = self.parent.server.group(_group_id)
            self.group = _group
            self.dut = DUT(server_config=_group.server_config)
        else:
            '''
            Configure Dut
            '''
            _group_id = str(_item.parent().data().toString())
            _group = self.parent.server.group(_group_id)
            self.group = _group
            self.dut = _group.dut(str(_item.data().toString()))

        self.setupUi(self)
        self.DeviceNamelineEdit.setText(self.dut.dut_name)
        self.DeviceIDlineEdit.setText(self.dut.dut_ip)
        self.SlaveDeviceNameLineEdit.setText(self.dut.slave_dut_name)
        self.SlaveDeviceIDLineEdit.setText(self.dut.slave_dut_ip)
        self.ProjectCodeLineEdit.setText(self.dut.project_code)
        self.PlatformLineEdit.setText(self.dut.platform)
        self.SubPlatformLineEdit.setText(self.dut.sub_platform)

        if self.dut.CIT in self.dut.test_type:
            self.radioButtonCIT.setChecked(True)
        else:
            self.radioButtonCIT.setChecked(False)

        if self.dut.PIT in self.dut.test_type:
            self.radioButtonPIT.setChecked(True)
        else:
            self.radioButtonPIT.setChecked(False)

        if self.dut.FULL in self.dut.test_type:
            self.radioButtonFULL.setChecked(True)
        else:
            self.radioButtonFULL.setChecked(False)

        if self.dut.PV in self.dut.branch:
            self.radioButtonPV.setChecked(True)
        else:
            self.radioButtonPV.setChecked(False)

        if self.dut.OTM in self.dut.branch:
            self.radioButtonOTM.setChecked(True)
        else:
            self.radioButtonOTM.setChecked(False)

        index = 0
        for _g in self.parent.server.groups():
            self.DeviceGroupComboBox.addItem(_g.group_name)
            if _g.group_name == self.group.group_name:
                self.DeviceGroupComboBox.setCurrentIndex(index)
            index += 1
        self.DeviceInfoTextEdit.setText(repr(self.dut.basic_info))

    def accept(self):
        self.dut.dut_name = str(self.DeviceNamelineEdit.text())
        self.dut.project_code = str(self.ProjectCodeLineEdit.text())
        self.dut.platform = str(self.PlatformLineEdit.text())
        self.dut.sub_platform = str(self.SubPlatformLineEdit.text())
        if self.dut.dut_ip != str(self.DeviceIDlineEdit.text()):
            self.dut.changeIP(str(self.DeviceIDlineEdit.text()))

        self.dut.test_type = []
        self.dut.branch = []
        if self.radioButtonCIT.isChecked():
            self.dut.test_type.append(self.dut.CIT)
        if self.radioButtonPIT.isChecked():
            self.dut.test_type.append(self.dut.PIT)
        if self.radioButtonFULL.isChecked():
            self.dut.test_type.append(self.dut.FULL)
        if self.radioButtonPV.isChecked():
            self.dut.branch.append(self.dut.PV)
        if self.radioButtonOTM.isChecked():
            self.dut.branch.append(self.dut.OTM)

        self.dut.basic_info = eval(str(self.DeviceInfoTextEdit.toPlainText()))
        for _g in self.parent.server.groups():
            if _g.group_name == str(self.DeviceGroupComboBox.currentText()):
                if self.dut.group and self.dut.group.group_name != _g.group_name:
                    self.dut.exchangeGroup(_g)
                elif self.dut.group and self.dut.group.group_name == _g.group_name:
                    pass
                else:
                    _g.addDUT(self.dut)
                break

        QtGui.QDialog.accept(self)

    def reject(self):
        QtGui.QDialog.reject(self)