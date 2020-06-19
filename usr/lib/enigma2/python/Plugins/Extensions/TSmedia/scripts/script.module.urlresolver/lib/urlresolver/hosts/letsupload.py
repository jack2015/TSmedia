import requests,re,time
Sgn=requests.session()
from base64 import b64decode
def get_video_url(url):
    video_urls = []
    hdr = {'Host': 'letsupload.co',
           'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:74.0) Gecko/20100101 Firefox/74.0',
           'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
           'Accept-Language': 'fr,fr-FR;q=0.8,en-US;q=0.5,en;q=0.3',
           'Accept-Encoding': 'gzip, deflate',
           'Connection': 'keep-alive',
           'Upgrade-Insecure-Requests': '1'}
    if '/plugins/' in url:
        r = Sgn.get(url).content
        rgxs = '''file: "(.+?)"'''
        download = re.findall(rgxs,r)
        video_urls.append(["Cool_letsupload_0", download[0]])
    else:
        if '&h=' in url:
            print "with H"
            h= url.split('&h=')[1]
            PM= {'h':h}
            r = Sgn.get(url,data=PM)
        else:
            print "without H"
            r = Sgn.get(url)
        data = r.text
        rgxt = """\('.download-timer'\).html\("<a class='btn btn-free' href='(.+?)'"""
        download = re.findall(rgxt,data)
        if download:
            hrf = download[0]
            _id = hrf.split('pt=')[1]
            prm = {'pt':_id}
            _r = Sgn.get(hrf,headers=hdr,data=prm).content
            rgy = '''tracker: "(.+?)"'''
            tracker = re.findall(rgy,_r)
            if tracker:
                tracker = tracker[0]
                tracker = b64decode(tracker)
                video_urls.append(["Cool_letsupload_1", tracker])
            else:
                download = re.findall(rgxt,_r)
                if download:
                    _id = download[0].split('pt=')[1]
                    _id = _id.replace('%3D','=')
                    prm1 = {'pt':_id}
                    time.sleep(5)
                    __r = Sgn.get(download[0],data=prm1).content
                    tracker = re.findall(rgy,__r)
                    if tracker:
                        tracker = tracker[0]
                        tracker = b64decode(tracker)
                        video_urls.append(["Cool_letsupload_2", tracker])
                    else:video_urls.append(["Oops_letsupload_2", 'Error'])
                else:video_urls.append(["Oops_letsupload_3", 'Error'])
        else:video_urls.append(["Oops_letsupload", 'Error'])
    return video_urls
#S1='https://letsupload.co/bzlE/[Anime2001.com]_FLGGG_EP21_[HD].mp4&h=894c4bb1d1921e95d7dd95f25fc3796f'
#S2 = 'https://letsupload.co/4dM4j/%5BAnime4up.com%5D_227_EP_05_HD.mp4'
#S3 = 'https://letsupload.co/plugins/mediaplayer/site/_embed.php?u=7z8q&amp'
#print get_video_url(S3)
