# -*- coding: utf-8 -*-

import js2py
import re,sys,ast
from requests import Session
def get_video_url(url):
    
   
    itemlist = []
    sn=Session()
    referer=sys.argv[-1]
    headers = {'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:66.0) Gecko/20100101 Firefox/66.0',
               'Referer':referer,
               'Cookie': 'pfm=1;sugamun=1;'}
    sn.headers.update(headers)
    data = sn.get(url,verify=False).content
   

    if 'File was deleted' in data or 'File was locked by administrator' in data:
        return ResolveError(0)
    elif 'Video is processing now' in data:
        return ResolveError(1)
    elif "File is awaiting for moderation" in data:
        return ResolveError(1)
    elif 'Video encoding error' in data:
        return ResolveError(5)

    packed = re.findall("<script type='text/javascript'>eval(.*?)\s</script>",data )[0]
    if packed:
        unpacked = js2py.eval_js(packed)

        video_url = re.findall('file:"([^"]+v.mp4)"',unpacked )[0]
        #logger.debug(video_url)
        if video_url:
            print "video_url",video_url
            itemlist.append(("mp4",video_url))

        
    return itemlist
#url='http://gamovideo.com/3eu8zayw00qa'

#get_video_url(url)
