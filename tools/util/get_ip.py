#coding=utf-8
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
import requests
from bs4 import BeautifulSoup
import lxml
from email import encoders
from email.header import Header
from email.header import decode_header
from email.mime.text import MIMEText
from email.utils import parseaddr,formataddr
from email.parser import Parser
import smtplib
import poplib
import platform
import time

def isWindows():
    if 'Linux' in platform.system():
        return False
    else:
        return True

def sprint(mes):
    if isWindows():
        mes=mes.encode('gbk')
    print mes

def get_ip():
    session=requests.Session()
    headers={
        'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:53.0) Gecko/20100101 Firefox/53.0'
        }
    session.headers.update(headers)
    res=session.get('http://1212.ip138.com/ic.asp')
#     print res
    res_content=res.content.decode('gbk')
#     print res_content
    bsobj=BeautifulSoup(res_content,'lxml')
    center=bsobj.find('center')
    res=center.get_text()
    print res
    return res

def read_ip():
    ip=''
    try:
        with open('ip.txt','r') as f:
            ip=f.read()
    except Exception,e:
        sprint(u'文件不存在，ip默认为空')
    return ip

def write_ip(ip):
    with open('ip.txt','w+') as f:
        f.write(ip)

def send_email(to_addr,subject,context):
    from_addr='1106405083@qq.com'#你的邮箱地址
    password='******'#你的邮箱第三方授权码
    mail_host='smtp.qq.com'
    msg=MIMEText(context,'plain','utf-8')
    msg['From']=Header(u'IP_change<%s>' % from_addr,'utf-8')
    msg['To']=Header(u'Aaron<%s>' % to_addr,'utf-8')
    msg['Subject']=Header(subject,'utf-8')
    smtp=smtplib.SMTP_SSL()
    sprint(u'[*]开始连接邮件SMTP服务器')
    smtp.connect(mail_host,465)
    sprint(u'[*]连接邮件SMTP服务器成功')
    smtp.login(from_addr,password)
    smtp.sendmail(from_addr,to_addr,msg.as_string())
    sprint(u'[*]邮件发送成功')
    smtp.quit()


def check_ip():
    ip_new=get_ip()
    ip_now=read_ip()
    if ip_new!=ip_now:
        sprint(u'IP地址变更，准备发送邮件')
        #你的邮箱地址，邮件主题，邮件内容
        send_email(u'1106405083@qq.com',u'ip地址变更',ip_new)
        write_ip(ip_new)
    else:
        sprint(u'IP地址无变更')
    
def main():
    while True:
        sprint(u'[*]当前时间：%s' % time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time())))
        try:
            check_ip()
            sprint(u'暂停60秒')
            time.sleep(60)
        except Exception,e:
            sprint(u'出现异常，稍后重试')
            sprint(u'暂停10秒')
            time.sleep(10)
        
if __name__=='__main__':
    main()