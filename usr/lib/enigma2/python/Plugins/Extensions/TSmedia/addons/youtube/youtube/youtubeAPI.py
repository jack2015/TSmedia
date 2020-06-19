# Embedded file name: /usr/lib/enigma2/python/Plugins/Extensions/TSmedia/addons/youtube/youtube/youtubeAPI.py
import sys
import urllib, urllib2, re, os, ast
from iTools import CBaseAddonClass, printD, printE, AppPath, getCachePath, cleanTitle, enigmaos, AppPath
import json
from Components.config import config
try:
    api_key = config.TSmedia.youtube_apiKey.value
    KEYV3 = api_key.strip()
except:
    try:
        dlocation = config.TSmedia.downloadlocation.value.strip()
        youtube_apiKey = open(dlocation + '/TSmedia/youtube_apikey').read().strip()
    except:
        youtube_apiKey = 'AIzaSyA6qqSPugRjEHPTz89EaoBqSp3FxjyOSR8'

    KEYV3 = api_key.strip()

auth_tok_file = '/tmp/auth_tok'
baseurl = 'https://www.youtube.com/'
std_headers = {'User-Agent': 'Mozilla/5.0 (X11; U; Linux x86_64; en-US; rv:1.9.2.6) Gecko/20100627 Firefox/3.6.6',
 'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.7',
 'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
 'Accept-Language': 'en-us,en;q=0.5'}
default_params = '&order=date'
print 'defaultParams', default_params
from Components.config import config
dlocation = config.TSmedia.downloadlocation.value
tubecache = AppPath + '/media/hdd'
access_token_file = tubecache + '/yt_access_token'
refresh_token_file = tubecache + '/yt_refresh_token'
enigmaos = enigmaos()

def reqData(url, headers = {}, params = None):
    import requests
    ses = requests.Session()
    if params:
        try:
            print 'heades', headers
            res = ses.post(url, headers=headers, params=params, verify=False, timeout=5)
            print 'res.status_code', res.status_code
            if res.status_code == 200:
                 
                return res.content
            e = res.raise_for_status()
            print 'error', e
            printD('Download error', e)
            return ''
        except requests.exceptions.RequestException as e:
            printD('Download error', str(e))
            printE()
            return ''

    else:
        try:
            res = ses.get(url, headers=headers, verify=False, timeout=5)
            if res.status_code == 200:
                return res.content
            e = res.raise_for_status()
            print 'error', e
            printD('Download error', e)
            return ''
        except requests.exceptions.RequestException as e:
            printD('Download error', str(e))
            printE()
            return ''


def getSettings():
 

    try:
        param_metalang = config.TStube.lang.value
    except:
        param_metalang = ''

    try:
        param_regionid = config.TStube.region.value
    except:
        param_regionid = ''

    try:
        param_duration = config.TStube.paraduration.value
    except:
        param_duration = ''

    try:
        order=config.TSmedia.youtubeSortBy.value
         
        if order=='':
            order='date'
        param_frequency = '&order=' + order
    except:
        printE()
        param_frequency = '&order=date'

    try:
        param_3d = config.TStube.para3d.value
    except:
        param_3d = ''

    try:
        safesearch = config.TStube.safesearch.value
    except:
        safesearch = '&safeSearch=none'

    return param_metalang + param_metalang + param_regionid + param_3d + param_frequency + safesearch


default_params = getSettings()
uParams = '&maxResults=45' + default_params + '&key=' + KEYV3
uParams2 = uParams.replace('order=viewCount', 'order=relevance')
 

class youtubeAPI(CBaseAddonClass):

    def __init__(self):
        CBaseAddonClass.__init__(self, {'cookie': 'youtube.cookie'})
        self.videoList = []
        self.USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:74.0) Gecko/20100101 Firefox/74.0'
        self.MAIN_URL = 'http://www.googleapis.com'
        self.HEADER = {'User-Agent': self.USER_AGENT,
         'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.7',
         'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
         'Accept-Language': 'en-us,en;q=0.5',
         'Referer': self.getMainUrl(),
         'Origin': 'http://www.googleapis.com'}
        self.AJAX_HEADER = dict(self.HEADER)
        self.AJAX_HEADER.update({'X-Requested-With': 'XMLHttpRequest',
         'Accept-Encoding': 'gzip, deflate',
         'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
         'Accept': 'application/json, text/javascript, */*; q=0.01'})
        self.cacheLinks = {}
        self.defaultParams = {'header': self.HEADER,
         'raw_post_data': True,
         'use_cookie': True,
         'load_cookie': True,
         'save_cookie': True,
         'cookiefile': self.COOKIE_FILE}

    def youtube_error(self, msg = ''):
        name = 'Error:%s' % msg
        url = ''
        mode = -1
        image = 'error.png'
        category = ''
        page = ''
        desc = ''
        extra = {}
        info = {'name': name,
         'url': url,
         'mode': mode,
         'image': image,
         'category': category,
         'page': page,
         'desc': desc,
         'extra': extra}
        return info

    def dInfo(self, name, url, mode, image, category, page = '', desc = '', extra = {}, dialog = ''):
        if '&' in name:
            name = name.split('&')[0]
        if '&' in desc:
            desc = desc.split('&')[0]
        info = {'name': name,
         'url': url,
         'mode': mode,
         'image': image,
         'category': category,
         'page': page,
         'desc': desc,
         'extra': extra,
         'dialog': dialog}
        self.videoList.append(info)

    def getaccesstoken(self):
        try:
            access_token = open(access_token_file).read()
            refresh_token = open(refresh_token_file).read()
            return (access_token, refresh_token)
        except:
            #printE()
            return ('', '')

    def getchannelsubmenu(self, cParams):
        main_title = cParams.get('name', '')

        def gettotalresults(url):
            list1 = []
            content = self.getPage(url)
             
            if content.startswith('Error'):
                return '0'
            data = json.loads(content)
            channelTitle = ''
            if data:
                totalResults = data.get('pageInfo')['totalResults']
                for item in data.get('items', {}):
                    channelId = item['snippet'].get('channelId', '')
                    channelTitle = item['snippet'].get('channelTitle', '')

                return (str(totalResults), channelTitle)
            else:
                return ('0', '')

        list1 = []
        chid = cParams.get('url', '')
        try:
            param_frequency = config.TStube.feed.value
        except:
            param_frequency = ''

        url = 'https://www.googleapis.com/youtube/v3/search?part=snippet&type=video&channelId=' + chid + uParams
        totalresults, channelTitle = gettotalresults(url)
        title = main_title + self.colorize(' videos(' + str(totalresults) + ')')
        self.dInfo(title, url, 100, 'img/video.png', main_title, '', desc='', extra={})
        url = 'https://www.googleapis.com/youtube/v3/search?part=snippet&type=playlist&channelId=' + chid + uParams
        totalresults, channelTitle = gettotalresults(url)
        title = main_title + self.colorize(' playlists(' + str(totalresults) + ')')
        self.dInfo(title, url, 100, 'img/playlist.png', main_title, '', desc='', extra={})

    def get_recommended(self, cParams):
        main_title = cParams.get('name', '')
        url = 'https://www.youtube.com/'
        data = self.getPage(url)
        printD("data",data)
        if data == '':
            return self.youtube_error('Download error')
        blocks = data.split('class="yt-lockup-title')
        i = 0
        list1 = []
        printD("blocks",len(blocks))
        for block in blocks:
            i = i + 1
            if i == 1:
                continue
            print 'blcokd', block
            regx = 'href="(.*?)"'
            try:
                href = re.findall(regx, block)[0]
            except:
                continue

            href = href.split('v=')[1]
            image = 'http://img.youtube.com/vi/' + href + '/default.jpg'
            href = 'plugin://plugin.video.youtube/?action=play_video&videoid=' + href
            regx = 'title="(.*?)"'
            try:
                name = re.findall(regx, block, re.M | re.I)[0]
            except:
                continue

            try:
                name = name.encode('utf-8')
            except:
                name = str(name)

            self.dInfo(name, href, 100, image, main_title, '', desc='', extra={})

    def getbest(self, cParams):
        filter = True
        filterRating = 50
        filterThreshold = 10
        list1 = []
        main_url = cParams.get('url', '')
        page = cParams.get('page', '1')
        main_title = cParams.get('name', ' ')
        main_mode = cParams.get('mode', ' ')
        main_url = 'http://www.bestofyoutube.com/index.php?page=%s' % page
        content = self.getPage(main_url)
        spl = content.split("<div class='main'>")
        for i in range(1, len(spl), 1):
            entry = spl[i]
            match = re.compile('youtube.com/embed/(.+?)"', re.DOTALL).findall(entry)
            id = match[0]
            if '?' in id:
                id = id[:id.find('?')]
            match = re.compile("name='up'>(.+?)<", re.DOTALL).findall(entry)
            up = float(match[0])
            match = re.compile("name='down'>(.+?)<", re.DOTALL).findall(entry)
            down = float(match[0])
            thumb = 'http://img.youtube.com/vi/' + id + '/0.jpg'
            match = re.compile("<div class='title'><a href='/(.+?)'>(.+?)</a>", re.DOTALL).findall(entry)
            title = match[0][1]
            title = cleanTitle(title)
            if up + down > 0:
                percentage = int(up / (up + down) * 100)
            else:
                percentage = 100
            if filter and up + down > filterThreshold and percentage < filterRating:
                continue
            title = title + ' (' + str(percentage) + '%)'
            url = 'plugin://plugin.video.youtube/?action=play_video&videoid=%s' % id
            self.dInfo(title, url, 100, thumb, main_title, '1', desc='', extra={})

        self.dInfo('More', 'best', main_mode, 'img/next.png', main_title, page=str(int(page) + 1), desc='', extra={}, dialog='nextpage')

    def getviedoList(self, cParams):
        default_params = getSettings()
        uParams = '&maxResults=45' + default_params + '&key=' + KEYV3
        uParams2 = uParams.replace('order=viewCount', 'order=relevance')
        main_title = cParams.get('title', '')
        main_url = cParams.get('url', '')
        if 'subscriptions' in main_url:
            main_url = main_url + uParams2
        elif 'key=' not in main_url:
            main_url = main_url + uParams
        printD('mainu url', main_url)
        page = cParams.get('page', '')
        main_mode = cParams.get('mode', 0)
        #main_url = main_url + uParams
         
        if page == '':
            url_page = main_url
        else:
            url_page = main_url + '&pageToken=' + str(page).strip()
        print 'url_page', url_page
        
        content = reqData(url_page, self.HEADER)
        
        if content.strip() == '':
            return self.youtube_error('download error')
        try:
            data = json.loads(content, strict=False)
        except:
            printE()

        c4_browse_ajax = str(data.get('nextPageToken', ''))
        page = c4_browse_ajax
        a = 0
        try:
            TotalResults = int(data.get('pageInfo', 0)['totalResults'])
        except:
            TotalResults = 0

        try:
            resultsPerPage = int(data.get('pageInfo', 0)['resultsPerPage'])
        except:
            resultsPerPage = 0

        etag = data.get('etag', 'none')
        extra = {'TotalResults': TotalResults,
         'resultsperpage': resultsPerPage,
         'etag': etag}
        if TotalResults < 1:
            return self.youtube_error('download error-No contents / results found!')
        list_item = 'ItemList' in data['kind']
        for item in data.get('items', {}):
            try:
                if not list_item:
                    try:
                        kind = item['id']['kind']
                    except:
                        kind = item['kind']

                else:
                    kind = item['kind']
                if kind:
                    title = item['snippet']['title'].encode('utf-8')
                    channelId = item['snippet'].get('channelId', '')
                    channelTitle = item['snippet'].get('channelTitle', '')
                    extra.update({'channelId': channelId,
                     'channelTitle': channelTitle})
                    desc = item['snippet']['description'].encode('utf-8', 'ignore').replace('&', '_').replace(';', '')
                    if kind.endswith('#video'):
                        try:
                            url = str(item['id']['videoId'])
                            img = str(item['snippet']['thumbnails']['default']['url'])
                            print 'url', url
                            stream_link = 'plugin://plugin.video.youtube/?action=play_video&videoid=%s' % url
                            if enigmaos == 'oe2.0':
                                title = '\\c0??????? ' + title
                            self.dInfo(title, stream_link, 0, img, main_title, page, desc=desc, extra=extra)
                        except:
                            continue

                    elif kind.endswith('#playlistItem'):
                        try:
                            url = str(item['snippet']['resourceId']['videoId'])
                            img = str(item['snippet']['thumbnails']['default']['url'])
                            url = 'plugin://plugin.video.youtube/?action=play_video&videoid=%s' % url
                            if enigmaos == 'oe2.0':
                                title = '\\c0??????? ' + title
                            self.dInfo(title, url, 0, img, main_title, page, desc=desc, extra=extra)
                        except:
                            pass

                    elif kind.endswith('#channel'):
                        url = str(item['id']['channelId'])
                        try:
                            img = str(item['snippet']['thumbnails']['default']['url'])
                        except:
                            img = ''

                        if enigmaos == 'oe2.0':
                            title = '\\c0000???? ' + title
                        self.dInfo(title, url, 12, img, main_title, page, desc=desc, extra=extra)
                    elif kind.endswith('#playlist'):
                        try:
                            url = str(item['id']['playlistId'])
                        except:
                            url = str(item['id'])

                        try:
                            img = str(item['snippet']['thumbnails']['default']['url'])
                        except:
                            img = ''

                        if enigmaos == 'oe2.0':
                            title = '\\c0000??00 ' + title
                        url = 'https://www.googleapis.com/youtube/v3/playlistItems?part=snippet&playlistId=' + url
                        self.dInfo(title, url, 100, img, main_title, page, desc=desc, extra=extra)
                    elif kind.endswith('#activity'):
                        try:
                            url = url = str(item['snippet']['channelId'])
                        except:
                            url = str(item['id'])

                        try:
                            img = str(item['snippet']['thumbnails']['default']['url'])
                        except:
                            img = ''

                        if enigmaos == 'oe2.0':
                            title = '\\c0000???? ' + title
                        self.dInfo(title, url, 12, img, main_title, page, desc=desc, extra=extra)
            except:
                printE()

        if not c4_browse_ajax == '':
            self.dInfo('More', main_url, 100, 'img/next.png', main_title, page, desc='', extra={}, dialog='nextpage')

    def getMyChannelData(self, cParams):
        list1 = []
        main_url = cParams.get('url', '')
        main_title = cParams.get('name', '')
        page = cParams.get('page', '')
        main_url = main_url + uParams
        access_token, refresh_token = self.getaccesstoken()
        url_page = main_url
        printD('url_page', url_page)
        content = self.getPage(url_page)
        try:
            data = json.loads(content)
            totalResults = data.get('pageInfo')['totalResults']
        except:
            printE()
            self.youtube_error('Please refresh login')
            title = 'Refresh login'
            url = ''
            mode = 20
            image = 'img/signin.png'
            page = ''
            desc = ''
            extra = {}
            self.dInfo(title, url, mode, image, 'my channel', page, desc=desc, extra=extra)
            title = 'New login'
            url = ''
            mode = 20
            image = 'img/signin.png'
            page = ''
            desc = ''
            self.dInfo(title, url, mode, image, 'my channel', page, desc=desc, extra=extra)
            return

        a = 0
        l = len(data)
        if int(totalResults) < 1:
            addDir('No contents / results found!', '', 1, '', '')
            self.dInfo('No contents / results found!', '', -1, '', 'my channel', '', desc='', extra='')
            return
        for item in data.get('items', {}):
            kind = item['kind']
            if not kind == 'youtube#channel':
                continue
            channelid = item['id']
            contentDetails = item['contentDetails']
            if contentDetails:
                favorites_id = item['contentDetails']['relatedPlaylists']['favorites']
                uploads_id = item['contentDetails']['relatedPlaylists']['uploads']
                watchHistory_id = item['contentDetails']['relatedPlaylists']['watchHistory']
                watchLater_id = item['contentDetails']['relatedPlaylists']['watchLater']
                likes_id = item['contentDetails']['relatedPlaylists']['likes']
                url = 'https://www.googleapis.com/youtube/v3/playlists?part=snippet&mine=true&' + '&access_token=' + self.access_token
                self.dInfo('playlists', url, 100, 'img/playlists.png', main_title, page, desc='', extra={})
                url = 'https://www.googleapis.com/youtube/v3/subscriptions?part=snippet&mine=true&' + '&access_token=' + self.access_token
                self.dInfo('Subscriptions', url, 100, 'img/subscriptions.png', main_title, page, desc='', extra={})
                url = 'https://www.googleapis.com/youtube/v3/activities?part=snippet,id,contentDetails&home=true&forMine=true' + '&access_token=' + self.access_token
                self.dInfo('Activities', url, 100, 'img/activities.png', main_title, page, desc='', extra={})
                url = 'https://www.googleapis.com/youtube/v3/playlistItems?part=snippet,contentDetails,status&playlistId=' + favorites_id + '&mine=true' + '&access_token=' + self.access_token
                self.dInfo('Favorites', url, 100, 'img/favorites.png', main_title, page, desc='', extra={})
                url = 'https://www.googleapis.com/youtube/v3/playlistItems?part=snippet,contentDetails,status&playlistId=' + uploads_id + '&mine=true' + '&access_token=' + self.access_token
                self.dInfo('My uploads', url, 100, 'img/myuploads.png', main_title, page, desc='', extra={})
                url = 'https://www.googleapis.com/youtube/v3/playlistItems?part=snippet,contentDetails,status&playlistId=' + likes_id + '&mine=true' + '&access_token=' + self.access_token
                self.dInfo('likes', url, 108, 'img/likes.png', main_title, page, desc='', extra={})
                url = 'https://www.googleapis.com/youtube/v3/playlistItems?part=snippet,contentDetails,status&playlistId=' + watchLater_id + '&mine=true' + '&access_token=' + self.access_token
                self.dInfo('WatchLater', url, 100, 'img/watch_later.png', main_title, page, desc='', extra={})
                url = 'https://www.googleapis.com/youtube/v3/playlistItems?part=snippet,contentDetails,status&playlistId=' + watchLater_id + '&mine=true' + '&access_token=' + self.access_token
                self.dInfo('Sign out', url, 106, 'img/signout.png', main_title, page, desc='', extra={})
