import requests,re
sgn = requests.Session()
from jsunpack import unpack
def get_eval_function(data,sPattern):
    r = re.search(sPattern, data, re.DOTALL + re.IGNORECASE)
    return r
def get_video_url(url):
    Urlo = ''
    video_urls = []
    data = sgn.get(url,verify=False).content
    sPattern = "javascript'>(eval.*?)</script>"
    code = get_eval_function(data,sPattern)
    code = code.group()
    code = unpack(code)
    if code:
        sPattern = '''sources:\["(.+?)"\]'''
        b = get_eval_function(code,sPattern)
        if b:
            b = b.group(1)
            w = ('Cool_* gounlimited',b)
            video_urls.append(w)
    else:
        w = ('Ooops_* gounlimited','http://error')
        video_urls.append(w)
    return video_urls
#S1="https://gounlimited.to/embed-14vgs6dhmkk1.html"
#print get_video_url(S1)
