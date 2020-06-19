# -*- coding: utf8 -*-
import urllib,urllib2,re,sys,os,ast
from iTools import CBaseAddonClass,printD,printE
baseurl="http://vlctest.eu5.net/"
##########################################
class vlctester(CBaseAddonClass):
    def __init__(self):
        CBaseAddonClass.__init__(self,{'cookie':'vlctester.cookie'})
        self.USER_AGENT = 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:40.0) Gecko/20100101 Firefox/40.0'
        self.MAIN_URL = 'http://vlctest.eu5.net/'
        self.HEADER = {'User-Agent': self.USER_AGENT, 'DNT':'1', 'Accept': 'text/html', 'Accept-Encoding':'gzip, deflate', 'Referer':self.getMainUrl(), 'Origin':self.getMainUrl()}
        self.AJAX_HEADER = dict(self.HEADER)
        self.AJAX_HEADER.update( {'X-Requested-With': 'XMLHttpRequest', 'Accept-Encoding':'gzip, deflate', 'Content-Type':'application/x-www-form-urlencoded; charset=UTF-8', 'Accept':'application/json, text/javascript, */*; q=0.01'} )
        self.cacheLinks  = {}
        self.defaultParams = {'header':self.HEADER, 'raw_post_data':True, 'use_cookie': True, 'load_cookie': True, 'save_cookie': True, 'cookiefile': self.COOKIE_FILE}
    def fixlink(self,url):
        try:
            #url='rtmp://5.63.151.4:443/atv<playpath>atv3<swfUrl>http://i.tmgrup.com.tr/p/flowplayer-3.2.9.swf?i=1<pageUrl>http://www.atv.com.tr/webtv/canli-yayin<live>1'
            url=url.replace('<swfUrl>',' swfUrl=').replace('<pageUrl>',' pageUrl=').replace('<live>',' live=') .replace('<playpath>',' playpath=').replace('<playpath>',' playpath=').strip()  
        except:
            pass   
        return url
    def getlinks(self,url=baseurl):
        list1=[]
        err='none'
        pagecounts=0
        done=True
        regx='''<h5><span style="(.*?)">(.*?)</span>(.*?)</h5>'''
        regx='''<strong><span style="(.*?)">(.*?)</span>(.*?)</strong><br>'''
        regx='''<strong><span style="(.*?)">(.*?)</span>(.*?)</strong><br>'''
        #regx='''<h5><span style="(.*?)</span>(.*?)</h5>'''
        debug=True
        if True:
            data=self.getPage(url)
            match = re.findall(regx,data, re.M|re.I)
            print "match",len(match)
            i=0
            for color,href,cdate in match:
                #continue
                i=i+1
                print "href",href
                active=True
                #continue
                active='working'
                if '#D04E0F' in color:
                    active='Not working'
                    img="img/red.png"
                else:
                    img="img/blue.png"    
                cdate=cdate.replace('|','').strip()
                name=href[:40]
                if href.startswith('rtmp'):
                    href=self.fixlink(href)
                isuspported=False   
                try:name,image,issupported=self.getDomain(href)
                except:pass    
                filename=os.path.split(href)[1]
                if issupported:
                    name =name+"-"+filename+'-'+active     
                    try:self.addDir(name,href,1,img,"",1,parseM3u8=False)
                    except:pass
                    continue
                else:
                    if href.endswith("m3u"):
                        try:self.addDir(name,href,2,img,"",1,parseM3u8=False)
                        except:pass
                        continue
                    filename=os.path.split(href)[1]
                    name=name+" "+cdate+"-"+active
                    try:self.addDir(name,href,0,img,"",1,parseM3u8=False)
                    except:pass
        else:
            err='Parsing error'
            list1=[]
        return None
    def runm3u(self,name,url,page):
        PLUGIN_PATH = '/usr/lib/enigma2/python/Plugins/Extensions/TSmedia'
        dlocation_file=PLUGIN_PATH+"/lib/defaults/download_location"
        try:
            iptv_folder=open(dlocation_file).read()
        except:
            iptv_folder="/media/hdd"
        iptv_folder = iptv_folder+"/TSmedia/iptv/"
        if not os.path.exists(iptv_folder):
            try:os.makedirs(iptv_folder)
            except:pass
        folder=iptv_folder
        module_path=iptv_folder
        success=downloadfile(url,iptv_folder+"tmp.m3u")
        printD("url",url)
        printD("success",success)
        if success:
            from m3u import listM3u
            listM3u(name,iptv_folder+"tmp.m3u",page,self.addDir)
    def downloadfile(self,url = None,localfile=''):
        import requests
        if url and url.startswith('http'):
            try:
                r = requests.get(url, timeout=10,verify=False)
                if r.status_code == 200:
                    with open(localfile, 'wb') as f:
                        f.write(r.content)
                    f.close()
                    return True
            except:
                printE()
        return False  
    def run(self):
        params=self.get_params()
        url=None
        name=None
        mode=None
        page=1
        name=params.get("name",None)
        url=params.get("url",None)
        try:mode=int(params.get("mode",None))
        except:mode=None
        image=params.get("image",None)
        section=params.get("section",None)
        page=int(params.get("page",1))
        extra=params.get("extra",None)
        show=params.get("show",None)
        ##menu and tools
        if mode==None:
            self.getlinks()
        elif mode==1:
            self.resolvehost(item,name,url)
        elif mode==2:
            self.runm3u(name,url,1)
        elif mode==10:
            from m3u import listM3ubygroup
            listM3ubygroup(name,url,page,self.addDir)
        elif mode==14:
            try:
                self.cfile=open("/tmp/TSmedia/m3ufile","w")
                self.cfile.write(name)
                self.cfile.close()
            except:
                pass
            from m3u import listM3unogroups   
            listM3unogroups(name,url,page,self.addDir)
            ###movies     
        elif mode == 16:
            server,image,issupported=self.getDomain(url)
            if issupported:
                self.resolvehost(name,url)
            else:
                self.playlink(url)
        elif mode == 17:
            sterm=self.getsearchtext()
            from m3u import listM3usearch
            listM3usearch(sterm,url,1,self.addDir)
        return self.endDir()
def start():
    addon=vlctester()
    return addon.run()