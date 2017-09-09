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
    # crontab needs absolute path
    abspath = '/path/to/your/conf.json'
    with open(abspath, 'r') as f:
        conf = json.load(f)
    return conf

def sendMail(ip_list):
    conf = getConf()
    # print 'now ip:', ip
    # print 'conf:', conf
    from_addr = conf['sender']
    password = conf['passwd']
    to_addr = conf['receivers']
    smtp_server = conf['SMTPServer']
    
    IPmsg = ''
    for ind, ip in enumerate(ip_list):
        IPmsg += 'IP ' + str(ind) + ' : ' + ip# + '\n'
    msg = MIMEText('hello, 创新大厦A区305外网IP已变化。\n' + IPmsg +
            'Sent by 创新大厦的 Python...', 'plain', 'utf-8')
    # print IPmsg
    msg['From'] = _format_addr(u'IP管理员 <%s>' % from_addr)
    msg['To'] = _format_addr(u'创新大厦用户 <%s>' % to_addr)

    title = u'创新大厦 IP'
    msg['Subject'] = Header(title, 'utf-8').encode()

    '''
    port即SMTP服务器端口，一般情况下，25为明文通信，587为加密通信。
    部分SMTP服务器，如Outlook邮箱，不支持明文通信,且使用starttls加密方式。

    user和password即登陆SMTP服务器的用户名和密码，
    一般情况下，其与你登录该邮箱时的用户名和密码相同，
    但有些服务器有不同，如QQ邮箱使用QQ号和邮箱授权码登录，163同理。
    '''
    server = smtplib.SMTP(smtp_server, 587)
    server.set_debuglevel(False)
    server.starttls()
    # server.connect(smtp_server, 587)
    server.ehlo()
    server.login(from_addr, password)
    server.sendmail(from_addr, to_addr.split(','), msg.as_string())
    server.quit()

def getIP():
    tmp1 = os.popen('wget http://ipecho.net/plain -O - -q ; echo').readlines()
    # print tmp1
    if tmp1 == []:
        tmp2 = os.popen('curl http://members.3322.org/dyndns/getip').readlines()
        ip = tmp2[0]#.strip('\n')
    else:
        ip = tmp1[0]#.strip('\n')
    return ip

def compareIP(ip):
    # crontab needs absolute path
    abspath = '/path/to/your/ip.txt'
    with open(abspath, 'r') as f:
        old_ip = f.readlines()
        #print 'old_ip:', old_ip

    if ip not in old_ip:
        # only has one ip
        if len(old_ip) == 1:
            old_ip.append(ip)
            # print old_ip
            with open(abspath, 'w') as f:
                f.writelines(old_ip)
            return old_ip
        else:
            with open(abspath, 'w') as f:
                f.write(ip)
            return [ip]
    else:
        return False

if __name__ == '__main__':
    now_ip = getIP()
    ip_list = compareIP(now_ip)
    if ip_list:
        sendMail(ip_list)
