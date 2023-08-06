# -*- coding: utf-8 -*-
import smtplib
from email.mime.text import MIMEText
from email.utils import formataddr

def sendmail(mail,mailpass,tomail,name,title,index):
    mail_host = "smtp.qq.com"
    mail_user = mail
    mail_pass = mailpass
    sender = mail  # 发送方qq邮箱
    receivers = tomail
    sendName = name
    message = MIMEText(index)
    message['From'] = formataddr([name, mail])
    message['Subject'] = title
    message['To'] = tomail
    smtpobj = smtplib.SMTP_SSL(mail_host, 465)
    smtpobj.set_debuglevel(1)
    smtpobj.login(mail_user, mail_pass)  # 登陆QQ邮箱服务器
    smtpobj.sendmail(sender, receivers, message.as_string())
    smtpobj.quit()
