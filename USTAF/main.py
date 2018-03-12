#-------------------------------------------------------------------------------
# Name:        main.py
# Purpose:
#
# Author:      yuboli
#
# Created:     02/05/2017
# Copyright:   (c) yuboli 2017
# Licence:     lybroman@hotmail.com
#-------------------------------------------------------------------------------
import sys
from PyQt4 import QtGui
import USTAF.core.logger
from USTAF.core.server import Server
from USTAF.core.mainWindow import MainWindow
import argparse

def main():
    app = QtGui.QApplication(sys.argv)
    server = Server()
    parser = argparse.ArgumentParser(description="USTAF parser")
    parser.add_argument('--config', type=str, default='')
    args = parser.parse_args()
    mainWin = MainWindow(server, args)
    mainWin.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()