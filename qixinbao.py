# -*- coding:utf-8 -*-
"""
author: liuyd
theme:启信宝网站调研
http://www.qixin.com/
需要登录才能查询，尝试将获取的目标企业写入excel
update_date: 2017/01/01
"""
from public.slide_check_code_recognition import get_validate_data_based_online
from public import Request
from public import Session
from requests.utils import dict_from_cookiejar
import re
from bs4 import BeautifulSoup
import time
import csv
import codecs
import json
from io import BytesIO
import pdb
import os
import urllib

class Qinxinbao(object):
    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36',
            'Host': 'www.qixin.com',

        }
        self.cookies = None

#访问主页获得cookies
    def VisitmainPhage(self):
        url = 'http://www.qixin.com/'
        options = {'method': 'get', 'url': url, 'headers': self.headers, 'timeout': 30}
        response = Request.basic(options)
        if response:
            self.cookies = dict_from_cookiejar(response.cookies)
            return self.VisitLoginPage()

#访问登录页面
    def VisitLoginPage(self):
        url = 'http://www.qixin.com/login'
        self.headers['Host'] = 'www.qixin.com'
        options = {'method': 'get', 'url': url, 'headers': self.headers,'cookies':self.cookies}
        response = Request.basic(options)
        if response:
            return self.getChallengegt()
#获得gt,challenge
    def getChallengegt(self):
        chgt={}
        url = 'http://www.qixin.com/service/gtregister?t=1487227669076&_=1487227669039'
        self.headers['Referer'] = 'http://www.qixin.com/login'
        options = {'method': 'get', 'url': url, 'headers': self.headers,'cookies':self.cookies}
        response = Request.basic(options)
        if response:
            result = response.content
            result = json.loads(result)
            challenge = result['data']['challenge']
            chgt['challenge']=challenge
            gt=result['data']['gt']
            chgt['gt']=gt
            return self.get_fourParams(chgt)
#获得获得验证码需要的参数
    def get_fourParams(self,chgt):
        url='http://api.geetest.com/get.php'
        params={
            'gt':chgt['gt'],
            'challenge':chgt['challenge'],
            'product':'float',
            'offline':'flase',
            'type':'slide',
             'callback': 'geetest_' + str(int(time.time() * 1000))

        }
        self.headers['Host']='api.geetest.com'
        self.headers['Referer']='http://www.qixin.com/login'
        options={'method':'get','url':url,'headers':self.headers,'params':params,'cookies':self.cookies}
        response=Request.basic(options)
        if response:
            res = json.loads(response.content.split('(')[1][:-1])
            challenge=res.get('challenge') if res.has_key('challenge') else "unknown"
            # 不完整图
            bg_url = 'http://static.geetest.com/' + res.get('bg') if res.has_key('bg') else 'Unknown'
            # 完整图
            fullbg_url = 'http://static.geetest.com/' + res.get('fullbg') if res.has_key('fullbg') else 'Unknown'

            return challenge,chgt['gt'],bg_url,fullbg_url

    def get_image(self,image_url):
            """
            获取验证码的图片
            :param image_url
            :return:
            """
            self.headers['Host']=None
            options={
                'url':image_url,'method':'get','headers':self.headers
            }
            response=Request.basic(options)
            if response:
                print response.status_code
                img=BytesIO(response.content)
                return img

    def get_validate(self,geetest):
        url='http://api.geetest.com/ajax.php'
        self.headers['Host']='api.geetest.com'
        self.headers['Referer']='http://www.qixin.com/login'
        options={
            'url':url,'method':'get','headers':self.headers,'params':geetest,'cookies':self.cookies
        }
        response=Request.basic(options)
        if response:
            gee = json.loads(response.content.split('(')[1][:-1])
            print gee
            if gee.has_key('validate'):
                self.cookies=dict_from_cookiejar(response.cookies)
                print "get validate:",self.cookies
                validate = gee.get('validate')
                return validate
            else:
                return None
        else:
            print "获取validate 失败........."

    def gtLoginValidate(self,data):
        url = 'http://www.qixin.com/service/gtloginvalidate'
        form = {
            'geetest_challenge':data['geetest_challenge'],
            'geetest_validate': data['geetest_validate'],
            'geetest_seccode':data['geetest_seccode']
        }
        self.headers['Referer'] = 'http://www.qixin.com/login'
        self.headers['Origin'] = 'http://www.qixin.com'
        options = {'method': 'post', 'url': url, 'headers': self.headers,'cookies':self.cookies,'form':form}
        response = Request.basic(options)
        result = response.content
        result=json.loads(response.content)
        r=result.get("status")
        if r == "success":
            print "登录参数认证成功........."
            print form
            cookies=dict_from_cookiejar(response.cookies)
            return data['geetest_seccode'],cookies
        else:
            return None

def loginQinbao(cookies,code):
    print cookies
    url='http://www.qixin.com/service/login'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36',
        'Host': 'www.qixin.com',
        'Referer':'http://www.qixin.com/login'

    }
    u1='15112643691'
    u2='18188600650'
    p1='python8899'
    p2='liuwg1234'
    form={
        'userAcct':u2,
        'userPassword':p2,
        'token':'4164bbd58daa37bd421fdb913aa3c455|jordan'
    }
    form['token']=code
    options={
        'url':url,'method':'post','headers':headers,'form':form,'cookies':cookies
    }
    response=Request.basic(options)
    loginres=json.loads(response.content)
    message=loginres['data']["message"]
    if message==u'登陆成功':
        #登录成功后服务器没有cookies返回
        print message
        return True
    else:
        return False

def VisitEnerprise(cookies,cname):
        url = 'http://www.qixin.com/search'
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36',
            'Host': 'www.qixin.com',
            'Referer': 'http://www.qixin.com/login'
        }
        params = {
            'key':cname,
            'type': 'enterprise',
            'method': ''
        }
        headers['Referer'] = 'http://www.qixin.com/'
        options = {'method': 'get', 'url': url, 'headers':headers, 'cookies':cookies, 'params': params,
                   'timeout': 30}
        response = Request.basic(options)
        print response.status_code
        if response:
            return response.content
        else:
            print "请求首页没有说返回"

def VisitEnerpriseverify(cookies,cname):
    url = 'http://www.qixin.com/search'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36',
        'Host': 'www.qixin.com',
        'Referer': 'http://www.qixin.com/login'
    }
    params = {
        'key': cname.encode('utf-8'),
        'type': 'enterprise',
        'source': '',
        'isGlobal':'Y'
    }
    url2='http://www.qixin.com/search/?'
    headers['Referer'] =url2+urllib.urlencode(params)
    print headers['Referer']
    options = {'method': 'get', 'url': url, 'headers': headers, 'cookies': cookies, 'params': params,
               'timeout': 30}
    response = Request.basic(options)
    print response.status_code
    if response:
        with open('testqixinbaoverify.html', 'w') as f:
            f.write(response.content)
        return response.content
    else:
        print "请求首页没有说返回"


def VisitEnerprisenextpage(cookies,cname,pagenum):
    url = 'http://www.qixin.com/search'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36',
        'Host': 'www.qixin.com',
        'Referer': 'http://www.qixin.com/login'
    }
    #http://www.qixin.com/search?key=%E8%85%BE%E8%AE%AF&type=enterprise&source=&isGlobal=Y&page=2
    #headers["Referer"]='http://www.qixin.com/search?key=%E8%85%BE%E8%AE%AF&type=enterprise&source=&isGlobal=Y'
    params = {
        'key': cname,
        'type': 'enterprise',
        'source':'',
        'isGlobal':'Y',
        'page':pagenum
    }
    #headers['Referer'] = 'http://www.qixin.com/'
    options = {'method': 'get', 'url': url, 'headers': headers, 'cookies': cookies, 'params': params,
               'timeout': 30}
    response = Request.basic(options)
    if response:
        print "请求下一页成功......."
        return response.content

def LoginMain():
    j=False
    t=10
    while t>0:
        q=Qinxinbao()
        challenge,gt,bg_url,fullbg_url=q.VisitmainPhage()
        bg_img=q.get_image(bg_url)
        fullgb_img=q.get_image(fullbg_url)

        geeTest = get_validate_data_based_online(challenge=challenge,
                                                 gt=gt,
                                                 raw_source_img=fullgb_img,
                                                 raw_chunk_img=bg_img)
        validate = q.get_validate(geeTest)
        if validate == None:
            print "验证码参数validate获取失败......"
            time.sleep(5)
            t -= 1
        else:
            validate_params = {
                'geetest_challenge': challenge,
                'geetest_validate': validate,
                'geetest_seccode': validate + '|jordan'
            }
            verify=q.gtLoginValidate(validate_params)
            if verify==None:
                print "登录参数认证失败重新获取参数再次认证..."
                t-=1
            else:
                global login_cookies
                code,login_cookies=verify
                logresult=loginQinbao(login_cookies,code)
                #如果登录成功调用搜索企业的函数
                if logresult == True:
                    print "启信宝登录成功........."
                    j = True
                    break
                else:
                    print "登录失败再次登录"
                    t-=1
                    return LoginMain()
    if t==0:
        print "尝试了10次登录失败不再登录请过段时间在尝试......."
    #登录成功后取得成功后的cookies信息搜索企业
    if j==True:
        return login_cookies

#定义一个列表用来获取查询出来的企业
company_lists = []
def serarchcompany(cookies,cname):
    print "开始对目标企业进行查询......."
    totalnum=1
  # 调用函数查询企业
    html=VisitEnerprise(cookies, cname)
    bsoup=BeautifulSoup(html,'lxml')
    #首先根据搜索企业的数量判断分页的情况
    result_lists = bsoup.find_all("span", {"id": "totalCount", "class": "search-result-counter"})
    if result_lists:
        for span in result_lists:
            print span
            r = str(span.contents[0]).isdigit()
            if r:
                totalnum = int(span.contents[0])
                print totalnum
                if totalnum==0:
                    print cname,"totalnum为0",'没有该企业的信息'
                    os._exit(0)
    else:
        print "不好，查询过程需要验证调用验证的请求的代码继续获取数据"
        html = VisitEnerpriseverify(cookies, cname)
        bsoup = BeautifulSoup(html, 'lxml')
    for span in result_lists:
        print span
        r = str(span.contents[0]).isdigit()
        if r:
            totalnum = int(span.contents[0])
            print totalnum
            if totalnum == 0:
                print cname, "totalnum为0", '没有该企业的信息'
                os._exit(0)

    #对分页多少进行判断
    pagenums=totalnum/10
    print totalnum
    print "pagenums:",pagenums
    if pagenums==0:
        parseHTML(bsoup)
        result=targetcomany(cname)
    if pagenums>0:
        #如果分页的页数大于1除了需要解析首页外还需要请求下一页解析源码
        parseHTML(bsoup)
        result = targetcomany(cname)
        if result:
            return
        else:
            for num in range(2,pagenums+2):
                text=VisitEnerprisenextpage(cookies,cname,num)
                next_bsoup=BeautifulSoup(text,'lxml')
                parseHTML(next_bsoup)
                result=targetcomany(cname)
                if result:
                    return
    #return cname
def targetcomany(cname):
    print company_lists
    is_exist=False
    for i in range(len(company_lists)):
        company_dict=company_lists.pop(-1)
        #cname是一个unicode
        if company_dict["company_name"]==cname:
            print "目标企业获取成功....."
            #中文unicode进行写入必须进行编码操作，不然会报错
            writerfile(company_dict['company_name'].encode('utf-8'),company_dict['company_url'])
            print "写入文件完成"
            is_exist = True
            return is_exist

    if is_exist == False:
        msg = "没有查到该企业的信息"
        print msg
        #cname也是一个Unicode的字符串需要进行编码操作,msg是一个字符串
        writerfile(cname.encode('utf-8'), msg)
    print "company_lists:", company_lists

def parseHTML(bsoup):
    div_lists = bsoup.find_all("div", {"class": "search-ent-row clearfix"})
    for div_tag in div_lists:
        company_dict = {}
        try:
            name = div_tag.find("a", class_="search-result-company-name").text
            company_dict["company_name"] = name
        except:
            pass
        try:
            url = div_tag.find("a", class_="search-result-company-name")["href"]
            company_dict["company_url"] = 'http://www.qixin.com'+url
        except:
            pass
        company_lists.append(company_dict)

#写入文件的方法
def writerfile(cname,curl):
    fieldnames = ['companyname', 'url']
    csvfile = file('company_qixinbao.csv', 'ab')
    csvfile.write(codecs.BOM_UTF8)
    writer = csv.writer(csvfile)
    #writer.writerow(fieldnames)
    writer.writerow((cname,curl))


if __name__ == "__main__":
    #login_cookies = LoginMain()
    total_lists = []
    with open('E:/company_lists.txt', 'r') as f:
        totalname_lists = f.readlines()
    # 由于列表里的数据都是gbk编码的需要转成unicode的形式
    for name in totalname_lists:
        cname = name.decode('gbk').strip()
        total_lists.append(cname)
    for company in total_lists:
        print type(company)














