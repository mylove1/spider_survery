# -*- coding:utf-8 -*-
"""
author: liuyd
theme:
update_date: 2017/01/01
"""
from bs4 import BeautifulSoup

company_lists=[]
with open('water.html','r') as f:
    bsoup=BeautifulSoup(f.read(),'lxml')

totalnum = bsoup.find('span', class_='sd_left_ss_number').text


def parseHtml(bsoup):
    company_dict = {}
    div_lists = bsoup.find_all('div', class_='or_search_list')
    base_url = 'http://www.shuidixy.com'
    for div in div_lists:
        a_text = div.find('a').text
        text = a_text.strip()
        company_dict['cname'] = text
        # 企业url
        company_dict['curl'] = base_url + div.find('a')['href']
        company_lists.append(company_dict)
        company_dict = {}
    print "成功获取数据"
parseHtml(bsoup)
with open('watertest.txt','w') as f:
    f.write('定')