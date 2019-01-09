import smtplib
from email.header import Header
from email.mime.text import MIMEText

from config import Config
from utils.log import Log

EMAIL_MESSAGES = {
    1: {"subject": "测试", "content": "this is a test email"}
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

            msg = MIMEText(s, 'plain', 'utf-8')  # 中文需参数‘utf-8’，单字节字符不需要
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
