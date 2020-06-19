import requests,re,base64,json
import warnings
from requests.packages.urllib3.exceptions import InsecureRequestWarning
warnings.simplefilter('ignore',InsecureRequestWarning)
sgn = requests.Session()
from jsunpack import unpack
def get_supervideo(url):
    ListV = []
    data= sgn.get(url).content
    packed = re.findall('.+?eval(.*?)</script>',data,re.S)
    if packed:
        _daty = packed[0].replace('\n\t','')
        _dat = unpack('eval'+_daty)
        rgx = '''\{file:"(.+?)".+?\}'''
        _file = re.findall(rgx,_dat)
        if _file:
            for x in _file:
                if '.png' in x or '.jpg' in x:continue
                print x
                print "========================"
                w = ('Cool_supervideo',x)
                ListV.append(w)
        else:
            w = ('Opps_supervideo','Error')
            ListV.append(w)
    else:
        w = ('Opps_supervideo','Error')
        ListV.append(w)
    return ListV
#S1 = "https://supervideo.tv/e/bwdw41nm5kb0"
#print get_supervideo(S1)
def get_vup(url):
    ListV = []
    data= sgn.get(url).content
    packed = re.findall('\{src: "(.+?)"',data,re.S)
    if packed:
        _daty = packed[0]
        w = ('Cool_VUp',_daty)
        ListV.append(w)
    else:
        w = ('Opps_VUp','Error')
        ListV.append(w)
    return ListV
#S1 = "https://vup.to/emb.html?zchj4704ile6=img.vup.to/64/01/00131/zchj4704ile6"

def get_video_url(S1):
    if "=img" in S1:
        _id = S1.split('=img')[0]
        _id = _id.split('?')[1]
        link = "https://vup.to/embed-"+str(_id)+".html?auto=1"
        return link
    print get_vup(link)
