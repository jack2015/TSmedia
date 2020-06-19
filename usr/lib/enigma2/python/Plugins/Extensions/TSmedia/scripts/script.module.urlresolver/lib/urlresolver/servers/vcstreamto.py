from urllib2 import urlopen, Request, URLError, HTTPError
import urllib,urllib2,re
Agent = {'User-agent': 'Mozilla/5.0 (X11; U; Linux x86_64; de; rv:1.9.0.15) Gecko/2009102815 Ubuntu/9.04 (jaunty) Firefox/56.0.1',
 'Connection': 'Close'}
##########################################main menu
urlo = 'https://vcstream.to/embed/5c8308732a84f/Serenity.2019.FRENCH.1080p.official-film-illimite.ws.mp4'
def Get_Id__vcstream(url):
    id_video=url.split('/embed/')[1].split('/')[0]
    return id_video
def import_urlv_vcstream(idv):
    fakir =''
    Infos=''
    baseurl ='https://vcstream.to/player?fid='+str(idv)+'&page=embed'
    regx = '''"file.+?".+?"(.+?)"'''
    request = urllib2.Request(baseurl, None, Agent)
    try:
        data = urllib2.urlopen(request).read()
    except URLError:
        data = ''
    except HTTPError:
        data = ''
    if data!='':
##        fakir = data
        Infos=re.findall(regx,data)
        for href in Infos:
            fakir+=href.replace('\\','')
    else:
        fakir='walou'
    return fakir
idv = Get_Id__vcstream(urlo)
print idv
AA =import_urlv_vcstream(idv)
print AA
