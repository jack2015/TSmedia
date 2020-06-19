# -*- coding: utf8 -*-
import warnings
from requests.packages.urllib3.exceptions import InsecureRequestWarning
warnings.simplefilter('ignore',InsecureRequestWarning)
def get_video_url(url)
  return postData(url)
def postData(url):
    from base64 import b64encode, b64decode
    import re
    import requests
    urlo = url.split('/x/')[1]
    url = 'https://clickopen.club/x/'+urlo
    print urlo
    urlfinal = []
    urlo2 = urlo.split('/')[1]
    link = 'https://clickopen.club/x/link/'+urlo2+'/'
    qlt = ''
    w = ''
    exemple = 'https://clickopen.club/x/link/wwdREQ2H694o5ac/720p/f50e50824c99d0b7a40208e9d62e1c3e/'
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:61.0) Gecko/20100101 Firefox/65.0',
        'Host': 'clickopen.club',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language': 'fr,fr-FR;q=0.8,en-US;q=0.5,en;q=0.3',
        'Referer': url
           }
    s = requests.Session()
    r = s.get(url, headers=headers)
    htmldata = r.content
    rgx = '''JuicyCodes.Run(.+?);</script>'''
    hlilef = str(re.findall(rgx,htmldata)).replace('"+"','')
    if hlilef:
        hlilef = b64decode(hlilef).split('file')[1].split('fontSize')#[0]
        print hlilef
        if hlilef:
            rgx_2 = '''mp4\|(.+?)\|label\|'''
            hlilef2 = re.findall(rgx_2,str(hlilef))
            print 'tttttttttttt',hlilef2
            if hlilef2:
                    w= ('cool_clickopen_360',link+'360'+'/'+hlilef2[0])
                    urlfinal.append(w)
                    w= ('cool_clickopen_480',link+'480'+'/'+hlilef2[0])
                    urlfinal.append(w)
                    w= ('cool_clickopen_720',link+'720'+'/'+hlilef2[0])
                    urlfinal.append(w)
                    w= ('cool_clickopen_1080',link+'1080'+'/'+hlilef2[0])
                    urlfinal.append(w)
    print urlfinal
    return urlfinal
#CC_1 = 'https://clickopen.club/x/embed/wwdREQ2H694o5ac/'
#BB = 'https://clickopen.club/x/embed/2Uqtx1HyI6DhKk8/'
#AA = postData(CC_1)
#print AA
