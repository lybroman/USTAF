__author__ = "yuboli"

import datetime, time
import requests, json, pprint, traceback
from USTAF.core.logger import LOGGER

# http://icg-dashboard.sample.com/rest/dev/
LOGIN_URL =     'http://sample.com/rest/login/'
CIT_URL =       'http://sample.com/rest/cit_case_view_set/'
PIT_LITE_URL =  'http://sample.com/rest/pit_lite_case_view_set/'
PIT_URL =       'http://sample.com/rest/pit_case_view_set/'
WEEKLY_URL =    'http://sample.com/rest/weekly_case_view_set/'
CIT_GUID_TYPE = 4
PIT_LITE_GUID_TYPE = 3
PIT_GUID_TYPE = 2
WEEKLY_GUID_TYPE = 1

result_map = {"fail":"Failed", "pass":"Passed", "repeat-pass": "Passed", "not-run":"N/A"}

login_password = ''
login_usr = ''

def api_login(**data):
    session = requests.Session()
    csrf_token = session.get(LOGIN_URL, data=data, timeout=60).json()
    return session, csrf_token

def get_current_intel_calendar():
    date = datetime.datetime.fromtimestamp(time.time()).strftime("%Y-%W-%w")
    year = date.split('-')[0]
    """
    solution for '2017'
    """
    week = int(date.split('-')[1])
    day = int(date.split('-')[2])
    date = str(date.split('-')[0]) + '/' + str(week) + '/' + str(day)
    return year, week, day, date


def insertTestResult(test_result, html_path=''):
    try:
        data = dict()
        session, csrf_token = api_login(**{'username': 'username', 'password': 'password'})
        year, week, day, date = get_current_intel_calendar()
        stack_index = 0
        if test_result.report_ww != 'NA':
            year, others = test_result.report_ww.split('WW')
            week, stack_index = others.split('_')

        if test_result.test_type == 'PIT_LITE':
            GUID_TYPE = PIT_LITE_GUID_TYPE
            URL = PIT_LITE_URL
        elif test_result.test_type == 'CIT':
            GUID_TYPE = CIT_GUID_TYPE
            URL = CIT_URL
        elif test_result.test_type == 'PIT':
            GUID_TYPE = PIT_GUID_TYPE
            URL = PIT_URL
        else:
            GUID_TYPE = WEEKLY_GUID_TYPE
            URL = WEEKLY_URL
            day = 0

        guid = {"year": year, "ww": week, "day": day, "type": GUID_TYPE, "stack_index": int(stack_index),
                 "platform": test_result.platform,
                 "sub_platform": test_result.sub_platform}

        if GUID_TYPE == CIT_GUID_TYPE:
            checkintest_detail = {}
            checkintest_detail["result_id"] = ''
            checkintest_detail["os"] = test_result.os
            checkintest_detail["subject"] = test_result.subject
            checkintest_detail["build"] = test_result.build
            checkintest_detail["scenario"] = str(test_result.scenario_name.split('_'))
            checkintest_detail["owner"] = test_result.owner
            checkintest_detail["patch"] = test_result.patch
            checkintest_detail["email"] = test_result.email
            checkintest_detail["html_fn"] = html_path
            checkintest_detail["html_fn_log"] = test_result.log_path
            checkintest_detail["scenario_for_retrigger"] = test_result.scenario_name
            data["checkintest_detail"]=checkintest_detail

        case_detail =list()
        cases = [case.name for case in test_result.cases]
        cases = queryCaseDetails(cases)

        if cases:
            for i in xrange(len(test_result.cases)):
                if not test_result.cases[i].bEnv and 'ENV' not in test_result.cases[i].name:
                    case_item = {
                        "case_name": test_result.cases[i].name,
                        "out_come": result_map.get(test_result.cases[i].pretty_result, "Failed"),
                        "case_id": test_result.cases[i].name,
                        "first_category": cases[i]["first_category"],
                        "second_category": cases[i]["second_category"],
                        "exe_type": "Auto",
                        "hsd": ''.join(test_result.cases[i].hsd_id),
                        "hsd_url": ''.join(test_result.cases[i].hsd_url),
                        "fail_rate": 1 - test_result.cases[i].pass_rate,
                        "build": test_result.build,
                        "owner" : test_result.owner,
                        "patch" :test_result.patch,
                        'error_log': {
                            'fail_type': 'True',
                            'driver_log': '',  # optional
                            'fw_log': '',  # optional
                            'crash_log': '',  # optional
                            'error_log': test_result.cases[i].error_log,  # optional
                            'exec_time': 0.0,
                            'rerun_time': '0.0'
                        }
                    }

                    case_detail.append(case_item)
                else:
                    LOGGER.debug("Bypass {} env case".format(test_result.cases[i].name))
        else:
            LOGGER.error("Failed to query case details from dashboard!")
            return

        data.update({"guid":guid, "case_detail":case_detail})
        data.update(csrf_token)
        LOGGER.debug(data)
        LOGGER.info('data: {0}'.format(data))
        response = session.post(URL,json = data)
        if response.status_code != 200 or 'success' not in str(response.content).lower():
            response = session.put(URL, json=data)
        LOGGER.info('upload results: {} {}'.format(response.status_code, response.content))

    except:
        LOGGER.error(traceback.format_exc())

def queryCaseDetails(cases):
    data = {'test_case_id_list':json.dumps(cases)}
    CASE_DETAIL_URL = 'http://10.239.111.152/rest/query_parent_category/'
    response = requests.post(url=CASE_DETAIL_URL, data=data)
    if response.status_code == 200:
        return json.loads(response.content)
    else:
        return None

def getPlatfrom():
    session, csrf_token = api_login(**{'username': 'sys_camsw', 'password': 'q!2345678'})
    url = 'http://10.239.111.152/rest/platform/get_allowed/'
    data = {}
    response = session.get(url, json=data).json()
    pprint.pprint(response)

#print queryCaseDetails(["CAMERA_CHECK_CAMERA_POSITION_PRIMARY_PREVIEW_NV12_VIDEO_MAX_NV12"])
#session, csrf_token = api_login(**{'username': 'sys_camsw', 'password': 'q!2345678'})
#print csrf_token

#session, csrf_token = api_login(**{'username': 'sys_camsw', 'password': 'q!2345678'})


def query_error_log_from_dashboard(platform, subversion, test_type):
    para_query_test_result = [{u'platform': u'IPU4-APL-WIN',
                               u'date': u'2017/29/8',
                               u'type': 'weekly',
                               u'daily_type': 'pit_lite',
                               u'sub_platform': '',
                               u'password': login_password,
                               u'username': login_usr,}]

    date = get_current_intel_calendar()

    pp = para_query_test_result[0]
    pp['platform'] = u'{0}'.format(platform)
    pp['sub_platform'] = u'{0}'.format(subversion)
    pp['date'] = u'{0}'.format(date)
    pp['type'] = u'{0}'.format(test_type)

    try:
        # data = {'test_case_id_list': json.dumps(pp)}
        data =pp
        # print(data)
        QUERY_URL = 'http://sample.com/rest/query_error_log/'
        response = requests.post(url=QUERY_URL, data=data)
        if response.status_code == 200:
            query_result = response.content
            return json.loads(query_result)["data"]["result"]
        else:
            return None
    except:
        print(traceback.format_exc())
        LOGGER.error(traceback.format_exc())
        return None

# print query_error_log_from_dashboard('TestPlatform', '', 'weekly')