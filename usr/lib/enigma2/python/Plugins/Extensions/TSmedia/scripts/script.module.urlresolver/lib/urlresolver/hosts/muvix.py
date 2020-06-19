# -*- coding: utf8 -*-
import requests,re
from jsunpack import unpack
import base64
S = requests.Session()
def get_video_url(url):
    _Don = ''
    _file = ''
    ListVid = []
    _r = S.get(url).content
    rgx = '''JuicyCodes.Run\((.+?)\)'''
    JuicyCodes = re.findall(rgx,_r)
    if JuicyCodes:
        _Don = JuicyCodes[0]
        _Don = _Don.replace('"+"','')
        _Don = _Don.replace('"','')
        _Don = _Don.decode('base64')
        _Don = unpack(_Don)
        tmx = '''\{"file":"(.+?)","label":"(.+?)","type".+?\}'''
        _file = re.findall(tmx,_Don)
        if _file:
            for href,qlt in _file:
                w = ('Cool_muvix ['+str(qlt)+']',href)
                ListVid.append(w)
        else:
            w = ('Ooops_muvix','Error')
            ListVid.append(w)
    else:
        w = ('Ooops_muvix','Error')
        ListVid.append(w)
    return ListVid
#url = "https://muvix.us/video/5la1N1988fR9fwB/"
#print get_video_url(url)
