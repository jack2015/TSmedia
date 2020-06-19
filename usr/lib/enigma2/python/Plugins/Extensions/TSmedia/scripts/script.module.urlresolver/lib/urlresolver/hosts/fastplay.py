# -*- coding: cp1256 -*-
from iTools import CBaseAddonClass
import sys,warnings
import urllib,urllib2,re,os,json,requests,hashlib,time
from requests.packages.urllib3.exceptions import InsecureRequestWarning
warnings.simplefilter('ignore',InsecureRequestWarning)
##########################################
Agent = {'User-agent': 'Mozilla/5.0 (Windows NT 10.0; �) Gecko/20100101 Firefox/65.0'}
import requests
import urllib2
import re
class fastplay(CBaseAddonClass):
    def __init__(self):
        CBaseAddonClass.__init__(self,{'cookie':'fastplay.cookie'})
        self.USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36'
        self.MAIN_URL = 'http://fastplay.online'
        self.HEADER = {}
        self.AJAX_HEADER = dict(self.HEADER)
        self.AJAX_HEADER.update( {'X-Requested-With': 'XMLHttpRequest', 'Accept-Encoding':'gzip, deflate', 'Content-Type':'application/x-www-form-urlencoded; charset=UTF-8', 'Accept':'application/json, text/javascript, */*; q=0.01'} )
        self.cacheLinks  = {}
        self.defaultParams ={}
    def get_video_url(self,url):
        import requests,re,urllib2
        Sgn = requests.Session()
        url = url.replace('embed-','')
        r = Sgn.get(url,verify=False).content
        regx = '''\{file:"(.+?)",label:"(.+?)"'''
        donnee = re.findall(regx,r)
        list1=[]
        if donnee:
            for link,qlt in donnee:
                list1.append((qlt,link))
        else:
            print 'nada'
        print "list1",list1    
        return list1
def get_video_url(url):
  return fastplay().get_video_url(url)