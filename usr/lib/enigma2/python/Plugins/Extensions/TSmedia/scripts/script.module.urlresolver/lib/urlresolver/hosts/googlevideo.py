# -*- coding: utf8 -*-

import sys
import urllib,urllib2,re,os,json

from iTools import CBaseAddonClass,printDBG, printExc,GetCookieDir,strwithmeta,unicode_escape
##########################################main menu
baseurl = 'https://www.moviflex.net'
      
##########################################main menu
class googlevideo(CBaseAddonClass):
    
        def __init__(self):
                CBaseAddonClass.__init__(self,{'cookie':'google.cookie'})
                

                         
        def parserGOOGLE(self, baseUrl):
                printDBG("parserGOOGLE baseUrl[%s]" % baseUrl)
                
                videoTab = []
                _VALID_URL = r'https?://(?:(?:docs|drive)\.google\.com/(?:uc\?.*?id=|file/d/)|video\.google\.com/get_player\?.*?docid=)(?P<id>[a-zA-Z0-9_-]{28,})'
                mobj = re.match(_VALID_URL, baseUrl)
                try:
                    video_id = mobj.group('id')
                    linkUrl = 'http://docs.google.com/file/d/' + video_id 
                except Exception:
                    linkUrl = baseUrl
                    
                _FORMATS_EXT = {
                    '5': 'flv', '6': 'flv',
                    '13': '3gp', '17': '3gp',
                    '18': 'mp4', '22': 'mp4',
                    '34': 'flv', '35': 'flv',
                    '36': '3gp', '37': 'mp4',
                    '38': 'mp4', '43': 'webm',
                    '44': 'webm', '45': 'webm',
                    '46': 'webm', '59': 'mp4',
                }
                
                HTTP_HEADER= self.cm.getDefaultHeader(browser='chrome')
                HTTP_HEADER['Referer'] = linkUrl
                
                COOKIE_FILE = GetCookieDir('google.cookie')
                print 'COOKIE_FILE',COOKIE_FILE
                defaultParams = {'header': HTTP_HEADER, 'use_cookie': True, 'load_cookie': False, 'save_cookie': True, 'cookiefile': COOKIE_FILE}
                
                sts, data = self.cm.getPage(linkUrl, defaultParams)
                if not sts: return False 
                
                cookieHeader = self.cm.getCookieHeader(COOKIE_FILE)
                fmtDict = {}
               
                fmtList = self.cm.ph.getSearchGroups(data, '"fmt_list"[:,]"([^"]+?)"')[0]
                fmtList = fmtList.split(',')
                for item in fmtList:
                    item = self.cm.ph.getSearchGroups(item, '([0-9]+?)/([0-9]+?x[0-9]+?)/', 2)
                    if item[0] != '' and item[1] != '':
                        fmtDict[item[0]] = item[1]
                        
                data = self.cm.ph.getSearchGroups(data, '"fmt_stream_map"[:,]"([^"]+?)"')[0]
                data = data.split(',')
                
                for item in data:
                     
                    item = item.split('|')
                    printDBG(">> type[%s]" % item[0])
                    
                    if 'mp4' in _FORMATS_EXT.get(item[0], ''):
                           
                        try: quality = int(fmtDict.get(item[0], '').split('x', 1)[-1])
                        except Exception: quality = 0
                        videoTab.append({'name':'drive.google.com: %s' % fmtDict.get(item[0], '').split('x', 1)[-1] + 'p', 'quality':quality, 'url':strwithmeta(unicode_escape(item[1]), {'Cookie':cookieHeader, 'Referer':'https://youtube.googleapis.com/', 'User-Agent':HTTP_HEADER['User-Agent']})})
                videoTab.sort(key=lambda item: item['quality'], reverse=True)
                print "cookieHeader",cookieHeader
                list1=[]
                for item  in videoTab:
                    url=item['url']+"#User-agent=%s&Cookie=%s&Referer=%s"%(HTTP_HEADER['User-Agent'],cookieHeader,'https://youtube.googleapis.com/')
                    name=item['name']
                    list1.append((str(name),str(url)))
                    
                        
                return list1



                        
                
                
def get_video_url(url):
    host=googlevideo()
    return host.parserGOOGLE(url)
    
