import sys, os, time, traceback
from USTAF.core.logger import LOGGER
import mbt_report
from winodwsWA import *
import json
import gerritApi
import uuid
import copy, gc

class TestResult(object):

    NORMAL = 0b00000000000000
    WARM_REBOOT = 0b00000000000001
    COLD_REBOOT = 0b00000000000010
    REBOOT_RECOVERY = 0b00000000000100
    INITIAL_REBOOT = 0b00000000001000
    MANUAL_CANCEL = 0b00000000010000
    ERROR = 0b00000000100000
    DEPENDENCY_FAIL = 0b00000001000000
    CRITICAL_FAIL = 0b00000010000000
    TBD = 0b00000100000000
    HANG_TO = 0b00001000000000
    PASS_BYPASS = 0b00010000000000
    CONNECTION_LOSS = 0b00100000000000
    ENV_FAILURE = 0b01000000000000
    BSOD = 0b10000000000000

    def fecthPatchInfo(self):
        if self.test_type in ['PIT_LITE', 'CIT']:
            # fetch build info
            for path in WIN_CI_BUILD_PATH_LIST:
                dir_path = r'{}/{}/distrib'.format(path, self.build)
                if os.path.isdir(dir_path):
                    files = os.listdir(dir_path)
                    for fl in files:
                        if fl.startswith('CI') and fl.endswith('.txt'):
                            with open('{}/{}'.format(dir_path, fl), 'r') as f:
                                self.patch_detail = f.read().replace('\n', '</br>')
                                self.artifacts_path = dir_path
                                LOGGER.debug(self.patch_detail)
                                break
                    if self.patch_detail:
                        break
        elif self.test_type in ['FULL']:
            '''
            Need implementation here... hwo to handle PV branch?
            '''
            pass

        try:
            lines = self.patch_detail.split('</br>')
            for line in lines:
                if 'Owner' in line:
                    self.owner = line.replace('Owner:', '').strip()
                    self.email = self.owner
                if 'Subject' in line:
                    self.subject = line.replace('Subject:', '').strip()
        except:
            LOGGER.error(traceback.format_exc())

    def __init__(self, scenario, dut):
        self.scenario_name = scenario.scenario_name
        self.project_code = dut.project_code
        # self.platform = dut.platform # whether use the one of scenario?
        self.platform = scenario.platform
        self.sub_platform = dut.sub_platform
        self.subversion = scenario.subversion
        self.build = dut.task_variable.get("build", "NA")
        self.component = dut.task_variable.get("component", "NA")
        if self.build == 'NA':
            self.build = dut.task_variable.get("Build_No_Variable", "NA")

        self.patch = dut.task_variable.get("patchset", "NA")
        self.manifest_id = dut.task_variable.get("manifest_id", "NA")

        if self.manifest_id != 'NA':
            self.gerrit_link = 'https://icggerrit.corp.sample.com/#/x/hydra-ci/iset/manifestvotes&manifest_id='.format(self.manifest_id)
        elif self.patch != 'NA':
            self.gerrit_link = 'https://icggerrit.corp.sample.com/#/c/{}/'.format(self.patch)
        else:
            self.gerrit_link = 'NA'

        self.owner = dut.task_variable.get("owner", "NA")
        self.author_email = dut.task_variable.get("author_email", "")
        if self.author_email:
            scenario.mail_list.append(self.author_email)

        if dut.task_variable.get("email", ""):
            scenario.mail_list.append(dut.task_variable["email"])

        self.os = dut.task_variable.get("os", "NA")
        self.test_type = scenario.test_type
        self.report_ww = dut.task_variable.get("report_ww", "NA")  # [year, ww, stackIndex, 2018WW2_0]
        self.fail_case_list = []
        self.bCancelled = False
        self.bEnv_failure = False
        self.cases = []
        self.server_config = dut.server_config
        self.dut_name = dut.dut_name
        self.dut_ip = dut.dut_ip
        self.total_count = 0
        self.non_gating_count = 0
        self.fail_count = 0
        self.pass_count = 0
        self.not_run_count = 0
        self.repeat_pass_count = 0
        self.start_time = time.ctime(dut.task_variable.get("start", time.time()))
        self.finish_time = time.ctime(dut.task_variable.get("finish", time.time()))
        self.patch_detail = 'NA'
        self.subject = 'NA'
        self.email = 'NA'
        self.artifacts_path = 'NA'
        self.dut_info = ''
        self.log_path = scenario.base_log_path if scenario.base_log_path else WIN_LOG_ROOT_PATH
        self.merge_slot_info = []
        self.merge_slot_info_str = ''
        self.user = dut.task_variable.get("username","NA") + ';' + dut.task_variable.get("killer","")
        self.run_id = str(uuid.uuid1()).split('-')[0]

        html_path = '{}_{}_{}_{}.html'.format(self.build, self.dut_name, self.scenario_name, dut.task_variable['UUID'])
        self.html_full_path = os.path.join(dut.server_config["base_share_path"], 'html', html_path)

        try:
            self.critical_issues = repr(scenario.bsod_dict) if scenario.bsod_dict else ''
        except:
            LOGGER.critical(traceback.format_exc())

        try:
            _t = dut.staf_handle.get_dut_info(dut)
            if _t:
                for key, value in _t.items():
                    self.dut_info += "{} : {} </br>".format(key, value)
        except:
            LOGGER.error(traceback.format_exc())

        try:
            self.fecthPatchInfo()
        except:
            LOGGER.error(traceback.format_exc())

        _last_cmd = ''

        if dut.task_variable.get("Interval_Cancel", False):
            self.bCancelled = True

        for case in scenario.cases():
            self.total_count += 1
            # self.cases.append(case)
            case.pretty_result = case.result()

            if case.pretty_result == 'running':
                case.pretty_result = 'fail'

            if case.pretty_result == 'fail' and case.gating:
                self.fail_count += 1
                self.fail_case_list.append(case.name)
            elif case.pretty_result == 'not-run' and case.gating:
                self.not_run_count += 1
            else:
                self.pass_count += 1
                if case.pretty_result == 'repeat-pass':
                    self.repeat_pass_count += 1

            if not case.gating:
                self.non_gating_count += 1

            if "MANUAL_CANCEL" in case.pretty_event:
                self.bCancelled = True

            if "ENV_FAILURE" in case.pretty_event and case.pretty_result == 'fail':
                self.bEnv_failure = True

            if not case.pretty_event:
                '''
                Dot not display on html
                '''
                case.pretty_event = ''
            elif case.always_pass:
                case.pretty_event = ''

            _last_cmd = case.cmd
            self.cases.append(case)

            err_log = ''
            std_log = ''
            for run in case.runs():
                err_log += '||'.join(['|'.join(_) for _ in run.error_log])
                std_log += run.std_out_err + '\r\n'
            case.error_log = err_log
            case.std_log = std_log

        self.pass_rate = '%.3f' % (float((1 - float(self.fail_count + self.not_run_count) / self.total_count) * 100.0)) + r'%'

        try:
            if _last_cmd:
                params = _last_cmd.split(' ')
                for param in params:
                    _p = param.strip('"').strip('{').strip('}')
                    if _p in dut.task_variable.keys():
                        self.log_path = os.path.join(self.log_path, dut.task_variable[_p])
                    if not os.path.exists(self.log_path):
                        os.makedirs(self.log_path)

                LOGGER.info(self.log_path)
        except:
            LOGGER.error(traceback.format_exc())

        try:
            if self.log_path:
                result_js_file = '{0}/../result-{1}.js'.format(self.log_path, dut.task_variable.get("UUID", 'NA'))
                result_js = {
                    'cancelled' : self.bCancelled,
                    'env_failed': self.bEnv_failure,
                    'pass' : self.pass_count,
                    'fail' : self.fail_count,
                    'not_run' : self.not_run_count,
                    'total' : self.total_count,
                    'pass_rate' : self.pass_rate,
                    'build' : self.build,
                    'patch' : self.patch,
                    'gerrit_link' : self.gerrit_link,
                    'scenario' : self.scenario_name,
                    'dut_id' : dut.dut_ip,
                    'dut_name' : dut.dut_name,
                    'failed_case_list' : self.fail_case_list,
                    'critical failure' : scenario.bsod_dict,
                    'reach_gating_fail_rate' : ((self.fail_count * 1.0) / self.total_count) > scenario.gating_fail_rate,
                    'mbt_report' : r'http://mbt.tm.sample.com/testreports?run_id={}'.format(self.run_id),
                    'html_report_full_path' : self.html_full_path,
                    'patch_detail' : self.patch_detail,
                }

                _f = open(result_js_file, 'w')
                json.dump(result_js, _f, indent=4)
                _f.close()
        except:
            LOGGER.error(traceback.format_exc())

        try:
            if self.test_type == 'PIT_LITE' and (self.component == 'SW' or "vied-vieddrv-camerasw_src" in self.patch_detail):
                gerritApi.getMergeSlotInfo(self.patch, self.merge_slot_info)
                if self.merge_slot_info:
                    for _s in self.merge_slot_info:
                        self.merge_slot_info_str += _s["subject"] + ":</br>"
                        for _ss in _s["sub_subjects"]:
                            self.merge_slot_info_str += _ss + "</br>"
        except:
            LOGGER.error(traceback.format_exc())


        try:
            # data, dut_name, platform, run_id, build
            mbt_report.send_to_server_th(copy.deepcopy(self.cases), copy.deepcopy(self.dut_name), \
                                         copy.deepcopy(self.platform), copy.deepcopy(self.run_id),\
                                         copy.deepcopy(self.build))
            gc.collect()
        except:
            LOGGER.error(traceback.format_exc())

