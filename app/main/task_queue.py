import os

from flask import current_app

from .. import celery


@celery.task
def remove_icon(uri):
    """
    根据相对的URI删除文件
    :param uri: 相对的URI
    """
    os.remove(uri)


def send_mail_to(text, to):
    admin = current_app.config['FLASK_ADMIN']
    code = current_app.config['MAIL_CODE']
    send_mail(text, to, admin, code)


@celery.task
def send_mail(text, to, admin, code):
    import smtplib
    from email.mime.text import MIMEText
    from email.header import Header

    msg = MIMEText('Hello world')
    msg['Subject'] = text
    msg['From'] = admin
    msg['To'] = to

    smtp = smtplib.SMTP_SSL('smtp.qq.com', 465, timeout=120)
    smtp.login(msg['From'], code)
    smtp.sendmail(msg['From'], msg['To'], msg.as_string())
