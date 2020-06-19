# -*- coding: utf-8 -*-
# ------------------------------------------------------------
##coded by yasinov-------------------------------------------

from xbmctools import addDir,trace_error,readnet
import re

def get_video_url(url):
        
        data=readnet(url)
        regx='''file:"(.+?)"}'''#,{file:"http://s12.vidshare.tv/pdomaj6nlsm4f4kmlebsh2tsh2vb4c7qykuv3fadqktvuwjirpegrcdrlwoq/v.mp4",label:"360"}],'''
        regx2='''file:"(.+?)",label:"(.+?)"'''
        try:
          href=re.findall(regx,data, re.M|re.I)[0]
        except:
            trace_error()
        print "href2",href
        #get_servericon(server)
        addDir('m3u8',href,9,"img/server.png",'',1,link=True)
        match2=re.findall(regx2,data.split("m3u8")[1], re.M|re.I)
        for href in match2:
               print "href2",href
               addDir(href[1],href[0],9,"img/server.png",'',1,link=True)

        return href[1],href[0]
