#-------------------------------------------------------------------------------
# Name:        logger.py
# Purpose:
#
# Author:      yuboli
#
# Created:     02/05/2017
# Copyright:   (c) yuboli 2017
# Licence:     lybroman@hotmail.com
#-------------------------------------------------------------------------------

from PyQt4 import QtCore, QtGui
import logging, sys, types, threading, os
LOCK = threading.Lock()
def level_name(level):
    return logging._levelNames[level]

class USTAFLogger(QtCore.QObject):
    __instance = None
    update_log = QtCore.SIGNAL("update_log")

    @staticmethod
    def __new__(cls, *args, **kwargs):
        if not cls.__instance:
            try:
                LOCK.acquire()
                if not cls.__instance:
                    cls.__instance = super(USTAFLogger, cls).__new__(cls, *args, **kwargs)
            finally:
                LOCK.release()
        return cls.__instance


    def __init__(self):
        super(USTAFLogger,self).__init__()
        self.__logger_name = 'USTAF'
        self.__logging = logging.getLogger(self.__logger_name)
        self.logging_config = {
        'logging_file_level' : 'DEBUG',
        'logging_stream_level' : 'DEBUG',
        'logging_stream' : sys.stdout,
        'logging_file_name' : 'C:/USTAF/Ustaf_log.log',
        'logging_format' : '"[%(asctime)s][%(filename)s][line:%(lineno)d][%(levelname)s]:%(message)s"'
        }

        self.debug = self.__logging.debug
        self.info = self.__logging.info
        # could avoid
        self.warn = self.__logging.warn
        # nothing could do to handle
        self.warning = self.__logging.warning
        self.error = self.__logging.error
        self.critical = self.__logging.critical

    def config(self, **kwargs):
        for key, value in kwargs.items():
            if key in self.logging_config.keys():
                self.logging_config[key] = value
        logging_stream = self.logging_config['logging_stream']

        self.__logging.propagate = False
        self.__logging.setLevel(logging.DEBUG)
        self.__logging.handlers = []

        # stream handler
        if logging_stream:
            stream_handler = logging.StreamHandler(logging_stream)
            stream_handler.setLevel(level_name(self.logging_config['logging_stream_level']))
            formatter = logging.Formatter(self.logging_config['logging_format'])
            stream_handler.setFormatter(formatter)
            self.__logging.addHandler(stream_handler)


            def combinedEmit(*args):
                record = args[1]
                self.emit(self.update_log, record)
                logging.StreamHandler.emit(*args)

            stream_handler.emit = types.MethodType(combinedEmit, stream_handler)

        logging_file_location = os.path.dirname(self.logging_config['logging_file_name'])
        if not os.path.isdir(logging_file_location):
            os.makedirs(logging_file_location)

        # using append mode
        file_handler = logging.FileHandler(self.logging_config['logging_file_name'], mode='a')
        file_handler.setLevel(level_name(self.logging_config['logging_file_level']))
        formatter = logging.Formatter(self.logging_config['logging_format'])
        file_handler.setFormatter(formatter)
        self.__logging.addHandler(file_handler)


LOGGER = USTAFLogger()







