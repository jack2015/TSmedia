import requests,re
sgn = requests.Session()
def get_eval_function(data,sPattern):
    r = re.search(sPattern, data, re.DOTALL + re.IGNORECASE)
    return r.group(1)
def get_video_url(url):
    Urlo = ''
    video_urls = []
    data = sgn.get(url,verify=False).content
    sPattern = '"file": "(.+?)"'
    Urlo = get_eval_function(data,sPattern)
    if Urlo:
        w = ('Cool_* gateaflam ',Urlo)
        video_urls.append(w)
    else:
        w = ('Ooops_* gateaflam ','http://error')
        video_urls.append(w)
    return video_urls
#S1="https://s3.gateaflam.com/player/hls.php?id=1215b1eccc2f8a1689bb2aad207d7216&img=6IMhJ8o93iNNSLRaSqIVIA1S5Y8.jpg&bkdrp=true"
#print get_video_url(S1)
