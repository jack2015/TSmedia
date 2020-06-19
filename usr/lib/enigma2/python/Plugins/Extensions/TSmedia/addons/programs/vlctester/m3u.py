


from xbmctools import Item,readnet,supported,get_params,getDomain,getserver_image,resolvehost,playlink,getsearchtext,logdata,trace_error
item=Item()
addDir=item.addDir
endDir=item.endDir
import sys
import urllib, urllib2, re,  sys ,os,requests

from httplib import HTTP
from urlparse import urlparse
import StringIO
import httplib
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


# -*- coding: utf8 -*-


import sys
import urllib,urllib2,re,os
from xbmctools import readnet,get_params,getDomain,resolvehost,getsearchtext,logdata,trace_error,extractdata,postData

################''

##########################################parsing tools
folder=iptv_folder
module_path=iptv_folder
def downloadfile(url = None,localfile=''):
    
    

      

        
        
        if url and url.startswith('http'):
            try:
                
                
                
                r = requests.get(url, timeout=10,verify=False)
                if r.status_code == 200:
                    with open(localfile, 'wb') as f:
                        f.write(r.content)
                    f.close()
                    return True
            except:
                
                trace_error()

        return False  

def geticon(title):
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

def _getM3uIcon( item,group_title):
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
def listM3u(name, m3ufile,page,addDir):
           
        baseUrl = ''
        data = ''
        data=open(m3ufile).read()        
        
        
        from m3uparser import  ParseM3u
        data = ParseM3u(data)

        
        groups = []
        groups_list=[]
        links=[]
        i=0
        addDir("Search",m3ufile,7,"img/search.png","",1)
        for item in data:
            i=i+1
            group_title = item.get('group-title', '')
            url = item['uri']
            icon = _getM3uIcon(item,group_title)
            
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
                    icon = _getM3uIcon(item,title)
                    
                    links.append((title,url,icon,i))                      
                    
                    
                        
        if len(groups)!=0:
             print "groups",groups
             for group in groups:
                 if "info" in group[0].lower() or "label" in group[0].lower():
                         continue
                 addDir(group[0],group[1],10,group[2],"",group[3])
             return groups
        else:
            for link in links:
                addDir(link[0], link[1], 0, link[2],"",link[3])
                

def listM3ubygroup(selgroup,m3ufile,page,addDir):
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
                
                print "group,selfgroup",group,selgroup 
                if group !="":    
                    if group ==selgroup:
           
            
            
                        count=count+1
                        title = item.get('title', '')
                        url = item['uri']
                        icon = _getM3uIcon(item,title)
                        links.append((title,url,icon))                      
                    else:
                       break

        if links:
            for link in links:
                addDir(link[0], link[1],0, link[2],selgroup,page)                
        if count>19:
           addDir(selgroup+"-next page", m3ufile,10, "img/next.png",selgroup,str(page+20))  
def listM3unogroups(name, m3ufile,page,addDir):
           
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
                    icon = _getM3uIcon(item,title)
                    count=count+1
                    links.append((title,url,icon))                      
                    
                    
                        
        print "links",links
        if links:
            for link in links:
                addDir(link[0], link[1], 0, link[2],name,page+50)

        if count>49:
           addDir(selgroup+"-next page", m3ufile,10, "img/next.png",name,str(page+50)) 
                
                      

def listM3usearch(sterm,m3ufile,page,addDir):
           
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
                        icon = _getM3uIcon(item,title)
                        
                        links.append((title,url,icon))                      
                    
                    
                        
        print "links",links
        if links:
            for link in links:
                addDir(link[0], link[1], 0, link[2],"Search",1)        
  


