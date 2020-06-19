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
        w = ('Cool_* 7-up [ '+a+'_'+b+' ]',c)
        video_urls.append(w)
    else:
        w = ('Ooops_* 7-up ','http://error')
        video_urls.append(w)
    return video_urls
#S1="https://7-up.net/embed-rz087mp6q2qv.html"
#print get_video_url(S1)
