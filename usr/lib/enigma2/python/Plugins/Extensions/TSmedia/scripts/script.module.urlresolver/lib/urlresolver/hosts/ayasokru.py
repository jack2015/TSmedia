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
    htmldata=str(htmldata).replace('\\', '').replace('&quot;','"').replace(';','').replace('u0026','&')
    coucou = re.findall(r'\{"name":"(.*?)","url":"(.*?)"', htmldata, re.DOTALL)
    if coucou:
        for a,b in coucou:
            w= ( 'Ok *__* '+a,b)
            URLIST.append(w)
    else:
        w = ('Ooops_Error','http//error')
        URLIST.append(w)
    return URLIST
#kl = 'https://ok.ru/videoembed/1049441405449'
#AA = postData(kl)
#print AA
def get_video_url(url):
   return postData(url)

