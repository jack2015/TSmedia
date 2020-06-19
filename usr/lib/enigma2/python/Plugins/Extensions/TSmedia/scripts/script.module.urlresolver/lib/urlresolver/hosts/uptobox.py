import re
import requests
from requests.auth import HTTPBasicAuth
import urllib
import requests,re,base64,urllib
S = requests.Session()
def decoder(data,fn):
    data = base64.b64decode(data)
    secretKey = {}
    url = ''
    temp = ''
    tempData = ''
    for i in xrange(len(data)):
        tempData += ("%" + format(ord(data[i]), '02x'))
    data = urllib.unquote(tempData)
    x = 0
    while x < 256:
        secretKey[x] = x
        x += 1
    y = 0
    x = 0
    while x < 256:
        y = (y + secretKey[x] + ord(fn[x % len(fn)])) % 256
        temp = secretKey[x]
        secretKey[x] = secretKey[y]
        secretKey[y] = temp
        x+=1
    x = 0
    y = 0
    i = 0
    while i < len(data.decode('utf-8')):
        x = (x + 1) % 256
        y = (y + secretKey[x]) % 256
        temp = secretKey[x]
        secretKey[x] = secretKey[y]
        secretKey[y] = temp
        url += (chr(ord(data.decode('utf-8')[i]) ^ secretKey[(secretKey[x] + secretKey[y]) % 256]))
        i += 1
    return url
def decodeur1(Html):
    from ast import literal_eval
    MyListV = []
    vl = re.search('var *(_\w+) *= *(\[[^;]+\]);',Html,re.DOTALL)
    if vl:
        var_name = vl.group(1)
        list_b64 = vl.group(2)
        start = Html.find(list_b64)
        Html = Html[start:]
        list_b64 = literal_eval(list_b64)
        nrvr = re.search(var_name + ',(0x\w+)\)*; *var *([^=]+) *=',Html,re.DOTALL)
        if nrvr:
            number_ref = int(nrvr.group(1),16)
            var_ref = nrvr.group(2)
            i = 0
            while i < number_ref:
                list_b64.append(list_b64.pop(0))
                i += 1
            test2 = re.findall("(?:;|;}\(\)\);)sources(.+?)};",Html,re.DOTALL)
            if test2:
                url = ''
                movieID = ''
                qua_list = []
                for page in test2:
                    tableau = {}
                    data = page.find("={")
                    if data != -1:
                        Html = page[data:]
                        if Html:
                            i = 0
                            vname = ''
                            for i in xrange(len(Html)):
                                fisrt_r = re.match("([^']+)':",Html,re.DOTALL)#re.match("([^']+)+",Html,re.DOTALL)#
                                if fisrt_r:
                                    vname = fisrt_r.group(1)
                                    tableau[vname] = 'null'
                                    index = len(fisrt_r.group()[:-1])
                                    Html = Html[index:]
                                whats =  re.match("[:+]'([^']+)'",Html,re.DOTALL)
                                if whats:
                                    if vname:
                                        ln = tableau[vname]
                                        if not ln == 'null':
                                            tableau[vname] = tableau[vname] + whats.group(1)
                                        else:
                                            tableau[vname] = whats.group(1)
                                    index = len(whats.group(0))
                                    Html = Html[index:]
                                else:
                                    whats = re.match("\+*" + var_ref + "\(\'([^']+)\' *, *\'([^']+)\'\)",Html,re.DOTALL)
                                    if whats:
                                        if vname:
                                            ln = tableau[vname]
                                            if not ln == 'null':
                                                tableau[vname] = tableau[vname] + decoder(list_b64[int(whats.group(1),16)],whats.group(2))
                                            else:
                                                tableau[vname] =  decoder(list_b64[int(whats.group(1),16)],whats.group(2))
                                        index = len(whats.group(0))
                                        Html = Html[index:]
                                if not whats:
                                    Html = Html[1:]
                        if tableau:
                            langFre = True
                            qual = ''
                            for i,j in tableau.items():
                                if j.startswith('http') and j.endswith('com'):
                                    url = tableau[i] if not tableau[i] in url else url
                                    continue
                                if len(i) == 5 and len(j) >=10 and j.isalnum() and not 'video' in j:
                                    movieID = j if not j in movieID else movieID
                                    continue
                                if len(test2)>1:
                                    if j == 'eng' :
                                        langFre = False
                                if j == '360' or j == '480' or j == '720' or j == '1080' :
                                    qual = j
                            if langFre and qual and qual not in qua_list:
                                qua_list.append(qual)
                qua_list.sort()
                url_list = []
                for qual in qua_list:
                    print "url==",url
                    url_list.append("{}/{}/{}/0/video.mp4".format(url,movieID,qual))
                MM = zip(qua_list,url_list)
                for x in MM:
                    if url!='' and x[1]!='':
                        w = ('Cool_uptostream_'+str(x[0]),x[1])
                        MyListV.append(w)
                    else:
                        w = ('Ooops_uptostream','Error')
                        MyListV.append(w)
                return MyListV
def get_urlvid(url):
    urlvideo = ''
    id_vid = ''
    if 'uptobox' in url:
        if '/iframe/' in url:
            print '_1_'
            id_vid = url.split('uptobox.com/iframe/')[1]
            if "?Key=" in id_vid:id_vid = id_vid.split('?Key=')[0].replace('/','')
            urlvideo = 'http://uptostream.com/iframe/'+str(id_vid)
        else:
            print '_2_'
            id_vid = url.split('uptobox.com/')[1]
            if "?Key=" in id_vid:id_vid = id_vid.split('?Key=')[0].replace('/','')
            urlvideo = 'http://uptostream.com/iframe/'+str(id_vid)
    else:
        if '/iframe/' in url:
            print '_3_'
            id_vid = url.split('uptostream.com/iframe/')[1]
            if "?Key=" in id_vid:id_vid = id_vid.split('?Key=')[0].replace('/','')
            urlvideo = url
        else:
            print '_4_'
            urlvideo = url.replace('uptostream.com/','uptostream.com/iframe/')
            id_vid = url.split('uptostream.com/iframe/')[1]
            if "?Key=" in id_vid:id_vid = id_vid.split('?Key=')[0].replace('/','')
    print "====================================",id_vid
    return urlvideo,id_vid
def get_video_url(page_url, premium=False, user="", password="", video_password=""):
    print '******************** get url video uptobox,uptostream ********************'
    ch,id_vid = get_urlvid(page_url)
    print "recup_url=",ch
    listvid = []
    s = requests.Session()
    r = s.get(ch,verify=False)
    data = r.content
    rgx = '''"src":"(.+?)","type":".+?","label":"(.+?)","res":".+?","lang":"(.+?)"'''
    vid = re.findall(rgx,data)
    if vid:
        for href,qlt,lang in vid:
            href = href.replace('\\','')
            print href
            w = ('Cool_uptobox '+'( '+qlt+'_'+lang+' )',href)
            listvid.append(w)
    else:
        r = s.get(page_url,verify=False)
        data = r.content
        regx = '''<a href="(.+?)".+?>.+?Click here to start your download.+?</a>'''
        vid = re.findall(regx,data,re.S)
        #print data
        print 'vid__',vid
        if vid:
            w = ('Cool_uptobox '+'( '+'Download'+' )',vid[0])
            listvid.append(w)
        else:
            url2 ="https://uptostream.com/api/streaming/source/get?token=null&file_code="+str(id_vid)
            print "TTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTT",url2
            Html = S.get(url2,verify=False).content
            listvid = decodeur1(Html)
    return listvid

