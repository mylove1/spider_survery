# -*- coding:utf-8 -*-
"""
author: liuyd
theme:
update_date: 2017/01/01
"""
total_lists=[]
def info():

    with open('E:/company_lists.txt', 'r') as f:
        totalname_lists = f.readlines()
    #由于列表里的数据都是gbk编码的需要转成unicode的形式
    for name in totalname_lists:
        #name是一个unicode的字符串需要解码用什么编码就要用什么解码
        cname=name.decode('gbk').strip()
        print type(cname)
        total_lists.append(cname)
        break
info()

for i in range(len(total_lists)):
    cname=total_lists[i]
    print type(cname)