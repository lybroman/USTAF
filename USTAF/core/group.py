#-------------------------------------------------------------------------------
# Name:        group.py
# Purpose:
#
# Author:      yuboli
#
# Created:     04/05/2017
# Copyright:   (c) yuboli 2017
# Licence:     <your licence>
#-------------------------------------------------------------------------------
import uuid, time
from logger import LOGGER
from dut import DUT


class Group(object):
    def __init__(self, server=None, group_name='N/A'):
        self.group_id = str(uuid.uuid1())
        time.sleep(0.01)
        self.group_name = group_name
        self.group_info = {"platform":"N/A", "subversion" : "N/A"}
        self.__duts = {}
        self.server_config = server.server_config


    def addDUT(self, dut):
        try:
            self.__duts[dut.dut_id] = dut
            dut.group = self
            LOGGER.debug('Add dut: %s' % str(dut.dut_name))
            return True
        except Exception, e:
            LOGGER.error(str(e))
            LOGGER.debug('Could not add dut: %s' % str(dut.dut_name))
            return False


    def removeDUT(self, dut):
        try:
            dut = self.__duts.pop(dut.dut_id)
            dut.group = None
            LOGGER.debug('Removed dut: %s' % str(dut.dut_name))
            return dut, True
        except Exception, e:
            LOGGER.error(str(e))
            LOGGER.debug('Could not remove dut: %s' % str(dut.dut_name))
            return None, False

    def getDutbyName(self, dut_name):
        for dut in self.duts():
            if dut.dut_name == dut_name:
                return dut
        return None

    def getDut(self, dut_ip):
        for dut in self.duts():
            if dut.dut_ip == dut_ip:
                return dut
        return None

    def duts(self):
        for dut_id, dut in self.__duts.items():
            yield dut

    def dut(self, dut_id):
        return self.__duts[dut_id]



