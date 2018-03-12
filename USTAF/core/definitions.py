#-------------------------------------------------------------------------------
# Name:        definitions.py
# Purpose:
#
# Author:      yuboli
#
# Created:     04/05/2017
# Copyright:   (c) yuboli 2017
# Licence:     <your licence>
#-------------------------------------------------------------------------------

EVENT_DICT = {
              0b00000000 : "NORMAL",
              0b00000001 : "WARM_REBOOT",
              0b00000010 : "COLD_REBOOT",
              0b00000100 : "REBOOT_RECOVERY",
              0b00001000 : "INITIAL_REBOOT",
              0b00010000 : "MANUAL_CANCEL",
              0b00100000 : "ERROR",
              "NORMAL"          : 0b00000000,
              "WARM_REBOOT"     : 0b00000001,
              "COLD_REBOOT"     : 0b00000010,
              "REBOOT_RECOVERY" : 0b00000100,
              "INITIAL_REBOOT"  : 0b00001000,
              "MANUAL_CANCEL"   : 0b00010000,
              "ERROR"           : 0b00100000,}

