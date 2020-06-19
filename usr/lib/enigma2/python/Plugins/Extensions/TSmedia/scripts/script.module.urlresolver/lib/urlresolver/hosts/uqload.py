# -*- coding: utf-8 -*-
import urllib2
import requests
import json
import re
def get_video_url(url, premium=False, user="", password="", video_password=""):	
    video_urls = []
    headers = {'host':'uqload.com',
     'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; rv:56.0) Gecko/20100101 Firefox/56.0',
     'Accept': '*/*',
     'Accept-Language': 'fr,fr-FR;q=0.8,en-US;q=0.5,en;q=0.3',
     'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
     'X-Requested-With': 'XMLHttpRequest',
     'Referer': url,
     'Connection': 'keep-alive'}
    s = requests.Session()
    r = s.get(url, headers=headers)
    htmldata = r.content
    data = re.findall('''sources: \[(.+?)\]''',htmldata)
    if len(data) != 0:
        data = Cleartxt(data[0])
        video_urls.append(["%s [uqload]" % 'cool', data])
    return video_urls
def Cleartxt(txt):
    txt = txt.replace("'",'').replace("]",'').replace("[",'').replace('"','')
    return txt
#AA = 'https://uqload.com/embed-zjhjqriw9gru.html'
#CC = get_video_url(AA)
#print CC
