# Embedded file name: /usr/lib/enigma2/python/Plugins/Extensions/TSmedia/addons/youtube/youtube/default.py
import sys
import urllib, urllib2, re, os, ast
from iTools import printD, printE
from youtubeAPI import youtubeAPI
import json
from Components.config import config
dlocation=config.TSmedia.downloadlocation.value
userFile=dlocation+"/TSmedia/youtube_user"

KEYV3 = 'AIzaSyACH1YzEacUk9Y_k2L7tLZPEFxQEZ7k-II'
api_key = 'AIzaSyDn2w07I3D8xNQ9D-QcY5t3n0JZ7RW8J8c'
auth_tok_file = '/tmp/auth_tok'
baseurl = 'https://www.youtube.com'
std_headers = {'User-Agent': 'Mozilla/5.0 (X11; U; Linux x86_64; en-US; rv:1.9.2.6) Gecko/20100627 Firefox/3.6.6',
 'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.7',
 'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
 'Accept-Language': 'en-us,en;q=0.5'}
def readUserFile(group='video'):
        listTab=[]
        try:
            if not os.path.exists(userFile):
                
                return []
            lines = open(userFile).readlines()            
            
            for line in lines:
                line = line.strip()
                if not line == '' and ':' in line:
                    items= line.split(':')
                    if group in items[0].strip().lower():
                        
                        itemTitle=items[1]
                        itemID=items[2]
                        if len(items)>3:
                            itemImage=items[3] 
                        else:
                            itemImage="img/%s.png"%group
                        listTab.append((itemTitle,itemID,itemImage))
        except:
            printE()
        return listTab                        

class youtube(youtubeAPI):

    def __init__(self):
        youtubeAPI.__init__(self)
        self.USER_AGENT = 'Mozilla/5.0 (X11; U; Linux x86_64; en-US; rv:1.9.2.6) Gecko/20100627 Firefox/3.6.6'
        self.MAIN_URL = 'https://www.youtube.com'
        self.HEADER = {'User-Agent': self.USER_AGENT,
         'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.7',
         'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
         'Accept-Language': 'en-us,en;q=0.5',
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
        self.access_token, self.refresh_token = self.getaccesstoken()

    def showmenu(self):
        baseurl = self.getMainUrl()
        self.addDir('search', baseurl, 103, 'img/search.png', '', '', searchall=__file__)
        self.addDir('Categories', baseurl, 11, 'img/categories.png', '', '')
        self.addDir('Channels', 'https://www.googleapis.com/youtube/v3/search?part=snippet&q=&type=channel', 100, 'img/channels.png', '', '')
        self.addDir('My Channels', 'https://www.googleapis.com/youtube/v3/channels?part=contentDetails&mine=true', 13, 'img/channels.png', '', '')
        self.addDir('Live Channels', 'https://www.googleapis.com/youtube/v3/search?part=snippet&q=&type=video&eventType=live', 100, 'img/live.png', '', '')
        self.addDir('Popular Channels', 'https://www.googleapis.com/youtube/v3/search?part=snippet&type=video,playlist&channelId=UCF0pVplsI8R5kcAqgtoRqoA', 100, 'img/popular.png', '', '')
        self.addDir('Playlists', 'https://www.googleapis.com/youtube/v3/search?part=snippet&q=&type=playlist', 100, 'img/popular.png', '', '')
        self.addDir('Best of Youtube', 'best', 14, 'img/popular.png', '', 1)

    def search(self, cParams = {}):
        sterm = cParams.get('sterm', '')
        page = cParams.get('page', '')
        surl = 'https://www.googleapis.com/youtube/v3/search?part=snippet&q=' + sterm + '&type=video,channel,playlist'
        if not page == '':
            page_url = 'https://www.googleapis.com/youtube/v3/search?part=snippet&q=' + sterm + '&type=video,channel,playlist&pageToken=%s' % page
        else:
            page_url = surl
        cParams.update({'url': page_url})
        self.getviedoList(cParams)
        for item in self.videoList:
            print 'item', item['mode']
            name = item.get('name', '')
            url = item.get('url', '')
            mode = item.get('mode', '')
            image = item.get('image', '')
            category = item.get('category', '')
            page = item.get('page', '')
            desc = item.get('desc', '')
            extra = item.get('extra', {})
            maintitle = item.get('maintitle', False)
            self.addDir(name, url, mode, image, category, page, maintitle, link=False, desc=desc, extra=extra)

    def getMainCats(self, cParams):
        self.addDir('All', 'https://www.googleapis.com/youtube/v3/search?part=snippet&q=&type=video', 100, 'img/playlists.png', 'Categories', '')
        self.addDir('Film', 'https://www.googleapis.com/youtube/v3/search?part=snippet&q=&type=video&videoCategoryId=30', 100, 'img/movies.png', 'Categories', '')
        self.addDir('Music', 'https://www.googleapis.com/youtube/v3/search?part=snippet&q=&type=video&videoCategoryId=10', 100, 'img/music.png', 'Categories', '')
        self.addDir('Autos', 'https://www.googleapis.com/youtube/v3/search?part=snippet&q=&type=video&videoCategoryId=2', 100, 'img/autos.png', 'Categories', '')
        self.addDir('Animals', 'https://www.googleapis.com/youtube/v3/search?part=snippet&q=&type=video&videoCategoryId=15', 100, 'img/animals.png', 'Categories', '')
        self.addDir('Sports', 'https://www.googleapis.com/youtube/v3/search?part=snippet&q=&type=video&videoCategoryId=17', 100, 'img/sports.png', 'Categories', '')
        self.addDir('Travels', 'https://www.googleapis.com/youtube/v3/search?part=snippet&q=&type=video&videoCategoryId=19', 100, 'img/travels.png', 'Categories', '')
        self.addDir('people', 'https://www.googleapis.com/youtube/v3/search?part=snippet&q=&type=video&videoCategoryId=22', 100, 'img/people.png', 'Categories', '')
        self.addDir('Comedy', 'https://www.googleapis.com/youtube/v3/search?part=snippet&q=&type=video&videoCategoryId=34', 100, 'img/comedy.png', 'Categories', '')
        self.addDir('Entertainment', 'https://www.googleapis.com/youtube/v3/search?part=snippet&q=&type=video&videoCategoryId=24', 100, 'img/entertainment.png', 'Categories', '')
        self.addDir('News', 'https://www.googleapis.com/youtube/v3/search?part=snippet&q=&type=video&videoCategoryId=25', 100, 'img/news.png', 'Categories', '')
        self.addDir('Eduation', 'https://www.googleapis.com/youtube/v3/search?part=snippet&q=&type=video&videoCategoryId=27', 100, 'img/education.png', 'Categories', '')
        self.addDir('Technology', 'https://www.googleapis.com/youtube/v3/search?part=snippet&q=&type=video&videoCategoryId=28', 100, 'img/technology.png', 'Categories', '')

    def getRecommeded(self, cParams):
        self.addDir('Recommended videos', 'https://www.googleapis.com/youtube/v3/search?part=snippet&q=&type=video', 15, 'img/recommended.png', 'Categories', '')
        self.addDir('Vevo', 'https://www.googleapis.com/youtube/v3/search?part=snippet&type=video&channelId=UC2pmfLm7iq6Ov1UwYrWYkZA', 100, 'img/vevo.png', 'Categories', '')
        self.addDir('Top Music', 'https://www.googleapis.com/youtube/v3/search?part=snippet&type=video&channelId=UCqmHXdMF817v4_1xreTw6sQ', 100, 'img/music.png', 'Categories', '')
        self.addDir('4k relaxation', 'https://www.googleapis.com/youtube/v3/search?part=snippet&type=video&channelId=UCg72Hd6UZAgPBAUZplnmPMQ', 100, 'img/4k.png', 'Categories', '')
        self.addDir('JustForLaughsTV', 'https://www.googleapis.com/youtube/v3/search?part=snippet&type=video&channelId=UCpsSadsgX_Qk9i6i_bJoUwQ', 100, 'img/justforlaughs.png', 'Categories', '')

    def getUserlists(self, cParams):
        main_title = cParams.get('name', '')
        self.addDir('User Playlists', '', 18, 'img/playlist', main_title, '1', desc="Put  %s id in %s"%("playlist",userFile), extra={})
        self.addDir('User Channels', '', 19, 'img/channel.png', main_title, '1', desc="Put  %s id in %s"%("channel",userFile), extra={})
        self.addDir('User videos', '', 20, 'img/video.png', main_title, '1',  desc="Put  %s id in %s"%("video",userFile), extra={})
    def getUserPlaylists(self,cParams):
                        listTab=readUserFile('playlist')
                        
                        for item in listTab:
                             href = 'https://www.googleapis.com/youtube/v3/playlistItems?part=snippet&playlistId=%s'%item[1]                   
                             self.addDir(item[0], href, 100, item[2], 'user playlists', '', desc='', extra={})

                 
    def getUserChannels(self,cParams):
                        listTab=readUserFile('channel')
                        
                        for item in listTab:
                             href = item[1]
                             #url = 'https://www.googleapis.com/youtube/v3/search?part=snippet&type=playlist&channelId=' + chid + uParams
                             self.addDir(item[0], href, 12, item[2], 'user channel', '', desc='', extra={})

       
                       
        
    def getUserVideos(self,cParams={}):
                        listTab=readUserFile('video')
                        for item in listTab:
                             href = 'plugin://plugin.video.youtube/?action=play_video&videoid=' + item[1]
                             
                             self.addDir(item[0], href, 0, item[2], 'user videos', '1', desc='', extra={})

   
   

    def getChannelsMenu(self, cParams):
        self.getchannelsubmenu(cParams)
        for item in self.videoList:
            print 'item', item['mode']
            name = item.get('name', '')
            url = item.get('url', '')
            mode = item.get('mode', '')
            image = item.get('image', '')
            category = item.get('category', '')
            page = item.get('page', '')
            desc = item.get('desc', '')
            extra = item.get('extra', {})
            self.addDir(name, url, mode, image, desc=desc, page=page, link=False, category=category, maintitle=True, extra=extra)

    def getMyChannel(self, cParams):
        list1 = []
        access_token, refresh_token = self.getaccesstoken()
        url = 'https://www.googleapis.com/youtube/v3/channels?part=contentDetails&mine=true&access_token=' + self.access_token.strip()
        printD('url', url)
        cParams.update({'url': url})
        self.getMyChannelData(cParams)
        
        for item in self.videoList:
            print 'item', item['mode']
            name = item.get('name', '')
            url = item.get('url', '')
            mode = item.get('mode', '')
            image = item.get('image', '')
            category = item.get('category', '')
            page = item.get('page', '')
            desc = item.get('desc', '')
            extra = item.get('extra', {})
            self.addDir(name, url, mode, image, desc=desc, page=page, link=False, category=category, maintitle=True, extra=extra)

    def getrecommended(self, cParams):
        self.get_recommended(cParams)
        for item in self.videoList:
            print 'item', item['mode']
            name = item.get('name', '')
            url = item.get('url', '')
            mode = item.get('mode', '')
            image = item.get('image', '')
            category = item.get('category', '')
            page = item.get('page', '')
            desc = item.get('desc', '')
            extra = item.get('extra', {})
            self.addDir(name, url, mode, image, desc=desc, page=page, link=False, category=category, maintitle=True, extra=extra)

    def getbestyoutube(self, cParams):
        self.getbest(cParams)
        for item in self.videoList:
            print 'item', item['mode']
            name = item.get('name', '')
            url = item.get('url', '')
            mode = item.get('mode', '')
            image = item.get('image', '')
            category = item.get('category', '')
            page = item.get('page', '')
            desc = item.get('desc', '')
            extra = item.get('extra', {})
            self.addDir(name, url, mode, image, desc=desc, page=page, link=False, category=category, maintitle=True, extra=extra)

    def getVideosList(self, cParams):
        self.getviedoList(cParams)
        for item in self.videoList:
            name = item.get('name', '')
            url = item.get('url', '')
            mode = item.get('mode', '')
            image = item.get('image', '')
            category = item.get('category', '')
            page = item.get('page', '')
            desc = item.get('desc', '')
            extra = item.get('extra', {})
            maintitle = item.get('maintitle', False)
            self.addDir(name, url, mode, image, category, page, maintitle, link=False, desc=desc, extra=extra)

    def run(self, cParams = None):
         
         
        if not cParams:
            params = self.get_params()
        else:
            params = cParams
        url = params.get('url', '')
        name = params.get('name', '')
        try:
            mode = int(params.get('mode', None))
        except:
            mode = None

        page = str(params.get('page', ''))
        section = params.get('section', '')
        extra = params.get('extra', {})
        try:
            extra = ast.literal_eval(extra)
        except:
            extra = {}

        show = params.get('show', '')
        image = params.get('image', '')
        print 'Mode: ' + str(mode)
        print 'URL: ' + str(url)
        print 'Name: ' + str(name)
        print 'page: ' + str(page)
        print 'section: ' + str(section)
        print 'extra: ' + str(extra)
        print 'show: ' + str(show)
        print 'image: ' + str(image)
        cParams = params
        printD('input Parameters', cParams)
        if mode == None:
            print ''
            self.showmenu()
        elif mode == 103:
            sterm = cParams.get('strem', '')
            printD('sterm', sterm)
            self.search(cParams)
        elif mode == 11:
            print '' + url
            self.getMainCats(cParams)
        elif mode == 12:
            print '' + url
            self.getChannelsMenu(cParams)
        elif mode == 13:
            print '' + url
            self.getMyChannel(cParams)
        elif mode == 14:
            print '' + url
            self.getbestyoutube(cParams)
        elif mode == 15:
            print '' + url
            self.getrecommended(cParams)
        elif mode == 16:
            print '' + url
             
            self.getUserlists(cParams)
        elif mode == 17:
            self.getRecommeded(cParams)
        elif mode == 18:
            self.getUserPlaylists(cParams)
            
        elif mode == 19:
            self.getUserChannels(cParams)
            

            
        elif mode == 20:
            self.getUserVideos(cParams)

            
        elif mode == 100:
            print '' + url
            self.getVideosList(cParams)
        return self.endDir()


def start(cParams = None):
     
    addon = youtube()
    return addon.run(cParams)
