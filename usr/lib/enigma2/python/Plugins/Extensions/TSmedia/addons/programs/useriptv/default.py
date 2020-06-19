# -*- coding: utf8 -*-
import urllib,urllib2,re,sys,os,ast
from iTools import CBaseAddonClass,printD,printE,AppPath,getos,downloadfile


##########################################
import sys
import urllib, urllib2, re,  sys ,os,requests

from httplib import HTTP
from urlparse import urlparse
import StringIO
import httplib
PLUGIN_PATH = AppPath
if getos=="windows":

         iptv_folder=PLUGIN_PATH+"/media/hdd/TSmedia/iptv/"       
else:
        dlocation_file="/tmp/TSmedia/downloadDir"
        
        try:
          iptv_folder=open(dlocation_file).read()
          iptv_folder = iptv_folder+"/TSmedia/iptv/"
        except:
          iptv_folder=AppPath+"/media/hdd/iptv"
        

        


if not os.path.exists(iptv_folder):
  try:os.makedirs(iptv_folder)
  except:pass


##########################################parsing tools
folder=iptv_folder
module_path=iptv_folder

class useriptv(CBaseAddonClass):
        def __init__(self):
                CBaseAddonClass.__init__(self,{'cookie':'useriptv.cookie'})

                self.USER_AGENT = 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:40.0) Gecko/20100101 Firefox/40.0'
                self.MAIN_URL = 'http://tv.TSmedia.com'
                self.HEADER = {'User-Agent': self.USER_AGENT, 'DNT':'1', 'Accept': 'text/html', 'Accept-Encoding':'gzip, deflate', 'Referer':self.getMainUrl(), 'Origin':self.getMainUrl()}
                self.AJAX_HEADER = dict(self.HEADER)
                self.AJAX_HEADER.update( {'X-Requested-With': 'XMLHttpRequest', 'Accept-Encoding':'gzip, deflate', 'Content-Type':'application/x-www-form-urlencoded; charset=UTF-8', 'Accept':'application/json, text/javascript, */*; q=0.01'} )
                self.cacheLinks  = {}
                self.defaultParams = {'header':self.HEADER, 'raw_post_data':True, 'use_cookie': True, 'load_cookie': True, 'save_cookie': True, 'cookiefile': self.COOKIE_FILE}
              


        def getuserlist(self):
           
            files = []
            fullpath = []
            user_iptv_file = iptv_folder+'iptvlist'
            print "user_iptv_file",user_iptv_file
            if os.path.exists(user_iptv_file):
                f = open(user_iptv_file, 'r')
                lines = f.readlines()
                print "linesxx",lines
                for line in lines:
                    line = line.strip()
                    if line.startswith('m3u'):
                        parts = line.split(';')
                        itemtype = parts[0]
                        itempath = parts[2]
                        itemname = parts[1]
                        try:
                            
                            if True:
                               success=downloadfile(itempath, iptv_folder + itemname + '.m3u')
                               printD("success",success)
                               
                            if not os.path.exists(folder + itemname + '.lnk') :
                               cfile=open(folder + itemname + '.lnk',"w")
                               cfile.write(itempath)
                               cfile.close()
                               
                        except:
                            printE()            
                            pass
        
                    if line.startswith('iptv'):
                        parts = line.split(';')
                        itemtype = parts[0]
                        itempath = parts[2]
                        itemname = parts[1]
                        self.addDir(itemname, itempath, 6, 'img/iptv.png','',1)                 
        
        
                          
        
            if os.path.exists(folder):
                emptyfolder = True
                for item in os.listdir(folder):
                    itempath = folder + item
                    if os.path.isfile(itempath):
                        if item.endswith('.m3u'):
                            itemname = item.replace('.m3u', '')
                            icon=self.geticon(itemname)
                            self.addDir(itemname, itempath, 1, icon,'',1)
                            
                            emptyfolder = False
        
                if emptyfolder == True:
                    self.addDir('No m3u file in '+iptv_folder,"http://", 1, '', '',1)
        def geticon(self,title):
                       icon=''
        
                       if 'sport' in title.lower():
                          icon=module_path+"/img/sport.png"               
        
                       if 'kids' in title.lower():
                          icon=module_path+"/img/kids.png"
                       
                       if 'movies' in title.lower():
                          icon=module_path+"/img/movies.png"
                       
                       if 'france' in title.lower() or 'fr:' in title.lower():
                          icon=module_path+"/img/france.png"
                       if 'arab' in title.lower() or 'ar' in title.lower():
                          icon=module_path+"/img/arab.png"
                       
                       if 'portugal' in title.lower():
                          icon=module_path+"/img/portugal.png"
                       if 'sky' in title.lower():
                          icon=module_path+"/img/sky.png"
                       
                       if 'nilesat' in title.lower() :
                          icon=module_path+"/img/nilesat.png"
                       if 'usa' in title.lower() :
                          icon=module_path+"/img/uk.png"
                       if 'tunisia' in title.lower():
                          icon=module_path+"/img/tunisia.png"                 
                          
                       if 'bein' in title.lower():
                          icon=module_path+"/img/bein.png"
                       if 'osn' in title.lower():
                          icon=module_path+"/img/osn.png"
                       if icon=='':
                           icon=module_path+"/icon.png"
                       return icon
        
        def _getM3uIcon(self,item,group_title):
                title=group_title
                icon = item.get('tvg-logo', '')
                if icon=='':
                   item.get('logo', '') 
                if icon=='':
                   icon = item.get('art', '')
                   
                if icon=='':
                       if 'sport' in title.lower():
                          icon=module_path+"/img/sport.png"               
        
                       if 'kids' in title.lower():
                          icon=module_path+"/img/kids.png"
                       
                       if 'movies' in title.lower():
                          icon=module_path+"/img/movies.png"
                       
                       if 'france' in title.lower() or 'fr:' in title.lower():
                          icon=module_path+"/img/france.png"
                       if 'arab' in title.lower() or 'ar' in title.lower():
                          icon=module_path+"/img/arab.png"
                       
                       if 'portugal' in title.lower():
                          icon=module_path+"/img/portugal.png"
                       if 'sky' in title.lower():
                          icon=module_path+"/img/sky.png"
                       
                       if 'nilesat' in title.lower() :
                          icon=module_path+"/img/nilesat.png"
                       if 'usa' in title.lower() :
                          icon=module_path+"/img/uk.png"
                       if 'tunisia' in title.lower() :
                          icon=module_path+"/img/tunisia.png"                 
                          
                       if 'bein' in title.lower():
                          icon=module_path+"/img/bein.png"
                       if 'osn' in title.lower():
                          icon=module_path+"/img/osn.png"
        
                       if icon=='':
                           icon=module_path+"/icon.png"
                          
                return icon
        def listM3u(self,name, m3ufile,page):
                   
                baseUrl = ''
                data = ''
                data=open(m3ufile).read()        
                
                
                from m3uparser import  ParseM3u
                data = ParseM3u(data)
        
                printD("data",data)
                groups = []
                groups_list=[]
                links=[]
                i=0
                self.addDir("Search",m3ufile,7,"img/search.png","",1)
                for item in data:
                    i=i+1
                    group_title = item.get('group-title', '')
                    url = item['uri']
                    icon = self._getM3uIcon(item,group_title)
                    
                    if item['f_type'] == 'inf':
                        
                        
                        if group_title !="":    
                            if group_title not in groups_list:
                                    groupIcon = item.get('group-logo', '')
                                    if groupIcon =='':
                                       groupIcon = item.get('group-art', '')
                                    if  groupIcon =='':
                                        groupIcon = icon
                                    
                                    groups_list.append(group_title)
                                    groups.append((group_title,m3ufile,groupIcon,i))
                                    
        
                        else:
                            title = item.get('title', '')
                            url = item['uri']
                            icon = self._getM3uIcon(item,title)
                            
                            links.append((title,url,icon,i))                      
                            
                            
                                
                if len(groups)!=0:
                     for group in groups:
                         if "info" in group[0].lower() or "label" in group[0].lower():
                                 continue
                         self.addDir(group[0],group[1],2,group[2],"",group[3])
                     return groups
                else:
                    for link in links:
                        self.addDir(link[0], link[1], 0, link[2],"",link[3])
                        
        
        def listM3ubygroup(self,selgroup,m3ufile,page):
                if "next page" in selgroup:
                    selgroup=selgroup.split("-")[0]
                baseUrl = ''
                data = ''
                data=open(m3ufile).read()        
                
                
                from m3uparser import  ParseM3u
                data = ParseM3u(data)
        
               
                groups = []
                links=[]
                i=0
                count=0
                for item in data:
                    i=i+1
                    if i<page:
                        continue
                    if i>(page+20):
                        break
                    group = item.get('group-title', '')
                    
                    if item['f_type'] == 'inf':
                        
                        if group !="":    
                            if group ==selgroup:
                   
                    
                    
                                count=count+1
                                title = item.get('title', '')
                                url = item['uri']
                                icon = self._getM3uIcon(item,title)
                                links.append((title,url,icon))                      
                            else:
                               break
        
                if links:
                    for link in links:
                        self.addDir(link[0], link[1],0, link[2],selgroup,page)                
                if count>19:
                   self.addDir(selgroup+"-next page", m3ufile,2, "img/next.png",selgroup,str(page+20))  
        def listM3unogroups(self,name, m3ufile,page):
                   
                baseUrl = ''
                data = ''
                data=open(m3ufile).read()        
                
                
                from m3uparser import  ParseM3u
                data = ParseM3u(data)
        
               
                groups = []
                groups_list=[]
                links=[]
                count=0
                for item in data:
                    i=i+1
                    if i<page:
                        continue
                    if i>(page+50):
                        break
                    group_title = item.get('group-title', '')
                    
                    
                    if item['f_type'] == 'inf':
                        
                        
                        
                            title = item.get('title', '')
                            url = item['uri']
                            icon = self._getM3uIcon(item,title)
                            count=count+1
                            links.append((title,url,icon))                      
                            
                            
                                
                if links:
                    for link in links:
                        self.addDir(link[0], link[1], 0, link[2],name,page+50)
        
                if count>49:
                   self.addDir(selgroup+"-next page", m3ufile,2, "img/next.png",name,str(page+50)) 
                        
                              
        
        def listM3usearch(self,sterm,m3ufile,page):
                   
                baseUrl = ''
                data = ''
                data=open(m3ufile).read()        
                
                
                from m3uparser import  ParseM3u
                data = ParseM3u(data)
        
                
                search_str=sterm
                groups_list=[]
                links=[]
                for item in data:
        
                    group_title = item.get('group-title', '')
                   
                    
                    if item['f_type'] == 'inf':
                        
                        
                        
                            title = item.get('title', '')
                            if search_str.lower() in title.lower():
                                url = item['uri']
                                icon = self._getM3uIcon(item,title)
                                
                                links.append((title,url,icon))                      
                            
                            
                                
                if links:
                    for link in links:
                        self.addDir(link[0], link[1], 0, link[2],"Search",1)        
          
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
                    name = 'Bouquets'
                    page = 1
                    
                    
                    self.getuserlist()
             
                      
                elif mode==1:
                    try:
                        self.cfile=open("/tmp/Tsmedia/m3ufile","w")
                        self.cfile.write(name)
                        self.cfile.close()
                    except:
                        pass
                        self.listM3u(name,url,page)
                elif mode==2:
                        self.listM3ubygroup(name,url,page)
                elif mode==4:
                    try:
                        self.cfile=open("/tmp/TSmedia/m3ufile","w")
                        self.cfile.write(name)
                        self.cfile.close()
                    except:
                        pass
                        self.listM3unogroups(name,url,page)
                ###movies     
                        
                elif mode == 6:
                    self.server,image,issupported=self.getDomain(url)
                   
                    if issupported:
                        self.resolvehost(name,url)
                    else:
                       
                      
                       self.addDir(name,url,0)
                elif mode == 7:
                        sterm=self.getsearchtext()
                        self.listM3usearch(sterm,url,1)
                
                return self.endDir()

def start():
    addon=useriptv()
    return addon.run()               


