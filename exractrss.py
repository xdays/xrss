#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
import urllib
import requests
from bs4 import BeautifulSoup

LIST_FILE = './bloglist.txt'
OUTPUT_FILE='./blogrss.txt'


bloglist = open(LIST_FILE, 'r')
rsslist = open(OUTPUT_FILE, 'w')
rss_list = []

for l in bloglist:
    try:
        l = l.strip('\n')
        response = requests.get(l)
        #print type(response)
        url,source = response.url,response.text
        soup = BeautifulSoup(source)
        #获取所有属性为rss的link标签
        for link in soup.find_all('link', type="application/rss+xml"):
            #处理相对链接
            if not re.search('^http.*', link['href']):
                rss_list.append(url+link['href'])
            #过滤掉comment的rss源
            elif re.search(r'.*comment.*',link['href']):
                continue
            #正常的源
            else:
                rss_list.append(link['href'])
    except:
        continue

print rss_list 
rsslist.write('\n'.join(rss_list).encode('utf8'))

bloglist.close()
rsslist.close()
