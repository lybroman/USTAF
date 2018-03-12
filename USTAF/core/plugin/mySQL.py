import MySQLdb
import traceback, datetime, time
from USTAF.core.logger import LOGGER
from dashboard import get_current_intel_calendar
import threading

# set maximum connection num to 100
semaphore = threading.Semaphore(100)

class SQLConnection(object):
    # need to modify the pwd, if you run this on your local host
    def __init__(self, host="localhost", port=3306, username="root", pwd="sample.123", schema="ustaf"):
        self.host = host
        self.port = port
        self.username = username
        self.pwd = pwd
        self.schema = schema
        self.conn = None
        self.cur = None

    def init(self):
        global semaphore
        semaphore.acquire()
        try:
            self.conn = MySQLdb.connect(
            host=self.host,
            port = self.port,
            user=self.username ,
            passwd=self.pwd,
            db =self.schema,
            )
            self.cur = self.conn.cursor()
            return True
        except:
            LOGGER.error(traceback.format_exc())
            return False
        finally:
            semaphore.release()

    def insertTestResults(self, test_result):
        sql = "INSERT INTO test_result(\
            test_type, project_code, platform, subversion, pass_rate, date, build_no, patch, owner, info, fail_case_list, test_set) \
            VALUES ('%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s' )" % \
              (test_result.test_type, test_result.project_code, test_result.platform, test_result.subversion,
               test_result.pass_rate, get_current_intel_calendar()[3], test_result.build,
               test_result.patch, test_result.owner, '', ';'.join(test_result.fail_case_list), test_result.scenario_name)

        self.cur.execute(sql)
        self.conn.commit()

    def close(self):
        if self.conn:
            if self.cur:
                self.cur.close()
            self.conn.close()
