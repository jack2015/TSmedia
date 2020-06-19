# -*- coding: utf-8 -*-

import os, sys, urllib,re
from xbmctools import addDir,finddata,getos,supported,getserver_image
from urlresolver.supservers import supported_servers
from iTools import printD as logdata,printE as trace_error
import os
module_path=os.path.split(os.path.realpath(__file__))[0]
default_mainserver='urlresolver'
forceresolve=True
def isvalidlink(link):
    if link is None:
        return False
    if  link.startswith("http") or  link.startswith("rtmp"):
        return True
    return False

def getDomain(url):
    
    print "url",url
    url=url.replace("embed.","")
    tmp = re.compile('//(.+?)/').findall(url)
    print "tmp",tmp
    domain = 'server'
    if len(tmp) > 0:
        domain = tmp[0].replace('www.', '')
    if 'google' in domain:
        domain = 'google'
    if '.' in domain:
        domain = domain.split('.')[0]
    print "domain",domain
    
    issupported=supported(domain)
    image=getserver_image(domain)
    
    return domain,image,issupported

def getmainserver(host):
       
       mainserver=''
       
       if True:
             if "wTSmedia" in module_path:##mfaraj
                plugin_path=module_path.split("wTSmedia")[0]+"wTSmedia"
                txt=open(plugin_path+"/scripts/script.module.urlresolver/lib/urlresolver/resolver.txt").read()
             else:
                plugin_path=module_path.split("TSmedia")[0]+"TSmedia"
                txt=open(plugin_path+"/scripts/script.module.urlresolver/lib/urlresolver/resolver.txt").read()
             
             resolver_mode=txt.strip()
             print 'resolver_mode',resolver_mode
             urlresolver_host=False
             pelisresolver_host=False
             tsresolver_host=False##mfaraj
             e2ipresolver_host=False##mfaraj
             youtube_dl_host=False##mfaraj
             
             servers_txt=open(plugin_path+"/scripts/script.module.urlresolver/lib/urlresolver/supservers.py").read()
              
             
             if resolver_mode=='auto' :
                 
                 
                 
                
                      
                     host=host.lower()
                     print 'host',host

                     server= supported_servers.get(host,[None,None])[1]
                     if  server:
                     
                     
                         if server=="urlresolver":
                            return True,False,False,False,False
                         if server=="pelisresolver":
                            return False,True,False,False,False                                     
                         if server=="tsresolver":
                            return False,False,True,False,False
                         if server=="e2ipresolver":
                            return False,False,False,True,False  
                         if server=="youtube_dl":
                            return False,False,False,False,True
                        
                     else:
                         return False,False,False,False,False


                     


                   

             elif resolver_mode=='all' :
                 
                 return True,True,True,True,True
                 
             elif resolver_mode=='urlresolver' :
                 
                 return True,False,False,False,False

             elif resolver_mode=='pelisresolver' :
                 
                 return False,True,False,False,False
             elif resolver_mode=='tsresolver' :
                 
                 return False,False,True,False,False

             elif resolver_mode=='e2ipresolver' :
                 
                 return False,False,False,True,False               
             elif resolver_mode=='youtube_dl' :
                 
                 return False,False,False,False,True  
             else:
                 
                 return False,False,False,False,False




    

            



def getclass(host):

        hostfile=module_path + "/plugins/" + host + ".py"
        if not os.path.exists(hostfile):
                return None
        lines =open(hostfile).readlines()
        for  line  in lines:
            if line.startswith("class") and "Resolver" in line:
                classname = line.split("(")[0].replace("class", "").strip()
                return classname
                
            
        return None
def get_host_id(host,url):

    import re
    
    hostfile=module_path + "/plugins/" + host + ".py"
    if not os.path.exists(hostfile):
                return None,None
    txt =open(hostfile).read()
    pattern =finddata(txt,"pattern = '","'")
    print "pattern",pattern
                   
    
    #pattern = '(?://|\.)(o(?:pen)??load\.(?:io|co|tv))/(?:embed|f)/([0-9a-zA-Z-_]+)'
    try:
        host,id = re.search(pattern, url).groups()
        
       
        return host,id
    except:
         return None,None
    


def get_linkid(web_url):
    parts = web_url.split('/')
    if parts:
        web_url = web_url.split('/')[len(parts) - 1]
    return web_url


def resolve(web_url = None, host = None, media_id = None, urllist = False,resolver=None):
    print "web_url",web_url
    print "hostxxx",host
  
    if host is None and web_url is not None:
        host,image,issupported = getDomain(web_url)
    else:
        print "No enough data"
        
        return "Error:Error: -err1-no data supplied by the addon"
    print "web_url",web_url

   
    stream_url = None
    done = True
    ###for debug

       
    ######
    try:
        host = host.lower()
    except:
        pass

    
    logdata("web_url",web_url)
    logdata("host",host)
    sys.argv.append(web_url)
    debug = True
    list1=[]
    urlresolver_host,pelisresolver_host,tsresolver_host,e2ipresolver_host,youtube_dl_host=getmainserver(host)

   

            
    print "urlresolver_host",urlresolver_host
    print "pelisresolver_host",pelisresolver_host
    print "tsresolver_host",tsresolver_host
    print "e2ipresolver_host",e2ipresolver_host
    print "youtube_dl_host",youtube_dl_host
    
    host_info=supported_servers.get(host,[None,None])
    default_server= host_info[1]
    host=host_info[0]    
     
    if  urlresolver_host==False and pelisresolver_host==False and tsresolver_host==False and e2ipresolver_host==False and youtube_dl_host==False:
            print "No supported module for given host"
            
            return "Error:No supported resolving module for given host"         
    
    
   

    if urlresolver_host==True and pelisresolver_host==True  and tsresolver_host==True and e2ipresolver_host==True and youtube_dl_host==True:                             
                      list1=[]   
                      print "\n\n####################urlresolver###################################################"
                      try:   
                        classname=getclass(host) 
                        txt='from urlresolver.plugins.'+host.strip()+" import " +classname.strip()+' as Resolver'
                       
                        exec(txt)                 
                       
                        resolver = Resolver()
                        print 'web_url',web_url
                        host1,media_id=get_host_id(host,web_url)
                       
                        stream_url = resolver.get_media_url(host1, media_id)
                        print 'stream_url',stream_url
                        if stream_url and  type(stream_url)==type([]):
                            if len(stream_url)==0:                  
                                      
                                       return "Error:Link is not available"
                                   
                            for item in stream_url:
                                        list1.append((item[0],item[1]))
                                       
                                        
                            
                        elif stream_url and not type(stream_url)==type([]):
                            list1.append(("link",stream_url))
                        else:
                            list1.append(("Error:urlresolver=",stream_url))
                      except:
                           trace_error()
                           list1.append(("Error:urlresolver",stream_url))
                               

                      

                      print "\n\n####################pelisresolver###################################################"
 
                      try:   
                        print 'web_url',web_url
                        print "host",host
                        exec('from urlresolver.servers.'+host.strip()+" import get_video_url")
                        
                        stream_url = get_video_url(web_url)
                        print 'stream_url',stream_url
                        if stream_url and  type(stream_url)==type([]):
                            if len(stream_url)==0:                  
                                      
                                       return "Error:Link is not available"
                                   
                            for item in stream_url:
                                        list1.append((item[0],item[1]))
                                       
                                        
                            
                        elif stream_url and not type(stream_url)==type([]):
                            list1.append((host,stream_url))
                        else:
                            list1.append(("Error:pelisresolver",stream_url))
                      except:
                           trace_error()
                           list1.append(("Error:pelisresolver",stream_url))
                               



                        
                      print "\n\n####################tsresolver###################################################"
 
                      try:   
                        print 'web_url',web_url
                                                
                        exec('from urlresolver.hosts.'+host.strip()+" import get_video_url")
                        
                        stream_url = get_video_url(web_url)
                        print 'stream_url',stream_url
                        if stream_url and  type(stream_url)==type([]):
                            if len(stream_url)==0:                  
                                      
                                       return "Error:Link is not available"
                                   
                            for item in stream_url:
                                        list1.append((item[0],item[1]))
                                       
                                        
                            
                        elif stream_url and not type(stream_url)==type([]):
                            list1.append((host,stream_url))
                        else:
                            list1.append(("Error:tsresolver",stream_url))
                      except:
                           trace_error()
                           list1.append(("Error:tsresolver",stream_url))
                               

                      print "\n\n####################e2iplayer-resolver###################################################"
 
                      try:   
                        print 'web_url',web_url
                        from IPTVPlayer.libs.urlparser import urlparser            
                        up=urlparser()
                        stream_url=up.getVideoLinkExt(web_url)
                        print "stream_urlx",stream_url
                        if stream_url and  type(stream_url)==type([]):
                            if len(stream_url)==0:                  
                                      
                                       return "Error:Link is not available"
                                   
                            for item in stream_url:
                                        list1.append((item['name'],item['url']))
                                       
                                        
                            
                        elif stream_url and not type(stream_url)==type([]):
                            list1.append((host,stream_url))
                        else:
                            list1.append(("Error:e2iresolver",stream_url))
                      except:
                           trace_error()
                           list1.append(("Error:e2iresolver",stream_url))                    
            

                      print "\n\n####################youtube_dl###################################################"
 
                      try:   
                        print 'web_url',web_url
                        import youtube_dl
                        
                        ydl = youtube_dl.YoutubeDL({'nocheckcertificate': True})
                        with ydl:
                            result = ydl.extract_info(
                                web_url,
                                download=False # We just want to extract the info
                            )
                                               
                        #result={u'display_id': u'1kLrJQ4odoTWlNhtKTkHanUjwKeOW4tRI', u'extractor': u'GoogleDrive', u'automatic_captions': {}, u'protocol': u'https', u'format': u'source - unknown', u'requested_subtitles': None, u'duration': 6924, u'format_id': u'source', u'quality': 1, u'id': u'1kLrJQ4odoTWlNhtKTkHanUjwKeOW4tRI', u'subtitles': {}, u'playlist': None, u'thumbnails': [{u'url': u'https://lh4.googleusercontent.com/p8w2_eqtNNTrG_XwxhzkNNUmz3bUIwJegDgE5NUzL1FGcuctmgnKYupiiOg=w1200-h630-p', u'id': u'0'}], u'title': u'The.Girl.in.the.Spiders.Web.2019.1080p.WEB-DL.mp4', u'url': u'https://drive.google.com/uc?export=download&id=1kLrJQ4odoTWlNhtKTkHanUjwKeOW4tRI&confirm=Ol0S', u'extractor_key': u'GoogleDrive', u'http_headers': {u'Accept-Language': u'en-us,en;q=0.5', u'Accept-Encoding': u'gzip, deflate', u'Accept': u'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8', u'User-Agent': u'Mozilla/5.0 (X11; Linux x86_64; rv:59.0) Gecko/20100101 Firefox/59.0', u'Accept-Charset': u'ISO-8859-1,utf-8;q=0.7,*;q=0.7', u'Cookie': 'download_warning_13058876669334088843_1kLrJQ4odoTWlNhtKTkHanUjwKeOW4tRI=Ol0S; NID=156=iHP5Vp-IhebgDeZGjJ9bCirTTsDMhyaYBU8FFkarralerWSAwQLG3xm2hHtlbzOvg86pDHlYqkwXXVOod4TQFHWIvpGN6aAdi4dUNzCTNAhP4RJeg89iSsxC-XOjT_6iqp1-kZXWNF_x3XdvK8W4rB5wN54QvYcqq2NBgqRBKok'}, u'playlist_index': None, u'ext': u'mp4', u'webpage_url': 'https://drive.google.com/file/d/1kLrJQ4odoTWlNhtKTkHanUjwKeOW4tRI/edit', u'formats': [{u'protocol': u'https', u'format': u'18 - 640x360', u'url': u'https://r4---sn-4g5e6nss.c.docs.google.com/videoplayback?id=57e35632e6df399d&itag=18&source=webdrive&requiressl=yes&mm=30&mn=sn-4g5e6nss&ms=nxu&mv=u&pl=24&sc=yes&ttl=transient&ei=2TJCXLq4FMSjqQX3z6b4Dw&susc=dr&driveid=1kLrJQ4odoTWlNhtKTkHanUjwKeOW4tRI&app=texmex&mime=video/mp4&dur=6924.585&lmt=1547687010977570&mt=1547841575&ip=37.202.64.169&ipbits=0&expire=1547856665&cp=QVNJWUlfVVZURlhOOkM1Q2JlNURIZ0Nu&sparams=ip%2Cipbits%2Cexpire%2Cid%2Citag%2Csource%2Crequiressl%2Cmm%2Cmn%2Cms%2Cmv%2Cpl%2Csc%2Cttl%2Cei%2Csusc%2Cdriveid%2Capp%2Cmime%2Cdur%2Clmt%2Ccp&signature=7F89467631A01321BEEAFF742D2E5FA5F2ED463C2D7D45EA630B4D775639150F.5554DF8AADBD8B7F39CA29AFD193D0D5577AB31450CE05E74262F5270CE4D8D9&key=us0', u'http_headers': {u'Accept-Language': u'en-us,en;q=0.5', u'Accept-Encoding': u'gzip, deflate', u'Accept': u'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8', u'User-Agent': u'Mozilla/5.0 (X11; Linux x86_64; rv:59.0) Gecko/20100101 Firefox/59.0', u'Accept-Charset': u'ISO-8859-1,utf-8;q=0.7,*;q=0.7', u'Cookie': 'NID=156=iHP5Vp-IhebgDeZGjJ9bCirTTsDMhyaYBU8FFkarralerWSAwQLG3xm2hHtlbzOvg86pDHlYqkwXXVOod4TQFHWIvpGN6aAdi4dUNzCTNAhP4RJeg89iSsxC-XOjT_6iqp1-kZXWNF_x3XdvK8W4rB5wN54QvYcqq2NBgqRBKok; DRIVE_STREAM=Z9Bzc1CKfCk'}, u'height': 360, u'width': 640, u'ext': u'mp4', u'format_id': u'18'}, {u'protocol': u'https', u'format': u'59 - 854x480', u'url': u'https://r4---sn-4g5e6nss.c.docs.google.com/videoplayback?id=57e35632e6df399d&itag=59&source=webdrive&requiressl=yes&mm=30&mn=sn-4g5e6nss&ms=nxu&mv=u&pl=24&sc=yes&ttl=transient&ei=2TJCXLq4FMSjqQX3z6b4Dw&susc=dr&driveid=1kLrJQ4odoTWlNhtKTkHanUjwKeOW4tRI&app=texmex&mime=video/mp4&dur=6924.585&lmt=1547687281756210&mt=1547841575&ip=37.202.64.169&ipbits=0&expire=1547856665&cp=QVNJWUlfVVZURlhOOkM1Q2JlNURIZ0Nu&sparams=ip%2Cipbits%2Cexpire%2Cid%2Citag%2Csource%2Crequiressl%2Cmm%2Cmn%2Cms%2Cmv%2Cpl%2Csc%2Cttl%2Cei%2Csusc%2Cdriveid%2Capp%2Cmime%2Cdur%2Clmt%2Ccp&signature=2A13F7DBF193FCFAFDAB3B9F89C24EF80D4B51A6D9E76E0F576312ED36C34095.47E3AAB3743C488DD71BD35B4335D20ACF706840F220BF267B07974E48E6E43C&key=us0', u'http_headers': {u'Accept-Language': u'en-us,en;q=0.5', u'Accept-Encoding': u'gzip, deflate', u'Accept': u'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8', u'User-Agent': u'Mozilla/5.0 (X11; Linux x86_64; rv:59.0) Gecko/20100101 Firefox/59.0', u'Accept-Charset': u'ISO-8859-1,utf-8;q=0.7,*;q=0.7', u'Cookie': 'NID=156=iHP5Vp-IhebgDeZGjJ9bCirTTsDMhyaYBU8FFkarralerWSAwQLG3xm2hHtlbzOvg86pDHlYqkwXXVOod4TQFHWIvpGN6aAdi4dUNzCTNAhP4RJeg89iSsxC-XOjT_6iqp1-kZXWNF_x3XdvK8W4rB5wN54QvYcqq2NBgqRBKok; DRIVE_STREAM=Z9Bzc1CKfCk'}, u'height': 480, u'width': 854, u'ext': u'mp4', u'format_id': u'59'}, {u'protocol': u'https', u'format': u'22 - 1280x720', u'url': u'https://r4---sn-4g5e6nss.c.docs.google.com/videoplayback?id=57e35632e6df399d&itag=22&source=webdrive&requiressl=yes&mm=30&mn=sn-4g5e6nss&ms=nxu&mv=u&pl=24&sc=yes&ttl=transient&ei=2TJCXLq4FMSjqQX3z6b4Dw&susc=dr&driveid=1kLrJQ4odoTWlNhtKTkHanUjwKeOW4tRI&app=texmex&mime=video/mp4&dur=6924.585&lmt=1547687208285348&mt=1547841575&ip=37.202.64.169&ipbits=0&expire=1547856665&cp=QVNJWUlfVVZURlhOOkM1Q2JlNURIZ0Nu&sparams=ip%2Cipbits%2Cexpire%2Cid%2Citag%2Csource%2Crequiressl%2Cmm%2Cmn%2Cms%2Cmv%2Cpl%2Csc%2Cttl%2Cei%2Csusc%2Cdriveid%2Capp%2Cmime%2Cdur%2Clmt%2Ccp&signature=0C881EAFFCFC4348BA11212D9E733482349B6C081D7F4B50E436588A3DFE0E8D.25A1B8CAE58A25899E6065178B324B0A608D78DA30292F0D4A9164486D2806C9&key=us0', u'http_headers': {u'Accept-Language': u'en-us,en;q=0.5', u'Accept-Encoding': u'gzip, deflate', u'Accept': u'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8', u'User-Agent': u'Mozilla/5.0 (X11; Linux x86_64; rv:59.0) Gecko/20100101 Firefox/59.0', u'Accept-Charset': u'ISO-8859-1,utf-8;q=0.7,*;q=0.7', u'Cookie': 'NID=156=iHP5Vp-IhebgDeZGjJ9bCirTTsDMhyaYBU8FFkarralerWSAwQLG3xm2hHtlbzOvg86pDHlYqkwXXVOod4TQFHWIvpGN6aAdi4dUNzCTNAhP4RJeg89iSsxC-XOjT_6iqp1-kZXWNF_x3XdvK8W4rB5wN54QvYcqq2NBgqRBKok; DRIVE_STREAM=Z9Bzc1CKfCk'}, u'height': 720, u'width': 1280, u'ext': u'mp4', u'format_id': u'22'}, {u'protocol': u'https', u'format': u'37 - 1920x1080', u'url': u'https://r4---sn-4g5e6nss.c.docs.google.com/videoplayback?id=57e35632e6df399d&itag=37&source=webdrive&requiressl=yes&mm=30&mn=sn-4g5e6nss&ms=nxu&mv=u&pl=24&sc=yes&ttl=transient&ei=2TJCXLq4FMSjqQX3z6b4Dw&susc=dr&driveid=1kLrJQ4odoTWlNhtKTkHanUjwKeOW4tRI&app=texmex&mime=video/mp4&dur=6924.585&lmt=1547687644376473&mt=1547841575&ip=37.202.64.169&ipbits=0&expire=1547856665&cp=QVNJWUlfVVZURlhOOkM1Q2JlNURIZ0Nu&sparams=ip%2Cipbits%2Cexpire%2Cid%2Citag%2Csource%2Crequiressl%2Cmm%2Cmn%2Cms%2Cmv%2Cpl%2Csc%2Cttl%2Cei%2Csusc%2Cdriveid%2Capp%2Cmime%2Cdur%2Clmt%2Ccp&signature=0B4A2AF50816B4B5A5CFA0D1530BAF1252E7F4FC92F11262AA72F1CDB1D0990F.89468F33FB9A7EBB9B85F11B2EE20D5E2729A633D15EB2D2E01E3892C0DC7A9F&key=us0', u'http_headers': {u'Accept-Language': u'en-us,en;q=0.5', u'Accept-Encoding': u'gzip, deflate', u'Accept': u'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8', u'User-Agent': u'Mozilla/5.0 (X11; Linux x86_64; rv:59.0) Gecko/20100101 Firefox/59.0', u'Accept-Charset': u'ISO-8859-1,utf-8;q=0.7,*;q=0.7', u'Cookie': 'NID=156=iHP5Vp-IhebgDeZGjJ9bCirTTsDMhyaYBU8FFkarralerWSAwQLG3xm2hHtlbzOvg86pDHlYqkwXXVOod4TQFHWIvpGN6aAdi4dUNzCTNAhP4RJeg89iSsxC-XOjT_6iqp1-kZXWNF_x3XdvK8W4rB5wN54QvYcqq2NBgqRBKok; DRIVE_STREAM=Z9Bzc1CKfCk'}, u'height': 1080, u'width': 1920, u'ext': u'mp4', u'format_id': u'37'}, {u'protocol': u'https', u'format': u'source - unknown', u'url': u'https://drive.google.com/uc?export=download&id=1kLrJQ4odoTWlNhtKTkHanUjwKeOW4tRI&confirm=Ol0S', u'http_headers': {u'Accept-Language': u'en-us,en;q=0.5', u'Accept-Encoding': u'gzip, deflate', u'Accept': u'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8', u'User-Agent': u'Mozilla/5.0 (X11; Linux x86_64; rv:59.0) Gecko/20100101 Firefox/59.0', u'Accept-Charset': u'ISO-8859-1,utf-8;q=0.7,*;q=0.7', u'Cookie': 'download_warning_13058876669334088843_1kLrJQ4odoTWlNhtKTkHanUjwKeOW4tRI=Ol0S; NID=156=iHP5Vp-IhebgDeZGjJ9bCirTTsDMhyaYBU8FFkarralerWSAwQLG3xm2hHtlbzOvg86pDHlYqkwXXVOod4TQFHWIvpGN6aAdi4dUNzCTNAhP4RJeg89iSsxC-XOjT_6iqp1-kZXWNF_x3XdvK8W4rB5wN54QvYcqq2NBgqRBKok'}, u'ext': u'mp4', u'format_id': u'source', u'quality': 1}], u'thumbnail': u'https://lh4.googleusercontent.com/p8w2_eqtNNTrG_XwxhzkNNUmz3bUIwJegDgE5NUzL1FGcuctmgnKYupiiOg=w1200-h630-p', u'webpage_url_basename': u'edit'}
                        for item in result['formats']:
                           
                            
                            name=item['format']
                           
                            if "source" in str(name):
                                    name="download link"
                            stream_url=item['url']+"#User-agent="+item['http_headers']['User-Agent']+'&Cookie='+item['http_headers']['Cookie']+"&Referer=https://youtube.googleapis.com"
                              
                            
                            list1.append((str(name),stream_url))

          
                                        
                            

                      except:
                           trace_error()
                           list1.append(("Error:youtube_dl",stream_url))      

                      return list1
    if urlresolver_host==True  : 

                      list1=[]   
                      print "\n\n####################urlresolver###################################################"
                      try:   
                        classname=getclass(host) 
                        txt='from urlresolver.plugins.'+host.strip()+" import " +classname.strip()+' as Resolver'
                       
                        exec(txt)                 
                       
                        resolver = Resolver()
                        print 'web_url',web_url
                        host,media_id=get_host_id(host,web_url)
                       
                        stream_url = resolver.get_media_url(host, media_id)
                        print 'stream_url',stream_url
                        if stream_url and  type(stream_url)==type([]):
                            if len(stream_url)==0:                  
                                      
                                       return "Error:Link is not available"
                                   
                            for item in stream_url:
                                        list1.append((item[0],item[1]))
                                       
                                        
                            
                        elif stream_url and not type(stream_url)==type([]):

                            if stream_url.strip()=='':
                               host="Error:invalid link" 
                            
                            list1.append((host,stream_url))
                        else:
                            if not stream_url or stream_url=='':
                                host="Error:invalid link"

                            
                            list1.append((host,stream_url))
                      except:
                           trace_error()
                           list1.append(("Error:invalid link",stream_url))
                               
                      return list1


                    
    if  pelisresolver_host==True  :
         
                      print "\n\n####################pelisresolver###################################################"
 
                      try:   
                        print 'web_url',web_url
                        exec('from urlresolver.servers.'+host.strip()+" import get_video_url")
                        
                        stream_url = get_video_url(web_url)
                        print 'stream_url',stream_url
                        if stream_url and  type(stream_url)==type([]):
                            if len(stream_url)==0:                  
                                      
                                       return "Error:Link is not available"
                                   
                            for item in stream_url:
                                        list1.append(('Error:invalid link'+"-"+item[0],item[1]))
                                       
                                        
                            
                        elif stream_url and not type(stream_url)==type([]):
                            if stream_url.strip()=='':
                               host="Error:invalid link" 
                            list1.append((host,stream_url))
                        else:
                            if not stream_url or stream_url=='':
                                host="Error:invalid link"
                            
                            list1.append((host,stream_url))
                      except:
                           trace_error()
                           list1.append(('Error:invalid link',stream_url))
                      return list1         
           

                  
    if  tsresolver_host==True  :
         
             

                      print "\n\n####################tsresolver###################################################"
 
                      try:   
                        print 'web_url',web_url
                                                
                        exec('from urlresolver.hosts.'+host.strip()+" import get_video_url")
                        
                        stream_url = get_video_url(web_url)
                        print 'stream_url',stream_url
                        if stream_url and  type(stream_url)==type([]):
                            if len(stream_url)==0:                  
                                      
                                       return "Error:Link is not available"
                                   
                            for item in stream_url:
                                        list1.append((item[0],item[1]))
                                       
                                        
                            
                        elif stream_url and not type(stream_url)==type([]):
                            if stream_url.strip()=='':
                               host="Error:invalid link" 
                            
                            list1.append((host,stream_url))
                        else:
                            if not stream_url or stream_url=='':
                                host="Error:invalid link"
                            list1.append((host,stream_url))
                      except:
                           trace_error()
                           list1.append(('Error:invalid link',stream_url))
                      return list1         
            
            

                
    if  e2ipresolver_host==True  :
         
                  
                      print "\n\n####################e2iplayer-resolver###################################################"
                      list1=[]
                      try:   
                        
                        from IPTVPlayer.libs.urlparser import urlparser
                        
                        up=urlparser()
                        stream_url=up.getVideoLinkExt(web_url)
                       
                        if stream_url and  type(stream_url)==type([]):
                            if len(stream_url)==0:                  
                                      
                                       return "Error:Link is not available"
                                   
                            for item in stream_url:
                                        list1.append((item['name'],item['url']))
                                       
                                        
                            
                        elif stream_url and not type(stream_url)==type([]):
                            list1.append((host,stream_url))
                        else:
                            list1.append((host,stream_url))
                      except:
                           trace_error()
                           list1.append(('Error:invalid link',stream_url))                    
                      
                      return list1
   
    if  youtube_dl_host==True  :
         

                      print "\n\n####################youtube_dl###################################################"
 
                     
 
                      try:   
                        print 'web_url',web_url
                        import youtube_dl
                        
                        ydl = youtube_dl.YoutubeDL({'nocheckcertificate': True})
                        with ydl:
                            result = ydl.extract_info(
                                web_url,
                                download=False # We just want to extract the info
                            )
                                               
                        #result={u'display_id': u'1kLrJQ4odoTWlNhtKTkHanUjwKeOW4tRI', u'extractor': u'GoogleDrive', u'automatic_captions': {}, u'protocol': u'https', u'format': u'source - unknown', u'requested_subtitles': None, u'duration': 6924, u'format_id': u'source', u'quality': 1, u'id': u'1kLrJQ4odoTWlNhtKTkHanUjwKeOW4tRI', u'subtitles': {}, u'playlist': None, u'thumbnails': [{u'url': u'https://lh4.googleusercontent.com/p8w2_eqtNNTrG_XwxhzkNNUmz3bUIwJegDgE5NUzL1FGcuctmgnKYupiiOg=w1200-h630-p', u'id': u'0'}], u'title': u'The.Girl.in.the.Spiders.Web.2019.1080p.WEB-DL.mp4', u'url': u'https://drive.google.com/uc?export=download&id=1kLrJQ4odoTWlNhtKTkHanUjwKeOW4tRI&confirm=Ol0S', u'extractor_key': u'GoogleDrive', u'http_headers': {u'Accept-Language': u'en-us,en;q=0.5', u'Accept-Encoding': u'gzip, deflate', u'Accept': u'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8', u'User-Agent': u'Mozilla/5.0 (X11; Linux x86_64; rv:59.0) Gecko/20100101 Firefox/59.0', u'Accept-Charset': u'ISO-8859-1,utf-8;q=0.7,*;q=0.7', u'Cookie': 'download_warning_13058876669334088843_1kLrJQ4odoTWlNhtKTkHanUjwKeOW4tRI=Ol0S; NID=156=iHP5Vp-IhebgDeZGjJ9bCirTTsDMhyaYBU8FFkarralerWSAwQLG3xm2hHtlbzOvg86pDHlYqkwXXVOod4TQFHWIvpGN6aAdi4dUNzCTNAhP4RJeg89iSsxC-XOjT_6iqp1-kZXWNF_x3XdvK8W4rB5wN54QvYcqq2NBgqRBKok'}, u'playlist_index': None, u'ext': u'mp4', u'webpage_url': 'https://drive.google.com/file/d/1kLrJQ4odoTWlNhtKTkHanUjwKeOW4tRI/edit', u'formats': [{u'protocol': u'https', u'format': u'18 - 640x360', u'url': u'https://r4---sn-4g5e6nss.c.docs.google.com/videoplayback?id=57e35632e6df399d&itag=18&source=webdrive&requiressl=yes&mm=30&mn=sn-4g5e6nss&ms=nxu&mv=u&pl=24&sc=yes&ttl=transient&ei=2TJCXLq4FMSjqQX3z6b4Dw&susc=dr&driveid=1kLrJQ4odoTWlNhtKTkHanUjwKeOW4tRI&app=texmex&mime=video/mp4&dur=6924.585&lmt=1547687010977570&mt=1547841575&ip=37.202.64.169&ipbits=0&expire=1547856665&cp=QVNJWUlfVVZURlhOOkM1Q2JlNURIZ0Nu&sparams=ip%2Cipbits%2Cexpire%2Cid%2Citag%2Csource%2Crequiressl%2Cmm%2Cmn%2Cms%2Cmv%2Cpl%2Csc%2Cttl%2Cei%2Csusc%2Cdriveid%2Capp%2Cmime%2Cdur%2Clmt%2Ccp&signature=7F89467631A01321BEEAFF742D2E5FA5F2ED463C2D7D45EA630B4D775639150F.5554DF8AADBD8B7F39CA29AFD193D0D5577AB31450CE05E74262F5270CE4D8D9&key=us0', u'http_headers': {u'Accept-Language': u'en-us,en;q=0.5', u'Accept-Encoding': u'gzip, deflate', u'Accept': u'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8', u'User-Agent': u'Mozilla/5.0 (X11; Linux x86_64; rv:59.0) Gecko/20100101 Firefox/59.0', u'Accept-Charset': u'ISO-8859-1,utf-8;q=0.7,*;q=0.7', u'Cookie': 'NID=156=iHP5Vp-IhebgDeZGjJ9bCirTTsDMhyaYBU8FFkarralerWSAwQLG3xm2hHtlbzOvg86pDHlYqkwXXVOod4TQFHWIvpGN6aAdi4dUNzCTNAhP4RJeg89iSsxC-XOjT_6iqp1-kZXWNF_x3XdvK8W4rB5wN54QvYcqq2NBgqRBKok; DRIVE_STREAM=Z9Bzc1CKfCk'}, u'height': 360, u'width': 640, u'ext': u'mp4', u'format_id': u'18'}, {u'protocol': u'https', u'format': u'59 - 854x480', u'url': u'https://r4---sn-4g5e6nss.c.docs.google.com/videoplayback?id=57e35632e6df399d&itag=59&source=webdrive&requiressl=yes&mm=30&mn=sn-4g5e6nss&ms=nxu&mv=u&pl=24&sc=yes&ttl=transient&ei=2TJCXLq4FMSjqQX3z6b4Dw&susc=dr&driveid=1kLrJQ4odoTWlNhtKTkHanUjwKeOW4tRI&app=texmex&mime=video/mp4&dur=6924.585&lmt=1547687281756210&mt=1547841575&ip=37.202.64.169&ipbits=0&expire=1547856665&cp=QVNJWUlfVVZURlhOOkM1Q2JlNURIZ0Nu&sparams=ip%2Cipbits%2Cexpire%2Cid%2Citag%2Csource%2Crequiressl%2Cmm%2Cmn%2Cms%2Cmv%2Cpl%2Csc%2Cttl%2Cei%2Csusc%2Cdriveid%2Capp%2Cmime%2Cdur%2Clmt%2Ccp&signature=2A13F7DBF193FCFAFDAB3B9F89C24EF80D4B51A6D9E76E0F576312ED36C34095.47E3AAB3743C488DD71BD35B4335D20ACF706840F220BF267B07974E48E6E43C&key=us0', u'http_headers': {u'Accept-Language': u'en-us,en;q=0.5', u'Accept-Encoding': u'gzip, deflate', u'Accept': u'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8', u'User-Agent': u'Mozilla/5.0 (X11; Linux x86_64; rv:59.0) Gecko/20100101 Firefox/59.0', u'Accept-Charset': u'ISO-8859-1,utf-8;q=0.7,*;q=0.7', u'Cookie': 'NID=156=iHP5Vp-IhebgDeZGjJ9bCirTTsDMhyaYBU8FFkarralerWSAwQLG3xm2hHtlbzOvg86pDHlYqkwXXVOod4TQFHWIvpGN6aAdi4dUNzCTNAhP4RJeg89iSsxC-XOjT_6iqp1-kZXWNF_x3XdvK8W4rB5wN54QvYcqq2NBgqRBKok; DRIVE_STREAM=Z9Bzc1CKfCk'}, u'height': 480, u'width': 854, u'ext': u'mp4', u'format_id': u'59'}, {u'protocol': u'https', u'format': u'22 - 1280x720', u'url': u'https://r4---sn-4g5e6nss.c.docs.google.com/videoplayback?id=57e35632e6df399d&itag=22&source=webdrive&requiressl=yes&mm=30&mn=sn-4g5e6nss&ms=nxu&mv=u&pl=24&sc=yes&ttl=transient&ei=2TJCXLq4FMSjqQX3z6b4Dw&susc=dr&driveid=1kLrJQ4odoTWlNhtKTkHanUjwKeOW4tRI&app=texmex&mime=video/mp4&dur=6924.585&lmt=1547687208285348&mt=1547841575&ip=37.202.64.169&ipbits=0&expire=1547856665&cp=QVNJWUlfVVZURlhOOkM1Q2JlNURIZ0Nu&sparams=ip%2Cipbits%2Cexpire%2Cid%2Citag%2Csource%2Crequiressl%2Cmm%2Cmn%2Cms%2Cmv%2Cpl%2Csc%2Cttl%2Cei%2Csusc%2Cdriveid%2Capp%2Cmime%2Cdur%2Clmt%2Ccp&signature=0C881EAFFCFC4348BA11212D9E733482349B6C081D7F4B50E436588A3DFE0E8D.25A1B8CAE58A25899E6065178B324B0A608D78DA30292F0D4A9164486D2806C9&key=us0', u'http_headers': {u'Accept-Language': u'en-us,en;q=0.5', u'Accept-Encoding': u'gzip, deflate', u'Accept': u'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8', u'User-Agent': u'Mozilla/5.0 (X11; Linux x86_64; rv:59.0) Gecko/20100101 Firefox/59.0', u'Accept-Charset': u'ISO-8859-1,utf-8;q=0.7,*;q=0.7', u'Cookie': 'NID=156=iHP5Vp-IhebgDeZGjJ9bCirTTsDMhyaYBU8FFkarralerWSAwQLG3xm2hHtlbzOvg86pDHlYqkwXXVOod4TQFHWIvpGN6aAdi4dUNzCTNAhP4RJeg89iSsxC-XOjT_6iqp1-kZXWNF_x3XdvK8W4rB5wN54QvYcqq2NBgqRBKok; DRIVE_STREAM=Z9Bzc1CKfCk'}, u'height': 720, u'width': 1280, u'ext': u'mp4', u'format_id': u'22'}, {u'protocol': u'https', u'format': u'37 - 1920x1080', u'url': u'https://r4---sn-4g5e6nss.c.docs.google.com/videoplayback?id=57e35632e6df399d&itag=37&source=webdrive&requiressl=yes&mm=30&mn=sn-4g5e6nss&ms=nxu&mv=u&pl=24&sc=yes&ttl=transient&ei=2TJCXLq4FMSjqQX3z6b4Dw&susc=dr&driveid=1kLrJQ4odoTWlNhtKTkHanUjwKeOW4tRI&app=texmex&mime=video/mp4&dur=6924.585&lmt=1547687644376473&mt=1547841575&ip=37.202.64.169&ipbits=0&expire=1547856665&cp=QVNJWUlfVVZURlhOOkM1Q2JlNURIZ0Nu&sparams=ip%2Cipbits%2Cexpire%2Cid%2Citag%2Csource%2Crequiressl%2Cmm%2Cmn%2Cms%2Cmv%2Cpl%2Csc%2Cttl%2Cei%2Csusc%2Cdriveid%2Capp%2Cmime%2Cdur%2Clmt%2Ccp&signature=0B4A2AF50816B4B5A5CFA0D1530BAF1252E7F4FC92F11262AA72F1CDB1D0990F.89468F33FB9A7EBB9B85F11B2EE20D5E2729A633D15EB2D2E01E3892C0DC7A9F&key=us0', u'http_headers': {u'Accept-Language': u'en-us,en;q=0.5', u'Accept-Encoding': u'gzip, deflate', u'Accept': u'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8', u'User-Agent': u'Mozilla/5.0 (X11; Linux x86_64; rv:59.0) Gecko/20100101 Firefox/59.0', u'Accept-Charset': u'ISO-8859-1,utf-8;q=0.7,*;q=0.7', u'Cookie': 'NID=156=iHP5Vp-IhebgDeZGjJ9bCirTTsDMhyaYBU8FFkarralerWSAwQLG3xm2hHtlbzOvg86pDHlYqkwXXVOod4TQFHWIvpGN6aAdi4dUNzCTNAhP4RJeg89iSsxC-XOjT_6iqp1-kZXWNF_x3XdvK8W4rB5wN54QvYcqq2NBgqRBKok; DRIVE_STREAM=Z9Bzc1CKfCk'}, u'height': 1080, u'width': 1920, u'ext': u'mp4', u'format_id': u'37'}, {u'protocol': u'https', u'format': u'source - unknown', u'url': u'https://drive.google.com/uc?export=download&id=1kLrJQ4odoTWlNhtKTkHanUjwKeOW4tRI&confirm=Ol0S', u'http_headers': {u'Accept-Language': u'en-us,en;q=0.5', u'Accept-Encoding': u'gzip, deflate', u'Accept': u'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8', u'User-Agent': u'Mozilla/5.0 (X11; Linux x86_64; rv:59.0) Gecko/20100101 Firefox/59.0', u'Accept-Charset': u'ISO-8859-1,utf-8;q=0.7,*;q=0.7', u'Cookie': 'download_warning_13058876669334088843_1kLrJQ4odoTWlNhtKTkHanUjwKeOW4tRI=Ol0S; NID=156=iHP5Vp-IhebgDeZGjJ9bCirTTsDMhyaYBU8FFkarralerWSAwQLG3xm2hHtlbzOvg86pDHlYqkwXXVOod4TQFHWIvpGN6aAdi4dUNzCTNAhP4RJeg89iSsxC-XOjT_6iqp1-kZXWNF_x3XdvK8W4rB5wN54QvYcqq2NBgqRBKok'}, u'ext': u'mp4', u'format_id': u'source', u'quality': 1}], u'thumbnail': u'https://lh4.googleusercontent.com/p8w2_eqtNNTrG_XwxhzkNNUmz3bUIwJegDgE5NUzL1FGcuctmgnKYupiiOg=w1200-h630-p', u'webpage_url_basename': u'edit'}
                        for item in result['formats']:
                           
                            
                            name=item['format']
                           
                            if "source" in str(name):
                                    name="download link"
                            stream_url=item['url']+"#User-agent="+item['http_headers']['User-Agent']+'&Cookie='+item['http_headers']['Cookie']+"&Referer=https://youtube.googleapis.com"
                              
                            
                            list1.append((str(name),stream_url))

          
                                        
                            

                      except:
                           trace_error()
                           list1.append(('Error:invalid link',stream_url))       
       

                      return list1
