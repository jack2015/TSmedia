# -*- coding: utf8 -*-
Agent = {'User-agent': 'Mozilla/5.0 (Windows NT 10.0; …) Gecko/20100101 Firefox/65.0'}
import requests
import urllib2
import re
import requests,re
from jsunpack import unpack
def get_packed_data(html):
    packed_data = ''
    for match in re.finditer('(eval\s*\(function.*?)</script>', html, re.DOTALL | re.I):
        try:
            js_data = unpack(match.group(1))
            js_data = js_data.replace('\\', '')
            packed_data += js_data
        except:
            pass
    return packed_data
def get_video_url(url):
    url = url.replace('embed-','')
    listServers= []
    request = urllib2.Request(url, None, Agent)
    data2 = urllib2.urlopen(request).read()
    if '(p,a,c,k,e,d)' in data2:
        data2 = get_packed_data(data2)
    r = re.findall('sources:\["(.+?)"',data2)
    if r:
        for href in r:
            if '.mpd' in href:continue
            w = ('Cool_vidshare',href)
            listServers.append(w)
    else:
        w = ('Oops_vidshare','Error')
        listServers.append(w)
    return listServers
