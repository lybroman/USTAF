#-------------------------------------------------------------------------------
# Name:        configEditor.py
# Purpose:
#
# Author:      yuboli
#
# Created:     04/05/2017
# Copyright:   (c) yuboli 2017
# Licence:     <your licence>
#-------------------------------------------------------------------------------

from USTAF.ui import configEditor_ui
from PyQt4 import QtGui, QtCore


class ConfigEditor(QtGui.QDialog, configEditor_ui.Ui_ServerConfigDialog):
    def __init__(self, server, logger):
        QtGui.QDialog.__init__(self)
        self.__server = server
        self.__logger = logger
        self.setupUi(self)
        self.AddresslineEdit.setText(self.__server.server_config["rabbitMQ_address"])
        self.PortlineEdit.setText(str(self.__server.server_config["rabbitMQ_port"]))
        self.ColdRebootAddressLineEditor.setText(self.__server.server_config["cold_reboot_server_address"])
        self.ColdRebootPortLineEditor.setText(str(self.__server.server_config["cold_reboot_server_port"]))
        self.BaseSharePathlineEdit.setText(str(self.__server.server_config["base_share_path"]))
        self.StdLoglineEdit.setText(str(self.__server.server_config["std_log_path"]))
        self.SocketPortLineEdit.setText(str(self.__server.server_config["socket_server_port"]))

        self.LogPathlineEdit.setText(str(self.__logger.logging_config["logging_file_name"]))
        level_list = ['CRITICAL', 'ERROR', 'WARNING', 'INFO', 'DEBUG']
        self.LogFilecomboBox.addItems(level_list)
        index = level_list.index(self.__logger.logging_config["logging_file_level"])
        self.LogFilecomboBox.setCurrentIndex(index)

        self.LogStreamcomboBox.addItems(level_list)
        index = level_list.index(self.__logger.logging_config["logging_stream_level"])
        self.LogStreamcomboBox.setCurrentIndex(index)

    def accept(self):
        self.__server.server_config["rabbitMQ_address"] = str(self.AddresslineEdit.text())
        self.__server.server_config["rabbitMQ_port"] = int(str(self.PortlineEdit.text()))
        self.__server.server_config["cold_reboot_server_address"] = str(self.ColdRebootAddressLineEditor.text())
        self.__server.server_config["cold_reboot_server_port"] = int(str(self.ColdRebootPortLineEditor.text()))
        self.__server.server_config["base_share_path"] = str(self.BaseSharePathlineEdit.text())
        self.__server.server_config["std_log_path"] = str(self.StdLoglineEdit.text())
        self.__server.server_config["socket_server_port"] = int(self.SocketPortLineEdit.text())
        self.__logger.logging_config["logging_file_name"] = str(self.LogPathlineEdit.text())
        self.__logger.logging_config["logging_file_level"] = str(self.LogFilecomboBox.currentText())
        self.__logger.logging_config["logging_stream_level"] = str(self.LogStreamcomboBox.currentText())

        self.__logger.config(logging_file_name=str(self.LogPathlineEdit.text()),
                                     logging_file_level=str(self.LogFilecomboBox.currentText()),
                                     logging_stream_level=str(self.LogStreamcomboBox.currentText()))

        QtGui.QDialog.accept(self)

    def reject(self):
        QtGui.QDialog.reject(self)