# -*- coding:utf-8 -*-
"""
author: liuyd
theme:
update_date: 2017/01/01
"""
from public import Request
from requests.utils import dict_from_cookiejar
import re
from bs4 import BeautifulSoup
import time
import csv
import codecs

company_lists = []
class Water(object):
    def __init__(self,name_list):
        self.headers={
            'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36',
            'Host':'www.shuidixy.com',

        }
        self.cookies=None
        self.name_list=name_list

    def VisitmainPhage(self):
        url='http://www.shuidixy.com/'
        options={'method':'get','url':url,'headers':self.headers}
        response=Request.basic(options)
        if response:
            self.cookies=dict_from_cookiejar(response.cookies)
            for i in range(len(self.name_list)):
                #cname是一个unicode
                cname=self.name_list[i]
                print cname
                result=self.get_firsthtml(cname)
                if result==0:
                    time.sleep(10)
                    continue
                else:
                    time.sleep(10)
                    continue

    def get_firsthtml(self,cname):
        #定义一个判断是否在查到的列表企业中有需要的企业名字的变量
        is_exist=False
        page_dict={}
        page_list=[]
        self.headers['Referer']='http://www.shuidixy.com/'
        url='http://www.shuidixy.com/search'
        params={
            'key':cname,
            'searchType':'all'

        }
        options={
            'method':'get','url':url,'headers':self.headers,'cookies':self.cookies,'params':params,'timeout':30
        }
        response=Request.basic(options)
        if response:
            bsoup=BeautifulSoup(response.content,'lxml')
            #把第一页企业名称与连接解析出来
            self.parseHtml(bsoup)
            #获取企业名称的总页数
            totalnum = bsoup.find('span', class_='sd_left_ss_number').text
            print totalnum
            if totalnum==u'0':
                msg="没有查到该企业的信息"
                print msg
                self.writerfile(cname.encode('utf-8'),msg,totalnum)
                return 0
            page_dict['totalnum']=totalnum
            #获取分页的具体数字
            pagenums = bsoup.find('div', class_='sd_left-padge pageCls').find_all('span')
            for page in pagenums:
                numstr = page.contents[0].strip()
                try:
                    num = int(numstr)
                    page_list.append(num)
                except:
                    pass
            print page_list
            for num in range(1,len(page_list)):
                self.get_nexthtml(totalnum,num,cname)

        #对获得的企业信息列表进行循环取出需要的元素
        for i in range(len(company_lists)):
            sname_dict=company_lists.pop(-1)
            if sname_dict['cname']==cname:
                self.writerfile(sname_dict['cname'],sname_dict['curl'],page_dict['totalnum'])
                print "写入文件完成"
                is_exist=True

        #循环结束进行判断是否有企业的信息
        if is_exist==False:
            msg = "没有查到该企业的信息"
            print msg
            #cname是一个unicode写入操作必须进行编码(因为它是一个中文unicode)
            self.writerfile(cname.encode('utf-8'),msg,u'0')
        print "company_lists:",company_lists

    def get_nexthtml(self,totalnum,num,cname):
        print num
        self.headers['Referer'] = 'http://www.shuidixy.com/search?'
        url = 'http://www.shuidixy.com/search'
        params={
            'key':cname,
            'searchType':'all',
            'provinceCode':'',
            'capitalNumber':'',
            'establishDuration':'',
            'secondLevelIndustryType':'',
            'sort':'',
            'entry':0,
            'mark':'',
            'total':totalnum,
            'npage':num
        }
        options = {
            'method': 'get', 'url': url, 'headers': self.headers, 'cookies': self.cookies, 'params': params,'timeout':30
        }
        response=Request.basic(options)
        if response:
            bsoup=BeautifulSoup(response.content,'lxml')
            self.parseHtml(bsoup)

    def parseHtml(self,bsoup):
        company_dict = {}
        div_lists = bsoup.find_all('div', class_='or_search_list')
        base_url = 'http://www.shuidixy.com'
        for div in div_lists:
            a_text = div.find('a').text
            #a_text就是一个unicode统一不要对它进行编码
            text=a_text.strip()
            company_dict['cname'] = text
            #企业url
            company_dict['curl'] = base_url + div.find('a')['href']
            company_lists.append(company_dict)
            company_dict = {}
        print "成功获取数据"

#写入文件的方法
    def writerfile(self,cname,curl,nums):
        fieldnames = ['companyname', 'url','nums']
        csvfile = file('company_water.csv', 'ab')
        csvfile.write(codecs.BOM_UTF8)
        writer = csv.writer(csvfile)
        #writer.writerow(fieldnames)
        writer.writerow((cname,curl,nums))



if __name__=="__main__":
    total_lists=[]
    with open('E:/company_lists.txt', 'r') as f:
        totalname_lists = f.readlines()
    #由于列表里的数据都是gbk编码的需要转成unicode的形式
    for name in totalname_lists:
        #name是一个unicode的字符串需要解码用什么编码就要用什么解码
        cname=name.decode('gbk').strip()
        print type(cname)
        total_lists.append(cname)
        break
    w=Water(total_lists)
    w.VisitmainPhage()