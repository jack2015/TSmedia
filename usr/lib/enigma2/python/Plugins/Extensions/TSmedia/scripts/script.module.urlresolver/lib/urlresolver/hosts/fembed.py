import requests,re,json
sgn = requests.Session()
def get_video_url(url):
    Urlo = ''
    data = ''
    video_urls = []
    url = sgn.get(url,verify=False).url
    print url
    if "feurl.com" in url:
        _Id = url.split('/')[-1]
        link = "https://feurl.com/api/source/"+str(_Id)
        _r = sgn.post(link).json()
        if _r and _r['success']== True:
            data = _r['data']
    if data !='':
        for keys in data:
            a = keys['file']
            b = keys['type']
            c = keys['label']
            w = ('Cool_* feurl [ '+str(b)+'_'+str(c)+' ]',a)
            video_urls.append(w)
    else:
        w = ('Ooops_* feurl ','http://error')
        video_urls.append(w)
    return video_urls
#S1="https://www.fembed.com/v/y2lzwaezpg4zn08"
#print get_video_url(S1)
