#-------------------------------------------------------------------------------
# Name:        server.py
# Purpose:
#
# Author:      yuboli
#
# Created:     04/05/2017
# Copyright:   (c) yuboli 2017
# Licence:     <your licence>
#-------------------------------------------------------------------------------
import threading
from USTAF.core.logger import LOGGER
from PyQt4.QtCore import QThread
import socket
LOCK = threading.Lock()
from dut import DUT
from scenario import Scenario
import subprocess, re, os, traceback, json
from USTAF.core.plugin import rabbitMQ

############################################
## Classs Server
##      Singleton instance of USTAF Server
############################################

class Server(object):
    # singleton instance
    __instance = None

    class SocketListener(QThread):
        @staticmethod
        def __get_ip_address():
            ip_address = None
            get_ip_process = subprocess.Popen('ipconfig -all', stdout=subprocess.PIPE)
            tmp_output = get_ip_process.communicate()[0]
            search_result = re.search('IPv4 Address(. )*: (\d{1,3}.\d{1,3}.\d{1,3}.\d{1,3})', tmp_output)
            if search_result is not None:
                ip_address = search_result.group(2)
            else:
                ip_address = 'localhost'
                LOGGER.critical('ERROR! Cannot find host IP!!!, using LOCALHOST')
            return ip_address

        @classmethod
        def __check_port_occupied(cls, port):
            _ = os.popen('netstat -ano | findstr "{}"'.format(port))
            tmp_output = _.readlines()
            LOGGER.info(tmp_output)
            if not tmp_output:
                return False
            else:
                return True

        def __init__(self, server):
            QThread.__init__(self)
            self.server = server
            self.sock = None
            self.launched = False

        def init(self):
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            ip = self.__get_ip_address()
            try:
                if not self.__check_port_occupied(self.server.server_config["socket_server_port"]):
                    self.sock.bind((ip, self.server.server_config["socket_server_port"]))
                    self.sock.listen(self.server.server_config["max_connection"])
                    LOGGER.info("Connect to server {}:{} with max connection {}".format(ip, self.server.server_config["socket_server_port"], self.server.server_config["max_connection"]))
                    self.launched = True
                    return True
                else:
                    LOGGER.warning("{} has been occupied!".format(self.server.server_config["socket_server_port"]))
                    return False
            except:
                LOGGER.error(traceback.format_exc())
                return False

        def launchConnection(self, sock):
            try:
                sock.settimeout(2)
                buf = ''
                while True:
                    try:
                        buf_frag = sock.recv(1024)
                        buf += buf_frag
                        #LOGGER.debug(buf)
                        if len(buf_frag) == 0:
                            break
                    except Exception, e:
                        LOGGER.debug(str(traceback.format_exc()))
                        break
                if buf:
                    LOGGER.debug(buf)
                    try:
                        data = json.loads(buf)
                        if data["option"] == 'QUERY':
                            LOGGER.debug("Action: Query Status")
                            '''
                            {"option" : "QUERY", "duts":[], "status":[]}
                            '''
                            status = []
                            for dut in data["duts"]:
                                bFound = False
                                for g in self.server.groups():
                                    d = g.getDutbyName(dut)
                                    if d:
                                        d.refreshStatus()
                                        status.append(d.status)
                                        break
                                else:
                                    status.append(DUT.STATUS_UNKNOWN)
                            data["status"] = status
                            sock.send(json.dumps(data))
                        if data["option"] == 'QUEUE':
                            LOGGER.debug("Action: Query Queue")
                            '''
                            {"option" : "QUEUE", "duts":[], "pools":[], queue":[]}
                            '''
                            queue = []

                            for dut in data.get('duts', []):
                                tmp = []
                                for g in self.server.groups():
                                    d = g.getDutbyName(dut)
                                    if d and d.task_runner:
                                        _t = d.task_runner.getCurrentTask()
                                        tmp.append(_t)
                                        tmp.append(d.getDedicatedTaskQueue())
                                    break

                                queue.append(tmp)

                            for q in data.get('pools', []):
                                queue.append(rabbitMQ.getDedicatedTaskQueue_pika(self.server.server_config, q))

                            data["queue"] = queue
                            sock.send(json.dumps(data))
                        if data["option"] == 'REORDER':
                            LOGGER.debug("Action: REORDER Queue")
                            '''
                            {"option" : "REORDER", "queue":"", "task_id":""}
                            '''
                            data["rc"] = rabbitMQ.moveToTop_pika(self.server.server_config, data["queue"], data["task_id"])
                            sock.send(json.dumps(data))
                        if data["option"] == 'LATE_LOCK':
                            LOGGER.debug("Action: LATE_LOCK DUT triggered")
                            # {"option": "LATE_LOCK", "lock": True, "dut" : "APL_TEST"}
                            if 'dut' not in data:
                                data['rc'] = -2
                                data['message'] = "key word dut missing!"
                                sock.send(json.dumps(data))
                            else:
                                for g in self.server.groups():
                                    d = g.getDutbyName(data["dut"])
                                    if d:
                                        d.task_runner.scenario_level_pause = data.get('lock', False)
                                        data['rc'] = 0
                                        data['message'] = "Action Triggered!"
                                        sock.send(json.dumps(data))
                                        break
                                else:
                                    data['rc'] = -1
                                    data['message'] = "Selected DUT not found!"
                                    sock.send(json.dumps(data))

                        if data["option"] == 'CANCEL':
                            LOGGER.debug("Action: CANCEL TASK")
                            '''
                            {"option" : "CANCEL", "dut": "", "queue":"", "task_id":""}
                            '''
                            if data.has_key("dut"):
                                # 1. the task might be already triggered
                                d = None
                                for g in self.server.groups():
                                    d = g.getDutbyName(data["dut"])
                                    if d:
                                        break
                                if d and d.task_variable:
                                    _cur_task = d.task_variable
                                    if _cur_task["task_id"] == data["task_id"]:
                                        LOGGER.info("Cancel a task in running with id {} on DUT {}".format(data["task_id"], data["dut"]))
                                        d.task_runner.b_clear = True
                                        d.task_variable["killer"] = data.get("killer", "NA")
                                        data["rc"] = 0
                                        sock.send(json.dumps(data))
                                    else:
                                        data["rc"] = -1
                                        data["message"] = "No such task!"
                                        sock.send(json.dumps(data))
                                else:
                                    data["rc"] = -2
                                    data["message"] = "No such DUT!"
                                    sock.send(json.dumps(data))
                            else:
                                # 2. the task is still in queue
                                #data["rc"] = rabbitMQ.cancelTask(self.server.server_config, data["queue"], data["task_id"])
                                data["rc"] = rabbitMQ.cancelTask_pika(self.server.server_config, data["queue"],
                                                                 data["task_id"])
                                sock.send(json.dumps(data))

                        if data["option"] == "DETAIL":
                            LOGGER.debug("Action: QUERY DETAIL")
                            try:
                                if data.has_key("dut"):
                                    d = None
                                    for g in self.server.groups():
                                        d = g.getDutbyName(data["dut"])
                                        if d:
                                            break
                                    else:
                                        data["rc"] = -1
                                        data["message"] = "No matched dut!"
                                        sock.send(json.dumps(data))
                                    if d.task_runner:
                                        _t = d.task_runner.getCurrentTaskDetails(data.get("case_name", None))
                                        data["result"] = _t
                                        data["rc"] = 0
                                        data["message"] = "query successfully"
                                        sock.send(json.dumps(data))
                                else:
                                    data["rc"] = -2
                                    data["message"] = "key dut missing!"
                                    sock.send(json.dumps(data))
                            except:
                                data["rc"] = -3
                                data["message"] = traceback.format_exc()
                                sock.send(json.dumps(data))
                        if data["option"] == "LOCK":
                            LOGGER.debug("Action: LOCK/UNLOCK DUT INFO")
                            # {"option": "LOCK", "lock": True, "dut" : "APL_TEST"}
                            if 'dut' not in data:
                                data['rc'] = -2
                                data['message'] = "key word dut missing!"
                                sock.send(json.dumps(data))
                            else:
                                for g in self.server.groups():
                                    d = g.getDutbyName(data["dut"])
                                    if d:
                                        if data.get('lock', False):
                                            d.pauseRunner()
                                        else:
                                            d.startRunner()
                                        data['rc'] = 0
                                        data['message'] = "Action Triggered!"
                                        sock.send(json.dumps(data))
                                        break
                                else:
                                    data['rc'] = -1
                                    data['message'] = "Selected DUT not found!"
                                    sock.send(json.dumps(data))

                        if data["option"] == "UPDATE":
                            LOGGER.debug("Action: Update DUT INFO")
                            # {"option": "UPDATE", "dut": "APL_TEST", "dut_name":"", "dut_ip":"",
                            # "test_type" : ["PIT"], "platform":"","subversion":"","project_code":""}
                            if 'dut' not in data:
                                data['rc'] = -2
                                data['message'] = "key word dut missing!"

                            for g in self.server.groups():
                                d = g.getDutbyName(data["dut"])
                                if d:
                                    d.dut_name = data.get("dut_name", d.dut_name)
                                    d.dut_ip = data.get("dut_ip", d.dut_ip)
                                    d.test_type = data.get("test_type", d.test_type)
                                    d.branch = data.get("branch", d.branch)
                                    d.project_code = data.get("project_code", d.project_code)
                                    d.platform = data.get("platform", d.platform)
                                    d.sub_platform = data.get("sub_platform", d.sub_platform)
                                    data['rc'] = 0
                                    sock.send(json.dumps(data))
                                    break
                            else:
                                data['rc'] = -1
                                data['message'] = "Selected DUT not found!"
                                sock.send(json.dumps(data))

                        if data["option"] == "PAAS":
                            LOGGER.debug("Action: PASS REQUIREMENT")
                            try:
                                if data.has_key("dut"):
                                    d = None
                                    for g in self.server.groups():
                                        d = g.getDutbyName(data["dut"])
                                        if d:
                                            break
                                    else:
                                        data["rc"] = -1
                                        data["message"] = "No matched dut!"
                                        sock.send(json.dumps(data))

                                    scenario = Scenario(d.dut_id)
                                    if scenario.load(data):
                                        d.addTestScenarioObject(scenario)
                                    else:
                                        data["rc"] = -4
                                        data["message"] = "failed to load cases from database"
                                        sock.send(json.dumps(data))

                                    data["rc"] = 0
                                    data["message"] = "PaaS scenario generated successfully"
                                    sock.send(json.dumps(data))

                                else:
                                    data["rc"] = -2
                                    data["message"] = "key dut missing!"
                                    sock.send(json.dumps(data))
                            except:
                                data["rc"] = -3
                                data["message"] = traceback.format_exc()
                                sock.send(json.dumps(data))
                    except:
                        sock.send(traceback.format_exc())
            except Exception, e:
                sock.send(-1)
            finally:
                sock.close()

        def run(self):
            while True:
                sock, address = self.sock.accept()
                LOGGER.debug('Connection setup!')
                th = threading.Thread(target=self.launchConnection, args=(sock,))
                th.setDaemon(True)
                th.start()

    def __init__(self):
        self.__groups = {}
        '''
        self.rabbitMQ_address = '127.0.0.1'
        self.rabbitMQ_port = 5678
        '''
        self.server_config = {"rabbitMQ_address" : "10.239.111.152", "rabbitMQ_port" : 5672,
                              "cold_reboot_server_address" : "10.239.132.241" , "cold_reboot_server_port" : 52587,
                              "socket_server_port" : 10001, "max_connection" : 10,
                              "base_share_path" : r"\\sample.com\ec\proj\iag\peg\icg\AUTO_TEST\USTAF",
                              "std_log_path" : 'C:/USTAFLOGS'}

        self.sock_listener = self.SocketListener(self)
        self.work_space_file = ''

    @staticmethod
    def __new__(cls, *args, **kwargs):
        if not cls.__instance:
            try:
                LOCK.acquire()
                if not cls.__instance:
                    cls.__instance = super(Server, cls).__new__(cls, *args, **kwargs)
            finally:
                LOCK.release()
        return cls.__instance

    def updateConfig(self, config):
        for key in self.server_config:
            if key in config:
                self.server_config[key] = config[key]

    def addGroup(self, group):
        self.__groups[group.group_id] = group

    def group(self, group_id):
        return self.__groups[group_id]

    def hasGroup(self,group_id):
        if group_id in self.__groups.keys():
            return True
        else:
            return False

    def groups(self):
        for group_id, group in self.__groups.items():
            yield group

    def clearGroups(self):
        self.__groups.clear()
