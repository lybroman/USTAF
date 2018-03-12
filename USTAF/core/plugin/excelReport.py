import os, sys, time
from pyExcelerator import *
from USTAF.core.logger import LOGGER
import traceback
from email.mime.text import MIMEText


def generateExcelResults(test_result):
    try:
        base_path = r'{}/excel/{}'.format(test_result.server_config["base_share_path"], test_result.dut_name)
        if not os.path.isdir(base_path):
            os.mkdir(base_path)
        filename = r'{}/{}_{}_{}.xls'.format(base_path, test_result.scenario_name, test_result.build, "%.3f" % time.time())

        w = Workbook()
        ws = w.add_sheet('case_result')
        # -------------------------------------------------------------------------- xls settings
        # -----------------------------------title
        pattern0 = Pattern()
        pattern0.pattern = pattern0.SOLID_PATTERN
        pattern0.pattern_fore_colour = 0x5
        pattern0.pattern_back_colour = 0x5
        style0 = XFStyle()
        style0.pattern = pattern0
        # ---------------------------------- blank
        pattern5 = Pattern()
        pattern5.pattern = pattern0.SOLID_PATTERN
        pattern5.pattern_fore_colour = 0x09
        pattern5.pattern_back_colour = 0x09
        style5 = XFStyle()
        style5.pattern = pattern5
        # -----------------------------------pass
        pattern1 = Pattern()
        pattern1.pattern = pattern0.SOLID_PATTERN
        pattern1.pattern_fore_colour = 0x11
        pattern1.pattern_back_colour = 0x11
        style1 = XFStyle()
        style1.pattern = pattern1
        # ----------------------------------fail
        pattern2 = Pattern()
        pattern2.pattern = pattern0.SOLID_PATTERN
        pattern2.pattern_fore_colour = 0x0A
        pattern2.pattern_back_colour = 0x0A
        style2 = XFStyle()
        style2.pattern = pattern2
        # ----------------------------------cancelled
        pattern3 = Pattern()
        pattern3.pattern = pattern0.SOLID_PATTERN
        pattern3.pattern_fore_colour = 0x17
        pattern3.pattern_back_colour = 0x17
        style3 = XFStyle()
        style3.pattern = pattern3
        # -----------------------------------repeat pass
        pattern4 = Pattern()
        pattern4.pattern = pattern0.SOLID_PATTERN
        pattern4.pattern_fore_colour = 0x35
        pattern4.pattern_back_colour = 0x35
        style4 = XFStyle()
        style4.pattern = pattern4
        # -------------------------------------set info
        ws.write(0, 0, 'CASE_NAME', style0)
        ws.write(0, 1, 'RESULT', style0)
        ws.write(0, 2, 'BEGIN TIME', style0)
        ws.write(0, 3, 'END TIME', style0)
        ws.write(0, 4, 'HSD ID', style0)
        ws.write(0, 5, 'ERROR LOG', style0)
        ws.write(0, 6, 'RERUN CMD', style0)
        ws.write(0, 7, 'ADDITIONAL INFO', style0)
        ws.write(0, 8, 'STDOUT/ERR', style0)

        i = 0
        std_logs_list = []
        for case in test_result.cases:
            try:
                ws.write(i + 1, 0, case.name)
                res = case.pretty_result
                style = style0
                if res == 'not-run':
                    style = style3
                elif res == 'pass':
                    style = style1
                elif res == 'fail':
                    style = style2
                elif res == 'repeat pass':
                    style = style4
                ws.write(i + 1, 1, res, style)
                ws.write(i + 1, 2, case.start)
                ws.write(i + 1, 3, case.end)
                err_log = ''
                std_log = str(i) + ' ' + case.name + ':\r\n'
                #print case.error_log
                """
                for run in case.runs():
                    err_log += '||'.join(['|'.join(_) for _ in run.error_log])
                    std_log += run.std_out_err + '\r\n'
                """
                ws.write(i + 1, 5, case.error_log)
                ws.write(i + 1, 6, case.cmd)
                ws.write(i + 1, 7, '')
                ws.write(i + 1, 8, '')
                std_logs_list.append(case.std_log)

            except:
                LOGGER.error(traceback.format_exc())
            i += 1

        w.save(filename)
        att = None

        try:
            try:
                std_logs_all = ''.join(std_logs_list)
                att = MIMEText(std_logs_all, 'plain', 'gb2312')
                att["Content-Type"] = 'text/plain'
                att["Content-Disposition"] = 'attachment; filename="case_std_details.log"'
            except Exception, e:
                LOGGER.error(str(traceback.format_exc()))
        except:
            LOGGER.error(traceback.format_exc())

        return filename, att

    except IOError:
        LOGGER.error(traceback)

    return None, None
