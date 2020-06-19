# -*- coding: utf8 -*-
import sys
import urllib,urllib2,re,os,ast
from iTools import CBaseAddonClass,printD,printE
extra={}
################''


##########################################parsing tools


class watchvideo(CBaseAddonClass):
    
        def __init__(self,cParams={}):
                
                CBaseAddonClass.__init__(self,{'cookie':'watchvideo.cookie','module_path':__file__})
                self.cParams=cParams
                self.USER_AGENT ='Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:68.0) Gecko/20100101 Firefox/68.0'
                self.MAIN_URL = 'http://watchvideo.us'
                

                self.HEADER = {'User-Agent': self.USER_AGENT, 'DNT':'1', 'Accept': 'text/html', 'Accept-Encoding':'gzip, deflate', 'Referer':self.getMainUrl(), 'Origin':self.getMainUrl()}


                self.AJAX_HEADER = dict(self.HEADER)
                self.AJAX_HEADER.update( {'X-Requested-With': 'XMLHttpRequest', 'Accept-Encoding':'gzip, deflate', 'Content-Type':'application/x-www-form-urlencoded; charset=UTF-8', 'Accept':'application/json, text/javascript, */*; q=0.01'} )
                self.cacheLinks  = {}
                self.defaultParams = {'header':self.HEADER, 'raw_post_data':True, 'use_cookie': True, 'load_cookie': True, 'save_cookie': True, 'cookiefile': self.COOKIE_FILE}
                self.module_path=__file__
                #self.getPage=self.cm.getPage#(self, url, addParams = {}, post_data = None)
               
        def get_watchvideo(self,url):
                    data=self.getPage(url)
                    #print "data",data

                    packed = self.getSG(data, "text/javascript'>(.*?)\s*</script>")[0]
                    
                    import lib.jsunpack as jsunpack
                    unpacked = jsunpack.unpack(packed)
                    video_urls=[]
                    media_urls = self.getSG(unpacked, 'file:"([^"]+)"')
                    for media_url in media_urls:
                        
                        if "m3u8" in media_url:
                            ext = "m3u8"
                          
                        video_urls.append(["%s [watchvideo]" % (ext), media_url])
                    print 'video_urls',video_urls
                    
                    
                    return video_urls


def get_video_url(url):
        addon=watchvideo()
        T1='https://watchvideo.us/embed-saz0x9iypvot.html'
        T2='https://watchvideo.us/embed-cgc8a7orhzs9.html'
                                
        return addon.get_watchvideo(url)              
