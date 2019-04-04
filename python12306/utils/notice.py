import smtplib
from email.header import Header
from email.mime.text import MIMEText

import requests

from python12306.config import Config
from python12306.utils.log import Log

MESSAGES = {
    1:
        {
            "subject": "测试", "content": "<h1>this is a test email</h1>"
        },
    2:
        {
            "subject": "抢票成功通知-python12306小助手",
            "content":
                """
<h1>你的火车票已经订票成功，订单号为{order_no}, 请登录你的12306账号进行查看并付款.</h1>
    <div>{ticket_info}</div>
<p>--- by python12306 小助手</p>
<p>Powered By <a href="https://github.com/versionzhang/python_12306">Python12306</a></p>
"""
        },
    3:
        {
            "subject": "您有未完成的订单,请处理后再运行本程序-python12306小助手",
            "content":
                """
<h1>您有未完成的订单,请处理后再运行本程序.</h1>
<p>--- by python12306 小助手</p>
<p>Powered By <a href="https://github.com/versionzhang/python_12306">Python12306</a></p>
"""
        }
}


class NoticeCollections(object):
    methods = ('weixin', 'email')

    def notice(self, msg_type, **kwargs):
        for v in self.methods:
            getattr(self, "send_{0}".format(v))(msg_type, **kwargs)

    def send_weixin(self, msg_type, **extra_var):
        if not Config.weixin_notice_enable:
            Log.v("未开启微信通知")
            return
        Log.v("{notice}".format(
            notice="你已开启微信通知，稍后会收到推送"))
        url = "https://sc.ftqq.com/{key}.send".format(key=Config.weixin_sckey)
        data = MESSAGES[msg_type]
        subject = data["subject"]
        s = data["content"].format(**extra_var)
        r = requests.post(url, data={"text": subject, "desp": s})
        if r.status_code == requests.codes.ok:
            Log.v("微信通知发送成功")
        else:
            Log.e("微信通知发送失败")

    def send_email(self, msg_type, **extra_var):
        """
        邮件通知
        :param self:
        :param msg_type: email content type id. in EMAIL_MESSAGE dict.
        :param extra_var: format content var dict.
        :return:
        """
        email_conf = Config.email_config
        if not Config.email_notice_enable:
            Log.v("未开启邮箱通知")
        else:
            Log.v("{notice}".format(
                notice="你已开启邮件通知，稍后会收到邮件"))
            data = MESSAGES[msg_type]
            Log.v("正在发送邮件...")
            try:
                sender = email_conf.from_email
                receiver = email_conf.notice_email_list
                subject = data["subject"]
                username = email_conf.username
                password = email_conf.password
                host = email_conf.email_gateway
                port = email_conf.email_port
                s = data["content"].format(**extra_var)

                msg = MIMEText(s, 'html', 'utf-8')
                msg['Subject'] = Header(subject, 'utf-8')
                msg['From'] = sender
                msg['To'] = ','.join(receiver)
                smtp = smtplib.SMTP(host)
                smtp.connect(host, port=port)
                smtp.login(username, password)
                smtp.send_message(msg)
                smtp.quit()
                Log.v("邮件发送成功")
            except Exception as e:
                Log.e("发送失败, 邮件配置有误, 请检查配置")


NoticeTool = NoticeCollections()
