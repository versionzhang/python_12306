import smtplib
from email.header import Header
from email.mime.text import MIMEText

from config import Config
from utils.log import Log

EMAIL_MESSAGES = {
    1:
        {
            "subject": "测试", "content": "this is a test email"
        },
    2:
        {
            "subject": "抢票成功通知 - python12306小助手",
            "content":
                """
你的火车票已经订票成功，订单号为{order_no}, 请登录你的12306账号进行查看并付款.
    
---by python12306 小助手
---github仓库链接 https://github.com/versionzhang/python_12306
"""
        }
}


def send_email(msg_type, **extra_var):
    """
    邮件通知
    :param msg_type: email content type id. in EMAIL_MESSAGE dict.
    :param extra_var: format content var dict.
    :return:
    """
    email_conf = Config.email_config
    if not Config.email_notice_enable:
        Log.v("未开启邮箱通知")
    else:
        data = EMAIL_MESSAGES[msg_type]
        try:
            sender = email_conf.from_email
            receiver = email_conf.notice_email_list
            subject = data["subject"]
            username = email_conf.username
            password = email_conf.password
            host = email_conf.email_gateway
            port = email_conf.port
            s = data["content"].format(**extra_var)

            msg = MIMEText(s, 'plain', 'utf-8')
            msg['Subject'] = Header(subject, 'utf-8')
            msg['From'] = sender
            msg['To'] = ','.join(receiver)
            print(host, port)
            smtp = smtplib.SMTP(host)
            smtp.connect(host, port=port)
            smtp.login(username, password)
            smtp.send_message(msg)
            smtp.quit()
            Log.v("邮件发送成功")
        except Exception as e:
            Log.e("发送失败, 邮件配置有误, 请检查配置")
