import requests,re,time
Sgn=requests.session()
from base64 import b64decode
def get_video_url(url):
    video_urls = []
    r = Sgn.get(url)
    data = r.text
    rgxt = "file: '(.+?)'"
    download = re.findall(rgxt,data)
    if download:
        hrf = download[0]
        video_urls.append(["Cool_4shared", hrf])
    else:video_urls.append(["Oops_4shared", 'Error'])
    return video_urls
#S1='https://www.4shared.com/video/q-WZrDufiq/Anime4upcom_227_EP_05_HD.html'
#print get_video_url(S1)
