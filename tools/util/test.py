#coding=utf-8
import requests
import time
import get_proxy
from bs4 import BeautifulSoup



def test_proxies(session,http_proxy):
    proxy={'http':http_proxy}
    session.proxies.update(proxy)
    cnt=0
    while True:
        if cnt>0:
            return False,''
        cnt+=1
        try:
            t1=time.time()
            res=session.get('http://1212.ip138.com/ic.asp',timeout=1)
            t2=time.time()
#             print res.status_code
            res_content=res.content.decode('gbk')
#             print res_content
            if res.status_code!=200 or '60.168.149.13' in res_content:
                raise Exception
            print t2-t1
            bsobj=BeautifulSoup(res_content,'lxml')
            ans=bsobj.find('center').get_text()
            return True,ans
        except Exception,e:
            print '\t[尝试失败]',http_proxy,cnt
    
    
def fun():
    http_list,https_list=get_proxy.get_proxies_from_xici()
    allow_list=[]
    session=requests.Session()
    headers={
        'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:53.0) Gecko/20100101 Firefox/53.0'
        }
    session.headers.update(headers)
    cnt=0
    for i in http_list:
#         time.sleep(1)
        cnt+=1
        try:
            flag,res=test_proxies(session,i)
            if not flag:
                raise Exception
            allow_list.append(res)
            print '[成功] 第',cnt,'个代理测试：',i
        except Exception,e:
            print '[失败] 第',cnt,'个代理测试：',i
    print '测试完毕'
    print '共成功',len(allow_list),'项，分别是：'
    for i in allow_list:
        print '\n'
        print i
    
if __name__=='__main__':
    fun()
