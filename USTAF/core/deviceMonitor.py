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
from USTAF.ui import deviceMonitor_ui
from caseInfo import casePropertyWindow
from runInfo import runInfoWindow
from PyQt4 import QtGui, QtCore
import os, sys
from logger import LOGGER
import traceback

class DeviceMonitor(QtGui.QMainWindow, deviceMonitor_ui.Ui_MainWindow):
    def __init__(self, mw, dut):
        QtGui.QMainWindow.__init__(self, mw)
        self.setupUi(self)
        self.setWindowTitle(dut.dut_name)
        self.dut = dut

        '''
        Models
        '''
        self.senarioTreeViewModel = QtGui.QStandardItemModel(self.senarioTreeView)
        self.senarioTreeView.setModel(self.senarioTreeViewModel)
        self.senarioTreeView.setSortingEnabled(True)

        self.queueTreeViewModel = QtGui.QStandardItemModel(self.queueTreeView)
        self.queueTreeView.setModel(self.queueTreeViewModel)

        '''
        signal & slot
        '''
        self.connect(self.actionAddScenario, QtCore.SIGNAL("triggered(bool)"), self.addScenario)
        self.connect(self.senarioTreeView, QtCore.SIGNAL("customContextMenuRequested(QPoint)"), self.senarioTreeMenuInit)
        self.connect(self.queueTreeView, QtCore.SIGNAL("customContextMenuRequested(QPoint)"),self.queueTreeViewMenuInit)
        self.connect(self.actionCaseDetails, QtCore.SIGNAL("triggered(bool)"), self.caseDetails)
        self.connect(self.actionRemoveCase, QtCore.SIGNAL("triggered(bool)"), self.removeCase)
        self.connect(self.actionRemoveScenario, QtCore.SIGNAL("triggered(bool)"), self.removeScenario)
        self.connect(self.actionAddToExecutionQueue, QtCore.SIGNAL("triggered(bool)"), self.addToQueue)
        self.connect(self.actionRun, QtCore.SIGNAL("triggered(bool)"), self.startRunner)
        self.connect(self.actionPause, QtCore.SIGNAL("triggered(bool)"), self.pauseRunner)
        self.connect(self.dut.task_runner, self.dut.task_runner.test_result_change, self.testResultChange, QtCore.Qt.UniqueConnection)
        self.connect(self.dut.task_runner, self.dut.task_runner.task_queue_change, self.testQueueChange, QtCore.Qt.UniqueConnection)
        self.connect(self.actionCancelCurrentTask, QtCore.SIGNAL("triggered(bool)"), self.cancelCurrentTaskUI)
        self.connect(self.actionClearTaskQueue, QtCore.SIGNAL("triggered(bool)"),self.clearTaskQueueUI)
        self.connect(self.actionClearResults, QtCore.SIGNAL("triggered(bool)"), self.clearResultsUI)
        self.connect(self.senarioTreeView, QtCore.SIGNAL("doubleClicked(QModelIndex)"), self.launchRunInfoWindow)
        self.connect(self.actionRemoveFromQueue, QtCore.SIGNAL("triggered(bool)"), self.removeTaskFromQueue)

        '''
        Icon init
        '''
        if self.dut.task_runner.b_started:
            self.actionRun.setDisabled(True)
            self.actionPause.setEnabled(True)
        else:
            self.actionRun.setEnabled(True)
            self.actionPause.setDisabled(True)

        '''
        load dut stuff
        '''
        self._refreshUI()

    def cancelCurrentTaskUI(self):
        if self.dut and self.dut.task_runner:
            self.dut.task_runner.cancelCurrentTaskUI()
        else:
            LOGGER.warning("DUT or task runner is not started!")

    def clearTaskQueueUI(self):
        if self.dut and self.dut.task_runner:
            self.dut.task_runner.clearTaskQueueUI()
        else:
            LOGGER.warning("DUT or task runner is not started!")

    def clearResultsUI(self):
        self.clearTaskQueueUI()
        selected_index = self.senarioTreeView.selectedIndexes()[0]
        item = self.senarioTreeViewModel.itemFromIndex(selected_index)
        if item and not item.parent():
            scenario_id = str(item.data().toPyObject())
            scenario = self.dut.getScenariobyID(scenario_id)
            if scenario:
                scenario.clearAllResults()
                self._refreshUI()

    def pauseRunner(self):
        if self.dut.task_runner.b_started:
            self.dut.pauseRunner()
            self.actionRun.setEnabled(True)
            self.actionPause.setDisabled(True)

            #self.self.dut.task_runner.b_started = False
            #self.dut.task_runner.scenario_level_pause = True
            LOGGER.critical("Pause task runner")

    def startRunner(self):
        if not self.dut.task_runner.b_started:
            self.dut.startRunner()

            self.actionRun.setDisabled(True)
            self.actionPause.setEnabled(True)

            # self.self.dut.task_runner.b_started = True
            # UI level unlock all the locks
            self.dut.task_runner.scenario_level_pause = False
            self.dut.task_runner.emit(self.dut.task_runner.fetch_a_task)
            LOGGER.debug("Start task runner")

    def caseDetails(self):
        try:
            item = None
            for selected_index in self.senarioTreeView.selectedIndexes():
                item = self.senarioTreeViewModel.itemFromIndex(selected_index)
                break
            if item and item.parent():
                scenario_id = str(item.parent().data().toPyObject())
                testcase_id = str(item.data().toPyObject())
                testcase = self.dut.getScenariobyID(scenario_id).case(id=testcase_id)
                if testcase:
                    _g_ui = casePropertyWindow(testcase)
                    _g_ui.exec_()
        except Exception,e:
            LOGGER.error(traceback.format_exc())

    def removeTaskFromQueue(self):
        try:
            case_ids, cases = self.dut.task_queue.list()
            for selected_index in self.queueTreeView.selectedIndexes():
                item = self.queueTreeViewModel.itemFromIndex(selected_index)
                target_case_id = str(item.data().toPyObject())
                if target_case_id in case_ids:
                    self.dut.task_queue.remove(target_case_id)
                else:
                    if str(item.text()) == self.dut.task_runner.cur_task.name:
                        self.cancelCurrentTaskUI()
            self._refreshUI()
        except Exception, e:
            LOGGER.error(traceback.format_exc())

    def launchRunInfoWindow(self, index):
        try:
            item = self.senarioTreeViewModel.itemFromIndex(index)
            if item and item.parent() and item.parent().parent():
                scenario_id = str(item.parent().parent().data().toPyObject())
                testcase_id = str(item.parent().data().toPyObject())
                testcase = self.dut.getScenariobyID(scenario_id).case(id=testcase_id)
                run_id = item.data().toPyObject()
                run = testcase.getRun(run_id)
                if run:
                    _g_ui = runInfoWindow(run)
                    _g_ui.exec_()
        except Exception,e:
            LOGGER.error(traceback.format_exc())

    def removeCase(self):
        pass

    def removeScenario(self):
        for selected_index in self.senarioTreeView.selectedIndexes():
            item = self.senarioTreeViewModel.itemFromIndex(selected_index)
            break
        scenario_id = str(item.data().toPyObject())
        scenario = self.dut.getScenariobyID(scenario_id)
        if self.dut.task_runner and self.dut.task_runner.cur_scenario and \
                self.dut.task_runner.cur_scenario.scenario_name == scenario.scenario_name:
                LOGGER.debug("Warning could not remove testsuite:\
                %s, as it is running, please cancel it firstly", scenario.scenario_name)
        else:
            self.dut.removeTestScenario(scenario)
            self._refreshScenarioViewUI()
            LOGGER.debug("Remove testsuite: %s", scenario.scenario_name)

    def testResultChange(self):
        self._refreshUI()

    def testQueueChange(self):
        self._refreshScenarioViewUI()
        self._refreshQueueUI()

    def addToQueue(self):
        for selected_index in self.senarioTreeView.selectedIndexes():
            item = self.senarioTreeViewModel.itemFromIndex(selected_index)
            if item.parent() is None:
                scenario_id = str(item.parent().data().toPyObject())
                self.dut.addTestScenarioToQueue(scenario_id)
            else:
                scenario_id = str(item.parent().data().toPyObject())
                testcase_id = str(item.data().toPyObject())
                self.dut.addTestcaseToQueue(scenario_id, testcase_id)

        self._refreshQueueUI()

    def addScenario(self,):
        test_suite_file_list = QtGui.QFileDialog.getOpenFileNames(self, "Add Test Suite")
        if len(test_suite_file_list):
            self.scenario_path = str(test_suite_file_list[0])
            for i in range(len(test_suite_file_list)):
                test_suite_file = test_suite_file_list[i]
                if os.path.isfile(test_suite_file):
                    self.dut.addTestScenario(str(test_suite_file))
                    self._refreshScenarioViewUI()
                    LOGGER.debug("Add testsuite: %s", test_suite_file)


    def senarioTreeMenuInit(self, point):
        try:
            _contextMenu = QtGui.QMenu()
            _index = self.senarioTreeView.indexAt(point)
            _i = self.senarioTreeViewModel.itemFromIndex(_index)
            if _i and _i.parent() is None:
                _contextMenu.addAction(self.actionRemoveScenario)
                _contextMenu.addAction(self.actionClearResults)
            elif _i and _i.parent() and _i.parent().parent() is None:
                _contextMenu.addAction(self.actionRemoveCase)
                _contextMenu.addAction(self.actionAddToExecutionQueue)
                _contextMenu.addAction(self.actionCaseDetails)
            elif _i and _i.parent() and _i.parent().parent():
                pass

            _contextMenu.exec_(self.senarioTreeView.mapToGlobal(point))

        except Exception, e:
            LOGGER.error(str(e))

    def queueTreeViewMenuInit(self, point):
        try:
            _contextMenu = QtGui.QMenu()
            _index = self.queueTreeView.indexAt(point)
            _i = self.queueTreeViewModel.itemFromIndex(_index)
            if _i:
                _contextMenu.addAction(self.actionRemoveFromQueue)
            _contextMenu.exec_(self.queueTreeView.mapToGlobal(point))
        except Exception, e:
            LOGGER.error(str(e))

    def _refreshUI(self):
        self._refreshScenarioViewUI()
        self._refreshQueueUI()

    def _refreshQueueUI(self):
        self.queueTreeViewModel.clear()
        doing_icon = QtGui.QIcon(QtGui.QPixmap(":icons/icons/running.png"))
        todo_icon = QtGui.QIcon(QtGui.QPixmap(":icons/icons/wait.png"))
        # under execution case
        if self.dut.task_runner.cur_task:
            case_item = QtGui.QStandardItem(doing_icon, QtCore.QString(self.dut.task_runner.cur_task.name))
            case_item.setData(QtCore.QVariant(self.dut.task_runner.cur_task.case_id))
            self.queueTreeViewModel.appendRow(case_item)

        # use deep copy of the queue
        case_ids, cases = self.dut.task_queue.list()
        for case_id in case_ids:
            case_item = QtGui.QStandardItem(todo_icon, QtCore.QString(cases[case_id].name))
            case_item.setData(QtCore.QVariant(case_id))
            self.queueTreeViewModel.appendRow(case_item)

    def _refreshScenarioViewUI(self):
        self.senarioTreeViewModel.clear()
        self.senarioTreeView.setSortingEnabled(True)
        _scenario_icon = QtGui.QIcon(QtGui.QPixmap(":icons/icons/scenario.png"))
        _case_not_run_icon = QtGui.QIcon(QtGui.QPixmap(":icons/icons/case-not-run.png"))
        _case_pass_icon = QtGui.QIcon(QtGui.QPixmap(":icons/icons/case-pass.png"))
        _case_rerun_pass_icon = QtGui.QIcon(QtGui.QPixmap(":icons/icons/rerun-pass.png"))
        _case_fail_icon = QtGui.QIcon(QtGui.QPixmap(":icons/icons/case-fail.png"))
        _case_question_icon = QtGui.QIcon(QtGui.QPixmap(":icons/icons/case-question.png"))
        _case_doing_icon = QtGui.QIcon(QtGui.QPixmap(":icons/icons/running.png"))
        _case_todo_icon = QtGui.QIcon(QtGui.QPixmap(":icons/icons/wait.png"))

        case_exec_ids, cases = self.dut.task_queue.list()
        case_id_list = [cases[_].case_id for _ in case_exec_ids]

        for scenario in self.dut.scenarios():
            scenario_item = QtGui.QStandardItem(_scenario_icon, QtCore.QString(scenario.scenario_name))
            scenario_item.setData(QtCore.QVariant(scenario.scenario_id))
            self.senarioTreeViewModel.appendRow(scenario_item)
            for case in scenario.cases():
                _case_icon = _case_not_run_icon
                case_item = QtGui.QStandardItem(_case_icon, QtCore.QString(case.name))
                _pass_count = 0
                _fail_count = 0
                b_pure = True
                for run in case.runs():
                    """
                    NotRun =     0b00000000
                    TBD =        0b00000001
                    Fail =       0b00000010
                    Pass =       0b00000100
                    ReRunPass =  0b00001000
                    ReAddPass =  0b00010000
                    RepeatPass = 0b00100000
                    Bypass =     0b01000000
                    AlwaysPass = 0b10000000
                    """
                    _run_icon = _case_not_run_icon

                    if run.result == run.NotRun:
                        _fail_count += 1
                    elif run.result == run.Fail:
                        _run_icon = _case_fail_icon
                        _fail_count += 1
                    elif run.result == run.Pass:
                        _run_icon = _case_pass_icon
                        _pass_count += 1
                    elif run.result == run.ReRunPass:
                        _run_icon = _case_rerun_pass_icon
                        b_pure = False
                        _pass_count += 1
                    elif run.result == run.AlwaysPass:
                        _run_icon = _case_pass_icon
                        _pass_count += 1
                    elif run.result == run.ReAddPass:
                        _run_icon = _case_pass_icon
                        _pass_count += 1

                    run_item = QtGui.QStandardItem(_run_icon, QtCore.QString(run.run_id))
                    run_item.setData(QtCore.QVariant((run.run_id)))
                    case_item.appendRow(run_item)

                if _fail_count > _pass_count:
                    _case_icon = _case_fail_icon

                elif _pass_count > 0 and _fail_count == 0 and b_pure:
                    _case_icon = _case_pass_icon
                elif _pass_count > _fail_count and (_fail_count > 0 or not b_pure):
                    _case_icon = _case_question_icon
                elif case.case_id in case_id_list:
                    _case_icon = _case_todo_icon

                if self.dut.task_runner.cur_task:
                    if self.dut.task_runner.cur_task.case_id == case.case_id:
                        case_item.setIcon(_case_doing_icon)
                    else:
                        case_item.setIcon(_case_icon)
                else:
                    case_item.setIcon(_case_icon)

                case_item.setData(QtCore.QVariant(case.case_id))
                scenario_item.appendRow(case_item)


    def closeEvent(self, *args, **kwargs):
        self.disconnect(self.dut.task_runner, self.dut.task_runner.test_result_change, self.testResultChange)
        self.disconnect(self.dut.task_runner, self.dut.task_runner.task_queue_change, self.testQueueChange)
        import gc
        gc.collect()
        self.close()
















