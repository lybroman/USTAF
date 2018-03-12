#-------------------------------------------------------------------------------
# Name:        run.py
# Purpose:
#
# Author:      yuboli
#
# Created:     16/05/2017
# Copyright:   (c) yuboli 2017
# Licence:     <your licence>
#-------------------------------------------------------------------------------
import os, sys, time, uuid
from USTAF.core.logger import LOGGER

class Run(object):

    # result definition
    NotRun =     0b00000000
    TBD =        0b00000001
    Fail =       0b00000010
    Pass =       0b00000100
    ReRunPass =  0b00001000
    ReAddPass =  0b00010000
    RepeatPass = 0b00100000
    Bypass =     0b01000000
    AlwaysPass = 0b10000000

    NORMAL =            0b000000000000000
    WARM_REBOOT =       0b000000000000001
    COLD_REBOOT =       0b000000000000010
    REBOOT_RECOVERY =   0b000000000000100
    INITIAL_REBOOT =    0b000000000001000
    MANUAL_CANCEL =     0b000000000010000
    ERROR =             0b000000000100000
    DEPENDENCY_FAIL =   0b000000001000000
    CRITICAL_FAIL =     0b000000010000000
    TBD =               0b000000100000000
    HANG_TO =           0b000001000000000
    PASS_BYPASS =       0b000010000000000
    CONNECTION_LOSS =   0b000100000000000
    ENV_FAILURE =       0b001000000000000
    BSOD =              0b010000000000000
    ReRun =             0b100000000000000


    Results = { NotRun : "Not Run",
                Fail : "Fail",
                Pass : "Pass",
                ReRunPass : "Re-Run Pass",
                ReAddPass : "Re-Add Pass",
                TBD       : "TBD",
                RepeatPass: "Repeat Pass",
                Bypass    : "Bypass",
                AlwaysPass: "Always Pass",
                "Not Run" : NotRun,
                "Fail" : Fail,
                "Pass" : Pass,
                "Re-Run Pass" : ReRunPass,
                "Re-Add Pass": ReAddPass,
                "TBD" : TBD,
                "Repeat Pass" : RepeatPass,
                "Bypass" : Bypass,
                "Always Pass" : AlwaysPass,}

    Event = { 0b000000000000000 : "NORMAL",
              0b000000000000001 : "WARM_REBOOT",
              0b000000000000010 : "COLD_REBOOT",
              0b000000000000100 : "REBOOT_RECOVERY",
              0b000000000001000 : "INITIAL_REBOOT",
              0b000000000010000 : "MANUAL_CANCEL",
              0b000000000100000 : "ERROR",
              0b000000001000000 : "DEPENDENCY_FAIL",
              0b000000010000000 : "CRITICAL_FAIL",
              0b000000100000000 : "TBD",
              0b000001000000000 : "HANG_TO",
              0b000010000000000 : "PASS_BYPASS",
              0b000100000000000 : 'CONNECTION_LOSS',
              0b001000000000000 : "ENV_FAILURE",
              0b010000000000000 : 'BSOD',
              0b100000000000000:  'RERUN',
              "NORMAL"          : 0b000000000000000,
              "WARM_REBOOT"     : 0b000000000000001,
              "COLD_REBOOT"     : 0b000000000000010,
              "REBOOT_RECOVERY" : 0b000000000000100,
              "INITIAL_REBOOT"  : 0b000000000001000,
              "MANUAL_CANCEL"   : 0b000000000010000,
              "ERROR"           : 0b000000000100000,
              "DEPENDENCY_FAIL" : 0b000000001000000,
              "CRITICAL_FAIL"   : 0b000000010000000,
              "TBD"             : 0b000000100000000,
              "HANG_TO"         : 0b000001000000000,
              "PASS_BYPASS"     : 0b000010000000000,
              'CONNECTION_LOSS' : 0b000100000000000,
              "ENV_FAILURE"     : 0b001000000000000,
              'BSOD'            : 0b010000000000000,
              'RERUN'           : 0b100000000000000,
              }

    TIMEOUT = 901212

    def __init__(self, case):
        self.__parent = case
        self.run_id = str(uuid.uuid1())
        time.sleep(0.01)
        self.result = self.NotRun
        self.event = self.NORMAL
        self.start = "%.3f" % time.time()
        self.end = ''
        # this field is to store the HSD/BSoD info
        self.comment = ''
        self.std_log_path = []
        self.std_out_err = ''
        self.separator = '-' * 20
        # used for log analysis
        self.error_log = []
        self.hsd_id = ''
        self.hsd_url= ''

    @property
    def pretty_event(self):
        _e = []
        for key in self.Event.keys():
            if type(key) == int and key & self.event > 0:
                _e.append(self.Event[key])
        return _e