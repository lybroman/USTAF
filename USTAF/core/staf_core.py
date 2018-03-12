#-------------------------------------------------------------------------------
# Name:        staf_core.py
# Purpose:
#
# Author:      yuboli
#
# Created:     02/05/2017
# Copyright:   (c) yuboli 2017
# Licence:     lybroman@hotmail.com
#-------------------------------------------------------------------------------
import sys, os, time, exceptions
from logger import LOGGER
from PyQt4 import QtCore
import re
XSTAF_BIN_PATH = r'C:\STAF\bin'
import traceback

try:
    sys.path.append(XSTAF_BIN_PATH)
    import PySTAF
except ImportError:
    LOGGER.error('Could not import PySTAF module')


class StafHandle(object):

    NO_SUCH_HANDLE_ID = -11
    CONNECTION_FAILED = -22
    INVALID_HANDLE_ID = -33
    UNEXPECTED_CONDITION= -44

    def __init__(self, handle_name="undefined"):
        self.__handle_name = handle_name
        self.staf_handle = None

    def init(self):
        try:
            LOGGER.debug('STAF Handle %s created' % self.__handle_name)
            self.staf_handle = PySTAF.STAFHandle(self.__handle_name)
        except PySTAF.STAFException, e:
            if e.rc == 21:
                LOGGER.error("Error code 21, STAF not running, please start it and try again")
            else:
                LOGGER.error("Error registering with STAF, RC: %d" % e.rc)
            return False

    ##################################################################
    ## Class SafeThread
    ##      to handle STAF stuck bug, kill th if timeout
    ##################################################################
    class SafeThread(QtCore.QThread):
        def __init__(self, func, timeout, **kwargs):
            super(QtCore.QThread, self).__init__()
            self.rc = None
            self.timeout = timeout
            self.func = func
            self.kwargs = kwargs

        def execute(self):
            self.start()
            count = 0
            while True:
                count += 1
                if self.rc:
                    return self.rc
                if count == self.timeout:
                    LOGGER.error("Get logger file failed by {0}s timeout".format(self.timeout))
                    try:
                        self.terminate()
                    except Exception, e:
                        LOGGER.error(str(e))
                    return None
                time.sleep(1)

        def run(self):
            self.rc = self.func(**self.kwargs)

    def __stafSubmit(self, location, service, request):
        rc = self.staf_handle.submit(location, service, request)
        return rc

    def _stafSubmit(self, location, service, request, timeout=30):
        th = self.SafeThread(self.__stafSubmit, timeout, location=location, service=service, request=request)
        th.execute()
        return th.rc

    '''
    Ping service: to check if dut alive
    '''
    def ping(self, dut):
        try:
            location = 'local'
            service = 'Ping'
            request = 'Ping machine %s' % dut
            rc = self._stafSubmit(location, service, request)
            if rc and rc.rc == 0 and rc.result == 'PONG':
                return 0
            else:
                return self.UNEXPECTED_CONDITION
        except:
            LOGGER.error(traceback.format_exc())
            return self.UNEXPECTED_CONDITION

    def unregister(self):
        self.staf_handle.unregister()


    '''
    Start a process
    '''
    def startProcessAsync(self, address, cmdline, log_path=''):
        try:
            location = address
            service = 'Process'
            if log_path:
                request = 'START SHELL COMMAND %s async workload %s stdout %s stderrTostdout' % (cmdline, self.__handle_name, log_path)
            else:
                request = 'START SHELL COMMAND %s async workload %s' % (cmdline, self.__handle_name)

            LOGGER.debug('START SHELL COMMAND %s async workload %s' % (cmdline,  self.__handle_name))
            rc = self._stafSubmit(location, service, request)
            '''
            handle id in str fmt
            '''
            return str(rc.resultContext.getRootObject())
        except:
            LOGGER.error(traceback.format_exc())
            return self.INVALID_HANDLE_ID

    def warmReboot(self, address, log_file=r'C:/XSTAF/warm_reboot.log'):
        try:
            location = '%s' % address
            service = 'Process'
            request = 'START SHELL COMMAND %s async workload %s stdout %s stderrTostdout' % ('shutdown -r -t 0', 'WARM_REBOOT', log_file)
            #request = 'START SHELL COMMAND %s async workload %s stdout %s stderrTostdout' % ('shutdown -r -t secs 0', 'WARM_REBOOT', log_file)
            rc = self._stafSubmit(location, service, request)
            return rc.rc
        except:
            LOGGER.error(traceback.format_exc())
            return -1

    def stopProcess(self, address, handle_id):
        try:
            location = address
            service = 'Process'
            request = 'STOP HANDLE %s' % (str(handle_id))
            LOGGER.debug('stop handle for handle id %s' % (str(handle_id)))
            rc = self._stafSubmit(location, service, request)
            if rc:
                return rc.rc
            else:
                return -1
        except:
            LOGGER.error(traceback.format_exc())
            return -1

    def clean_process_status(self, address):
        '''
        free process info, we need to free process info before start new process
        '''
        LOGGER.debug("clean process +")
        location = '%s' % address
        service = 'Process'
        request = 'free workload %s' % self.__handle_name
        rc = self._stafSubmit(location, service, request)
        LOGGER.debug("clean process -")
        return rc
    '''
    Query test results
    '''
    def queryResultAsync(self, address, handle_id):
        location = address
        service = 'Process'
        request = 'Query HANDLE %s' % (handle_id)
        rc = self._stafSubmit(location, service, request)
        """
        query result template as below
        1. The specified handle does not exist: xxx
        2. {
              Handle         : 134
              Handle Name    : <None>
              Title          : <None>
              Workload       : test
              Shell          : <Default Shell>
              Command        : cmd.exe notepad
              Parms          : <None>
              Workdir        : <None>
              Focus          : Background
              User Name      : <None>
              Key            : <None>
              PID            : 33104
              Start Mode     : Async
              Start Date-Time: 20170522-13:41:47
              End Date-Time  : 20170522-13:41:50
              Return Code    : 3221225786
            }
        """
        if rc and rc.rc == 0:
            result = rc.resultContext.getRootObject()
            return result['startTimestamp'], result['endTimestamp'], result['rc']
        elif rc and rc.rc == 5:
            return None, None, self.NO_SUCH_HANDLE_ID
        elif rc and (rc.rc == 16 or rc.rc == 22):
            return None, None, self.CONNECTION_FAILED
        else:
            LOGGER.error(rc.resultContext)
            return None, None, self.UNEXPECTED_CONDITION

    def setVar(self, address, variable, value):
        location = address
        service = 'VAR'
        request = 'SET SYSTEM VAR {0}={1}'.format(variable, value)
        rc = self._stafSubmit(location, service, request)
        if rc and rc.rc == 0:
            LOGGER.info('SET SYSTEM VAR {0}={1}'.format(variable, value))
            return True
        else:
            return False

    def getFile(self, address, path):
        service = "FS"
        location = '%s' % address
        request = 'GET FILE {0}'.format(path)
        rc = self._stafSubmit(location, service, request)
        # rc = 48 -> no such file
        if rc and rc.rc == 0:
            logs = str(rc.resultContext)
            return logs
        else:
            return ''

    def get_dut_hostname_windows(self, address):
        '''
        need handle the OS: Win or Linux or Android?
        THIS FUNCTION COULD NOT BE REUSED.... as some HARDCODE are here....
        '''
        hostname = ""
        mac = ""
        cmd = "hostname"
        location = '%s' % address
        service = 'PROCESS'
        request = 'START SHELL COMMAND "{0}" STDERRTOSTDOUT RETURNSTDOUT WAIT'.format(cmd)
        result = self.staf_handle.submit(location, service, request)
        try:
            if result and result.resultContext.getRootObject()['fileList'][0]['data']:
                info = {}
                # return result.resultContext.getRootObject()['fileList'][0]['data']
                lines = result.resultContext.getRootObject()['fileList'][0]['data'].replace('\n', '').split('\r')
                # LOGGER.info(lines)
                hostname = lines[0]
                # LOGGER.info(hostname)
            else:
                return None, None
        except Exception, e:
            LOGGER.error(str(e))

        cmd = "getmac"
        location = '%s' % address
        service = 'PROCESS'
        request = 'START SHELL COMMAND "{0}" STDERRTOSTDOUT RETURNSTDOUT WAIT'.format(cmd)
        result = self.staf_handle.submit(location, service, request)
        try:
            if result and result.resultContext.getRootObject()['fileList'][0]['data']:
                info = {}
                # return result.resultContext.getRootObject()['fileList'][0]['data']
                lines = result.resultContext.getRootObject()['fileList'][0]['data'].replace('\n', '').split('\r')
                for line in lines:
                    # LOGGER.info(line)
                    if 'disconnected' not in str.lower(line) and len(
                            line) > 0 and "=" not in line and "address" not in str.lower(line):
                        mac = line.split(" ")[0]
                        break
            else:
                return None, None
        except Exception, e:
            LOGGER.error(str(e))

        return hostname, mac

    def get_dut_info(self, dut):
        '''
        need handle the OS: Win or Linux or Android?
        THIS FUNCTION COULD NOT BE REUSED.... as some HARDCODE are here....
        '''
        if dut.dut_type == 'linux':
            # linux dut info is not available
            return {}

        address = dut.dut_ip
        cmd = 'systeminfo'
        location = '%s' % address
        service = 'PROCESS'
        request = 'START SHELL COMMAND "{0}" STDERRTOSTDOUT RETURNSTDOUT WAIT'.format(cmd)
        result = self._stafSubmit(location, service, request)
        try:
            if result and result.resultContext.getRootObject()['fileList'][0]['data']:
                info = {}
                info['GFX'] = ''
                # return result.resultContext.getRootObject()['fileList'][0]['data']
                lines = result.resultContext.getRootObject()['fileList'][0]['data'].replace('\n', '').split('\r')
                for line in lines:
                    if 'System Model' in line:
                        info['System Model'] = line.split(':')[1].strip()
                    if 'OS Name' in line:
                        info['OS Name'] = line.split(':')[1].strip()
                    if 'OS Version' in line and 'BIOS Version' not in line:
                        info['OS Version'] = line.split(':')[1].strip()
                    if 'BIOS Version' in line:
                        info['BIOS Version'] = line.split(':')[1].strip()
                hostname, mac = self.get_dut_hostname_windows(address)
                if hostname and mac:
                    info["dut_mac_address"] = mac + " " + hostname
                '''
                get bkc and gfx
                '''
                try:
                    service = "FS"
                    location = '%s' % address
                    request = 'GET FILE C:/Tools/IntelDeviceDoctor/Telemetry/ProcessedFiles/BKCMeta.xml'
                    result, event = self.staf_handle(location, service, request)
                    line = str(result.resultContext)

                    if '<ProgramName>' in line:
                        pt = re.compile('<ProgramName>(\S*)</ProgramName>')
                        rc = re.search(pt, line)
                        info['BKC'] = rc.group(1)

                    if '<Wwk>' in line:
                        pt = re.compile('<Wwk>(\S*)</Wwk>')
                        rc = re.search(pt, line)
                        info['BKC'] += '-' + rc.group(1)

                    """
                    <Name>Intel(R) HD Graphics</Name>
                    <Vendor>Intel Corporation</Vendor>
                    <Version>20.19.15.4408</Version>
                    """

                    pt = re.compile(
                        '<Name>Intel\(R\) HD Graphics</Name><Vendor>Intel Corporation</Vendor><Version>(\S*)</Version>')
                    rc = re.search(pt, line)
                    info['GFX'] = '[BKC CONFIG]Intel(R) HD Graphics: {}'.format(rc.group(1))

                except:
                    pass
                    # print traceback.format_exc()

                try:
                    cmd = "C:/AutoBAT/bat/CommonTools/dism /online /get-drivers"
                    location = '%s' % address
                    service = 'PROCESS'
                    request = 'START SHELL COMMAND "{0}" STDERRTOSTDOUT RETURNSTDOUT WAIT'.format(cmd)
                    result = self.staf_handle.submit(location, service, request)
                    if result and result.resultContext.getRootObject()['fileList'][0]['data']:
                        lines = result.resultContext.getRootObject()['fileList'][0]['data'].replace('\n', '').split(
                            '\r')
                        for i in range(0, len(lines)):
                            if 'Display' in lines[i]:
                                info['GFX'] += '[DISM]' + lines[i + 2] + ' ' + lines[i + 3]
                                break
                except:
                    LOGGER.error(traceback.format_exc())
                    info['GFX'] += '[DISM]' + 'Failed to Get version w/ DISM Tool'
                return info
            else:
                return {}
        except Exception, e:
            LOGGER.error(str(e))

    def trigger_cmdline(self, DUT, cmdline):
        location = DUT
        service = 'PROCESS'
        request = 'START SHELL COMMAND {0} STDERRTOSTDOUT RETURNSTDOUT WAIT 60s'.format(cmdline)

        result = self.staf_handle.submit(location, service, request)
        if result.rc == 0:
            return True, result
        else:
            LOGGER.warning("trigger cmd line %s fail, RC: %d, Result: %s" % (cmdline, result.rc, result.result))
            return False, result

    def get_bsod_files_adv(self, dut_instance):
        bsod_dict = {}
        if dut_instance.dut_type == 'linux':
            # linux not support BSoD analysis
            return [], {}
        try:
            # TODO: directly return for linux device!
            # print DUT
            get_bsod_cmd = 'C:/AutoBAT/bat/CommonTools/CameraCommonLogAnalysis.py'
            bget, result = self.trigger_cmdline(dut_instance.dut_ip, get_bsod_cmd)
            if bget and result.rc == 0:
                if result.resultContext.getRootObject()['fileList'][0]['data']:
                    # print result.resultContext.getRootObject()['fileList'][0]['data']
                    lines = result.resultContext.getRootObject()['fileList'][0]['data'].replace('\n', '').split('\r')
                    # print lines
                    i = -1
                    for line in lines:
                        i += 1
                        # print line
                        if ':' in line:
                            if line.split(':')[0] in bsod_dict.keys():
                                bsod_dict[line.split(':')[0] + '_' + str(i)] = line.split(':')[1]
                            else:
                                bsod_dict[line.split(':')[0]] = line.split(':')[1]
                    return bsod_dict.keys(), bsod_dict
                else:
                    return [], {}
            else:
                return [], {}
        except Exception, e:
            # in case of unexpected conditions
            LOGGER.error(str(e))
            return [], {}

    def create_directory(self, DUT, directory):
        try:
            location = '%s' % DUT
            service = 'FS'
            request = 'CREATE DIRECTORY %s FULLPATH' % directory
            rc = self._stafSubmit(location, service, request)
            if rc and rc.rc == 0:
                return 0
            else:
                return -1
        except:
            LOGGER.error(traceback.format_exc())
            return - 2

    def copy_sync_file(self, DUT, local_file, remote_file):
        try:
            LOGGER.debug("File on server:{0}, file on DUT {1}".format(local_file, remote_file))
            location = '%s' % DUT
            service = "FS"
            if not os.path.isfile(local_file):
                return -3
            request = 'COPY FILE %s TOFILE  %s TOMACHINE %s' % (local_file, remote_file, location)
            self.create_directory(DUT, os.path.dirname(remote_file))
            rc = self._stafSubmit('local', service, request)
            if rc and rc.rc == 0:
                return 0
            else:
                return -1
        except:
            LOGGER.error(traceback.format_exc())
            return - 2


# sample test code
'''
a = StafHandle('123')
a.init()
log = a.trigger_cmdline("10.238.133.100", "~/sw_val/scripts/tools/print_err_msg.sh 46780 CAMERA_FUNCTION_AUTO_NORMAL_30FPS_BASIC_CAPTURE_SINGLE_CAM_USERPTR_1920x1080_NV12 ")
print log
'''