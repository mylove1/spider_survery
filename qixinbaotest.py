# -*- coding:utf-8 -*-
"""
author: liuyd
theme:
update_date: 2017/01/01
"""
from bs4 import BeautifulSoup

company_lists=[]
with open('qixinbao.html','r') as f:
    bsoup=BeautifulSoup(f.read(),'lxml')
result_lists=bsoup.find_all("span",{"id":"totalCount","class":"search-result-counter"})
for span in result_lists:
    r=str(span.contents[0]).isdigit()
    if r:
        totalnum=int(span.contents[0])


div_lists=bsoup.find_all("div",{"class":"search-ent-row clearfix"})
for div_tag in div_lists:
    company_dict={}
    try:
        name=div_tag.find("a",class_="search-result-company-name").text
        company_dict["company_name"] = name
    except:
        pass
    try:
        url=div_tag.find("a",class_="search-result-company-name")["href"]
        company_dict["company_url"] ='http://www.qixin.com/'+url
    except:
        pass
    company_lists.append(company_dict)

for i in  range(len(company_lists)):
    name='深圳市腾讯计算机系统有限公司'
    tarname=company_lists.pop(-1)
    if tarname['company_name']=='深圳市腾讯计算机系统有限公司'.decode('utf-8'):
        print tarname['company_name']


