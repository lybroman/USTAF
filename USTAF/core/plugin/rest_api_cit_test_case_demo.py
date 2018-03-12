# -*- coding: utf-8 -*-
import requests


LOGIN_URL = 'http://sample.com/rest/login/'
CIT_URL = 'http://sample.com/rest/cit_case_view_set/'
CIT_GUID_TYPE = 4


def api_login(**data):
    session = requests.Session()
    csrf_token = session.get(LOGIN_URL, data=data).json()
    return session, csrf_token


def insert_cit_case(session, **csrf_token):
    data = {
        "guid": {# All the fields is required.
            "year": 2017,
             "ww": 3,
             "day": 0,
             "type": CIT_GUID_TYPE,
             "stack_index": 24,
             "platform": "CIF-SF_3g-Android",
             "sub_platform": "x64"},
        "case_detail": [# ["case_id", "case_name", "out_come", "first_category", "second_category"] is required.
            {
            "case_id": "37020000000001",
            "case_name": "22_XGB--CAMERA_ANDROID_API_PRI_SI_resolution_1280x720",
            "case_type": "Camera_AndroidAPI_PRI",
            "out_come": "Passed",
            "fail_rate": 1,
            "first_category": "Camera Test of Primary",
            "second_category": "Capture Image - Basic",
            "hsd": "22_XGB0000001",
            "hsd_url": "www.22_XGB.com",
            "submitter": "22_XGB",
            "description": "22_XGB description",
            "exe_type": "Auto",
            "patch": "PATCH00000001",
            "owner": "gaobo_22",
            "build": "BUILD00000001"
        },
            {
            "case_id": "37020000000002",
            "case_name": "22_XGB--CAMERA_ANDROID_API_PRI_SI_resolution_1280x740",
            "case_type": "Camera_AndroidAPI_PRI",
            "out_come": "Passed",
            "fail_rate": 1,
            "first_category": "Camera Test of Primary",
            "second_category": "Capture Image - Basic",
            "hsd": "22_XGB0000001",
            "hsd_url": "www.22_XGB.com",
            "submitter": "22_XGB",
            "description": "22_XGB description",
            "exe_type": "Auto",
            "patch": "PATCH00000002",
            "owner": "gaobo_22",
            "build": "BUILD00000002"
            }]
    }
    # set csrf token for post
    data.update(csrf_token)

    response = session.post(CIT_URL, json=data)
    print response.status_code, response.content


def update_cit_case(session, **csrf_token):
    data = {
        "guid": {"year": 2017, "ww": 3, "day": 0, "type": CIT_GUID_TYPE, "stack_index": 24, "platform": "CIF-SF_3g-Android",
                 "sub_platform": "x64"},
        "cit_detail": [{
            "case_id": "37020000000001",
            "case_name": "23_XGB--CAMERA_ANDROID_API_PRI_SI_resolution_1280x720",
            "case_type": "Camera_AndroidAPI_PRI",
            "out_come": "Passed",
            "fail_rate":1,
            "first_category": "Camera Test of Primary",
            "second_category": "Capture Image - Basic",
            "hsd": "23_XGB0000001",
            "hsd_url": "www.23_XGB.com",
            "submitter": "23_XGB",
            "description": "23_XGB description",
            "exe_type": "Auto",
            "patch": "PATCH00000001",
            "owner": "gaobo_23",
            "build": "BUILD00000001"
        },
        {
            "case_id": "37020000000002",
            "case_name": "23_XGB--CAMERA_ANDROID_API_PRI_SI_resolution_1280x740",
            "case_type": "Camera_AndroidAPI_PRI",
            "out_come": "Passed",
            "fail_rate": 1,
            "first_category": "Camera Test of Primary",
            "second_category": "Capture Image - Basic",
            "hsd": "23_XGB0000001",
            "hsd_url": "www.23_XGB.com",
            "submitter": "23_XGB",
            "description": "23_XGB description",
            "exe_type": "Auto",
            "patch": "PATCH00000002",
            "owner": "gaobo_23",
            "build": "BUILD00000002"
        }]
    }
    # set csrf token for post
    data.update(csrf_token)
    response = session.put(CIT_URL, json=data)
    print response.status_code, response.content


def delete_cit_case(session, **csrf_token):
    data = {
        "guid": {"year": 2017, "ww": 3, "day": 0, "type": CIT_GUID_TYPE, "stack_index": 24, "platform": "CIF-SF_3g-Android",
                 "sub_platform": "x64"}
    }
    # set csrf token for post
    data.update(csrf_token)
    response = session.delete(CIT_URL, json=data)
    print response.status_code, response.content


session, csrf_token = api_login(**{'username': 'sys_camsw', 'password': 'q!2345678'})

# test insert cit case data
insert_cit_case(session, **csrf_token)

# test update cit case data
#update_cit_case(session, **csrf_token)

# test delete cit case data
#delete_cit_case(session, **csrf_token)

# rest/platform/get_allowed/ get valid platform