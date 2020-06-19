# -*- coding: utf-8 -*-
# ------------------------------------------------------------
##coded by yasinov-------------------------------------------

from iTools import printE


def get_video_url(server_url):
    import requests , re
    s = requests.Session()
    r = s.get(server_url)
    html = r.content
    html=html.replace("\u0026", "&")
    html=html.replace("\&","&")

    regx='''hlsManifestUrl(.*?)&quot;,'''        
    M3U8Url=re.findall(regx,html, re.M|re.I)[0][13:]
    print "stream_link3",M3U8Url
   
    r = s.get(M3U8Url)
    data=r.content

    
    #stream_links = r.content
    #print "stream_link2",stream_link
    #from xbmctools import addDir
    video_urls=[]
    print data
    #quals=['sd','lowest','low','hd','mobile']
    quality=''
    #line=#EXT-X-STREAM-INF:PROGRAM-ID=1, BANDWIDTH=161349, QUALITY=mobile
    linkstab=[]
    try:
        lines=data.split("\n")
        i=0
        
        for line in lines:
           
            line=line.strip()
            if 'QUALITY=' in line:
                quality=line.split('QUALITY=')[1]
                
            if not line.startswith("http"):
                continue
           
            
            if quality=='hd':
                hd=str(line).strip()
            linkstab.append((quality,str(line).strip()))    
            i=i+1
        return linkstab           
    except:
        printE()

        return []
        

