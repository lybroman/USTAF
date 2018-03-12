import websocket
import json
from USTAF.core.logger import LOGGER
import threading
import traceback


def send_to_server_th(data, dut_name, platform, run_id, build):
    th = threading.Thread(target=send_to_server, args=(data, dut_name, platform, run_id, build,))
    th.start()


def send_to_server(data, dut_name, platform, run_id, build):
    for case in data:
        jt = json_template.copy()
        jt["hw_serial"] = dut_name
        jt["hw_type"] = platform
        jt["run_id"] = run_id
        jt["sw_version"] = build

        try:
            jt["timestamp"] = float(case.start)
            jt["duration"] = float(case.end) - float(case.start)
        except:
            LOGGER.warning(traceback.format_exc())

        jt["application"]["name"] = case.name
        jt["action_verdicts"]["final"] = case.pretty_result

        try:
            err_log = ''
            for run in case.runs():
                err_log += '||'.join(['|'.join(_) for _ in run.error_log])
            jt["notes"] = [err_log]
        except:
            LOGGER.error(traceback.format_exc())

        LOGGER.debug(jt)
        send_report(json.dumps(jt))

json_template = {
    "hw_serial": "placeholder",
    "hw_type": "placeholder",
    "sw_version": "placeholder",
    "run_id": "placeholder",
    "timestamp": 0,
    "duration": 0,
    "application": {
        "name": "placeholder"
    },
    "action_verdicts": {
        "final": "placeholder"
    },
    "notes": [],
    "screenshots": {}
}


def send_report(report_str):
    """Send contents of report_str to server"""
    report_error = None
    reportws = "ws://mbt.tm.sample.com/stream/testruns"

    print "online reporting %s kB to %s..." %(len(report_str)/1024, reportws)
    try:
        ws = websocket.create_connection(reportws, header=["Sec-WebSocket-Protocol:logmongo"], timeout=10)
        if json.loads(ws.recv())["retval"] != 0:
            raise Exception("Nonzero retval from %s." %(reportws,))
        LOGGER.debug("online reporting connected")
    except Exception, e:
        report_error = "Connection error: (%s) %s" % (type(e), e)
    if not report_error:
        try:
            ws.send(report_str)
            LOGGER.debug( "online report sent")
            rc = ws.recv() #Print out the server response.
            print(rc)
            LOGGER.info(rc)
        except Exception, e:
            LOGGER.error(e)
            report_error = "sending report to %s failed: %s" %(reportws, e)
    else:
        print(report_error)
        LOGGER.error( "Failed to send report!")
        LOGGER.error( report_error)

