__author__ = "yubo.li"

import re, traceback
from USTAF.core.logger import  LOGGER
import datetime,time
from string import maketrans

class LogAnalysis(object):
    def __init__(self, dut, platform, test_type, case_id, case_cmd, log_base_path="C:/AutoBAT Results/TestLogs", query_result=None):
        self.dut = dut
        self.date = self.get_current_intel_calendar()
        self.platform = platform
        self.test_type = test_type
        self.case_id = case_id
        self.log_base_path = log_base_path
        self.error_log = []
        self.hsd_id = []
        self.hsd_url = []
        self.hsd_description = ''
        self.case_id = case_id
        self.additional_info = ''
        self.extra_check_log = ''
        self.case_cmd = case_cmd
        self.query_result = query_result


    class log_structure():
        def __init__(self, case, raw_data):
            self.raw_data = raw_data
            self.case_id = case.name
            # currently only app log only
            self.error_info_raw = raw_data
            self.error_info = []
            self.drv_error_info_raw = ''
            self.drv_error_info = []
            self.FW_error_info_raw = ''
            self.FW_error_info = []
            self.fail_type = ''
            self.Bug_ID = ''
            self.Outcome = ''
            self.Comment = ''
            self.log_set = set()
            self.log_splitter = '||'
            self.log_list = None
            # parse log
            self.log_to_set()

        def log_to_set(self):
            if type(self.error_info_raw) == str or type(self.error_info_raw) ==unicode:
                self.log_list = str(self.error_info_raw).split('|')
                # print(self.error_info_raw)
                if len(self.log_list) < 1:
                    return
            elif type(self.error_info_raw) == list:
                self.log_list = self.error_info_raw

            for i in range(0, len(self.log_list)):
                error_new = self.log_list[i]
                error_new = error_new.strip(' ')
                transtab = maketrans('0123456789[]{}:();', '                  ')
                error_new = error_new.translate(transtab)
                error_new = error_new.replace(' ', '')
                if error_new not in self.log_set:
                    self.log_set.add(error_new)

    @staticmethod
    def get_current_intel_calendar():
        date = datetime.datetime.fromtimestamp(time.time()).strftime("%Y-%W-%w")
        year = date.split('-')[0]
        """
        solution for '2017'
        """
        week = int(date.split('-')[1])
        day = int(date.split('-')[2])
        date = str(date.split('-')[0]) + '/' + str(week) + '/' + str(day)
        return date

    def parse(self, os='windows'):
        """
         Note: this log analysis parser need to be characterized by each user according to the log structure!
        """
        # step 1 get default test log
        if os == 'linux':
            try:
                cmd_line = '~/sw_val/scripts/tools/print_err_msg.sh {}'.format(self.case_id)
                res, log = self.dut.staf_handle.trigger_cmdline(self.dut.dut_ip, cmd_line)
                if res:
                    self.error_log = log.resultContext.getRootObject()['fileList'][0]['data'].split('\n')[:-1]
                else:
                    LOGGER.info("can not get testid.log, so directly return")
                    self.error_log = []
                    return -1
            except:
                LOGGER.error(traceback.format_exc())
                return -1
        else:
            try:
                log = self.dut.staf_handle.getFile(self.dut.dut_ip, '{}/{}.log'.format(self.log_base_path, self.case_id))
                LOGGER.debug(log)
                if log:
                    log_list = log.split('\r')
                    for i in range(0, len(log_list)):
                        if 'TestSet:' in log_list[i]:
                            try:
                                pt = re.compile(r'TestSet:(.*)]')
                                res = re.search(pt, log_list[i])
                                self.additional_info = res.group(1)
                            except Exception, e:
                                LOGGER.error(str(e))
                        if 'Log file:' in log_list[i]:
                            try:
                                pt = re.compile(r'Log file:(.*)]')
                                res = re.search(pt, log_list[i])
                                self.extra_check_log = res.group(1)
                            except Exception, e:
                                LOGGER.error(str(e))

                        if '[ERROR]' in str(log_list[i]):
                            self.error_log.append(log_list[i].split('[ERROR]')[1])
                else:
                    LOGGER.info("can not get testid.log, so directly return")
                    self.error_log = []
                    return -1
            except Exception,e:
                LOGGER.error(traceback.format_exc())
                return -1

        if 'RunStoreAppAutoTest' in self.case_cmd:
            try:
                """
                for metro case need to get app log
                """
                log = self.dut.staf_handle.getFile(self.dut.dut_ip, '{}/{}._AppLog.txt'.format(self.log_base_path, self.case_id))
                if log:
                    log_list = log.split('\r')
                    for i in range(0, len(log_list)):
                        if '[ERROR]' in str(log_list[i]):
                            self.error_log.append(log_list[i].split('[ERROR]')[1])

                        if len(log_list[i]) > 2:
                            last_line = log_list[i]

                    for j in range(1, len(last_line.split(']')) + 1):
                        if len(last_line.split(']')[-j]) > 2:
                            self.error_log.append('[Potential FAILED]' + last_line.split(']')[-j])
                            break
                else:
                    LOGGER.debug("Not metro case...")
            except Exception, e:
                LOGGER.error(traceback.format_exc())

            """
            check additional log files if needed
            """
            try:
                log = self.dut.staf_handle.getFile(self.dut.dut_ip, self.extra_check_log)
                if log:
                    log_list = log.split('\r')
                    for i in range(0, len(log_list)):
                        if '[ERROR]' in str(log_list[i]):
                            self.error_log.append(log_list[i].split('[ERROR]')[1])
                        """
                        Always record the last step
                        """
                        '''
                        > 2 : /r/n
                        '''
                        if len(log_list[i]) > 2:
                            last_line = log_list[i]

                    for j in range(1, len(last_line.split(']')) + 1):
                        if len(last_line.split(']')[-j]) > 2:
                            self.error_log.append('[Potential FAILED]' + last_line.split(']')[-j])
                            break
                else:
                    LOGGER.debug("No extra error log to parse...")
            except Exception, e:
                LOGGER.error(traceback.format_exc())

            try:
                metro_feature_log = 'C:/Users/IRP/Documents/AutoTest_W8StoreApp_FeatureLog.txt'
                log = self.dut.staf_handle.getFile(self.dut.dut_ip, metro_feature_log)
                if log:
                    log_list = log.split('\r')
                    for i in range(0, len(log_list)):
                        if '[ERROR]' in str(log_list[i]):
                            self.error_log.append(log_list[i].split('[ERROR]')[1].strip())
            except Exception, e:
                LOGGER.error(traceback.format_exc())
        else:
            LOGGER.debug("Not a metro case, bypass related check points")

    def is_new_bug(self, work, run):
        try:
            # one run could contain multiple run results, due to failrerun functionality
            log_cur = self.log_structure(work, self.error_log)
            b_new, pretty_result = self._is_new_bug(log_cur, work, run)
            LOGGER.info('{} is {}'.format(work.name, pretty_result))
            return b_new
        except:
            LOGGER.critical(traceback.format_exc())
            return True

    def _is_new_bug(self, log_cur, work, run):
        if self.query_result:
            for i in range(0, len(self.query_result)):
                if 'case_id' in self.query_result[i].keys():
                    if self.query_result[i]['case_id'] == log_cur.case_id:

                        if (work.test_type.lower() == 'weekly' and self.query_result[i]['guid__day'] == 0) or \
                            (work.test_type.lower() != 'weekly' and self.query_result[i]['guid__day'] != 0):
                            LOGGER.info("matched one case: {0} from DB".format(log_cur.case_id))
                            '''
                            to identify history and current error log
                            '''
                            rst_error_log = self.query_result[i].get('error_log', '').replace('[}{]', '')

                            # print rst_error_log
                            log_prev = self.log_structure(work, rst_error_log)

                            LOGGER.info("prev error_log {0}".format(log_prev.log_set))
                            LOGGER.info("cur error_log {0}".format(log_cur.log_set))

                            '''
                            get category
                            '''
                            if 'second_category' in self.query_result[i].keys():
                                work.category = self.query_result[i]['second_category']
                            else:
                                work.category=''
                            if len(log_prev.log_set) >= len(log_cur.log_set):
                                run.fail_type = 'known'
                                """
                                API changed, just keep today's error log
                                """
                                # run.erbror_log
                                # += '[}{]' + self.query_result[i]['error_log']
                                run.hsd_id = self.query_result[i]['hsd']
                                run.hsd_url = self.query_result[i]['hsd_url']
                                
                                LOGGER.info('run.hsd_id:%s'% run.hsd_id )
                                if run.hsd_id == 'new' or run.hsd_id == '':
                                    run.hsd_id = 'known-not-filed'
                                return False, run.hsd_id
                            # elif self.test_type == work.test_type and self.sub_version == work.sub_version:
                            else:
                                """
                                API changed, just keep today's error log
                                """
                                LOGGER.info("a potenial new bug:{0}".format(log_cur.case_id))
                                # run.bug_id += self.query_result[i]['HSD']
                                '''
                                [}{]to indentify history and current error log
                                '''
                                # run.error_log += '[}{]' + self.query_result[i]['error_log']
            try:
                """
                check in same sub category cases
                """
                if len(work.category) > 1:
                    for i in range(0, len(self.query_result)):
                        if self.query_result[i]['second_category'] == work.category:
                            '''
                            to indentify history and current error log
                            '''
                            rst_error_log = self.query_result[i]['error_log'].replace('[}{]', '')
                            log_prev = self.log_structure(work, rst_error_log)
                            if len(log_prev.log_set) >= len(log_cur.log_set):
                                run.fail_type = 'known'
                                """
                                API changed, just keep today's error log
                                """
                                run.hsd_id = self.query_result[i]['hsd']
                                run.hsd_url = self.query_result[i]['hsd_url']
                                if run.hsd_id == 'new' or run.hsd_id == '':
                                    run.hsd_id = 'known-not-filed'
                                return False, run.hsd_id
                            else:
                                """
                                API changed, just keep today's error log
                                """
                                pass
            except Exception, e:
                LOGGER.error(str(e))

        run.fail_type = 'new'
        run.hsd_id = 'new'
        return True, 'new'