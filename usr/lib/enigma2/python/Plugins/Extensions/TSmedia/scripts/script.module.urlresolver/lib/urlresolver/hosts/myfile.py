# -*- coding: utf-8 -*-
# ------------------------------------------------------------
##coded by aime_jeux-------------------------------------------

from xbmctools import addDir,trace_error

def postData(url):
    import re
    import requests
    URLIST = []
    s = requests.Session()
    r = s.get(url)
    htmldata = r.content
    rgx = 'class="btn btn-primary btn-block".+?href="(.+?)">'
    coucou = re.findall(rgx, htmldata, re.DOTALL)
    print coucou
    if coucou:
        for a in coucou:
            w= ( 'Cool_myfile *__* mp4',a)
            URLIST.append(w)
    else:
        w = ('Ooops_Error','http//error')
        URLIST.append(w)
    return URLIST
#nn = 'https://myfile.is/ZeUb1cXam3'
#AA = postData(nn)
#print AA
def get_video_url(url):
   return postSata(url)

