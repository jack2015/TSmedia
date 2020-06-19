# Embedded file name: /usr/lib/enigma2/python/Plugins/Extensions/TSmedia/scripts/script.module.main/lib/uTools.py
import urllib, urllib2, re, sys, os, ast, json
from iTools import CBaseAddonClass, printD, printE
pluginhandle = int(sys.argv[1])
default_params = '&order=date'
print 'defaultParams', default_params
from Components.config import config
try:
  
    youtube_apiKey=config.TSmedia.youtube_apiKey.value
except:
   youtube_apiKey='AIzaSyA6qqSPugRjEHPTz89EaoBqSp3FxjyOSR8'

KEYV3 = youtube_apiKey

class uTools(CBaseAddonClass):

    def __init__(self):
        CBaseAddonClass.__init__(self, {'cookie': 'uTools.cookie',
         'module_path': __file__})
        self.USER_AGENT = 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:40.0) Gecko/20100101 Firefox/40.0'
        self.MAIN_URL = 'http://youtube.com'
        self.HEADER = {'User-Agent': self.USER_AGENT,
         'DNT': '1',
         'Accept': 'text/html',
         'Accept-Encoding': 'gzip, deflate',
         'Referer': self.getMainUrl(),
         'Origin': self.getMainUrl()}
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

    def getchannelid(self, chusername):
        url = 'https://www.googleapis.com/youtube/v3/channels?part=id&forUsername=%s&key=%s' % (chusername, KEYV3)
        content = self.getPage(url)
        list1 = []
        if content:
            data = json.loads(content)
            channelId = str(data['items'][0]['id'])
            return channelId

    def mainmenu(self, list1):
        for item in list1:
            try:
                mode = item[2]
            except:
                mode = 1001

            try:
                pic = item[3]
            except:
                pic = ''

            try:
                page = item[5]
            except:
                page = ''

            try:
                dialog = item[6]
            except:
                dialog = None

            self.addDir(item[0], item[1], mode, pic, '', page, dialog=dialog)

        return

    def gettotalresults(self, url):
        list1 = []
        content = self.getPage(url)
        if content.startswith('Error'):
            return '0'
        data = json.loads(content)
        print data
        if data:
            totalResults = data.get('pageInfo')['totalResults']
            return str(totalResults)
        else:
            return '0'

    def submenu(self, name, chid, page = ''):
        url = 'https://www.googleapis.com/youtube/v3/search?part=snippet&type=playlist&channelId=' + chid + '&maxResults=11' + default_params + '&key=' + KEYV3
        printD('urlvv', url)
        pcount = str(self.gettotalresults(url))
        url = 'https://www.googleapis.com/youtube/v3/search?part=snippet&type=video&channelId=' + chid + '&maxResults=11' + default_params + '&key=' + KEYV3
        vcount = str(self.gettotalresults(url))
        if int(pcount) > 0 and int(vcount) == 0:
            self.addDir('\\c0000??00 ' + 'Playlists(' + pcount + ')', url, 0, 'img/playlist.png', name, '')
            url = 'https://www.googleapis.com/youtube/v3/search?part=snippet&type=playlist&channelId=' + chid + '&maxResults=11' + default_params + '&key=' + KEYV3
            getviedoList(name, url, page)
        if int(pcount) == 0 and int(vcount) > 0:
            self.addDir('\\c0??????? Videos(' + vcount + ')', url, 0, 'img/video.png', name, '')
            url = 'https://www.googleapis.com/youtube/v3/search?part=snippet&type=video&channelId=' + chid + '&maxResults=11' + default_params + '&key=' + KEYV3
            getviedoList(name, url, page)
        if int(pcount) > 0 and int(vcount) > 0:
            url = 'https://www.googleapis.com/youtube/v3/search?part=snippet&type=playlist&channelId=' + chid + '&maxResults=11' + default_params + '&key=' + KEYV3
            self.addDir('\\c0000??00 ' + 'Playlists(' + pcount + ')', url, 1002, 'img/playlist.png', name, '')
            url = 'https://www.googleapis.com/youtube/v3/search?part=snippet&type=video&channelId=' + chid + '&maxResults=11' + default_params + '&key=' + KEYV3
            self.addDir('\\c0??????? Videos(' + vcount + ')', url, 1002, 'img/video.png', name, '')
        if int(pcount) == 0 and int(vcount) == 0:
            self.addDir('Error:No videos or playlists in channel', url, 0, 'img/error.png', name, '')

    def getviedoList(self, name1, urlmain, page = ''):
        print 'page', page
        if page == '':
            url_page = urlmain
        else:
            url_page = urlmain + '&pageToken=' + str(page).strip()
        print 'url_page', url_page
        content = self.getPage(url_page)
        if content is None:
            self.addDir('Error:downoad error', '', 1, '', '', section=name1)
            return
        else:
            data = json.loads(content)
            c4_browse_ajax = str(data.get('nextPageToken', ''))
            a = 0
            l = len(data)
            if l < 1:
                self.addDir('No contents / results found!', '', 1, '', '')
                return
            print 'data', data
            list_item = 'ItemList' in data['kind']
            for item in data.get('items', {}):
                if not list_item:
                    kind = item['id']['kind']
                else:
                    kind = item['kind']
                if kind:
                    title = item['snippet']['title'].encode('utf-8')
                    desc = item['snippet']['description'].encode('utf-8', 'ignore').replace('&', '_').replace(';', '')
                    if kind.endswith('#video'):
                        try:
                            url = str(item['id']['videoId'])
                            img = str(item['snippet']['thumbnails']['default']['url'])
                            print 'url', url
                            stream_link = 'plugin://plugin.video.youtube/?action=play_video&videoid=%s' % url
                            self.addDir('\\c0??????? ' + title, stream_link, 1004, img, name1, '', link=True, desc=desc)
                        except:
                            continue

                    elif kind.endswith('#playlistItem'):
                        try:
                            url = str(item['snippet']['resourceId']['videoId'])
                            img = str(item['snippet']['thumbnails']['default']['url'])
                            url = 'plugin://plugin.video.youtube/?action=play_video&videoid=%s' % url
                            self.addDir(title, url, 1004, img, name1, '', desc=desc)
                        except:
                            pass

                    elif kind.endswith('#channel'):
                        url = str(item['id']['channelId'])
                        try:
                            img = str(item['snippet']['thumbnails']['default']['url'])
                        except:
                            img = ''

                        url = 'https://www.googleapis.com/youtube/v3/search?part=snippet&type=video&channelId=' + url + '&maxResults=11' + default_params + '&key=' + KEYV3
                        self.addDir(title, url, 1002, img, name1, '', desc=desc)
                    elif kind.endswith('#playlist'):
                        url = str(item['id']['playlistId'])
                        try:
                            img = str(item['snippet']['thumbnails']['default']['url'])
                        except:
                            img = ''

                        url = 'https://www.googleapis.com/youtube/v3/playlistItems?part=snippet&playlistId=' + url + '&maxResults=11' + default_params + '&key=' + KEYV3
                        self.addDir(title, url, 1002, img, name1, '', desc=desc)

            if not c4_browse_ajax == '':
                self.addDir('next page>', urlmain, 1002, '', '', c4_browse_ajax)
            return
            return

    def getplayList(self, name1, urlmain, page = ''):
        print 'mahmou1', urlmain
        print 'page', page
        if page == '':
            urlmain = 'https://www.googleapis.com/youtube/v3/search?part=snippet&type=playlist&channelId=' + urlmain + '&maxResults=11' + default_params + '&key=' + KEYV3
            url_page = urlmain
        else:
            url_page = urlmain + '&pageToken=' + page
        print 'url_page', url_page
        content = self.getPage(url_page)
        if content is None:
            self.addDir('Error:downoad error', '', 1, '', '')
            return
        else:
            data = json.loads(content)
            c4_browse_ajax = str(data.get('nextPageToken', ''))
            a = 0
            l = len(data)
            if l < 1:
                self.addDir('No contents / results found!', '', 1, '', '')
                return
            list_item = 'ItemList' in data['kind']
            for item in data.get('items', {}):
                if not list_item:
                    kind = item['id']['kind']
                else:
                    kind = item['kind']
                if kind:
                    title = item['snippet']['title'].encode('utf-8')
                    desc = item['snippet']['description'].encode('utf-8').replace('&', '_').replace(';', '')
                    if kind.endswith('#video'):
                        try:
                            url = str(item['id']['videoId'])
                            img = str(item['snippet']['thumbnails']['default']['url'])
                            print 'url', url
                            stream_link = 'plugin://plugin.video.youtube/?action=play_video&videoid=%s' % url
                            self.addDir(title + '_' + desc, stream_link, 1004, img, name1, '', link=True, desc=desc)
                        except:
                            continue

                    elif kind.endswith('#playlistItem'):
                        try:
                            url = str(item['snippet']['resourceId']['videoId'])
                            img = str(item['snippet']['thumbnails']['default']['url'])
                            url = 'plugin://plugin.video.youtube/?action=play_video&videoid=%s' % url
                            self.addDir(title, url, 1004, img, name1, '', desc=desc)
                        except:
                            pass

                    elif kind.endswith('#channel'):
                        url = str(item['id']['channelId'])
                        img = str(item['snippet']['thumbnails']['default']['url'])
                        url = 'https://www.googleapis.com/youtube/v3/search?part=snippet&type=video&channelId=' + url + '&maxResults=12' + default_params + '&key=' + KEYV3
                        self.addDir(title, url, 1002, img, name1, '', desc=desc)
                    elif kind.endswith('#playlist'):
                        url = str(item['id']['playlistId'])
                        img = str(item['snippet']['thumbnails']['default']['url'])
                        url = 'https://www.googleapis.com/youtube/v3/playlistItems?part=snippet&playlistId=' + url + '&maxResults=12' + default_params + '&key=' + KEYV3
                        self.addDir(title, url, 1002, img, name1, '', desc=desc)

            if not c4_browse_ajax == '':
                self.addDir('next page>', urlmain, 1002, img, desc, c4_browse_ajax)
            return
            return

    def getmode(self, url):
        if url and url.endswith('/'):
            url = url[:-1]
        if 'videoid=' in url:
            url = url.split('videoid=')[1]
            return (url, 1007)
        if 'channelid=' in url:
            url = url.split('channelid=')[1]
            return (url, 1001)
        if '/channel/' in url:
            url = os.path.split(url)[1]
            return (url, 1001)
        if '/user/' in url:
            url = os.path.split(url)[1]
            return (url, 1005)
        if 'channel_id=' in url:
            url = url.split('channel_id=')[1]
            if '&' in url:
                url = url.split('&')[0]
            return (url, 1001)
        if 'userchannel=' in url:
            url = url.split('userchannel=')[1]
            return (url, 1005)
        if 'user_channel=' in url:
            url = url.split('user_channel=')[1]
            if '&' in url:
                url = url.split('&')[0]
            return (url, 1005)
        if 'playlistid=' in url:
            url = url.split('playlistid=')[1]
            return (url, 1006)
        if 'playlist_id=' in url:
            url = url.split('playlist_id=')[1]
            if '&' in url:
                url = url.split('&')[0]
            return (url, 1006)
        if '/playlist/' in url:
            url = os.path.split(url)[1]
            return (url, 1006)
        if 'video_id=' in url:
            url = url.split('video_id=')[1]
            if '&' in url:
                url = url.split('&')[0]

    def getlist(self, url = None, name = None):
        print 'url', url
        if url is not None and url.startswith('plugin:'):
            url, mode = getmode(url)
            print 'url,mode', url, mode
        else:
            return
        if mode == None:
            mainmenu(list1)
        elif mode == 1001:
            submenu(name, url, '')
        elif mode == 1002:
            print 'url444', url
            getviedoList(name, url, page)
        elif mode == 1003:
            getplayList(name, url, page)
        elif mode == 1004:
            if not url.startswith('plugin://'):
                url = 'plugin://plugin.video.youtube/?action=play_video&videoid=' + url
            self.addDir('link', url, 1007, '', name, 1, link=True)
        elif mode == 1005:
            print '', url
            chid = getchannelid(url)
            submenu(name, chid, page='')
        elif mode == 1006:
            print 'url', url
            url = 'https://www.googleapis.com/youtube/v3/playlistItems?part=snippet&playlistId=' + url + '&maxResults=11&order=date&key=' + KEYV3
            name = 'playlist'
            page = ''
            getviedoList(name, url, page)
        elif mode == 1007:
            if not url.startswith('plugin://'):
                url = 'plugin://plugin.video.youtube/?action=play_video&videoid=' + url
            print 'url', url, mode
            self.addDir('link', url, 1007, '', name, 1, link=True)
        return

    def run(self, list1 = []):
        params = self.get_params()
        print 'paramsxxx', params
        url = None
        name = None
        mode = None
        page = ''
        print 'url', url
        print 'mode', mode
        try:
            url = urllib.unquote_plus(params['url'])
        except:
            pass

        try:
            name = urllib.unquote_plus(params['name'])
        except:
            pass

        try:
            mode = int(params['mode'])
        except:
            pass

        try:
            page = str(params['page'])
        except:
            pass

        print 'Mode: ' + str(mode)
        print 'URL: ' + str(url)
        print 'Name: ' + str(name)
        print 'page: ' + str(page)
        if type(url) == type(str()):
            url = urllib.unquote_plus(url)
        if url is not None and url.startswith('plugin:'):
            url, mode = getmode(url)
            print 'url,mode', url, mode
        if mode == None:
            self.mainmenu(list1)
        elif mode == 1001:
            self.submenu(name, url, '')
        elif mode == 1002:
            print 'url', url
            self.getviedoList(name, url, page)
        elif mode == 1003:
            self.getplayList(name, url, page)
        elif mode == 1004:
            if not url.startswith('plugin://'):
                url = 'plugin://plugin.video.youtube/?action=play_video&videoid=' + url
            self.addDir(name, url, 1007, '', '', 1, link=True)
        elif mode == 1005:
            print '', url
            chid = self.getchannelid(url)
            self.submenu(name, chid, page='')
        elif mode == 1006:
            print 'url', url
            url = 'https://www.googleapis.com/youtube/v3/playlistItems?part=snippet&playlistId=' + url + '&maxResults=11&order=date&key=' + KEYV3
            name = 'playlist'
            page = ''
            self.getviedoList(name, url, page)
        elif mode == 1007:
            if not url.startswith('plugin://'):
                url = 'plugin://plugin.video.youtube/?action=play_video&videoid=' + url
            self.addDir(name, url, 1007, '', '', 1, link=True)
        elif mode == 103:
            search_txt = self.getsearchtext(marker='+')
            print 'searchtext', search_txt
            url = 'https://www.googleapis.com/youtube/v3/search?part=snippet&type=video&channelId=' + url + '&q=' + search_txt + '&maxResults=11&key=' + KEYV3
            name = 'Search'
            page = ''
            self.getviedoList(name, url, page)
        elif mode == 1009:
            search_txt = self.getsearchtext(marker='+')
            url = self.getchannelid(url)
            url = 'https://www.googleapis.com/youtube/v3/search?part=snippet&type=video&channelId=' + url + '&q=' + search_txt + '&maxResults=11&key=' + KEYV3
            name = 'Search'
            page = ''
            self.getviedoList(name, url, page)
        elif mode == 1000:
            if not url.startswith('plugin://'):
                url = 'plugin://plugin.video.youtube/?action=play_video&videoid=' + url
            self.getlist(url, name)
        return
