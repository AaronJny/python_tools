#acoding=utf-8
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
import requests
from bs4 import BeautifulSoup
import lxml
import time

def get_proxies_from_xici():
    """
    get proxies from 'http://www.xicidaili.com/'.
    return http_list,https_list
    从西刺爬取国内代理，并根据代理协议类型分类，返回两个集合，
    分别存放http类型代理和https类型代理
    """
    url='http://www.xicidaili.com/nn/'
    session=requests.Session()
    headers={
        'Host': 'www.xicidaili.com',
        'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:53.0) Gecko/20100101 Firefox/53.0',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'Accept-Encoding': 'gzip, deflate',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
        'Cache-Control': 'max-age=0'
        }
    session.headers.update(headers)
    http_list=set()
    https_list=set()
    for num in range(1,4):
        res=session.get(url+str(num))
        print res
#         print res.content
        bsobj=BeautifulSoup(res.content,'lxml')
        trs=bsobj.find('table',{'id':'ip_list'}).find_all('tr',{'class':'odd'})
        for tr in trs:
            tds=tr.find_all('td',{'class':''})
            ss=tds[0].get_text()+':'+tds[1].get_text()
            if tds[3].get_text()=='HTTP':
                http_list.add(ss)
            elif tds[3].get_text()=='HTTPS':
                https_list.add(ss)
        print len(trs)
        print len(http_list)
        print len(https_list)
    print 'HTTP代理：',len(http_list)
    for i in http_list:
        print i
    print 'HTTPS代理：',len(https_list)
    for i in https_list:
        print i
    session.close()
    return http_list,https_list
    
def get_proxies_from_kuaidaili():
    """
    get proxies from 'http://www.kuaidaili.com/'.
    return http_list,https_list
    """
    http_list=set()
    https_list=set()
    headers={
        'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:53.0) Gecko/20100101 Firefox/53.0',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'Accept-Encoding': 'gzip, deflate',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
        'Cache-Control': 'max-age=0'
        }
#     url='http://www.kuaidaili.com/free/inha/'
    url='http://www.kuaidaili.com/free/intr/'
    session=requests.Session()
    session.headers.update(headers)
    for i in range(1,4):
        res=session.get(url+str(i))
        print res
        res_content=res.content
        bsobj=BeautifulSoup(res_content,'lxml')
        table=bsobj.find('div',{'id':'list'}).find('table',{'class':'table table-bordered table-striped'})
        trs=table.find('tbody').find_all('tr')
        for tr in trs:
            ip=tr.find('td',{'data-title':'IP'}).get_text()
            port=tr.find('td',{'data-title':'PORT'}).get_text()
            http_list.add(ip+':'+port)
        print trs
        time.sleep(1)
    print len(http_list)
    for i in http_list:
        print i
    return http_list,https_list

def get_proxies_from_goubanjia():
    """
    get proxies from 'http://www.goubanjia.com/'.
    return http_list,https_list
    """
    http_list=set()
    https_list=set()
    url='http://www.goubanjia.com/free/gngn/index.shtml'
    session=requests.Session()
    headers={
        'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:53.0) Gecko/20100101 Firefox/53.0',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'Accept-Encoding': 'gzip, deflate',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1'
        }
    session.headers.update(headers)
    res=session.get(url)
    print res
    print res.content
    bsobj=BeautifulSoup(res.content,'lxml')
    table=bsobj.find('div',{'id':'list'}).find('table',{'class':'table'}).find('tbody')
    trs=table.find_all('tr')
    for tr in trs:
        ip=tr.find('td')
        none_p=ip.find_all('p',{'style':'display: none;'})
        for i in none_p:
            i.extract()
        none_p=ip.find_all('p',{'style':'display:none;'})
        for i in none_p:
            i.extract()
        ip.find('span',{'class':'port'}).extract()
#         print ip
        http_list.add(ip.get_text()+'808')
    return http_list,https_list
        
    
def get_proxies():
    http_list1,https_list1=get_proxies_from_kuaidaili()
    http_list2,https_list2=get_proxies_from_xici()
    return http_list1|http_list2,https_list1|https_list2

if __name__=='__main__':
    get_proxies_from_xici()