Agent = {'User-agent': 'Mozilla/5.0 (X11; U; Linux x86_64; de; rv:1.9.0.15) Gecko/2009102815 Ubuntu/9.04 (jaunty) Firefox/65.0.1',
 'Connection': 'Close'}
def gounlimitedto(url):
    import urllib2
    import re
    import requests
    headers = {'host':'gounlimited.to',
     'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; rv:62.0) Gecko/20100101 Firefox/65.0.2',
     'Accept': '*/*',
     'Accept-Language': 'fr,fr-FR;q=0.8,en-US;q=0.5,en;q=0.3',
     'Content-Type': 'application/x-www-form-urlencoded',
     'Accept-Encoding' : 'deflate',
     'X-Requested-With': 'XMLHttpRequest',
     'Referer': url,
     'Connection': 'keep-alive'}
    request = urllib2.Request(url, None, headers)
    data2 = urllib2.urlopen(request).read()
    rgx = '\|preload\|(.+?)\|(.+?)\|(.+?)\|'
    urlvidoza = re.findall(rgx, data2)
    print 'https://'+urlvidoza[0][2]+'.gounlimited.to/'+urlvidoza[0][1]+'/v.'+urlvidoza[0][0]
urlo = 'https://gounlimited.to/embed-g532lctmca1h.html'
AA = gounlimitedto(urlo)
print AA
