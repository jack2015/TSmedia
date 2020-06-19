## Embedded file name: /usr/lib/enigma2/python/Plugins/Extensions/TSmedia/scripts/script.module.main/lib/xbmctools.py
import sys
import os
import urllib
import urllib2
import ssl
import re,ast,json
from urlparse import parse_qs, urlparse
import xbmc,xbmcplugin
from iTools import getimage_basename,AppPath
plugin_path='/usr/lib/enigma2/python/Plugins/Extensions/TSmedia/'
extra={"rating":"","year":"","quality":"","year":"","duration":"","pg":"","language":"","subtitle":"","imdb_id":""}
data_file="/tmp/TSmedia/data.json"
try:
    import requests
except:
    pass

def logtmpdata(label_name = '', data = None):
    return
    try:
        data=str(data)
        
        
        fp = open('/tmp/tmp.log', 'a')
        fp.write('\n' + str(label_name) + ': ' + data)
        fp.close()
    except:
        pass
def colorize(txt,color='default',marker1="(",marker2=")"):

         if getos()=="windows":
            return txt
        
         ##\c007?7?7? grey
         ##'\c0000??00 green
         ##"\c00????00" yellow
         ##"\c0??????" white
         
         if color=="default":
            color='\c0000????' 
         elif color=="green":
            color='\c0000??00'
         elif color=='ivory':   
            color="\c0???????"
         elif color=='yellow':
            color="\c00????00"
         else:
             color='\c0000????'
            
         
         if True:
            if not marker1 in txt :
                return txt
            txtparts=txt.split(marker1)
            txt1=txtparts[0]
            txt2=txtparts[1]
            if marker2 in txt:
                txt3=txt2.split(marker2)[0]
            else:
                txt3=txt2 
            
            ftxt=txt1+" "+color+marker1+txt3+marker2
            
            return ftxt
         else:
             trace_error()
             return txt
def getmetadata(imdb_id):
           try:
               
                from Plugins.Extensions.TSmedia.screens.imdb import getTmdbMovie
                dic = getTmdbMovie(imdb_id)
                
                return dic
           except:
               trace_error()
               return {}

def convert_vtt2srt(vttfile):
    from vtt2srt.vtt2srt import convertVTTtoSRT
    try:
        srt_file=convertVTTtoSRT(vttfile)
        return srt_file
    except:
        trace_error()
        return None
def downloadfile(url = None,basename=''):
    import requests
    ofile=None
    if basename=='':
       basename=os.path.basename(url)
       print 'basename',basename
      
    if url is None or url.strip() == '':
        return None
    else:
        
        if os.name == 'nt':
            path = 'd:/tmp'
        else:
            path = '/media/hdd'
        if url and url.startswith('http'):
            try:
                
                ofile = os.path.join(path, basename)
                
                r = requests.get(url, timeout=0.5,verify=False)
                if r.status_code == 200:
                    with open(ofile, 'wb') as f:
                        f.write(r.content)
                    f.close()
                    return ofile
            except:
                ofile=None
                trace_error()

        return ofile  
def getmainitem_image():
    try:
        imagefile='/tmp/TSmedia/mimage'
        image=open(imagefile).read()
        return image

    except:
        return ''
def getdebug_mode():
    debugmode='user'
    debugmode_file = '/tmp/TSmedia/debugmode'
    if os.path.exists(debugmode_file):
        try:
            debugmode = open(debugmode_file).read()
            return debugmode
        except:
            pass
    else:
        return debugmode
    return debugmode
def getpage(url):
    import Queue
    import threading
    import urllib2

    # called by each thread
    def get_url(q, url):
        q.put(getnet(url))

    #theurls = ["http://google.com", "http://yahoo.com"]

    q = Queue.Queue()

    if True:
        t = threading.Thread(target=get_url, args = (q,url))
        t.daemon = False
        t.start()

    s = q.get()
    return s
def decodeHtmlentities(string):
    string = entitiesfix(string)
    entity_re = re.compile("&(#?)(\d{1,5}|\w{1,8});")

    def substitute_entity(match):
        from htmlentitydefs import name2codepoint as n2cp
        ent = match.group(2)
        if match.group(1) == "#":
            return unichr(int(ent)).encode('utf-8')
        else:
            cp = n2cp.get(ent)

            if cp:
                return unichr(cp).encode('utf-8')
            else:
                return match.group()

    return entity_re.subn(substitute_entity, string)[0]
def getos():
    if __file__.startswith('/usr'):
        return 'enigma2'
    else:
        return 'windows'

datasearch_file="/tmp/TSmedia/datasearch"
def get_youtube_link(value):
    """
    Examples:
    - http://youtu.be/SA2iWivDJiE
    - http://www.youtube.com/watch?v=_oPAwA_Udwc&feature=feedu
    - http://www.youtube.com/embed/SA2iWivDJiE
    - http://www.youtube.com/v/SA2iWivDJiE?version=3&amp;hl=en_US
    -'plugin://plugin.video.youtube/?action=play_video&amp;videoid=FBBLhRgrw0o'
    """
    from urlparse import urlparse
    vid = None
    if value is None:
        return
    else:
        value = value.strip()
        if value.startswith('plugin://'):
            try:
                vid = value.split('=')[value.count('=')]
            except:
                return

        else:
            query = urlparse(value)
            if query.hostname == 'youtu.be':
                vid = query.path[1:]
            elif query.hostname in ('www.youtube.com', 'youtube.com'):
                if query.path == '/watch':
                    p = parse_qs(query.query)
                    vid = p['v'][0]
                if query.path[:7] == '/embed/':
                    vid = query.path.split('/')[2]
                if query.path[:3] == '/v/':
                    vid = query.path.split('/')[2]
                    
        if vid is not None:            
           return 'plugin://plugin.video.youtube/?action=play_video&videoid=%s' % vid
        else:
           return


def extractdata(data, marker1, marker2, withMarkers = False, caseSensitive = True):
    if caseSensitive:
        idx1 = data.find(marker1)
    else:
        idx1 = data.lower().find(marker1.lower())
    if -1 == idx1:
        idx1 = 0
    if caseSensitive:
        idx2 = data.find(marker2, idx1 + len(marker1))
    else:
        idx2 = data.lower().find(marker2.lower(), idx1 + len(marker1))
    if -1 == idx2:
        idx2 = len(data) - 1
    if withMarkers:
        idx2 = idx2 + len(marker2)
    else:
        idx1 = idx1 + len(marker1)
    return data[idx1:idx2]


def cleanparam(param):
    param = param.strip()
    if '&' in param and ';' in param:
        sdata = finddata(param, '&', ';', True)
        if not sdata.strip() == '':
            param = param.replace(sdata, '')
          
            if '&' in param and ';' in param:
                param = cleanparam(param)
    return param


def geturlbyreferal(url, referer):
    request2 = urllib2.Request(url)
    request2.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36')
    request2.add_header('Referer', referer)
    request2.add_header('Accept', 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8')
    request2.add_header('Accept-Language', 'de,en-US;q=0.7,en;q=0.3')
    response2 = urllib2.urlopen(request2)


def findalldata(data, marker1, marker2, index = 0, fdata = []):
    
    data = data[index:len(data)]
    idx1 = data.find(marker1)
    if -1 == idx1:
        return fdata
    idx2 = data.find(marker2, idx1 + len(marker1))
    if -1 == idx2:
        return fdata
    idx1 = idx1 + len(marker1)
    fdata.append(data[idx1:idx2])
    findalldata(data, marker1, marker2, idx2 + len(marker2), fdata)


def cfdownloadImage(url = None,images_chachepath=None,localfile=None):
    ofile=''

    if url is None or url.strip() == '':
        return ''
    else:
        if 'ExQ' in url:
            url.replace('ExQ', '=')
        if getos() == 'windows':
            path = 'd:\\tmp'
        else:
            path = images_chachepath
         
        if url and url.startswith('http'):
            try:
                if localfile is None:
                    filename = url.split('/')[-1]
                    ofile = os.path.join(path, filename)

                else:
                    ofile=localfile
                if os.path.exists(ofile):
                    return ofile
                try:
                    r = cfresolve(url)
                    with open(ofile, 'wb') as f:
                        f.write(r)
                    f.close()
                    return ofile
                except:
                    pass

            except:
                trace_error()

        return ofile
        return


def downloadImage(url = None,images_chachepath=None,localfile=None):
    ofile=True

    if url is None or url.strip() == '':
        return ''
    else:
        if 'ExQ' in url:
            url.replace('ExQ', '=')
        if getos() == 'windows':
            path = 'd:\\tmp'
        else:
            path = images_chachepath
       
       
        if url and url.startswith('http'):
            try:
                if localfile is None:
                    filename = url.split('/')[-1]
                    ofile = os.path.join(path, filename)

                else:
                    ofile=localfile

                if os.path.exists(ofile):
                     
                    return ofile
                r = requests.get(url, timeout=0.5,verify=False)
                if r.status_code == 200:
                    with open(ofile, 'wb') as f:
                        f.write(r.content)
                    f.close()
                    
                    return ofile
            except:
                trace_error()
            
        return ofile
        return


def getitems(regx, data):
    items = re.findall(regx, data, re.M | re.I)
    return items


def finditem(text, from_string, to_string, excluding = True):
    import re
    import string
    if excluding:
        try:
            r = re.search('(?i)' + from_string + '([\\S\\s]+?)' + to_string, text).group(1)
        except:
            r = ''

    else:
        try:
            r = re.search('(?i)(' + from_string + '[\\S\\s]+?' + to_string + ')', text).group(1)
        except:
            r = ''

    return r


def finditems(text, start_with, end_with):
    import re
    r = re.findall('(?i)(' + start_with + '[\\S\\s]+?' + end_with + ')', text)
    return r


def removeunicode(data):
    try:
        try:
            data = data.encode('utf', 'ignore')
        except:
            pass

        data = data.decode('unicode_escape').encode('ascii', 'replace').replace('?', '').strip()
    except:
        pass

    return data


def readhttps(url):


    list1 = []
    try:
        req = urllib2.Request(url)
        try:
            response = urllib2.urlopen(req, context=ssl._create_unverified_context())
        except:
            response = urllib2.urlopen(req)

        data = response.read()
        response.close()
        return data
    except urllib2.URLError as e:
        trace_error()
        if hasattr(e, 'code'):
            print 'We failed with error code - %s.' % e.code
            if '401' in str(e.code):
                trace_error()
                return None
            if '404' in str(e.code):
                trace_error()
                return None
            if '400' in str(e.code):
                trace_error()
                return None
            if '403' in str(e.code):
                trace_error()
                return None
        elif hasattr(e, 'reason'):
                trace_error()
                return None
        


def requestsurl(url):
    
    try:
        import requests
        session = requests.Session()
        USER_AGENT = 'Mozilla/5.0 (X11; Ubuntu; Linux i686; rv:30.0) Gecko/20100101 Firefox/30.0'
        session.headers.update({'User-Agent': USER_AGENT})
        return session.get(url, verify=False).content
    except:

     
                trace_error()
                return None


def readtrueurl(url):
    hdr = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
     'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
     'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
     'Accept-Encoding': 'none',
     'Accept-Language': 'en-US,en;q=0.8',
     'Connection': 'keep-alive'}
    req = urllib2.Request(url, headers=hdr)
    page = urllib2.urlopen(req)
    url = page.geturl()
    return url


def logdata(label_name = '', data = None):
    try:
        data=str(data)
        data=data.replace('AxNxD', '&').replace('ExQ', '=')
        data = urllib.unquote_plus(data)   
        caller_name = getcaller_name()
        fp = open('/tmp/TSmedia_log', 'a')
        fp.write('\n' + caller_name + ':' + str(label_name) + ': ' + data)
        fp.close()
    except:
        pass
def deldata():
    try:
        if os.path.exists('/tmp/TSmedia/data.txt'):
            os.remove('/tmp/TSmedia/data.txt')
        if os.path.exists('/tmp/TSmedia_log'):
            os.remove('/tmp/TSmedia_log')

            
    except:
        pass

def getcaller_name():
    try:
        import inspect
        import os
        frame = inspect.currentframe()
        frame = frame.f_back.f_back
        code = frame.f_code
        calling_module = os.path.basename(code.co_filename)
        return calling_module
    except:
        return ''


def trace_error():
    import sys
    import traceback
    try:
        #traceback.print_exc(file=sys.stdout)
        if os.path.exists('/tmp/TSmedia_log'):
            logfile = '/tmp/TSmedia_log'
        else:
            return
        traceback.print_exc(file=open(logfile, 'a'))
    except:
        pass

def getData(url, data = {}, host = '', Referer = ''):
    import requests
    headers = {'Host': host,
     'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; rv:56.0) Gecko/20100101 Firefox/56.0',
     'Accept': '*/*',
     'Accept-Language': 'fr,fr-FR;q=0.8,en-US;q=0.5,en;q=0.3',
     'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
     'X-Requested-With': 'XMLHttpRequest',
     'Referer': Referer,
     'Connection': 'keep-alive'}
    s = requests.Session()
    r = s.get(url, headers=headers,verify=False)
    htmldata = r.content
    return htmldata


def postData(url, data, host, Referer):
    import requests
    headers = {'Host': host,
     'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; rv:56.0) Gecko/20100101 Firefox/56.0',
     'Accept': '*/*',
     'Accept-Language': 'fr,fr-FR;q=0.8,en-US;q=0.5,en;q=0.3',
     'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
     'X-Requested-With': 'XMLHttpRequest',
     'Referer': Referer,
     'Connection': 'keep-alive'}
    s = requests.Session()
    r = s.post(url, headers=headers, data=data,verify=False)
    htmldata = r.content
    return htmldata


def getItems(data, pattern, ignoreCase = False):
    if ignoreCase:
        match = re.findall(pattern, data, re.IGNORECASE)
    else:
        match = re.findall(pattern, data)
    return match


def getGroups(data, pattern, grupsNum = 1, ignoreCase = False):
    tab = []
    if ignoreCase:
        match = re.search(pattern, data, re.IGNORECASE)
    else:
        match = re.search(pattern, data)
    for idx in range(grupsNum):
        try:
            value = match.group(idx + 1)
        except:
            value = ''

        tab.append(value)

    return tab


def getBaseUrl(url):
    from urlparse import urlparse
    parsed_uri = urlparse(url)
    domain = '{uri.scheme}://{uri.netloc}/'.format(uri=parsed_uri)
    return domain

def getimage(server=None):
    
    if server is None:
       return plugin_path+"/interface/servers/server.png"
    image=plugin_path+"/interface/servers/"+server+".png"
    if os.path.exists(image):
         return image
    else:
         return plugin_path+"/interface/servers/server.png"
        
def getserver_image(server=None):
    #img=getmainitem_image()
    server=server.lower()
    if server is None :
              return plugin_path+"/interface/servers/server.png"
        
   
    else: 
          image=plugin_path+"/interface/servers/"+server+".png"
          if os.path.exists(image):
              return image
          else:  
              return plugin_path+"/interface/servers/server.png"
    
    
    
                
def getmainTitle():
    try:
        mtitle=open("/tmp/TSmedia/mtitle").read()
        return mtitle
    except:
        return ''
def playlink(item=None,name='',url=''):

    if type(item) is str:
        url=item  
    if name=='':
           name='play'
    if "plugin.youtube" in url:
        stream_link=get_youtube_link(url)
    else:
        stream_link=url
   
 

    if stream_link.startswith("Error"):
       addDir(stream_link,stream_link,-1,"",name,1)
       return
        
    if stream_link==None :
        addDir("Error:invalid stream_link","Error:invalid stream_link",-1,"",name,1)
        return
              
    maintitle=getmainTitle()
    if not maintitle=='':
                name=maintitle+"-"+name
                name=name.replace(".","-")   
    addDir(name,stream_link,0,'',name,1,link=True)
def resolvehost(item=None,name=None,url=None):
    
    if type(item) is str:
        url=item
        
        resolvehost2(url)
        return
    else:    
       addDir=item.addDir
       endDir=item.endDir    
    from urlresolver import resolve
    if name=='':
           name='play'
    if "youtube" in url:
        stream_link=get_youtube_link(url)
    else:    
        stream_link=resolve(url)
    
    print  'stream_link',stream_link

    if not stream_link :
        addDir("Error:invalid stream_link","Error:invalid stream_link",-1,"",name,1)
        return
    
    if  type(stream_link)==type([]):
      
       
       for ditem in stream_link:

           
           name=str(ditem[0])
           url=str(ditem[1])
           addDir(name,url,0,"",name,1,link=True)
       return  

    if stream_link.startswith("Error"):
       addDir(stream_link,stream_link,-1,"",name,1)
       return
        
    
    try:addDir(name,stream_link,0,'',name,1)
    except: trace_error()
    return stream_link	            	       
def resolvehost2(url):
  
    from urlresolver import resolve
    
    name='play'
    if "youtube" in url:
        stream_link=get_youtube_link(url)
    else:    
        stream_link=resolve(url)
    if not stream_link :
        addDir("Error:invalid stream_link","Error:invalid stream_link",-1,"",name,1)
        return    

    if type(stream_link)==type([]):
       
       for ditem in stream_link:

           #maintitle=getmainTitle()
           name=ditem[0]
           url=ditem[1]
           addDir(name,url,0,"",name,1,link=True)
           return
      


        

        
 
    if stream_link.startswith("Error"):
       addDir(stream_link,stream_link,-1,"",name,1)
       return
              
    
    addDir(name,stream_link,0,'',name,1,link=True)
    
    	            	       
def resolvehost2(url):
  
    from urlresolver import resolve
    
    name='play'
    if "youtube" in url:
        stream_link=get_youtube_link(url)
    else:    
        stream_link=resolve(url)
    if not stream_link :
        addDir("Error:invalid stream_link","Error:invalid stream_link",-1,"",name,1)
        return    

    if type(stream_link)==type([]):
       
       for ditem in stream_link:

           #maintitle=getmainTitle()
           name=ditem[0]
           url=ditem[1]
           addDir(name,url,0,"",name,1,link=True)
           return
      


        

        
 
    if stream_link.startswith("Error"):
       addDir(stream_link,stream_link,-1,"",name,1)
       return
              
    
    addDir(name,stream_link,0,'',name,1,link=True)
    
            	    
    
def readnet(url,start=None,end=None,split=None,cloudflare=False,http=False):

    
    if cloudflare or http==True:
        from core.httptools import downloadpage
        try:
            data= downloadpage(url,bypass_cloudflare=cloudflare).data
       
        except:
            
           logdata("download error-http",data)

        

    else:
        data=getnet(url,bypass_cloudflare=cloudflare)
        if data is None:
           data=requestsurl(url) 
           
    if not data or data.strip()=='':
        logdata("download error","download error")
        return None
    
 
    
    if start and end:
        data=extractdata(data,start,end)
    if split:
        try:
            blocks=data.split(split)
            if blocks[0]==data:
              
               return None
            
        except:
            trace_error()
            
            blocks=[]
        return blocks
    return data    


def getnet(url,bypass_cloudflare=False):
    try:
        logdata('url',url)
        from addon.common.net import Net
        net = Net()
        USER_AGENT = 'Mozilla/5.0 (X11; Ubuntu; Linux i686; rv:30.0) Gecko/20100101 Firefox/30.0'
        MAX_TRIES = 3
        headers = {'User-Agent': USER_AGENT,
         'Referer': url}
        try:
            data = net.http_GET(url).content
        except:
            logdata('getnet',"download error")
            data=requestsurl(url)
            if data is None:
                logdata('requests',"error")
        try:data=data.encode('utf-8',"ignore")
        except:pass
        if not data:
            return None
    
      
        return data
    except:
        trace_error()
        return None

    return None


def postnet(url, data, referer):
    try:
        from addon.common.net import Net
        net = Net()
        USER_AGENT = 'Mozilla/5.0 (X11; Ubuntu; Linux i686; rv:30.0) Gecko/20100101 Firefox/30.0'
        MAX_TRIES = 3
        headers = {'User-Agent': USER_AGENT,
         'Referer': referer}
        html = net.http_POST(url, form_data=data, headers=headers).content
        return html
    except:
        trace_error()


def readurl(url):
 
    try:
        req = urllib2.Request(url)
        response = urllib2.urlopen(req)
        data = response.read()
        response.close()
        return data
    except urllib2.URLError as e:
        if hasattr(e, 'code'):
            print 'We failed with error code - %s.' % e.code
            trace_error()
            return None
        elif hasattr(e, 'reason'):
            print 'We failed to reach a server.'
            trace_error()
            return None

        return endDir()
def trueUrl(site):
    hdr = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
     'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
     'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
     'Accept-Encoding': 'none',
     'Accept-Language': 'en-US,en;q=0.8',
     'Connection': 'keep-alive'}
    req = urllib2.Request(site, headers=hdr)
    page = urllib2.urlopen(req)
    url = page.geturl()
    return url


def readurlwithhost(url, host):
    try:
        req = urllib2.Request(url)
        req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
        req.add_header('Host', host)
        req.add_header('Accept', 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8')
        req.add_header('Cookie', 'popNum=8; __atuvc=6%7C34%2C3%7C35; popundr=1; PHPSESSID=478ff84e532ad811df5d63854f4f0fe1; watched_video_list=MTgzNDY%3D')
        response = urllib2.urlopen(req)
        link = response.read()
        return link
    except Exception:
            trace_error()
            return None

def getsearchtext(marker = '+'):
        import os
        if os.path.exists('/tmp/TSmedia/searchSTR'):
            file = open('/tmp/TSmedia/searchSTR', 'r')
            sstr = file.read().replace(' ', marker)
            file.close()
        else:
            sstr = None
        return sstr
    
   


def removebbcode(incomingString):
    try:
        import bbcode
        parser = bbcode.Parser()
        code = incomingString
        plain_txt = parser.strip(code)
        return plain_txt
    except:
        return incomingString


def supported(hostname):##mfaraj
    hostname=hostname.lower()
    try:
        from urlresolver.supservers import supported_servers  
        
        if supported_servers.has_key(hostname):
            supported=True
        else:
            supported =False
        return supported    
   
    except:
        trace_error()
        return False




def cfresolve(url_page = None):
    
    if url_page:
        from core import  httptools
        data = httptools.downloadpage(url_page,bypass_cloudflare=True).data
        return data


def parsedata(data, regx):
    try:
        match_list = re.findall(regx, data, re.M | re.I)
        return match_list
    except:
        return []
def cleanhtml2(raw_html):

    def replaceSpecialCharacters(sString):
        return sString.replace('\\/','/').replace('&amp;','&').replace('\xc9','E').replace('&#8211;', '-').replace('&#038;', '&').replace('&rsquo;','\'').replace('\r','').replace('\n','').replace('\t','').replace('&#039;',"'").replace('&quot;','"').replace('&gt;','>').replace('&lt;','<').replace('&nbsp;','')

    
    cleanr = re.compile('<.*?>')
    cleantext = re.sub(cleanr, '', raw_html)
    
    return replaceSpecialCharacters(cleantext)


def cleanhtml(raw_html):
    cleanr = re.compile('<.*?>')
    cleantext = re.sub(cleanr, '', raw_html)
   
    return cleanhtml2(cleantext)

def getHostName(url, nameOnly = True):
        
        hostName=''
        if True:
            match = re.search('https?://(?:www.)?(.+?)/', url)
            if match:
                hostName = match.group(1)
                if (nameOnly):
                    n = hostName.split('.')
                    try: hostName = n[-2]
                    except Exception: trace_error()
            hostName = hostName.lower()
        
        return hostName
def getDomain(url):
    
    try:plugin_path=sys.argv[0]
    except:plugin_path=''
    
    domain=getHostName(url)
    issupported=supported(domain)
    
    image=getserver_image(domain)
    if "plugin.video" in plugin_path or "plugin.audio" in plugin_path:
        return domain
    return domain,image,issupported


def GetDomain(url):
    tmp = re.compile('//(.+?)/').findall(url)
    domain = 'server'
    if len(tmp) > 0:
        domain = tmp[0].replace('www.', '')
    if '.' in domain:
        domain = domain.split('.')[0]
    
    return domain


def getwebfilesize(link):
    try:
        site = urllib.urlopen(link)
        meta = site.info()
        pagesize = int(float(meta.getheaders('Content-Length')[0]) / 1048576)
        return str(pagesize) + 'MB'
    except:
        return ''


def traceerror():
    import sys
    import traceback
    traceback.print_exc(file=sys.stdout)


def gethostname(url):
    try:
        from urlparse import parse_qs, urlparse
        query = urlparse(url)
        hostname = query.hostname
        hostname = hostname.replace('www.', '')
        hostname = hostname.replace('.com', '')
        hostname = hostname.replace('.net', '')
        if 'google' in hostname:
            hostname = 'google'
        if '.' in hostname:
            hostname = hostname.split('.')[0]
        return hostname
    except:
        return url


def finddata(data, marker1, marker2, withMarkers = False, caseSensitive = True):
    if caseSensitive:
        idx1 = data.find(marker1)
    else:
        idx1 = data.lower().find(marker1.lower())
    if -1 == idx1:
        return ''
    if caseSensitive:
        idx2 = data.find(marker2, idx1 + len(marker1))
    else:
        idx2 = data.lower().find(marker2.lower(), idx1 + len(marker1))
    if -1 == idx2:
        return ''
    if withMarkers:
        idx2 = idx2 + len(marker2)
    else:
        idx1 = idx1 + len(marker1)
    return data[idx1:idx2]


class cParser:

    def parseSingleResult(self, sHtmlContent, sPattern):
        aMatches = re.compile(sPattern).findall(sHtmlContent)
        if len(aMatches) == 1:
            aMatches[0] = self.__replaceSpecialCharacters(aMatches[0])
            return (True, aMatches[0])
        return (False, aMatches)

    def __replaceSpecialCharacters(self, sString):
        return sString.replace('\\/', '/').replace('&amp;', '&').replace('\xc9', 'E').replace('&#8211;', '-').replace('&#038;', '&').replace('&rsquo;', "'").replace('\r', '').replace('\n', '').replace('\t', '').replace('&#039;', "'")

    def parse(self, sHtmlContent, sPattern, iMinFoundValue = 1):
        sHtmlContent = self.__replaceSpecialCharacters(str(sHtmlContent))
        aMatches = re.compile(sPattern, re.IGNORECASE).findall(sHtmlContent)
        if len(aMatches) >= iMinFoundValue:
            return (True, aMatches)
        return (False, aMatches)

    def replace(self, sPattern, sReplaceString, sValue):
        return re.sub(sPattern, sReplaceString, sValue)

    def escape(self, sValue):
        return re.escape(sValue)

    def getNumberFromString(self, sValue):
        sPattern = '\\d+'
        aMatches = re.findall(sPattern, sValue)
        if len(aMatches) > 0:
            return aMatches[0]
        return 0


def addDirectoryItem(name, url,image,desc,section,extra={}):
    if '|' in url:
        url = url.split('|')[0]
    url = url.replace('&', 'AxNxD')
    url = url.replace('=', 'ExQ')

    extra=str(extra)
    data =str({'name':name,'url':url,'image':image,'desc':desc,'section':section,'extra':extra})
    file = open('/tmp/TSmedia/data.txt', 'a')
    file.write(data + '\n')
    file.close()
    return

class Item(object):
    def __init__(self,section_id='',addon_id=''):

        self.list=[]
        self.spath=sys.argv[0]
        self.addonPath=os.path.split(self.spath)[0]
        self.addon_id=self.spath.split("/")[-2]
        self.section_id=self.spath.split("/")[-3]
        self.addonSPath=self.section_id+"/"+self.addon_id


            
        #self.__dict__ = self.toutf8(self.__dict__)
    def addDir(self,name='', url='', mode=0, image='',category='',page=1,maintitle = False, link = False,desc='', extra={},show='', searchall = None,type='',dialog=None):
            category=str(category)
            
            info=''
            if isinstance(extra, dict):
                if not extra=={} :
                    for key in extra.keys():
                        info=info+"|"+str(extra[key])

            else:
                info=extra.replace(",","|")
            info=info.replace("'",'').replace(",",'')
            info=cleanhtml2(info)
            extra={}
            extra.update({'info':info})
           
            m3u8=False
           
            if name and  name.startswith("Error") :
                mode=-1
                if not dialog:
                   dialog="error"
               
            if name and mode==-1 :
                if not dialog:
                   dialog="error"
                name="Error:"+name
               
            if name and  (name.startswith("Message") or str(url).startswith("Message")):
                mode=-2
                if not dialog:
                   dialog='message'
                name=name.replace("Message:","")
            if name and mode==-2 and not name.startswith("Message"):
                if not dialog:
                    dialog='message'
                name="Message:"+name 
                
            if mode==-5 :
                m3u8=True
                mode=0
                
            if url and ('m3u8' in url) :
               m3u8=True 
            if mode==-6:
                m3u8=False 
                mode=0       
            
            if link==True:
                mode=0
            if mode==0:
                link=True
          
                
            if mode==503:
                if not dialog:
                   dialog="input"
            if mode==903:
                if not dialog:
                   dialog="login"                
            if mode==103 or mode==603 or mode==703 or mode==803 or mode==1003 or mode==2003:
                if not dialog:
                   dialog="search"                  
            if url.startswith('plugin://plugin.video.youtube') or 'youtube.com' in url:
                             link=True
                             mode=0
            if image.startswith("img/"):
                image=AppPath+"/addons/"+self.addonSPath+"/"+image
            if not image.startswith("http") and not os.path.exists(image):
               image=AppPath+"/addons/"+self.addonSPath+"/icon.png"  
            imageBasename=getimage_basename(image)     
            try:
                name = name.encode('utf-8', 'ignore')
                name=name.replace("'",'')
            except:
                pass             
                pass             
            try:
                category = category.encode('utf-8', 'ignore')
                category=category.replace("'",'')
            except:
                pass              
            try:
                desc = desc.encode('utf-8', 'ignore')
                desc=desc.replace("'",'')
            except:
                pass                
            

            try:image = image.encode('utf-8', 'ignore')
            except:pass 
            try:url = url.encode('utf-8', 'ignore')
            except:pass  
            m3u8add=False
            if  m3u8==True:
                
                try:
                    from m3u8player import getm3u8playlist
                    list = getm3u8playlist(url)
                    for item in list:
                            url = str(item[1])
                            
                            try:             
                                title ='quality'+"-"+ str(item[0]).encode('utf-8', 'replace')
                                
                            except:
                                title=item[0]

                            cParams={}   
                            cParams["name"]=title
                            cParams["title"]=title
                            cParams["url"]=url
                            cParams["mode"]=0
                            cParams["image"]=image
                            cParams["category"]=category
                            cParams["page"]=page
                            cParams["maintitle"]=maintitle
                            cParams['desc']=desc
                            cParams['extra']=extra
                            cParams['type']=str(type)
                            cParams['show']=show
                            cParams['caddon_id']=self.addon_id
                            cParams['csection_id']=self.section_id
                            cParams['dialog']=dialog
                            cParams['imageBasename']=imageBasename
                            self.list.append(cParams)
                            m3u8add=True
                                    
                       
                except:
                        
                        pass
            if  m3u8add:
                return
            cParams={}   
            cParams["name"]=name
            cParams["url"]=url
            cParams["mode"]=mode
            cParams["image"]=image
            cParams["category"]=category
            cParams["page"]=page
            cParams["maintitle"]=maintitle
            cParams['desc']=desc
            cParams['extra']=extra
            cParams['type']=str(type)
            cParams['show']=show
            cParams['caddon_id']=self.addon_id
            cParams['csection_id']=self.section_id
            cParams['dialog']=dialog
            cParams['imageBasename']=imageBasename
            self.list.append(cParams)

            
            if searchall is not None  :
                search_file= self.addonPath+"/searchall"
                print "searchfile",search_file
                try:
                    afile = open(search_file, 'w')
                    
                    afile.write(self.addon_id + ';;' + str(cParams))
                    afile.close()
                         
                except:
                    trace_error()
                    pass





        


    def endDir(self):

            datalist=self.list
            logdata('xbmctools-datalist',datalist)                 
            self.list=[]
            try:                 
                debugmode=sys.argv[3]
            except:
                trace_error()
                debugmode='user'
                
              
            
            logdata('xbmctools--debugmode',debugmode) 
            if debugmode=='developer':
                                
                  
                 try:
                    f=open(data_file,"w")
                    for item in datalist:
                        f.write(str(item)+"\n")
                    f.close()            
                        
                 except:
                     print ">>>Error storing output data to json file,check error>>"
                     trace_error()
                 return    
            if debugmode=="SearchAll":
                f=open(data_file,"w")
                f.close()
                
            

            self.list=[]
            return datalist

         
    def ListItem(self,name,  iconImage=None, thumbnailImage="DefaultFolder.png"):##for wTSmedia

              if (".jpg" not in thumbnailImage.lower() ) and (".png" not in thumbnailImage.lower()) and (".jpeg" not in thumbnailImage.lower()):
                      thumbnailImage = "DefaultFolder.png"
              
              if thumbnailImage is not None:
                      thumbnailImage = thumbnailImage.replace(" ", "-")
                      thumbnailImage = thumbnailImage.replace("&", "AxNxD")
                      thumbnailImage = thumbnailImage.replace("=", "ExQ")

                 
              
              data = "name=" + str(name) + "&thumbnailImage=" + str(thumbnailImage)
 
              
             
              self.list.append(data)


        
    def get_params(self):
        params = {}
        item=sys.argv[2]
        try:
            #item=item.replace('"','')
            params=ast.literal_eval(item)
           
            return params
        except:
           trace_error() 
           pass

        
       
        item = item.replace('AxNxD', '&').replace('ExQ', '=')
        paramstring = item
        if len(paramstring) >= 2:
            
            cleanedparams = paramstring.replace('?', '&')

            pairsofparams = cleanedparams.split('&')
            
            for i in range(len(pairsofparams)):
                splitparams = {}
                splitparams = pairsofparams[i].split('=')
                if len(splitparams) == 2:
                    p=splitparams[1]  
                    if isinstance(splitparams[1], basestring) :
                        p=urllib.unquote_plus(splitparams[1])
                    
                           
                    params[splitparams[0]] = p
        return params            

           
def addDir(name, url, mode, image, section = '', page = 0, maintitle = False,desc='', plugin = None, link = False, searchall = None,extra={}):
    spath = sys.argv[0]
    desc=str(desc)
    extra=str(extra)
    section=str(section)
    m3u8=False
    
    if name and  (name.startswith("Error") or url.startswith("Error")):
        mode=-1
       
    if name and mode==-1 and not name.startswith("Error"):

        name="Error:"+name
       
    if name and  (name.startswith("Message") or url.startswith("Message")):
        mode=-2
        name=name.replace("Message:","")
    if name and mode==-2 and not name.startswith("Message"):

        name="Message:"+name 
        
    if mode==-5:
        m3u8=True
        mode=0
    
    if link==True:
        mode=0
    if mode==0:
        link=True
    try:
        name = name.encode('utf-8', 'ingnore')
        section = section.encode('utf-8', 'ingnore')
        desc = desc.encode('utf-8', 'ingnore')
        if ";" in name :
                  name=cleanparam(name)                 
        if ";" in section :
                  section=cleanparam(section)
        if ";" in desc :
                  desc=cleanparam(desc)        
    except:
        pass


    if plugin is not None:
        path = spath.replace('/default.py', '')
        spath = os.path.split(path)[0] + '/' + plugin + '/default.py'
    if image and image.lower().startswith("img"):
        image=os.path.split(spath)[0]+"/"+image
    if maintitle:
                 try:
                   ftitle=open("/tmp/TSmedia/mtitle","w")
                   ftitle.write(name)
                   ftitle.close()
                 except:
                     pass

        
    mtitle=''
    if link==True:
        if os.path.exists("/tmp/TSmedia/mtitle"):
           mtitle=open("/tmp/TSmedia/mtitle").read()
           name=name+"-"+mtitle
        
           if image is None or image=='':
              image=plugin_path+"/interface/servers/play.png"
           elif "play.png" in image:
                 image=plugin_path+"/interface/servers/play.png"
           else:
                 image=plugin_path+"/interface/servers/play.png"

    if image.strip()=='':
                image=os.path.split(spath)[0]+"/icon.png"        
    if not image.startswith("http") and  os.path.exists(image)==False:
               image= os.path.split(spath)[0]+"/icon.png"

        
    maintitle=str(maintitle)     
    link=str(link)
    try:
        desc = desc.encode('utf-8', 'ingnore')
    except:
        pass
    try:
        section = section.encode('utf-8', 'ingnore')
    except:
        pass
    if link=='True':
        u=url
    else:    
        u = spath + '?url=' + urllib.quote_plus(url) + '&mode=' + str(mode) + '&name=' + urllib.quote_plus(name) + "&" + "image="+image+'&page=' + str(page) + '&desc=' + urllib.quote_plus(desc)+ '&section=' + urllib.quote_plus(section)+'&maintitle=' + maintitle+ '&extra=' + urllib.quote_plus(extra)



    if ('m3u8' in url and not name == 'm3u8_0') or m3u8==True :
        try:
            from m3u8player import getm3u8playlist
            list = getm3u8playlist(url) 
            for item in list:
                url = str(item[1])
                title = str(item[0])+"-"+ name
                image = item[2]
                
                #u = spath + '?url=' + urllib.quote_plus(url) + '&mode=' + str(mode) + '&name=' + urllib.quote_plus(name) + "&" + "image="+image+'&page=' + str(page) + '&desc=' + urllib.quote_plus(desc)+ '&section=' + urllib.quote_plus(section)+'&maintitle=' + maintitle+ '&extra=' + urllib.quote_plus(extra)+ '&link=True' 

                
                addDirectoryItem(name+"_"+title,url,image,desc,section)

            return
        except:
                addDirectoryItem(name,url,image,desc,section)
                return


    if searchall is not None:
        try:
            dirname = os.path.split(searchall)[0]
            plugin_name = os.path.basename(dirname)
            search_file = searchall.replace('default.pyc', 'searchall').replace('default.pyo', 'searchall').replace('default.py', 'searchall')
            afile = open(search_file, 'w')
            afile.write(plugin_name + ';;' + u)
            afile.close()
        except:
            pass

    ok = addDirectoryItem(name,u,image,desc,section)
    return ok





def get_params():
        params = {}
        item=sys.argv[2]
        if True:
            item=item.replace('"','')
            params=ast.literal_eval(item)
             
            return params
        else:
           trace_error() 
           pass
    
            
        item = item.replace('AxNxD', '&').replace('ExQ', '=')
        paramstring = item
        if len(paramstring) >= 2:
            
            cleanedparams = paramstring.replace('?', '&')

            pairsofparams = cleanedparams.split('&')
            
            for i in range(len(pairsofparams)):
                splitparams = {}
                splitparams = pairsofparams[i].split('=')
                if len(splitparams) == 2:
                    p=splitparams[1]  
                    if isinstance(splitparams[1], basestring) :
                        p=urllib.unquote_plus(splitparams[1])
                    
                           
                    params[splitparams[0]] = p
        return params            

