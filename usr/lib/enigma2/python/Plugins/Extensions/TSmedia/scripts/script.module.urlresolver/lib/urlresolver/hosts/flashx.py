def get_video_url(url):
    import re
    import requests
    from requests.auth import HTTPBasicAuth
    import urllib
    ListVid = []
    s = requests.Session()
    r = s.get(url)
    htmldata2 = r.text
    Rgx = '''onclick="location.href='(.+?)'"'''
    cline = re.findall(Rgx,htmldata2)
    if cline:
        cline = cline[0]
        print 'jjjj__',cline
        headers = {'Host': 'www.flashx.net',
               'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:67.0) Gecko/20100101 Firefox/67.0',
               'Accept': '*/*',
               'Accept-Language': 'fr,fr-FR;q=0.8,en-US;q=0.5,en;q=0.3',
               #'Referer': cline[0],
               'X-Requested-With': 'XMLHttpRequest',
               'Connection': 'keep-alive',
               'TE': 'Trailers'}
        r = s.get(cline,headers=headers)
        htmldata = r.text
        rgx = '''src: '(.+?)',type:.+?,label: '(.+?)',res'''
        urlvid = re.findall(rgx,htmldata)
        if urlvid:
            w=('Cool_flashx_'+urlvid[0][1],urlvid[0][0])
            ListVid.append(w)
        else:
            w=('Ooops_flashx_Error','http://error')
            ListVid.append(w)
    else:
        w=('Ooops_flashx_Error','http://error')
        ListVid.append(w)
    return ListVid

#S1= 'https://www.flashx.tv/embed-i7g996wm1qw4.html'
#S2='https://www.flashx.tv/embed-xp4zmad57v4n.html'
#print get_video_url(S1)
