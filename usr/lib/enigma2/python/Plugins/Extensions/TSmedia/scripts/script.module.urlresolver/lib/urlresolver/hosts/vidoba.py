import requests,re,jsunpack
sgn=requests.Session()
def get_video_url(url):
    r = sgn.get(url).content
    data = jsunpack.unpack(r)
    rgx = '''file:"(.+?)"'''
    files = re.findall(rgx,data)
    list=[]
    for item in files:
        if "m3u" in item:
           list.append(("m3u8",item))
        if "mp4" in item:
           list.append(("mp4",item))           
        
    return list
#S1='https://vidoba.net/embed-ykpckj3acwsz.html'
#print get_jsunpack(S1)
