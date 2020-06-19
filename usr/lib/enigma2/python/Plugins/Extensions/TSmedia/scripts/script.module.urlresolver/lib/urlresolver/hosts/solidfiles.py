import requests,re,time
Sgn=requests.session()
from base64 import b64decode
def get_video_url(url):
    video_urls = []
    r = Sgn.get(url,verify=False,timeout)
    data = r.text
    rgxt = '''"streamUrl":"(.+?)"'''
    download = re.findall(rgxt,data)
    if download:
        hrf = download[0]
        video_urls.append(["Cool_solidfiles", hrf])
    else:video_urls.append(["Oops_solidfiles", 'Error'])
    return video_urls
#S1='http://www.solidfiles.com/v/4yQR7pMXP4WZy/dl'
#print get_video_url(S1)
