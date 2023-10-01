import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.header import Header
from django.core.handlers.wsgi import WSGIRequest
import datetime
from shop.models import *


def sendemail(email, head, content):
    # 1. 连接邮箱服务器
    con = smtplib.SMTP_SSL('smtp.qq.com', 465)
    # 2. 登录邮箱
    con.login('1975044006@qq.com', 'vhfpdbsrkrkbdgfd')
    # 2. 准备数据
    # 创建邮件对象
    msg = MIMEMultipart()
    # 设置邮件主题
    subject = Header(head, 'utf-8').encode()
    msg['Subject'] = subject
    # 设置邮件发送者
    msg['From'] = 'mysite <1975044006@qq.com>'
    # 设置邮件接受者
    msg['To'] = email
    # 添加⽂文字内容
    text = MIMEText(content, 'plain', 'utf-8')
    msg.attach(text)
    # 3.发送邮件
    con.sendmail('1975044006@qq.com', email, msg.as_string())
    con.quit()


def getip(request: WSGIRequest):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]  # 所以这里是真实的ip
    else:
        ip = request.META.get('REMOTE_ADDR')  # 这里获得代理ip
    return ip


def nowtime2str():
    a = datetime.datetime.now()
    astr = a.strftime("%Y-%m-%d %H:%M:%S")
    return astr


def getAuthority(request):
    a = Members.objects.filter(userName=request.COOKIES.get("username")).first()
    if a is not None:
        return a.authority
    else:
        return None


def listGet(l: list, index):
    if index < l.__len__():
        return l[index]
    else:
        return None


def addoplog(operation: str, userName: str, request: WSGIRequest):
    OperationLog.objects.create(
        operation=operation,
        userName_id=userName,
        ip=getip(request)
    )

qwer = 1