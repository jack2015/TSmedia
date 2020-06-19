# -*- coding: cp1256 -*-

from iTools import CBaseAddonClass,printD,printE
import sys,warnings
import urllib,urllib2,re,os,json,requests,hashlib,time,jsunpack
from urlparse import urlparse
from requests.packages.urllib3.exceptions import InsecureRequestWarning
warnings.simplefilter('ignore',InsecureRequestWarning)
##########################################



Agent = {'User-agent': 'Mozilla/5.0 (Windows NT 10.0; �) Gecko/20100101 Firefox/65.0'}
import requests
import urllib2
import re

class upstream(CBaseAddonClass):
        def __init__(self):
                CBaseAddonClass.__init__(self,{'cookie':'moshahda.cookie'})

                self.USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36'
                self.MAIN_URL = 'http://upstream.online'
                self.HEADER = {}#{'User_agent':self.USER_AGENT,'Content-Type': 'text/html;', 'charset':'UTF-8','Transfer-Encoding': 'chunked', 'Content-Encoding': 'gzip', 'Referer':self.getMainUrl(), 'Origin':self.getMainUrl()}
                self.AJAX_HEADER = dict(self.HEADER)
                self.AJAX_HEADER.update( {'X-Requested-With': 'XMLHttpRequest', 'Accept-Encoding':'gzip, deflate', 'Content-Type':'application/x-www-form-urlencoded; charset=UTF-8', 'Accept':'application/json, text/javascript, */*; q=0.01'} )
                self.cacheLinks  = {}
                self.defaultParams ={}# {'header':self.HEADER, 'raw_post_data':True, 'use_cookie': True, 'load_cookie': True, 'save_cookie': True, 'cookiefile': self.COOKIE_FILE}
              

        def get_video_url(self,url):

                            

                    data=self.getPage(url)

                    sources = scrape_sources(data)
                    print "sources",sources
                    return sources
                    
 


def scrape_sources(html, result_blacklist=None, scheme='http', patterns=None, generic_patterns=True):
    if patterns is None: patterns = []
    
    def __parse_to_list(_html, regex):
        _blacklist = ['.jpg', '.jpeg', '.gif', '.png', '.js', '.css', '.htm', '.html', '.php', '.srt', '.sub', '.xml', '.swf', '.vtt', '.mpd']
        _blacklist = set(_blacklist + result_blacklist)
        streams = []
        labels = []
        for r in re.finditer(regex, _html, re.DOTALL):
            match = r.groupdict()
            stream_url = match['url'].replace('&amp;', '&')
            file_name = urlparse(stream_url[:-1]).path.split('/')[-1] if stream_url.endswith("/") else urlparse(stream_url).path.split('/')[-1]
            blocked = not file_name or any(item in file_name.lower() for item in _blacklist)
            if stream_url.startswith('//'): stream_url = scheme + ':' + stream_url
            if '://' not in stream_url or blocked or (stream_url in streams) or any(stream_url == t[1] for t in source_list):
                continue
    
            label = match.get('label', file_name)
            if label is None: label = file_name
            labels.append(label)
            streams.append(stream_url)
            
        matches = zip(labels, streams)
        if matches:
            print "matches",matches
        return matches

    if result_blacklist is None:
        result_blacklist = []
    elif isinstance(result_blacklist, str):
        result_blacklist = [result_blacklist]
        
    html = html.replace("\/", "/")
    html += get_packed_data(html)

    source_list = []
    if generic_patterns or not patterns:
        source_list += __parse_to_list(html, '''["']?label\s*["']?\s*[:=]\s*["']?(?P<label>[^"',]+)["']?(?:[^}\]]+)["']?\s*file\s*["']?\s*[:=,]?\s*["'](?P<url>[^"']+)''')
        source_list += __parse_to_list(html, '''["']?\s*(?:file|src)\s*["']?\s*[:=,]?\s*["'](?P<url>[^"']+)(?:[^}>\]]+)["']?\s*label\s*["']?\s*[:=]\s*["']?(?P<label>[^"',]+)''')
        source_list += __parse_to_list(html, '''video[^><]+src\s*[=:]\s*['"](?P<url>[^'"]+)''')
        source_list += __parse_to_list(html, '''source\s+src\s*=\s*['"](?P<url>[^'"]+)['"](?:.*?res\s*=\s*['"](?P<label>[^'"]+))?''')
        source_list += __parse_to_list(html, '''["'](?:file|url)["']\s*[:=]\s*["'](?P<url>[^"']+)''')
        source_list += __parse_to_list(html, '''param\s+name\s*=\s*"src"\s*value\s*=\s*"(?P<url>[^"]+)''')
    for regex in patterns:
        source_list += __parse_to_list(html, regex)
        
    source_list = list(set(source_list))
    
   

    return source_list
def get_packed_data(html):
    packed_data = ''
    for match in re.finditer('(eval\s*\(function.*?)</script>', html, re.DOTALL | re.I):
        try:
            js_data = jsunpack.unpack(match.group(1))
            js_data = js_data.replace('\\', '')
            packed_data += js_data
        except:
            pass
        
    return packed_data

def get_video_url(url):

  return upstream().get_video_url(url)
