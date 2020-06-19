import base64
import hashlib,urllib
import json
import time
import requests
FF_USER_AGENT='Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:77.0) Gecko/20100101 Firefox/77.0'
ua = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.103 Safari/537.36'
class strwithmeta(str):
    def __new__(cls,value,meta={}):
        obj = str.__new__(cls, value)
        obj.meta = {}
        if isinstance(value, strwithmeta):
            obj.meta = dict(value.meta)
        else:
            obj.meta = {}
        obj.meta.update(meta)
        return obj

def append_headers(headers):
    return '|%s' % '&'.join(['%s=%s' % (key, urllib.quote_plus(headers[key])) for key in headers])
def get_media_url(media_id):
        referer = 'https://tune.pk/video/%s' % media_id
        vids = ''
        apiurl = 'https://api.tune.pk/v3/videos/{}'.format(media_id)
        currentTime = time.time()
        x_req_time = time.strftime('%a, %d %b %Y %H:%M:%S GMT',time.gmtime(currentTime))
        tunestring = 'videos/{} . {} . KH42JVbO'.format(media_id, int(currentTime))
        token = hashlib.sha1(tunestring).hexdigest()
        headers = {'Content-Type': 'application/json; charset=utf-8',
                   'User-Agent': FF_USER_AGENT,
                   'X-KEY': '777750fea4d3bd585bf47dc1873619fc',
                   'X-REQ-TIME': x_req_time,
                   'X-REQ-TOKEN': token}
        response = requests.get(apiurl, headers=headers)
        jdata = json.loads(response.content)
        if jdata['message'] == 'OK':
            vids = jdata['data']['videos']['files']
            sources = []
            for key in vids.keys():
                a = ""
                sources.append((vids[key]['label'], vids[key]['file']))
        sources.reverse()
        serverTime = long(jdata['timestamp']) + (int(time.time()) - int(currentTime))
        hashLifeDuration = long(jdata['data']['duration']) * 5
        if hashLifeDuration < 3600:
            hashLifeDuration = 3600
        expiryTime = serverTime + hashLifeDuration
        for elm in sources:
            video_url = elm[1]
            titre = elm[0]
            try:
                startOfPathUrl = video_url.index('/files/videos/')
                #print "====",startOfPathUrl
                pathUrl = video_url[startOfPathUrl:None]
                #print "====",pathUrl
            except ValueError:
                pass
            htoken = hashlib.md5(str(expiryTime) + pathUrl + ' ' + 'c@ntr@lw3biutun3cb').digest()
            htoken = base64.urlsafe_b64encode(htoken).replace('=', '').replace('\n', '')
            headers = {'Referer': referer, 'User-Agent': ua}
            urll=video_url + '?h=' + htoken + '&ttl=' + str(expiryTime)
            urll = strwithmeta(urll,headers)
            print urll
media_id = '8769971'
print get_media_url(media_id)
