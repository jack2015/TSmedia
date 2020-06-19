# -*- coding: utf-8 -*-
import requests,re,json,time
T = requests.Session()
def get_video_url(url):
    url = url.replace('embed-','')
    link = ''
    prm = {}
    ListVideo = []
    hdr = {'Host': 'jawcloud.co',
           'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:71.0) Gecko/20100101 Firefox/71.0',
           'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
           'Accept-Language': 'fr,fr-FR;q=0.8,en-US;q=0.5,en;q=0.3',
           'Accept-Encoding': 'gzip, deflate, br',
           'Connection': 'keep-alive',
           'Referer': url,
           'Upgrade-Insecure-Requests': '1'}
    r = T.get(url,headers=hdr).content
    rgx = '''onclick="download_video\((.+?)\)">(.+?)</a>'''
    mpegURL = re.findall(rgx,r)
    if mpegURL:
        for x,y in mpegURL:
            X = x.replace("'","")
            X = X.split(',')
            prm ={"op":"download_orig","id":X[0],"mode":X[1],"hash":X[2]}
            link = "https://jawcloud.co/dl?op=download_orig&id="+str(X[0])+"&mode="+str(X[1])+"&hash="+str(X[2])
            T.get(link,headers=hdr)
            time.sleep(3)
            data = T.get(link,headers=hdr).content
            Direct = re.findall('''<a href="(.+?)">Direct Download Link</a>''',data)
            if Direct:
                print Direct[0]
                w = ('Cool_jawcloud [ '+y+' ]',Direct[0])
                ListVideo.append(w)
            else:
                w = ('Oops_jawcloud ','Error')
                ListVideo.append(w)
    else:
        w = ('Oops_jawcloud ','Error')
        ListVideo.append(w)
    return ListVideo