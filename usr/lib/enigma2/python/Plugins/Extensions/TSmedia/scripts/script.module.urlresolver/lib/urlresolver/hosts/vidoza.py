import requests,re
T = requests.Session()
def get_video_url(url):
    url = url.replace('embed-','')
    import urllib2
    import re
    video_urls = []
    headers = {'Host': 'vidoza.net',
     'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; rv:62.0) Gecko/20100101 Firefox/65.0.2',
     'Accept': '*/*',
     'Accept-Language': 'fr,fr-FR;q=0.8,en-US;q=0.5,en;q=0.3',
     'Content-Type': 'application/x-www-form-urlencoded',
     'Accept-Encoding' : 'deflate',
     'X-Requested-With': 'XMLHttpRequest',
     'Referer': url,
     'Connection': 'keep-alive'}
    request = T.get(url)#urllib2.Request(url, None, headers)
    data2 = request.content#urllib2.urlopen(request).read()
##    print data2
    rgx = 'src\s*:\s*"(.+?)".*?res\s*:\s*"(.+?)"'
    urlvidoza = re.findall(rgx, data2)
    for x,y in urlvidoza:
        w = (y + "_vidoza_",x)
        video_urls.append(w)
    return video_urls
