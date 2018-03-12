#-------------------------------------------------------------------------------
# Name:        scenario.py
# Purpose:
#
# Author:      yuboli
#
# Created:     04/05/2017
# Copyright:   (c) yuboli 2017
# Licence:     <your licence>
#-------------------------------------------------------------------------------
import uuid, time
import json, os, sys, time, requests
from plugin import excelReport
from plugin import mySQL
from plugin import testResult
from plugin import htmlReport
from plugin.winodwsWA import *
from plugin.myEmail import *
from plugin.dashboard import *
import re
import gc


class Scenario(object):
    def __init__(self, dut_id, path='N/A'):
        self.scenario_id = str(uuid.uuid1())
        #print self.scenario_id
        time.sleep(0.01)
        self.path = path
        self.__parent_id = dut_id
        self.__case_list = []
        self.__case_info = {}
        self.mail_list = []
        self.scenario_name = 'N/A'
        self.test_type = 'N/A'
        self.platform = 'N/A'
        self.subversion = 'N/A'
        self.base_log_path = r'\\ccr\ec\proj\iag\peg\icg\AUTO_TEST\TWSResult'
        # default should larger than 100%
        self.gating_fail_rate = 1.1
        self.bsod_list = []
        self.bsod_dict = {}

        self.sync_files = {}

    def load(self, data=None):
        if self.path.endswith('.js') or self.path.endswith('.json'):
            return self.loadScenarioFromJASONFile()
        elif data:
            return self.loadScenarioFromDB(data)
        else:
            LOGGER.error( 'Not a supported file format!')
            return False

    @staticmethod
    def queryDetailFromDataBase(cases):
        try:
            data = {'test_case_id_list': json.dumps(cases)}
            response = requests.post(url=CASE_DETAIL_URL, data=data)
            if int(response.status_code) == 200:
                return json.loads(response.content)
            else:
                return {}
        except:
            traceback.format_exc()
            return {}

    def reload(self):
        del self.__case_list
        self.__case_list = []
        self.__case_info.clear()
        del self.mail_list
        self.mail_list = []
        self.scenario_name = 'N/A'
        self.test_type = 'N/A'
        self.platform = 'N/A'
        self.subversion = 'N/A'
        self.base_log_path = r'\\ccr\ec\proj\iag\peg\icg\AUTO_TEST\TWSResult'
        self.bsod_list = []
        self.bsod_dict = {}
        self.load()

        c =gc.collect()
        LOGGER.debug("collect {} after reload scenario instance".format(c))

    def loadScenarioFromDB(self, data):
        if str.lower(data.get('os', 'windows')) == "windows":
            try:
                # step 1 prepare setup Env cases
                generateSetupEnvCases(self)
                # step 2 query from database
                name = data["name"]
                cases = self.queryDetailFromDataBase(data["cases"])
                if cases:
                    self.scenario_name = name
                    for i in xrange(0, len(cases)):
                        testcase = Case(self)
                        testcase.name = data["cases"][i]
                        testcase.cmd = WIN_PREFIX + cases[i]["script_id"]
                        # Hard code as repetition and count  = 5
                        testcase.repetition = 5
                        self.__case_info[testcase.case_id] = testcase
                        self.__case_list.append(testcase.case_id)
                else:
                    return False
                # step 3 prepare copy results cases
                generateCopyCases(self)
                return True
            except Exception, e:
                LOGGER.error(traceback.format_exc())
                return False
        else:
            LOGGER.warning("ONLY WINDOWS PAAS is supported now!")
            return False

    def loadScenarioFromJASONFile(self):
        try:
            if os.path.isfile(self.path):
                ff = open(self.path)
                scenario_js = json.load(ff)

                if 'name' in scenario_js.keys():
                    self.scenario_name = scenario_js['name']
                if 'test_type' in scenario_js.keys():
                    self.test_type = scenario_js['test_type']
                if 'platform' in scenario_js.keys():
                    self.platform = scenario_js['platform']
                if 'subversion' in scenario_js.keys():
                    self.subversion = scenario_js['subversion']
                if 'mail_list' in scenario_js.keys():
                    self.mail_list = scenario_js['mail_list']
                else:
                    self.mail_list = ['yubo.li@sample.com']

                if 'gating_fail_rate' in scenario_js.keys():
                    self.gating_fail_rate = scenario_js['gating_fail_rate']

                if "collateral" in scenario_js.keys():
                    for i in range(0, len(scenario_js["collateral"])):
                        try:
                            self.sync_files[scenario_js["collateral"][i][0]] = scenario_js["collateral"][i][1]
                        except Exception,e:
                            LOGGER.warning(traceback.format_exc())

                if 'root_artifacts_path' in scenario_js.keys():
                    self.base_log_path = scenario_js['root_artifacts_path']

                for i in range(0, len(scenario_js["tools"])):
                    testcase = Case(self)
                    testcase.executable = scenario_js["tools"][i]['executable']
                    testcase.name = scenario_js["tools"][i]['name']
                    testcase.parameters = scenario_js["tools"][i]['parameters']
                    _pt = re.compile('%([\w\.]+)%')
                    parameters = _pt.sub(r'{\1}', testcase.parameters).replace('"', '')
                    testcase.cmd = '%s %s' % (testcase.executable, parameters)
                    if scenario_js["tools"][i].has_key('dependencies'):
                        testcase.dependencies = scenario_js["tools"][i]['dependencies']
                    if scenario_js["tools"][i].has_key('pass_bypass'):
                        testcase.pass_bypass = scenario_js["tools"][i]['pass_bypass']
                    if scenario_js["tools"][i].has_key('critical'):
                        testcase.critical = scenario_js["tools"][i]['critical']
                    if scenario_js["tools"][i].has_key('failrerun'):
                        testcase.failrerun = scenario_js["tools"][i]['failrerun']
                    if scenario_js["tools"][i].has_key('repetition'):
                        testcase.repetition = scenario_js["tools"][i]['repetition']
                    if scenario_js["tools"][i].has_key('failrepetition'):
                        testcase.failrepetition = scenario_js["tools"][i]['failrepetition']
                    if scenario_js["tools"][i].has_key('timeout'):
                        testcase.timeout = scenario_js["tools"][i]['timeout']
                    if scenario_js["tools"][i].has_key('mustrun'):
                        testcase.mustrun = scenario_js["tools"][i]['mustrun']
                    if scenario_js["tools"][i].has_key('alwayspasses'):
                        testcase.always_pass = scenario_js["tools"][i]['alwayspasses']
                    if scenario_js["tools"][i].has_key('env'):
                        testcase.bEnv = scenario_js["tools"][i]['env']
                    if scenario_js["tools"][i].has_key('sleeptime'):
                        testcase.sleep_time = scenario_js["tools"][i]['sleeptime']

                    testcase.platform = self.platform
                    testcase.test_type = self.test_type

                    self.__case_info[testcase.case_id] = testcase
                    self.__case_list.append(testcase.case_id)

            else:
                LOGGER.error('Could find the scenario file %s' % self.path)
                return False
        except Exception,e:
            LOGGER.error(str(e))
            return False
        return True

    def cases(self):
        for _id in self.__case_list:
            yield self.__case_info[_id]

    def case(self, **kwargs):
        if 'id' in kwargs.keys():
            return self.__case_info[kwargs['id']]
        elif 'name' in kwargs.keys():
            for c in self.cases():
                if c.name == kwargs['name']:
                    return c
        else:
            return None

    def addTestCaseObject(self, testcase):
        self.__case_info[testcase.case_id] = testcase
        self.__case_list.append(testcase.case_id)

    def clearAllResults(self):
        for case_id in self.__case_list:
            self.__case_info[case_id].clearAllRuns()

        self.bsod_list = []
        self.bsod_dict = {}


    def generateReport(self, dut):

        LOGGER.critical(" + generating report...")

        test_result = testResult.TestResult(self, dut)

        # Step 1. generate spread sheet
        excel = None
        try:
           excel, std_att = excelReport.generateExcelResults(test_result)
        except:
            LOGGER.error(traceback.format_exc())

        # Step 2. generate html
        try:
            html = htmlReport.HtmlGenerator(test_result, dut.server_config["base_share_path"])
            html_path = '{}_{}_{}_{}.html'.format(test_result.build, test_result.dut_name, test_result.scenario_name, dut.task_variable['UUID'])
            html.generate(html_path)
        except:
            LOGGER.error(traceback.format_exc())

        # Step 3. save to mysql
        try:
            _conn = mySQL.SQLConnection()
            _conn.init()
            _conn.insertTestResults(test_result)
            _conn.close()
        except:
            LOGGER.error(traceback.format_exc())
        finally:
            pass


        LOGGER.info("+ upload results")
        # Step 4. Upload results/logs to dashboard via REST API
        try:
            insertTestResult(test_result, dut.server_config["base_share_path"] + '/html/' + html_path)
        except:
            LOGGER.error(traceback.format_exc())
        LOGGER.info("- upload results")


        # Step 5. send email
        try:
            sendEmailReport(test_result, dut.server_config["base_share_path"], html_path, self.mail_list, excel, std_att)
        except:
            LOGGER.error(traceback.format_exc())

        # Step 6. gerrit add tag
        # AMQP

        try:
            del test_result
            del html
            del _conn
        finally:
            c = gc.collect()
        LOGGER.critical("collect {} after del test result instance".format(c))

        LOGGER.critical(" - generating report...")


# test sample
# a = Scenario(r'C:\Users\yuboli\My_Files\test_framework\USTAF\scenarios\Camera_PIT_Lite_OTM_KBL_W10_X64_IMX135_OV5693.js')