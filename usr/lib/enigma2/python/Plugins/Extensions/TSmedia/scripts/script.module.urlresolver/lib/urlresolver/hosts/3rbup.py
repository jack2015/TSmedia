# -*- coding: utf8 -*-
Agent = {'User-agent': 'Mozilla/5.0 (Windows NT 10.0; …) Gecko/20100101 Firefox/65.0'}
import requests
import re
def get_video_url(url):
    import urllib2
    import re
    video_urls = []
    url_test = ''
    htmldata = ''
    b = ''
    if '?pt' in url:
        url = url.split('?pt')[0]
        print url
        if 'fs1' not in url:
            url1 = url.split('3rbup')[1]
            url = 'https://fs1.3rbup'+url1
        else:url = url
    else:
        if 'fs1' not in url:
            url1 = url.split('3rbup')[1]
            url = 'https://fs1.3rbup'+url1
        else:url = url
    print url
    headers = {'Host': '3rbup.com',
     'Accept': 'text/html,application/xhtml+xm…ml;q=0.9,image/webp,*/*;q=0.8',
     'Accept-Language': 'fr,fr-FR;q=0.8,en-US;q=0.5,en;q=0.3',
     'Upgrade-Insecure-Requests': '1',
     'Connection': 'keep-alive',
     'Content-Type': 'text/html; charset=UTF-8',
     'Referer': url,
     'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; …) Gecko/20100101 Firefox/65.0',
     'X-Requested-With': 'XMLHttpRequest'}
    s = requests.Session()
    r = s.get(url, headers=headers)
    html = r.content
    rgx = '''download-timer'\).html\("<a class='btn btn-default' href='(.+?)'>'''
    Token = re.findall(rgx,html)
    print Token[0]
    r1 = s.get(Token[0])
    html1 = r1.content
    rgx ='''file: "(.*?)"'''
    url_video = re.findall(rgx,html1)
    if url_video:
        w = ('Cool_3rbup *_* ',url_video[0])
        video_urls.append(w)
    else:
        w = ('Ooops_streamango *_* Error','http//Error')
        video_urls.append(w)
    return video_urls
HH_1 = 'https://3rbup.com/9e34b8c32be658df?pt=cUEgAL7fzDUbPEnp0F1p1ydrSGSbRiSF5dw9kJ8oYiA%3D'
cc = 'https://fs1.3rbup.com/9e34b8c32be658df'
AA = get_urlvideo_3rbup(cc)
print AA
