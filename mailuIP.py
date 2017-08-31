# -*- coding: utf-8 -*-

import os
import json

from email.mime.text import MIMEText
from email import encoders
from email.header import Header
from email.mime.text import MIMEText
from email.utils import parseaddr, formataddr
import smtplib

def _format_addr(s):
    name, addr = parseaddr(s)
    return formataddr(( \
        Header(name, 'utf-8').encode(), \
        addr.encode('utf-8') if isinstance(addr, unicode) else addr))

def getConf():
    with open('conf.json', 'r') as f:
        conf = json.load(f)
    return conf

def sendMail(ip):
    conf = getConf()
    # print 'now ip:', ip
    # print 'conf:', conf
    from_addr = conf['sender']
    password = conf['passwd']
    to_addr = conf['receivers']
    smtp_server = conf['SMTPServer']

    msg = MIMEText('hello, send by Python...', 'plain', 'utf-8')
    msg['From'] = _format_addr(u'创新大厦A区305外网IP变化 <%s>' % from_addr)
    msg['To'] = _format_addr(u'IP管理员 <%s>' % to_addr)
    text = u'新 IP ：' + ip
    msg['Subject'] = Header(text, 'utf-8').encode()

    server = smtplib.SMTP(smtp_server, 25)
    server.set_debuglevel(1)
    server.connect(smtp_server, 587)
    server.ehlo()
    server.login(from_addr, password)
    server.sendmail(from_addr, [to_addr], msg.as_string())
    server.quit()

def getIP():
    tmp = os.popen('curl ifconfig.me').readlines()
    ip = tmp[0].strip('\n')
    return ip

def compareIP(ip):
    with open('ip.txt', 'r') as f:
        old_ip = f.read().strip('\n')
        # print 'old_ip:', old_ip
    if old_ip != ip:
        with open('ip.txt', 'w') as f:
            f.write(ip)
        return True
    else:
        return False

if __name__ == '__main__':
    ip = getIP()
    # print ip
    if compareIP(ip):
        sendMail(ip)