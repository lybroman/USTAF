import urllib2
import requests
import time
import json
import re
from USTAF.core.logger import LOGGER
import traceback

def gerritRequest(query_url):
    username = 'username'
    password = "password"
    base_url = query_url
    try:
        time.sleep(0.1)
        password_mgr = urllib2.HTTPPasswordMgrWithDefaultRealm()
        password_mgr.add_password(None, base_url, username, password)
        urllib2.install_opener(urllib2.build_opener(urllib2.HTTPBasicAuthHandler(password_mgr)))
        res = urllib2.urlopen(urllib2.Request(base_url))
        response = res.read().lstrip(")]}'").strip()
        res.close()
        return json.loads(response)
    except Exception, e:
        print str(e)
        return None

def getParentInfo(commit_id, bundle_id_list, slot, iter=False):
    query_url = "https://icggerrit.corp.sample.com/a/changes/?q=commit:%s" % commit_id
    rc = gerritRequest(query_url)
    if rc and type(rc) == list and len(rc) > 0:
        if "patches" not in slot:
            slot["patches"] = [rc[0]["change_id"]]
            slot["sub_subjects"] = [rc[0]["subject"]]
        else:
            slot["patches"].append(rc[0]["change_id"])
            slot["sub_subjects"].append(rc[0]["subject"])

        if iter:
            getMergeSlotInfo(rc[0]["change_id"], bundle_id_list)


def isMergeSlot(subject):
    try:
        pt = re.compile('Merge "(.*)"')
        rc = re.search(pt, subject)
        if rc and rc.group(0):
            #print rc.group(1)
            return True
        else:
            return False
    except:
        LOGGER.error(traceback.format_exc())
        return False


def getMergeSlotInfo(change_id, bundle_id_list):
    LOGGER.critical("change id: {}".format(change_id))
    _d = dict()
    _d["change_id"] = change_id
    if '/' in change_id:
        change_id = change_id.split('/')[0]

    query_url = "https://sample.com/a/changes/%s/detail/?o=CURRENT_REVISION&o=CURRENT_COMMIT" % change_id
    rc = gerritRequest(query_url)
    _d["subject"] = rc['subject']
    if 'Merge' in rc['subject']:
        _ls = rc["revisions"][rc["revisions"].keys()[0]]["commit"]["parents"]
        for _i in _ls:
            print _i["subject"], _i["commit"]
            if isMergeSlot(_i["subject"]):
                getParentInfo(str(_i["commit"]), bundle_id_list, _d, True)
            else:
                getParentInfo(str(_i["commit"]), bundle_id_list, _d, False)

        bundle_id_list.append(_d)
    return


#b = []
#getMergeSlotInfo("263105", b)
#print b

#print "262805/1".split('/')[0]
