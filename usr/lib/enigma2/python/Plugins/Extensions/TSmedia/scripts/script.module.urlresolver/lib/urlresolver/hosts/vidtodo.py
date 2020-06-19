import requests,re
from CloudflareScraper.cfscrape.cloudflare import CloudflareBypass
#from cloudflare import CloudflareBypass
BB = CloudflareBypass()
sgn=requests.Session()
def get_video_url(url):
    ListV = []
    url= url.replace('vidtodo','vidtodu')
    if '=' in url:
        url = url.split('=')[0]
        if 'emb.html?' in url:
            url = url.replace('emb.html?','embed-')+'.html'
    else:url=url
    r = BB.GetHtml(url)
    r1 = re.findall('eval\(function\(p,a,c,k,e,d\)(.+?)split', r,re.S)
    tmx = '''\|type\|(.+?)\|sources\|'''
    rgx = '''mp4\|(.+?)\|ready\|'''
    sources = re.findall(tmx,r1[0],re.S)
    ready = re.findall(rgx,r1[0],re.S)
    if ready:
        link = "https://"+ready[0]+".vidtodo.com/"+sources[0]+"/v.mp4"
        w = ('Cool_Vidtodu',link)
        ListV.append(w)
    else:
        w = ('Ooops_Vidtodu','Error')
        ListV.append(w)
    return ListV