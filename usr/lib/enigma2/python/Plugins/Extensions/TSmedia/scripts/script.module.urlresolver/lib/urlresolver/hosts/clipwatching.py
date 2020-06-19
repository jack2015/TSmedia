# -*- coding: cp1256 -*-

from iTools import CBaseAddonClass,printD,printE
from urlresolver.hTools import scrape_sources
import sys,warnings
import urllib,urllib2,re,os,json,requests,hashlib,time
from requests.packages.urllib3.exceptions import InsecureRequestWarning
warnings.simplefilter('ignore',InsecureRequestWarning)
##########################################



Agent = {'User-agent': 'Mozilla/5.0 (Windows NT 10.0; �) Gecko/20100101 Firefox/65.0'}
import requests
import urllib2
import re

class clipwatching(CBaseAddonClass):
        def __init__(self):
                CBaseAddonClass.__init__(self,{'cookie':'moshahda.cookie'})

                self.USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36'
                self.MAIN_URL = 'http://clipwatching.online'
                self.HEADER = {}#{'User_agent':self.USER_AGENT,'Content-Type': 'text/html;', 'charset':'UTF-8','Transfer-Encoding': 'chunked', 'Content-Encoding': 'gzip', 'Referer':self.getMainUrl(), 'Origin':self.getMainUrl()}
                self.AJAX_HEADER = dict(self.HEADER)
                self.AJAX_HEADER.update( {'X-Requested-With': 'XMLHttpRequest', 'Accept-Encoding':'gzip, deflate', 'Content-Type':'application/x-www-form-urlencoded; charset=UTF-8', 'Accept':'application/json, text/javascript, */*; q=0.01'} )
                self.cacheLinks  = {}
                self.defaultParams ={}# {'header':self.HEADER, 'raw_post_data':True, 'use_cookie': True, 'load_cookie': True, 'save_cookie': True, 'cookiefile': self.COOKIE_FILE}
              

        def get_video_url(self,url):

                            

                 
                html = self.getPage(url)

                if html:
                    _srcs = re.search(r'sources\s*:\s*\[(.+?)\]', html)
                    if _srcs:
                        srcs = scrape_sources(_srcs.group(1), patterns=['''["'](?P<url>http[^"']+)'''])
                        print "srcs",srcs
                        return srcs




def get_video_url(url):

  return clipwatching().get_video_url(url)
