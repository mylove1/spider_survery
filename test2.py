# -*- coding:utf-8 -*-
"""
author: liuyd
theme:
update_date: 2017/01/01
"""

with open('E:/company_lists.txt','r') as f:
    company_lists=f.readlines()
    for i in range(len(company_lists)):
        print i,company_lists[i].decode('gbk')
