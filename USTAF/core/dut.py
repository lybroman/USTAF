#-------------------------------------------------------------------------------
# Name:        dut.py
# Purpose:
#
# Author:      yuboli
#
# Created:     04/05/2017
# Copyright:   (c) yuboli 2017
# Licence:     <your licence>
#-------------------------------------------------------------------------------
from USTAF.core.logger import LOGGER
from staf_core import *
from scenario import Scenario
import Queue
import uuid
import copy
from staf_core import StafHandle
from run import Run
import traceback, re
from USTAF.core.plugin import rabbitMQ
from USTAF.core.plugin import sock
from USTAF.core.plugin.logAnalysis import LogAnalysis
from USTAF.core.plugin.dashboard import query_error_log_from_dashboard
import threading
import json,sys, time
import gc


class Listener(QtCore.QThread):
    def __init__(self, dut):
        super(Listener, self).__init__()
        self.dut = dut

    def run(self):
        LOGGER.debug("connect task runner to fetch a task")
        self.connect(self.dut.task_runner, self.dut.task_runner.fetch_a_task, self.fetchTaskFromRabbitMQ,  QtCore.Qt.UniqueConnection)

    def fetchTaskFromRabbitMQ(self):
        try:
            '''
            if task runner queue is empty, fetch a new task from rabbit server
            1. current task is finished
            2. queue is empty
            '''
            if self.dut.task_runner.scenario_level_pause:
                LOGGER.critical("Scenario level execution is disabled")
                return
            elif self.dut.task_queue.len == 0:
                try:
                    self.dut.queue_lock.acquire()
                    task = rabbitMQ.queryTask1(self.dut.server_config, self.dut.dut_name, self.dut.project_code,
                                              self.dut.test_type, self.dut.branch)
                    if task:
                        self.dut.task_variable = task
                        self.dut.task_runner.cur_scenario = self.dut.getScenariobyName(task["scenario_name"])
                        if self.dut.task_runner.cur_scenario:
                            #LOGGER.critical('size of dut is {}'.format(sys.getsizeof(self.dut)))
                            #LOGGER.critical('size of scenario is {}'.format(sys.getsizeof(self.dut.task_runner.cur_scenario)))
                            self.dut.updateScenarioByName(task["scenario_name"])
                            self.dut.addTestScenarioToQueueByName(task["scenario_name"])
                            self.dut.task_variable["start"] = time.time()
                            self.dut.task_variable['UUID'] = task.get('trigger_id', str(uuid.uuid1()).split('-')[0])
                            self.dut.emit(self.dut.task_runner.test_result_change)

                            # ERROR_LOG_ANALYSIS
                            # query error log data base from dashboard database
                            self.dut.query_error_log_result = query_error_log_from_dashboard(
                                self.dut.task_runner.cur_scenario.platform,
                                self.dut.task_runner.cur_scenario.subversion,
                                self.dut.task_runner.cur_scenario.test_type)

                            try:
                                for local_file, remote_file in self.dut.task_runner.cur_scenario.sync_files.items():
                                    rc = self.dut.staf_handle.copy_sync_file(self.dut.dut_ip, local_file, remote_file)
                                    LOGGER.info('{} -> {} rc: {}'.format(local_file, remote_file, rc))

                                LOGGER.critical('fetch a task: {}'.format(task))
                            except:
                                LOGGER.error(traceback.format_exc())

                        else:
                            LOGGER.critical(
                                "scenario:{} not found, task : {} is not triggered".format(task["scenario_name"],
                                                                                           str(task)))
                except:
                    LOGGER.error(traceback.format_exc())
                    self.dut.query_error_log_result = ''
                finally:
                    self.dut.queue_lock.release()
        except:
            LOGGER.error(traceback.format_exc())

class TaskRunner(QtCore.QThread):

    test_result_change = QtCore.SIGNAL("test_result_change")
    runner_busy = QtCore.SIGNAL("runner_busy")
    runner_idle = QtCore.SIGNAL("runner_idle")
    task_finished = QtCore.SIGNAL("task_finished")
    fetch_a_task = QtCore.SIGNAL("fetch_a_task")
    task_queue_change = QtCore.SIGNAL("task_queue_change")

    def __init__(self, dut):
        super(TaskRunner, self).__init__()
        self.__dut_instance = dut
        self.__handle = dut.staf_handle
        self.__queue = dut.task_queue
        self.b_clear = False
        self.b_cancel_current_task = False
        self.cur_task = None
        self.cur_scenario = None
        self.b_started = False
        self.listener = Listener(self.__dut_instance)
        self.scenario_level_pause = False

    def start(self):
        LOGGER.info("DUT task runner thread for DUT %s start" % self.__dut_instance.dut_ip)
        if not self.b_started:
            QtCore.QThread.start(self)
            self.listener.start()
            self.b_started = True
        else:
            LOGGER.warning("Runner has already started!")

    def terminate(self):
        LOGGER.info("DUT task runner thread for DUT %s terminate" % self.__dut_instance.dut_ip)
        """
        still a OPEN: how to handle the termination behaviors
        """
        #self.cancelCurrentTaskUI()
        if self.b_started:
            QtCore.QThread.terminate(self)
            try:
                self.__dut_instance.queue_lock.release()
            except:
                LOGGER.debug("Lock for task queue has already been released!")
            finally:
                self.b_started = False
        else:
            LOGGER.warning("Runner has not already started!")

    def getCurrentTask(self):
        if self.__queue.len >= 0 and self.__dut_instance.task_variable:
            #return str(self.__dut_instance.task_variable)
            return self.__dut_instance.task_variable
        else:
            return None

    def getCurrentTaskDetails(self, case_name=None):
        if self.__queue.len >= 0 and self.__dut_instance.task_variable:
            _t = {}
            _t["scenario_name"] = self.__dut_instance.task_variable["scenario_name"]
            _t["details"] = []
            scenario = self.__dut_instance.getScenariobyName(self.__dut_instance.task_variable["scenario_name"])
            for case in scenario.cases():
                if not case_name:
                    _t["details"].append({"case_name" : case.name, "result" : case.result(),
                                          "total_count" : case.total_count, "pass_count" : case.pass_count})
                                         #"start_time" : time.ctime(self.__dut_instance.task_variable.get("start", time.time()))})
                elif case.name == case_name:
                    _t["details"].append({"case_name": case.name, "result": case.result(),
                                          "total_count" : case.total_count, "pass_count" : case.pass_count,
                                          "std_log" : case.std_log_otf, "error_log" : case.error_log_otf})

            return _t
        else:
            return {}

    def waitUp(self, reboot_countdown=5, reboot_times=3, duration=45):
        for i in xrange(reboot_times):
            for j in xrange(reboot_countdown):
                rc = self.__handle.ping(self.__dut_instance.dut_ip)

                if rc == 0:
                    LOGGER.debug(' DUT {} is alive'.format(self.__dut_instance.dut_ip))
                    return
                elif self.b_clear:
                    LOGGER.debug(' DUT {} is manually cleared up!'.format(self.__dut_instance.dut_ip))
                    return
                else:
                    LOGGER.debug(' DUT {} is dead, sleep for {}'.format(self.__dut_instance.dut_ip, duration))
                    time.sleep(duration)

            rc = self.coldReboot()
            if rc == 0:
                time.sleep(duration)
                return 0

        while True:
            # As the DUT might has been broken, will not keep cold-reboot
            rc = self.__handle.ping(self.__dut_instance.dut_ip)
            if rc == 0:
                LOGGER.debug(' DUT {} is alive'.format(self.__dut_instance.dut_ip))
                break
            elif self.b_clear:
                LOGGER.debug(' DUT {} is manually cleared up!'.format(self.__dut_instance.dut_ip))
                break
            else:
                LOGGER.debug(' DUT {} is dead, sleep for {}'.format(self.__dut_instance.dut_ip, duration))
                time.sleep(duration)

        LOGGER.debug("Wait dut alive - ")

    def warmReboot(self):
        if self.__dut_instance.dut_type == 'linux':
            # linux WA
            rc = self.coldReboot()
            LOGGER.warning('DUT {} trigger COLD reboot with rc: {}'.format(self.__dut_instance.dut_ip, rc))
        else:
            # windows
            rc = self.__handle.warmReboot(self.__dut_instance.dut_ip)
            LOGGER.debug('DUT {} trigger warm reboot with rc: {}'.format(self.__dut_instance.dut_ip, rc))

        return rc

    def coldReboot(self):
        try:
            skt = sock.SOCK(self.__dut_instance.server_config["cold_reboot_server_address"],
                            self.__dut_instance.server_config["cold_reboot_server_port"],
                            150)
            rc = skt.communicate(self.__dut_instance.dut_name)
            if rc and int(rc) == 0:
                LOGGER.debug('DUT {} trigger cold reboot with rc: {}'.format(self.__dut_instance.dut_ip, rc))
                return 0
            else:
                LOGGER.warning('DUT {} trigger cold reboot with rc: {}'.format(self.__dut_instance.dut_ip, rc))
                return -1
            skt.finish()
        except Exception, e:
            LOGGER.warning(traceback.format_exc())
            return -1

    def clearTaskQueue(self, b_all=False):
        LOGGER.debug('Enter clear task queue + ')
        self.__queue.clear(b_all)
        self.b_clear = False
        LOGGER.debug('Leave clear task queue - ')

    def clearTaskQueueUI(self):
        if self.__queue.len > 0:
            LOGGER.warning("Clear task queue is trigger on UI!")
            self.b_clear = True
        else:
            LOGGER.warning("Queue is empty!")

    def cancelCurrentTaskUI(self):
        if self.cur_task:
            LOGGER.warning("cancel current task {}".format(self.cur_task.name))
            self.b_cancel_current_task = True
        else:
            LOGGER.warning("no task in queue!")

    def generateReport(self, scenario):
        LOGGER.debug("All task finished, generate report.")
        self.__dut_instance.task_variable["finish"] = time.time()
        scenario.generateReport(self.__dut_instance)
        scenario.clearAllResults()
        self.__dut_instance.task_variable = {}
        self.emit(self.test_result_change)

    def runTask(self, run, case):
        """
        The most key part of the framework...
        Logic of execution and DUT status handling
        """
        try:
            '''
            Step 0. Wait Dut Up
                    this would be a BLOCK function unless manual cancellation
            '''
            self.waitUp(reboot_countdown=5, reboot_times=3)
            self.__handle.clean_process_status(self.__dut_instance.dut_ip)

            '''
            Step 1. Execute fail-rerun strategy
            '''
            if not self.b_clear or self.b_cancel_current_task:
                run.start = "%.3f" % time.time()
                for i in xrange(case.failrerun + 1):
                    '''
                    replace var
                    '''

                    if re.search('{\S*}', case.cmd):
                        for (variable, value) in self.__dut_instance.task_variable.items():
                            self.__handle.setVar(self.__dut_instance.dut_ip, variable, value)

                    _p = '{0}{3}{1}{3}{2}.log'.format(self.__dut_instance.server_config["std_log_path"], case.name, run.start, os.sep)
                    run.std_log_path.append(_p)
                    handle_id = self.__handle.startProcessAsync(self.__dut_instance.dut_ip, case.cmd, _p)

                    if handle_id != self.__handle.INVALID_HANDLE_ID:
                        '''
                        Start the Query Loop
                        '''
                        current_run_start_time = "%.3f" % time.time()
                        while True:
                            current_time = "%.3f" % time.time()
                            if float(current_time) - float(current_run_start_time) > float(case.timeout):
                                '''
                                Timeout occurred during execution
                                '''
                                # stop the process
                                LOGGER.debug("Case timeout on DUT {} ".format(self.__dut_instance.dut_ip))
                                run.result = run.Fail
                                rc = self.__handle.stopProcess(self.__dut_instance.dut_ip, handle_id)
                                LOGGER.debug("Stop the process due to timeout with rc: {} ".format(rc))
                                if rc == 0:
                                    LOGGER.debug("Stop the process successfully!")
                                else:
                                    LOGGER.warn("Failed to Stop the process!")

                                '''
                                Try warm reboot
                                '''
                                rc = self.warmReboot()
                                '''
                                Try cold reboot if warm reboot not work!
                                '''
                                if rc != 0:
                                    LOGGER.warning("Failed to trigger warm reboot, might be due to CONNECTION LOST!")
                                    rc = self.coldReboot()
                                    if rc != 0:
                                        run.event |= run.ERROR
                                    else:
                                        run.event |= run.COLD_REBOOT
                                else:
                                    run.event |= run.WARM_REBOOT

                                break
                            elif self.b_clear or self.b_cancel_current_task:
                                run.result = run.Fail
                                run.event |= run.MANUAL_CANCEL
                                # try 5(HARD CODE) times
                                for i in xrange(0,5):
                                    rc = self.__handle.stopProcess(self.__dut_instance.dut_ip, handle_id)
                                    if rc == 0:
                                        break
                                    else:
                                        time.sleep(10)
                                LOGGER.info("Manual Cancellation has been triggered!, stop process rc:{}".format(rc))
                                break
                            else:
                                (t0, t1, rc) = self.__handle.queryResultAsync(self.__dut_instance.dut_ip, handle_id)
                                if rc:
                                    rc = int(rc)
                                    if rc == 0 and i == 0:
                                        LOGGER.debug('case {} passed'.format(case.name))
                                        run.result = run.Pass
                                        break
                                    elif rc == 0 and i > 0:
                                        LOGGER.debug('case {} rerun passed'.format(case.name))
                                        run.result = run.ReRunPass
                                        run.event |= run.ReRun
                                        break
                                    elif rc == self.__handle.CONNECTION_FAILED:
                                        LOGGER.debug('case {} : CONNECTION LOST'.format(case.name))
                                        run.event |= run.CONNECTION_LOSS
                                        # might temporary network issue
                                    elif rc == self.__handle.UNEXPECTED_CONDITION:
                                        LOGGER.debug('case {} failed: UNEXPECTED CONDITION'.format(case.name))
                                        run.event |= run.ERROR
                                        run.result = run.Fail
                                        break
                                    elif rc != 0:
                                        # case failed
                                        LOGGER.debug('case {} failed'.format(case.name))
                                        run.result = run.Fail
                                        if rc == run.TIMEOUT:
                                            run.event |= run.HANG_TO
                                        elif rc == self.__handle.NO_SUCH_HANDLE_ID:
                                            LOGGER.debug('case {} failed: NO SUCH HANDLE ID'.format(case.name))
                                            run.event |= run.ERROR
                                            run.result = run.Fail

                                        # fetch error log and check regression
                                        if self.__dut_instance.dut_type != 'XXX':
                                            b_new = True
                                            try:
                                                _t = LogAnalysis(self.__dut_instance, case.platform, case.test_type, case.name,
                                                                 case.cmd)
                                                _t.parse()
                                                if _t.error_log:
                                                    run.error_log.append(_t.error_log)

                                                    # ERROR_LOG_ANALYSIS
                                                    # regression check
                                                    # check if known issue or new failure
                                                    if self.__dut_instance.query_error_log_result:
                                                        _t.query_result = self.__dut_instance.query_error_log_result
                                                        b_new = _t.is_new_bug(case, run)

                                                else:
                                                    b_new = True
                                                    run.hsd_id = 'new'
                                                    pass

                                                del _t
                                                c = gc.collect()
                                                LOGGER.debug("collect {} LogAnalysis module".format(c))

                                            except:
                                                LOGGER.error(traceback)
                                        else:
                                            LOGGER.warning('bypass log analysis for linux')

                                        break
                                    else:
                                        LOGGER.critical('unexpected condition for query results')
                                        run.event |= run.ERROR
                                        run.result = run.Fail
                                        break
                                else:
                                    LOGGER.debug('case {} still in execution...'.format(case.name))
                                    pass

                            time.sleep(3)

                        if run.result >= run.Pass:
                            LOGGER.debug('case {} passed/rerun passed'.format(case.name))
                            break
                    else:
                        LOGGER.error("Trigger test case failed due to invalid handle id!")
                        run.result = run.Fail
                        run.event |= run.ERROR

                    if self.b_clear or self.b_cancel_current_task:
                        run.event |= run.MANUAL_CANCEL
                        LOGGER.warning("Break fail rerun loop due to manual cancellation!")
                        break

            else:
                run.result = run.Fail
                run.event |= run.MANUAL_CANCEL
                LOGGER.info("Manual Cancellation has been triggered!")

            if case.bEnv and run.result == run.Fail:
                run.event |= run.ENV_FAILURE

            run.end = "%.3f" % time.time()

        except Exception,e:
            LOGGER.critical(traceback.format_exc())

    def run(self):
        '''
        there is possibility cancellation failed if triggered at the beginning...
        '''
        self.b_clear = False

        original_queue_length = -1
        current_scenario_fail_count = 0

        while True:
            c = gc.collect()
            LOGGER.debug("collect {} in run loop".format(c))

            self.b_cancel_current_task = False
            '''
            Step 0. fetch a task if queue is empty
            '''
            while self.__queue.len == 0:
                self.emit(self.fetch_a_task)
                time.sleep(1)
                if self.__queue.len == 0:
                    current_scenario_fail_count = 0
                    original_queue_length = -1
                    LOGGER.debug("No task is available in queue, dut {} is idle, sleep 15s for next query cycle!".format(self.__dut_instance.dut_name))
                    time.sleep(15)
                else:
                    current_scenario_fail_count = 0
                    original_queue_length = self.__queue.len
                    self.b_clear = False

            '''
            Step 1. Check if need clear task queue
                    Must Run cases would still be executed
            '''
            if self.b_clear:
                LOGGER.info("Current task would be cancelled...")
                try:
                    self.__dut_instance.task_variable["Interval_Cancel"] = True
                except:
                    LOGGER.warning(traceback.format_exc())

                self.clearTaskQueue()
                if self.__queue.len == 0:
                    try:
                        # make sure the fetch thread would not compete with generate report
                        self.__dut_instance.queue_lock.acquire()
                        if self.cur_scenario:
                            self.generateReport(self.cur_scenario)
                        else:
                            LOGGER.warning("Not triggered by scenario level, no report would be generated!")
                    except:
                        LOGGER.error(traceback.format_exc())
                    finally:
                        self.__dut_instance.queue_lock.release()
                        self.cur_scenario = None
                        self.emit(self.fetch_a_task)

            '''
            Step 2. Fetch next task and execute
            '''
            test_case = self.__queue.get(block=True)
            test_case.start = "%.3f" % time.time()
            '''
            refresh ui
            '''
            self.emit(self.test_result_change)
            self.cur_task = test_case

            LOGGER.debug("test case %s is under execution for DUT %s " % (test_case.name, self.__dut_instance.dut_name))

            '''
            Step 3. Execurte M repetition times
            '''
            for i in xrange(test_case.repetition):
                r = Run(test_case)
                test_case.addRun(r)
                self.emit(self.test_result_change)

                '''
                Dependency fail & PassBypass & Execute
                '''
                if len(test_case.dependencies) > 0 and not test_case.checkDependencyPass():
                    r.result = r.Fail
                    r.event = r.DEPENDENCY_FAIL
                elif len(test_case.pass_bypass) > 0 and test_case.checkPassByPass():
                    r.result = r.Bypass
                    r.event = r.PASS_BYPASS
                else:
                    '''
                    Step 4. execute the task for at most N rerun times
                    '''
                    self.runTask(r, test_case)

                    '''
                    Step 5. Check if always pass
                    '''
                    if test_case.always_pass:
                        r.result = r.AlwaysPass

                    # for each execution, reboot to clean the env!
                    if r.result >= r.Pass:
                        LOGGER.debug('case passed for current execution, no need to reboot')
                    else:
                        # fail count +1
                        if i == 0 and test_case.gating:
                            current_scenario_fail_count += 1

                        self.waitUp()
                        # did note expect a reboot if only execute once!
                        if test_case.repetition > 1 and not self.b_clear and not self.b_cancel_current_task:
                            r.event |= r.WARM_REBOOT
                            LOGGER.warn('case failed for current execution, will reboot before repetition')
                            self.warmReboot()

                    # get stdout/err log after dut is available
                    self.waitUp()
                    for ii in range(len(r.std_log_path)):
                        try:
                            log = self.__dut_instance.staf_handle.getFile(self.__dut_instance.dut_ip,
                                                                          r.std_log_path[ii])
                            if log:
                                r.std_out_err += r.separator + '# {}'.format(ii) + r.separator + '\r\n'
                                log_list = log.split('\r')
                                for line in log_list:
                                    try:
                                        if type(line).__name__ != "unicode":
                                            r.std_out_err += (line + '\r\n')
                                        else:
                                            r.std_out_err += 'fail to get std log(None ascii)\r\n'
                                    except Exception, e:
                                        r.std_out_err += 'fail to get std log(exception)\r\n'
                            else:
                                """
                                might potential BSOD that clean up the script!
                                """
                                r.event = r.event | r.Event['TBD']
                                r.std_out_err += "Cannot find stdout/err file: {0}".format(r.std_log_path[ii]) + '\r\n'
                        except Exception, e:
                            LOGGER.error(traceback.format_exc())

                    if r.result < r.Pass and test_case.critical:
                        r.event |= r.CRITICAL_FAIL

                    if (not test_case.force_repeat) and (r.result >= r.Pass) and (i == 0):
                        LOGGER.warning('run result {}, round: {}'.format(r.result, i))
                        LOGGER.warning('case passed and not a FORCE REPEAT case will quit repetition loop')
                        break
                    else:
                        LOGGER.warning('case is marked as force repeated or failed for fisrt run, thus will continue the repetition loop(if any!)')

                    if self.b_clear or self.b_cancel_current_task:
                        r.event |= r.MANUAL_CANCEL
                        LOGGER.warning("Break repetition loop due to manual cancellation!")
                        break

                # gather all the event during execution
                #test_case.event |= r.event
            '''
            Step 6. Check if critical fail
            '''
            if not test_case.isPass and test_case.critical:
                self.clearTaskQueue()

            '''
            Step 6+. check if pass rate < th
            '''
            if ((current_scenario_fail_count * 1.0)/ original_queue_length) >= self.cur_scenario.gating_fail_rate:
                LOGGER.critical('fail rate > gating fail rate: {}'.format(self.cur_scenario.gating_fail_rate))
                self.clearTaskQueue()

            '''
            Step 7. Check if reboot needed
            '''
            if test_case.reboot and not self.b_clear and not self.b_cancel_current_task:
                self.__dut_instance.warmReboot()

            '''
            Step 8. Check if sleep time is needed
            '''
            if not self.b_clear and not self.b_cancel_current_task:
                time.sleep(test_case.sleep_time)


            test_case.end = "%.3f" % time.time()

            '''
            refresh ui
            '''
            self.cur_task = None
            self.emit(self.test_result_change)

            if self.b_clear:
                try:
                    self.__dut_instance.task_variable["Interval_Cancel"] = True
                except:
                    LOGGER.warning(traceback.format_exc())
                self.clearTaskQueue()

            '''
            Check if queue is empty and generate report
            '''
            if self.__queue.len == 0:
                try:
                    try:
                        if self.__dut_instance.dut_type == 'windows':
                            LOGGER.info("try to get bsod results")
                            # get bsod_info
                            self.cur_scenario.bsod_list, self.cur_scenario.bsod_dict = \
                                self.__dut_instance.staf_handle.get_bsod_files_adv(self.__dut_instance)
                    except Exception, e:
                        LOGGER.error("get bsod info fail: %s" % str(e))

                    # make sure the fetch thread would not compete with generate report
                    self.__dut_instance.queue_lock.acquire()
                    if self.cur_scenario:
                        self.generateReport(self.cur_scenario)
                except:
                    LOGGER.error(traceback.format_exc())
                finally:
                    self.__dut_instance.queue_lock.release()
                    self.cur_scenario = None
                    self.emit(self.fetch_a_task)
                    current_scenario_fail_count = 0
                    original_queue_length = -1

class DUT(QtCore.QObject):

    STATUS_ALIVE =   0b0000
    STATUS_LOST =    0b0001
    STATUS_LOCKED =  0b0010
    STATUS_UNKNOWN = 0b0100
    STATUS_BUSY = 0b1000

    CIT = "CIT"
    PIT = "PIT"
    FULL = "FULL"
    PV = "PV"
    OTM = "OTM"

    _status = {\
    STATUS_UNKNOWN : "Unknown",
    STATUS_LOST : "Dead",
    STATUS_LOCKED : "Locked",
    STATUS_ALIVE : "Alive",
    STATUS_BUSY : "Busy",
    }

    class SafeQueue(Queue.Queue):
        def __init__(self, parent_queue=None):
            Queue.Queue.__init__(self)
            # only id is stocked in queue
            self.__queue = []
            # additional lookup table for task details
            self.__queue_details = {}
            # related Queue
            self.parent_queue = parent_queue

        @property
        def len(self):
            return len(self.__queue)

        def _qsize(self):
            return len(self.__queue)

        # overwrite _put
        def _put(self, item):
            '''
            Class Queue will handle the lock
            '''
            try:
                _id = str(uuid.uuid1())
                self.__queue.append(_id)
                self.__queue_details[_id] = item
                b = True
            except Exception,e:
                LOGGER.error(str(e))
                b = False
            finally:
                return b

        # overwrite _get
        def _get(self):
            try:
                _id = self.__queue.pop(0)
                _item = self.__queue_details.pop(_id)
                LOGGER.debug("get test case %s" % _item.name)
            except Exception,e:
                LOGGER.error(str(e))
                _item = None
            finally:
                return _item

        def remove(self, _id):
            try:
                self.mutex.acquire()
                if _id in self.__queue and _id in self.__queue_details:
                    self.__queue.remove(_id)
                    self.__queue_details.pop(_id)
                    self.not_full.notify()
            except Exception,e:
                LOGGER.error(str(e))
            finally:
                self.mutex.release()

        def clear(self, b_all=False):
            try:
                self.mutex.acquire()
                if b_all:
                    self.__queue = []
                    self.__queue_details.clear()
                else:
                    tmp = copy.deepcopy(self.__queue)
                    for _id in tmp:
                        case = self.__queue_details[_id]
                        if case.mustrun:
                            LOGGER.warning("case {} is makred as must run, would still be executed".format(case.name))
                        else:
                            self.__queue.remove(_id)
                            self.__queue_details.pop(_id)
                b = True
                self.not_full.notify()
            except Exception,e:
                LOGGER.error(traceback.format_exc())
                b = False
            finally:
                self.mutex.release()
                return b

        def reorder(self, _id0, _id1):
            try:
                self.mutex.acquire()
                if _id0 in self.__queue and _id0 in self.__queue_details\
                and _id1 in self.__queue and _id1 in self.__queue_details:
                   index0 = self.__queue.index(_id0)
                   index1 = self.__queue.index(_id1)
                   self.__queue[_id0], self.__queue[_id1] = \
                    self.__queue[_id1], self.__queue[_id0]
            except Exception,e:
                LOGGER.error(str(e))
            finally:
                self.mutex.release()

        def list(self):
            try:
                self.mutex.acquire()
                q, qd = None, None
                q, qd = copy.deepcopy(self.__queue), copy.deepcopy(self.__queue_details)
            except Exception,e:
                LOGGER.error(str(e))
            finally:
                self.mutex.release()
                return q, qd

    def __init__(self, dut_name='N/A', dut_ip='N/A', group=None, server_config=None):
        super(DUT, self).__init__()
        self.group = group
        self.dut_id = str(uuid.uuid1())
        time.sleep(0.01)
        self.dut_name = dut_name
        self.dut_ip = dut_ip
        self.slave_dut_name = 'N/A'
        self.slave_dut_ip = 'N/A'
        self.slave_dut = None
        self.__scenraios = {}
        self.__scenraios_lookup = {}
        self.workload = []
        self.status = self.STATUS_UNKNOWN
        self.basic_info = {\
            'os' : '',
            'name' : dut_name,
            'ip'  : dut_ip,
            'mac' : '',
            'gfx' :''}

        self.staf_handle = StafHandle(self.dut_id)
        self.staf_handle.init()
        self.task_queue = self.SafeQueue()
        self.task_runner = TaskRunner(self)

        self.project_code = 'N/A'
        self.branch = []
        self.test_type = []
        self.server_config = server_config
        self.task_variable = {}
        self.platform = 'N/A'
        self.sub_platform = 'N/A'
        self.query_error_log_result = ''
        self.queue_lock = threading.Lock()

    @property
    def dut_type(self):
        return str.lower(str(self.task_variable.get('os', 'windows')))

    def setGroup(self, group):
        self.group = group

    def exchangeGroup(self, new_group):
        old_group = self.group
        self.group = new_group
        dut, rc = old_group.removeDUT(self)
        if rc:
            rc &= new_group.addDUT(self)
        else:
            old_group.addDUT(self)
            self.group = old_group
        return rc

    @property
    def prettyStatus(self):
        return self._status[self.status]

    def scenarios(self):
        for _id, scenario in self.__scenraios.items():
            yield scenario

    def refreshStatus(self):
        rc = self.staf_handle.ping(self.dut_ip)
        if rc == 0:
            self.status = self.STATUS_ALIVE
        else:
            self.status = self.STATUS_LOST

    def changeIP(self, new_ip):
        self.dut_ip = new_ip
        self.status= self.STATUS_UNKNOWN

    def updateScenarioByName(self, scenario_name):
        scenario = self.__scenraios[self.__scenraios_lookup[scenario_name]]
        scenario.reload()

    def removeTestScenario(self, scenario):
        if scenario.scenario_id in self.__scenraios and scenario.scenario_name in self.__scenraios_lookup:
            del self.__scenraios[scenario.scenario_id ]
            del self.__scenraios_lookup[scenario.scenario_name]

    def removeTestScenarioByNmae(self, scenaio_name):
        if self.__scenraios_lookup.has_key(scenaio_name):
            del self.__scenraios[self.__scenraios_lookup[scenaio_name]]
            del self.__scenraios_lookup[scenaio_name]

    def addTestScenario(self, path):
        scenario = Scenario(self.dut_id, path)
        if scenario.load():
            if self.__scenraios_lookup.has_key(scenario.scenario_name):
                self.removeTestScenarioByNmae(scenario.scenario_name)
            self.__scenraios[scenario.scenario_id] = scenario
            self.__scenraios_lookup[scenario.scenario_name] = scenario.scenario_id

    def addTestScenarioObject(self, scenario):
        self.__scenraios[scenario.scenario_id] = scenario
        self.__scenraios_lookup[scenario.scenario_name] = scenario.scenario_id

    def _addTestcaseToQueue(self, case):
        self.task_queue.put(case)
        self.emit(self.task_runner.task_queue_change)
        LOGGER.debug("add test case %s" % case.name)

    def addTestScenarioToQueue(self, scenario_id):
        scenario = self.__scenraios[scenario_id]
        for case in scenario.cases():
            self._addTestcaseToQueue(case)
        self.emit(self.task_runner.task_queue_change)

    def addTestScenarioToQueueByName(self, scenario_name):
        scenario = self.__scenraios[self.__scenraios_lookup[scenario_name]]
        for case in scenario.cases():
            self._addTestcaseToQueue(case)

    def addTestcaseToQueue(self, scenario_id, case_id):
        scenario = self.__scenraios[scenario_id]
        case = scenario.case(id=case_id)
        self._addTestcaseToQueue(case)


    def startRunner(self):
        if not self.task_runner is None:
            self.task_runner.start()

    def pauseRunner(self):
        if not self.task_runner is None:
            self.task_runner.terminate()

    def getTestType(self):
        _ = []
        if self.PIT in self.test_type:
            _.append('PIT')
        if self.CIT in self.test_type:
            _.append('CIT')
        if self.FULL in self.test_type:
            _.append('FULL')
        return _

    def setTestType(self, str_fmt):
        if 'PIT' in str_fmt:
            self.test_type.append(self.PIT)
        if 'CIT' in str_fmt:
            self.test_type.append(self.CIT)
        if 'FULL' in str_fmt:
            self.test_type.append(self.FULL)

    def getBranch(self):
        _ = []
        if self.PV in self.branch:
            _.append('PV')
        if self.OTM in self.branch:
            _.append('OTM')
        return _

    def setBranch(self, str_fmt):
        if 'PV' in str_fmt:
            self.branch.append(self.PV)
        if 'OTM' in str_fmt:
            self.branch.append(self.OTM)

    def getScenariobyName(self, scenario_name):
        try:
            scenario =  self.__scenraios[self.__scenraios_lookup[scenario_name]]
            return scenario
        except Exception,e:
            LOGGER.error('No such scenario : {}'.format(scenario_name))
            return None

    def getScenariobyID(self, scenario_id):
        try:
            scenario = self.__scenraios[scenario_id]
            return scenario
        except Exception, e:
            LOGGER.error('No such scenario : {}'.format(scenario_id))
            return None

    def getDedicatedTaskQueue(self):
        #return rabbitMQ.getDedicatedTaskQueue(self.server_config, self.dut_name)
        return rabbitMQ.getDedicatedTaskQueue_pika(self.server_config, self.dut_name)