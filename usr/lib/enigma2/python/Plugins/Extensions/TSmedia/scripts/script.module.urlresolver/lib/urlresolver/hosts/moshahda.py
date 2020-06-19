import requests,re,time
Sgn=requests.session()
from base64 import b64decode
from jsunpack import unpack
def get_packed_data(html):
    packed_data = ''
    for match in re.finditer('(eval\s*\(function.*?)</script>', html, re.DOTALL | re.I):
        try:
            js_data = unpack(match.group(1))
            js_data = js_data.replace('\\', '')
            packed_data += js_data
        except:
            pass
    return packed_data
def get_video_url(url):
    def cleartxt(txt):
        if txt == 'm3u8':
            return txt
        txt = txt.replace(',','')
        txt = txt.split(':')[1]
        txt = txt.replace('"','')
        txt = txt.replace('x','P')
        return txt
    video_urls = []
    r = Sgn.get(url)
    data = r.text
    rgxt = '''{file:"(.+?)"(.+?)}'''
    download = re.findall(rgxt,data)
    if download:
        for x,y in download:
            if 'onclick' in y:continue
            if '.m3u8' in x:y='m3u8'
            y = cleartxt(y)
            video_urls.append(["Cool_moshahda [ "+str(y)+" ]", x])
    else:
        if '(p,a,c,k,e,d)' in data:
            data2 = get_packed_data(data)
            _don = re.findall(rgxt,data2)
            if _don:
                for x,y in _don:
                    if 'onclick' in y:continue
                    if '.m3u8' in x:y='m3u8'
                    y = cleartxt(y)
                    video_urls.append(["Cool_moshahda [ "+str(y)+" ]", x])
        else:video_urls.append(["Oops_moshahda", 'Error'])
    return video_urls
