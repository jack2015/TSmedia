import requests,re
sgn = requests.Session()
def get_eval_function(data,sPattern):
    r = re.search(sPattern, data, re.DOTALL + re.IGNORECASE)
    return r
def get_video_url(url):
    Urlo = ''
    video_urls = []
    data = sgn.get(url,verify=False).content
    sPattern = '''{file:"(.+?)"}'''
    code = get_eval_function(data,sPattern)
    if code:
        a = code.group(1)
        b = a[-4:]
        w = ('Cool_* vidfast [ '+b+' ]',a)
        video_urls.append(w)
    else:
        w = ('Ooops_* vidfast ','http://error')
        video_urls.append(w)
    return video_urls
#S1="https://vidfast.co/embed-csc1cxso0lc5.html"
#print get_video_url(S1)
