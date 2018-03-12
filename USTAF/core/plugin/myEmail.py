import smtplib

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage

from USTAF.core.logger import LOGGER
import traceback


def sendEmailReport(test_result, base_path, html_path, mail_list=None, excel=None, std_att=None):
    try:

        html_path = '{}/html/{}'.format(base_path, html_path)

        base_path += '/template'

        msg = MIMEMultipart()
        html = open(html_path).read()
        html_part = MIMEText(html, 'html')
        html_part.set_charset('utf-8')
        msg.attach(html_part)

        fp = open( '{}/imgs/header.png'.format(base_path),'rb')
        msgImage = MIMEImage(fp.read())
        fp.close()
        msgImage.add_header('Content-ID', '<header>')
        msg.attach(msgImage)

        fp = open('{}/imgs/footer.png'.format(base_path),'rb')
        msgImage = MIMEImage(fp.read())
        fp.close()
        msgImage.add_header('Content-ID', '<footer>')
        msg.attach(msgImage)

        fp = open('{}/imgs/device_icon.png'.format(base_path), 'rb')
        msgImage = MIMEImage(fp.read())
        fp.close()
        msgImage.add_header('Content-ID', '<dut>')
        msg.attach(msgImage)

        fp = open('{}/imgs/driver_icon.png'.format(base_path), 'rb')
        msgImage = MIMEImage(fp.read())
        fp.close()
        msgImage.add_header('Content-ID', '<driver>')
        msg.attach(msgImage)

        fp = open('{}/imgs/link_icon.png'.format(base_path), 'rb')
        msgImage = MIMEImage(fp.read())
        fp.close()
        msgImage.add_header('Content-ID', '<link>')
        msg.attach(msgImage)

        fp = open('{}/imgs/log_icon.png'.format(base_path), 'rb')
        msgImage = MIMEImage(fp.read())
        fp.close()
        msgImage.add_header('Content-ID', '<log>')
        msg.attach(msgImage)

        fp = open('{}/imgs/warning_icon.png'.format(base_path), 'rb')
        msgImage = MIMEImage(fp.read())
        fp.close()
        msgImage.add_header('Content-ID', '<warning>')
        msg.attach(msgImage)

        fp = open('{}/imgs/user_icon.png'.format(base_path), 'rb')
        msgImage = MIMEImage(fp.read())
        fp.close()
        msgImage.add_header('Content-ID', '<user>')
        msg.attach(msgImage)

        fp = open('{}/imgs/wiki_icon.png'.format(base_path), 'rb')
        msgImage = MIMEImage(fp.read())
        fp.close()
        msgImage.add_header('Content-ID', '<wiki>')
        msg.attach(msgImage)

        fp = open('{}/imgs/patch_icon.png'.format(base_path), 'rb')
        msgImage = MIMEImage(fp.read())
        fp.close()
        msgImage.add_header('Content-ID', '<patch>')
        msg.attach(msgImage)

        if excel:
            att1 = MIMEText(open(excel, 'rb').read(), 'base64', 'gb2312')
            att1["Content-Type"] = 'application/octet-stream'
            att1["Content-Disposition"] = 'attachment; filename="result.xls"'
            msg.attach(att1)

        if std_att:
            msg.attach(std_att)

        mailto = mail_list if mail_list else ["yubo.li@sample.com"]
        msg['to'] = ','.join(mailto)
        msg['from'] = 'USTAF@sample.com'
        msg['subject'] = '{}_{}_{}_{}'.format(test_result.build, test_result.platform, test_result.scenario_name, test_result.pass_rate)

        try:
            server = smtplib.SMTP('mail.sample.com')
            mail_results = server.sendmail(msg['from'], mailto, msg.as_string())
            server.quit()
            LOGGER.debug(str(mail_results))
        except Exception, e:
            LOGGER.error(str(traceback.format_exc()))
    except:
            LOGGER.error(traceback.format_exc())