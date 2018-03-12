#-------------------------------------------------------------------------------
# Name:        mainWindow.py
# Purpose:
#
# Author:      yuboli
#
# Created:     04/05/2017
# Copyright:   (c) yuboli 2017
# Licence:     <your licence>
#-------------------------------------------------------------------------------

from USTAF.ui import mainWindow_ui
from USTAF.core import logger
from PyQt4 import QtCore, QtGui
from PyQt4.QtGui import QTreeView
from PyQt4.QtCore import QPoint
from group import Group
from dut import DUT
from scenario import Scenario
from groupEditor import GroupEditor
from dutEditor import DutEditor
from deviceMonitor import DeviceMonitor
from configEditor import ConfigEditor
import types, time, os, sys, json
import traceback
import quitWindow
import pickle


class MainWindow(QtGui.QMainWindow, mainWindow_ui.Ui_MainWindow):
    def __init__(self, server, args):
        QtGui.QMainWindow.__init__(self)
        self.server = server
        self.setupUi(self)
        self.__dragged_dut = None
        logger.LOGGER.config()

        '''
        models
        '''
        self.groupTreeModel = QtGui.QStandardItemModel(0, 2, self.groupTreeView)
        self.groupTreeModel.setHorizontalHeaderLabels(['Hierarchy', 'Device ID', 'Status'])
        self.groupTreeView.setModel(self.groupTreeModel)
        self.groupTreeView.setColumnWidth(0, 150)
        self.groupTreeView.setColumnWidth(1, 150)
        self.groupTreeView.setSortingEnabled(True)

        '''
        signal & slot definitions
        '''
        self.connect(logger.LOGGER, logger.LOGGER.update_log, self.update_log)
        self.connect(self.actionCreateGroup, QtCore.SIGNAL("triggered(bool)"), self.createNewGroup)
        self.connect(self.actionAddNewDut, QtCore.SIGNAL("triggered(bool)"), self.addNewDut)
        self.connect(self.actionOpenDutView, QtCore.SIGNAL("triggered(bool)"), self.openDutWindow)
        self.connect(self.actionRefresh, QtCore.SIGNAL("triggered(bool)"), self.refreshDutStatus)
        self.connect(self.actionConfigureDut, QtCore.SIGNAL("triggered(bool)"), self.configureDut)
        self.connect(self.groupTreeView, QtCore.SIGNAL("doubleClicked(QModelIndex)"), self.editGroup)
        self.connect(self.groupTreeView, QtCore.SIGNAL("customContextMenuRequested(QPoint)"), self.groupManagementMenuInit)

        self.connect(self.actionLoadWorkSpace, QtCore.SIGNAL("triggered(bool)"), self.loadWorkSpace)
        self.connect(self.actionSaveWorkSpace, QtCore.SIGNAL("triggered(bool)"), self.saveWorkSpace)

        self.connect(self.actionConfigServer, QtCore.SIGNAL("triggered(bool)"), self.configServer)

        self.connect(self.actionStartListener, QtCore.SIGNAL("triggered(bool)"), self.startListener)

        self.args = args
        if args.config:
            with open(args.config, 'r') as f:
                config_all = pickle.load(f)
                work_space = config_all["workspace"]
                if work_space:
                    self.loadWorkSpacefromConfig(work_space)
                    self.server.updateConfig(config_all)
                    self.server.work_space_file = work_space
        self._refreshUI()

        '''
        UI drag and drop event overwrite
        '''
        def dropEvent(tree_view, e):
            try:
                _index = tree_view.indexAt(QPoint(e.pos().x(), e.pos().y()))
                _i = self.groupTreeModel.itemFromIndex(_index)
                if _i and _i.parent() is None and self.__dragged_dut:
                    _index = tree_view.indexAt(QPoint(e.pos().x(), e.pos().y()))
                    _g = self.groupTreeModel.itemFromIndex(_index)
                    _group_id = str(_g.data().toPyObject())
                    _group = self.server.group(_group_id)
                    self.__dragged_dut.exchangeGroup(_group)
                    QTreeView.dropEvent(tree_view, e)
            except Exception, e:
                logger.LOGGER.error(str(e))
            finally:
                self._refreshUI()

        def dragEnterEvent(tree_view, e):
            try:
                _index = tree_view.indexAt(QPoint(e.pos().x(), e.pos().y()))
                _i = self.groupTreeModel.itemFromIndex(_index)
                if _i and _i.parent():
                    _g = _i.parent()
                    _group_id = str(_g.data().toPyObject())
                    _group = self.server.group(_group_id)
                    self.__dragged_dut = _group.dut(str(_i.data().toPyObject()))
                    print '***', str(self.__dragged_dut.dut_name)
                    QTreeView.dragEnterEvent(tree_view, e)
                else:
                    print 'no item dragged'
            except Exception,e:
                print 'error', str(e)
            finally:
                pass

        #self.groupTreeView.dropEvent = types.MethodType(dropEvent, self.groupTreeView)
        #self.groupTreeView.dragEnterEvent = types.MethodType(dragEnterEvent, self.groupTreeView)

    def startListener(self):
        if not self.server.sock_listener.launched:
            if self.server.sock_listener.init():
                self.server.sock_listener.start()
        else:
            logger.LOGGER.warning("Socket listener has already been started!")

    def configServer(self):
        logger.LOGGER.debug('+ config server')
        _g_ui = ConfigEditor(self.server, logger.LOGGER)
        _g_ui.exec_()
        logger.LOGGER.debug('- config server')

    def update_log(self, record):
        levelno = record.levelno
        if levelno >= logger.level_name("CRITICAL"):
            color_str = '<div style="color:red">%s</div>' # red
        elif levelno >= logger.level_name("ERROR"):
            color_str = '<div style="color:red">%s</div>' # red
        elif levelno >= logger.level_name("WARN"):
            color_str = '<div style="color:orange">%s</div>' # orange
        elif levelno >= logger.level_name("INFO"):
            color_str = '<div style="color:black">%s</div>' # black
        elif levelno >= logger.level_name("DEBUG"):
            color_str = '<div style="color:gray">%s</div>' # gray
        else:
            color_str = '<div style="color:black">%s</div>' # black
        msg = color_str % ("[ %s ][ %s ][ %s:%s ] %s" % (time.strftime("%m-%d %H:%M:%S"), logger.level_name(levelno), record.filename, record.lineno, record.getMessage()))
        self.logTextEdit.append(msg)

    def loadWorkSpacefromConfig(self, work_space_file):
        try:
            if os.path.isfile(str(work_space_file)):
                self.server.clearGroups()
                work_space = json.load(open(str(work_space_file)))
                for g in work_space["groups"]:
                    new_g = Group(self.server, g["group_name"])
                    new_g.group_info = g["group_info"]
                    for d in g["duts"]:
                        new_d = DUT(d["dut_name"], d["dut_ip"], None, self.server.server_config)
                        new_d.setBranch(d["branch"])
                        new_d.setTestType(d["test_type"])
                        new_d.project_code = d["project_code"]
                        new_d.platform = d["platform"]
                        new_d.sub_platform = d["sub_platform"]
                        for sce in d["scenarios"]:
                            new_d.addTestScenario(sce["path"])
                        new_g.addDUT(new_d)
                    self.server.addGroup(new_g)
                self._refreshUI()
        except:
            logger.LOGGER.error(traceback.format_exc())

        self.server.work_space_file = str(work_space_file)

    def loadWorkSpace(self):
        """
        - Group
          - DUT
            - Scenario
              -- case
        """
        work_space_file = QtGui.QFileDialog.getOpenFileName(self, "Select a work space JSON file")
        if os.path.isfile(str(work_space_file)):
            self.server.clearGroups()
            work_space = json.load(open(str(work_space_file)))
            for g in work_space["groups"]:
                new_g = Group(self.server, g["group_name"])
                new_g.group_info = g["group_info"]
                for d in g["duts"]:
                    new_d = DUT(d["dut_name"], d["dut_ip"], None, self.server.server_config)
                    new_d.setBranch(d["branch"])
                    new_d.setTestType(d["test_type"])
                    new_d.project_code = d["project_code"]
                    new_d.platform = d["platform"]
                    new_d.sub_platform = d["sub_platform"]
                    for sce in d["scenarios"]:
                        new_d.addTestScenario(sce["path"])
                    new_g.addDUT(new_d)
                self.server.addGroup(new_g)
            self._refreshUI()

        self.server.work_space_file = str(work_space_file)


    def saveWorkSpace(self):
        """
        - Group
          - DUT
            - Scenario
              -- case
        """
        work_space_file = QtGui.QFileDialog.getSaveFileName(self, "Save work space as JSON file", "/home/untitled.js", "*.js")
        work_space = {"groups": []}
        for group in self.server.groups():
            g = {"group_name": "", "group_info": {}, "duts": []}
            g["group_name"] = group.group_name
            g["group_info"] = group.group_info
            for dut in group.duts():
                d = {"dut_name": "", "dut_ip": "", "scenarios": [], "project_code": "", "test_type": [], "branch": []}
                d["dut_name"] = dut.dut_name
                d["dut_ip"] = dut.dut_ip
                d["test_type"] = dut.getTestType()
                d["branch"] = dut.getBranch()
                d["project_code"] = dut.project_code
                d["platform"] = dut.platform
                d["sub_platform"] = dut.sub_platform
                for scenario in dut.scenarios():
                    s = {"scenario_name": "", "path": ""}
                    s["scenario_name"] = scenario.scenario_name
                    s["path"] = scenario.path
                    if os.path.isfile(s["path"]):
                        d["scenarios"].append(s)
                g["duts"].append(d)
            work_space["groups"].append(g)


        f = open(str(work_space_file), 'w')
        json.dump(work_space, f, indent=4)

        self.server.work_space_file = str(work_space_file)

    def createNewGroup(self):
        logger.LOGGER.debug('+ create a new group')
        _g_ui = GroupEditor(self, self.server)
        _g_ui.exec_()
        self._refreshUI()
        logger.LOGGER.debug('- create a new group')

    def editGroup(self, index):
        _i = self.groupTreeModel.itemFromIndex(index)
        if not _i.parent():
            _group_id = str(_i.data().toPyObject())
            _g = self.server.group(_group_id)
            _g_ui = GroupEditor(self, self.server, _g)
            _g_ui.exec_()
            self._refreshUI()

    def groupManagementMenuInit(self, point):
        try:
            _contextMenu = QtGui.QMenu()
            _index = self.groupTreeView.indexAt(point)
            _i = self.groupTreeModel.itemFromIndex(_index)
            if _i and _i.parent() is None:
                _contextMenu.addAction(self.actionAddNewDut)
            elif _i:
                _contextMenu.addAction(self.actionConfigureDut)
                _contextMenu.addAction(self.actionRefresh)
                _contextMenu.addAction(self.actionOpenDutView)

            _contextMenu.exec_(self.groupTreeView.mapToGlobal(point))

        except Exception, e:
            logger.LOGGER.error(str(e))

    def addNewDut(self):
        _d_ui = DutEditor(self)
        _d_ui.exec_()
        self._refreshUI()

    def configureDut(self):
        _d_ui = DutEditor(self)
        _d_ui.exec_()
        self._refreshUI()

    def openDutWindow(self):
        _selected_index = self.groupTreeView.selectedIndexes()[0]
        _dut_item = self.groupTreeModel.itemFromIndex(_selected_index)
        _group_item = _dut_item.parent()
        _group = self.server.group(str(_group_item.data().toString()))
        _dut = _group.dut(str(_dut_item.data().toString()))
        _d_ui = DeviceMonitor(self, _dut)
        _d_ui.show()

    def refreshDutStatus(self):
        _selected_index = self.groupTreeView.selectedIndexes()[0]
        _dut_item = self.groupTreeModel.itemFromIndex(_selected_index)
        _group_item = _dut_item.parent()
        _group = self.server.group(str(_group_item.data().toString()))
        _dut = _group.dut(str(_dut_item.data().toString()))
        _dut.refreshStatus()
        self._refreshUI()

    def _refreshUI(self):
        self.groupTreeModel.clear()
        '''
        Group item
        '''
        self.groupTreeModel.setHorizontalHeaderLabels(['Hierarchy', 'Device ID', 'Status'])
        self.groupTreeView.setColumnWidth(0, 150)
        self.groupTreeView.setColumnWidth(1, 150)
        self.groupTreeView.setSortingEnabled(True)

        _group_icon = QtGui.QIcon(QtGui.QPixmap(":icons/icons/cluster.png"))
        _device_icon = QtGui.QIcon(QtGui.QPixmap(":icons/icons/device.png"))
        for group in self.server.groups():
            group_item = QtGui.QStandardItem(_group_icon, QtCore.QString(group.group_name))
            group_item.setData(QtCore.QVariant(group.group_id))
            self.groupTreeModel.appendRow(group_item)
            '''
            DUT item
            '''
            alive_icon = QtGui.QIcon(QtGui.QPixmap(":icons/icons/alive.png"))
            dead_icon = QtGui.QIcon(QtGui.QPixmap(":icons/icons/dead.png"))
            unknown_icon = QtGui.QIcon(QtGui.QPixmap(":icons/icons/unknown.png"))
            locked_icon = QtGui.QIcon(QtGui.QPixmap(":icons/icons/locked.png"))
            icon_dict = {DUT.STATUS_ALIVE:alive_icon, DUT.STATUS_LOST:dead_icon,
            DUT.STATUS_LOCKED:locked_icon, DUT.STATUS_UNKNOWN:unknown_icon}

            for dut in group.duts():
                dut_item = QtGui.QStandardItem(_device_icon, QtCore.QString(dut.dut_name))
                dut_item.setData(QtCore.QVariant(dut.dut_id))
                icon = icon_dict[dut.status]
                group_item.appendRow([dut_item, QtGui.QStandardItem(QtCore.QString(dut.dut_ip)), QtGui.QStandardItem(icon, QtCore.QString(dut.prettyStatus))])


    def closeEvent(self, event):
        if self.server.work_space_file:
            self.server.server_config["workspace"] = self.server.work_space_file
        else:
            self.server.server_config["workspace"] = ''
        quit_window = quitWindow.QuitWindow(self.server.server_config)
        quit_window.exec_()