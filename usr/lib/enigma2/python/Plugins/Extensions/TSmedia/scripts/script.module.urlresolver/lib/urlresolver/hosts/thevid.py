
import requests,re,jsunpack
sgn = requests.Session()
def get_video_url(url):
    url = url.replace('/v/','/e/')
    Link = ''
    r = sgn.get(url).content
    Tmx = '''<script>eval\(function.+?</script>.+?<script>(.+?)</script>.+?<video id="videojs"'''
    fonction = re.findall(Tmx,r,re.S)
    
    data = jsunpack.unpack("eval\("+fonction[0])
    rgx = '''var vldAb="(.+?)"'''
    video = re.findall(rgx,data)
    
    if video:
        if video[0].startswith('//'):Link="https:"+video[0]


    print "video",video    
    return Link


#S1="https://thevid.live/e/64tiv3y0x6dmmaryhx"
#print get_thevid(S1)
