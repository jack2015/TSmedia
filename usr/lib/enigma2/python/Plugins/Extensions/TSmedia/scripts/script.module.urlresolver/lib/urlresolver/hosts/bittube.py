# -*- coding: utf8 -*-
import requests,re
S = requests.Session()
def get_video_url(url):
    _Don = ''
    _file = ''
    hdr = {'Host': 'bittube.video',
           'User-Agent': 'WebTorrent/0.107.16 (https://webtorrent.io)',
           'Accept': '*/*',
           'Accept-Language': 'fr,fr-FR;q=0.8,en-US;q=0.5,en;q=0.3',
           'Accept-Encoding': 'gzip, deflate',
           'Referer': url,
           'Connection': 'keep-alive',
           'Pragma': 'no-cache',
           'Cache-Control': 'no-cache',
           'TE': 'Trailers'}
    for x in range(3):
        link = url.replace('https://bittube.video/videos/embed','https://bittube.video/static/torrents')+ "-"+str((x+1)*360)+".torrent"
        _r = S.get(link,headers=hdr).content
        yum = '''url-listl.+?:http(.+?).mp4'''
        Y = re.findall(yum,_r)
        if Y:
            w = ('Cool_bittube ['+str((x+1)*360)+'p]',"http"+Y[0]+".mp4")
            ListVid.append(w)
    return ListVid
#url = "https://bittube.video/videos/embed/ece6ff1d-27f9-4d7a-b70f-99e808ee1196"
#print get_video_url(url)
