# -*- coding: cp1256 -*-

from iTools import CBaseAddonClass,printD,printE,GetIPTVSleep
import sys,warnings
import urllib,urllib2,re,os,json,requests,hashlib,time
from requests.packages.urllib3.exceptions import InsecureRequestWarning
warnings.simplefilter('ignore',InsecureRequestWarning)
##########################################



Agent = {'User-agent': 'Mozilla/5.0 (Windows NT 10.0; �) Gecko/20100101 Firefox/65.0'}
import requests
import urllib2
import re

class holavid(CBaseAddonClass):
        def __init__(self):
                CBaseAddonClass.__init__(self,{'cookie':'moshahda.cookie'})

                self.USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36'
                self.MAIN_URL = 'http://holavid.online'
                self.HEADER = {}#{'User_agent':self.USER_AGENT,'Content-Type': 'text/html;', 'charset':'UTF-8','Transfer-Encoding': 'chunked', 'Content-Encoding': 'gzip', 'Referer':self.getMainUrl(), 'Origin':self.getMainUrl()}
                self.AJAX_HEADER = dict(self.HEADER)
                self.AJAX_HEADER.update( {'X-Requested-With': 'XMLHttpRequest', 'Accept-Encoding':'gzip, deflate', 'Content-Type':'application/x-www-form-urlencoded; charset=UTF-8', 'Accept':'application/json, text/javascript, */*; q=0.01'} )
                self.cacheLinks  = {}
                self.defaultParams ={}# {'header':self.HEADER, 'raw_post_data':True, 'use_cookie': True, 'load_cookie': True, 'save_cookie': True, 'cookiefile': self.COOKIE_FILE}
              

        def get_video_url(self,url):
      
                Listos = []
                def get_Vid(url):
                    
                   
                        r = self.getPage(url)
                        ymx = '''sources: \[(.+?)\]'''
                        source = re.findall(ymx,r)
                        Video = source[0].split('","')
                        print "source",source
                        x = len(Video)
                        for i in range(x):
                            w = (Video[i].replace('"',''))
                            if w.endswith("m3u8"):
                                    
                               Listos.append(("m3u8",w))
                            elif w.endswith("mp4"):
                                 Listos.append(("mp4",w))
                            else:
                                 Listos.append(("holavid",w))   
                        return Listos
                #S1="https://www.el7l.video/watch.php?vid=35b0046fe"
                #T1="https://www.el7l.video/v.php?vid=35b0046fe"
                Listos=get_Vid(url)
                return Listos




def get_video_url(url):

  return holavid().get_video_url(url)
