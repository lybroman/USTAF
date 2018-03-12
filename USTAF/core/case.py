#-------------------------------------------------------------------------------
# Name:        case
# Purpose:
#
# Author:      yuboli
#
# Created:     04/05/2017
# Copyright:   (c) yuboli 2017
# Licence:     <your licence>
#-------------------------------------------------------------------------------
import uuid, time
from run import Run
from logger import LOGGER
from run import Run
import traceback
import gc

class Case(object):
    def __init__(self, scenario, **kwargs):
        self.case_id = str(uuid.uuid1())
        time.sleep(0.01)
        self.__parent = scenario
        self.executable = ''
        self.name = ''
        self.parameters = ''
        self.cmd = ''
        self.dependencies = []
        self.pass_bypass = []
        self.critical = False
        self.failrerun = 0
        self.repetition = 1
        self.execution = 1
        self.failrepetition = 0
        self.sleep_time = 0
        self.reboot = False
        self.always_pass = False
        self.mustrun = False
        self.timeout = 600
        self.__runs = []
        self.base_share_path = r"\\sample.com\ec\proj\iag\peg\icg\AUTO_TEST\USTAF\LOGs"
        self.platform = ''
        self.test_type = ''
        self.gating = True
        self.bEnv = False
        self.start = '0.0'
        self.end = '0.0'
        self.force_repeat = False

        '''
        Post execution parmas
        '''
        #self.event = []
        self.pretty_event = []
        self.hsd_id = []
        self.hsd_url = []
        self.pretty_result = 'NA'
        self.pass_rate = 0.0
        self.error_log = ''
        self.std_log = ''

        self.total_count = 0
        self.pass_count = 0

    def addRun(self, r):
        self.__runs.append(r)

    def runs(self):
        for r in self.__runs:
            yield r

    @property
    def std_log_otf(self):

        std_log = ''
        for run in self.runs():
            std_log += run.std_out_err + '\r\n'

        return std_log

    @property
    def error_log_otf(self):
        error_log = ''
        for run in self.runs():
            error_log += '||'.join(['|'.join(_) for _ in run.error_log])

        return error_log

    @ property
    def isPass(self):
        '''''''''''''''''
        ' Vote strategy '
        '''''''''''''''''
        __pass_count = 0
        __not_pass_count = 0
        for run in self.__runs:
            if run.result >= run.Pass:
                __pass_count += 1
            else:
                __not_pass_count += 1

        if __pass_count > __not_pass_count:
            return True
        else:
            return False

    def result(self):
        __pass_count = 0
        __fail_count = 0
        __not_run_count = 0
        if len(self.__runs) == 0:
            self.pretty_event = []
            self.hsd_id = []
            self.hsd_url = []
            self.pass_rate = 0.0
            return "not-run"
        else:
            self.pretty_event = []
            self.pass_rate = 0.0
            for run in self.__runs:
                if run.result >= run.Pass:
                    __pass_count += 1
                elif run.result == run.NotRun:
                    __not_run_count += 1
                else:
                    __fail_count += 1

                for e in run.pretty_event:
                    if e not in self.pretty_event:
                        self.pretty_event.append(e)

                if run.hsd_id not in self.hsd_id:
                    try:
                        self.hsd_id.append(str(run.hsd_id))
                    except:
                        LOGGER.error(traceback.format_exc())
                if run.hsd_url not in self.hsd_url:
                    try:
                        self.hsd_url.append(str(run.hsd_url))
                    except:
                        LOGGER.error(traceback.format_exc())

            self.pass_rate = float(__pass_count)/(__pass_count + __fail_count + __not_run_count)

            self.total_count = __pass_count + __not_run_count + __fail_count
            self.pass_count = __pass_count

            if __fail_count > 0 and __pass_count <= __fail_count:
                return "fail"
            elif __pass_count > __fail_count and __fail_count > 0:
                return "repeat-pass"
            elif __pass_count > __fail_count and __fail_count == 0:
                return "pass"
            elif __fail_count == 0 and __not_run_count > 0:
                return "running"


    def checkDependencyPass(self):
        for case_name in self.dependencies:
            case = self.__parent.case(name=case_name)
            if not case.isPass:
                LOGGER.warning('dependency case %s failed!' % case_name)
                return False
        return True

    def checkPassByPass(self):
        for case_name in self.pass_bypass:
            case = self.__parent.case(name=case_name)
            if case.isPass:
                LOGGER.warning('passBypass case %s passed!' % case_name)
                return True
        return False

    def getID(self):
        return self.case_id

    @property
    def getScenario(self):
        return self.__parent

    def clearAllRuns(self):
        del self.pretty_event
        self.pretty_event = []
        del self.hsd_id
        self.hsd_id = []
        del self.hsd_url
        self.hsd_url = []
        self.pretty_result = 'NA'
        del self.__runs
        self.__runs = []
        self.pass_rate = 0.0
        self.total_count = 0
        self.pass_count = 0
        self.start = '0.0'
        self.end = '0.0'
        self.error_log = ''
        self.std_log = ''

        c = gc.collect()
        LOGGER.debug("collect {} after del runs instance".format(c))

    def getRun(self, run_id):
        for run in self.__runs:
            if run.run_id == run_id:
                return run
        return None

