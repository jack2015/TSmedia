import requests,re
sgn = requests.Session()
def get_eval_function(data,sPattern):
    r = re.search(sPattern, data, re.DOTALL + re.IGNORECASE)
    return r
def get_video_url(url):
    Urlo = ''
    video_urls = []
    data = sgn.get(url,verify=False).content
    sPattern = '''\{"label":"(.+?)","type":"(.+?)","file":"(.+?)"\}'''
    code = get_eval_function(data,sPattern)
    if code:
        a,b,c = code.group(1),code.group(2),code.group(3)
        b = b.replace('/','_')
        w = ('Cool_* sandup [ '+a+'_'+b+' ]',c)
        video_urls.append(w)
    else:
        w = ('Ooops_* sandup ','http://error')
        video_urls.append(w)
    return video_urls
#S1="https://sandup.co/embed-2r5f4sxg255w.html"
#print get_video_url(S1)
