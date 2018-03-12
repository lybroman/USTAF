from USTAF.ui import quit_ui
from PyQt4 import QtGui, QtCore
import pickle, os

class QuitWindow(QtGui.QDialog, quit_ui.Ui_Dialog):
    def __init__(self, server_config):
        QtGui.QDialog.__init__(self)
        self.setupUi(self)
        self.server_config = server_config

    def accept(self):
        config_file = QtGui.QFileDialog.getSaveFileName(self, "Select a configuration pickle file", "/home/untitled.pickle", "*.pickle")
        with open(str(config_file), 'w') as f:
            pickle.dump(self.server_config, f)
        QtGui.QDialog.accept(self)

    def reject(self):
        QtGui.QDialog.reject(self)