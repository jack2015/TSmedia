## @file  ihost.py
#

###################################################
# E2 GUI COMMPONENTS 
###################################################
from xbmctools import Item,getnet,logdata,readnet,get_params,extractdata,cfresolve,finddata,postData,getData,playlink,getDomain,getsearchtext,finddata,trace_error,removeunicode,getmetadata,cleanhtml,resolvehost

############################
from addonsParser.components.addonsParserinit import TranslateTXT as _, GetIPTVNotify,GetIPTVSleep
from addonsParser.libs.urlparserhelper import unpackJSPlayerParams, unpackJS, \
                                                               JS_FromCharCode, \
                                                               JS_toString, \
                                                               VIDUPME_decryptPlayerParams,    \
                                                               SAWLIVETV_decryptPlayerParams,  \
                                                               TEAMCASTPL_decryptPlayerParams, \
                                                               VIDEOWEED_decryptPlayerParams, \
                                                               KINGFILESNET_decryptPlayerParams, \
                                                               captchaParser, \
                                                               getDirectM3U8Playlist, \
                                                               getMPDLinksWithMeta, \
                                                               getF4MLinksWithMeta, \
                                                               decorateUrl, \
                                                               int2base, drdX_fx, \
                                                               unicode_escape
from addonsParser.tools.iptvtypes import strwithmeta
from addonsParser.components.asynccall import MainSessionWrapper
from addonsParser.libs.pCommon import common, CParsingHelper
from addonsParser.libs.urlparser import urlparser
from addonsParser.tools.iptvtools import getCachePath,getAppTmp,getAppDukPath,getAppPath,CSearchHistoryHelper, GetCookieDir, printDBG, printExc, GetLogoDir, byteify,MergeDicts
from addonsParser.libs.e2ijson import loads as json_loads, dumps as json_dumps
from addonsParser.libs import ph
from addonsParser.tools.e2ijs import js_execute


from urlparse import urljoin

class ArticleContent:
    VISUALIZER_DEFAULT = 'DEFAULT'
    # Posible args and values for richDescParams:
    RICH_DESC_PARAMS        = ["alternate_title", "original_title", "station", "price", "age_limit", "views", "status", "type", "first_air_date", "last_air_date", "seasons", "episodes", "country", "language", "duration", "quality", "subtitles", "year", "imdb_rating", "tmdb_rating",\
                               "released", "broadcast", "remaining", "rating", "rated", "genre", "genres", "category", "categories", "production", "director", "directors", "writer", "writers", \
                               "creator", "creators", "cast", "actors", "stars", "awards", "budget", "translation",]
    # labels here must be in english language 
    # translation should be done before presentation using "locals" mechanism
    RICH_DESC_LABELS = {"alternate_title":   "Alternate Title:",
                        "original_title":    "Original Title:",
                        "station":           "Station:",
                        "price":             "Price:",
                        "status":            "Status:",
                        "type":              "Type:",
                        "age_limit":         "Age limit:",
                        "first_air_date":    "First air date:",  
                        "last_air_date":     "Last air date:", 
                        "seasons":           "Seasons:",
                        "episodes":          "Episodes:",
                        "quality":           "Quality:",
                        "subtitles":         "Subtitles:",
                        "country":           "Country:", 
                        "language":          "Language",
                        "year":              "Year:", 
                        "released":          "Released:",
                        "broadcast":         "Broadcast:",
                        "remaining":         "Remaining:",
                        "imdb_rating":       "IMDb Rating:",
                        "tmdb_rating":       "TMDb Rating:",
                        "rating":            "Rating:", 
                        "rated":             "Rated:",
                        "duration":          "Duration:", 
                        "genre":             "Genre:", 
                        "genres":            "Genres:", 
                        "category":          "Category:",
                        "categories":        "Categories:",
                        "production":        "Production:",
                        "director":          "Director:",
                        "directors":         "Directors:",
                        "writer":            "Writer:",
                        "writers":           "Writers:",
                        "creator":           "Creator:",
                        "creators":          "Creators:",
                        "cast":              "Cast:",
                        "actors":            "Actors:", 
                        "stars":             "Stars:",
                        "awards":            "Awards:",
                        "views":             "Views:",
                        "budget":            "Budget:",
                        "translation":       "Translation:"
                        }
    def __init__(self, title = '', text = '', images = [], trailers = [], richDescParams = {}, visualizer=None):
        self.title    = title
        self.text     = text
        self.images   = images
        self.trailers = trailers
        self.richDescParams = richDescParams
        if None == visualizer: 
            self.visualizer = ArticleContent.VISUALIZER_DEFAULT
        else:
            self.visualizer = visualizer
        


    
'''
CHostBase implements some typical methods
          from IHost interface
'''

    

class CBaseHostClass(Item):
    def __init__(self, params={}):
        Item.__init__(self)
        self.ItemClass=Item()
        self.sessionEx = MainSessionWrapper() 
        self.up = urlparser()
        
        proxyURL = params.get('proxyURL', '')
        useProxy = params.get('useProxy', False)
        self.cm = common(proxyURL, useProxy)

        self.currList = []
        self.currItem = {}
        if '' != params.get('cookie', ''):
            self.COOKIE_FILE = GetCookieDir(params['cookie'])
        self.moreMode = False
        
    def informAboutGeoBlockingIfNeeded(self, country, onlyOnce=True):
        try: 
            if onlyOnce and self.isGeoBlockingChecked: return
        except Exception: 
            self.isGeoBlockingChecked = False
        sts, data = self.cm.getPage('https://dcinfos.abtasty.com/geolocAndWeather.php')
        if not sts: return
        try:
            data = json_loads(data.strip()[1:-1], '', True)
            if data['country'] != country:
                message = _('%s uses "geo-blocking" measures to prevent you from accessing the services from outside the %s Territory.') 
                GetIPTVNotify().push(message % (self.getMainUrl(), country), 'info', 5)
            self.isGeoBlockingChecked = True
        except Exception: printExc()
    def TSaddDir(self,currList=[],need_resolve=None):
                        print "need_resolvexxx1",need_resolve
                        if currList:
                           self.currList=currList
                        else:
                           currList =self.currList
                           
                        for item in currList:
                               
                               
                               
                               
                               #####
                               title=item.get('title',"")
                               if title=='':
                                  title=item.get('name',"")
                               title=title.replace("'\c0000????'","")
                               url=item.get('url',"")
                               mode=item.get('gnr',"")
                               image=item.get('icon',"")
                               category=item.get('category',"")
                               type=item.get('type',"")
                               if need_resolve is None:
                                   try:need_resolve=item['need_resolve']
                                   except:pass
                                   
                               
                             
                               print 'need_resolvexxx',need_resolve
                                                             
                               if mode=="":
                                   
                                   if need_resolve==0:
                                       mode=0
                                       print 'modexx0',mode
                                   elif need_resolve==1:
                                        mode=2
                                   elif category== 'search':
                                        mode=103
                                   else:
                                        pass                              

       
                                                 
                               
                              
                               self.ItemClass.addDir(str(title),url,mode,image,"",1,category=category,type=type,extra=str(item))
                        #return self.ItemClass.endDir()
                       ####     
    def listsTab(self, tab, cItem, type='dir'):
        defaultType = type
        for item in tab:
            params = dict(cItem)
           
            
            params.update(item)
            params['name']  = 'category'
            type = item.get('type', defaultType)
            print "####item",item
            print "######type###",type
            if type == 'dir':
                list=self.addDir(params)

            elif type == 'marker': self.addMarker(params)
            else: self.addVideo(params)
        #self.endHandleService( 0, 0)

        return list

    def listSubItems(self, cItem):
        printDBG("CBaseHostClass.listSubItems")
        self.currList = cItem['sub_items']

    def listToDir(self, cList, idx):
        return self.cm.ph.listToDir(cList, idx)
    
    def getMainUrl(self):
        return self.MAIN_URL
    
    def setMainUrl(self, url):
        if self.cm.isValidUrl(url):
            self.MAIN_URL = self.cm.getBaseUrl(url)
            return True
        return False
    
    def getFullUrl(self, url, currUrl=None):
        if currUrl == None or not self.cm.isValidUrl(currUrl):
            try:
                currUrl = self.getMainUrl()
            except Exception:
                currUrl = None
            if currUrl == None or not self.cm.isValidUrl(currUrl):
                currUrl = 'http://fake/'
        return self.cm.getFullUrl(url, currUrl)

    def getFullIconUrl(self, url, currUrl=None):
        if currUrl != None: return self.getFullUrl(url, currUrl)
        else: return self.getFullUrl(url)
        
    def getDefaulIcon(self, cItem=None):
        try:
            return self.DEFAULT_ICON_URL
        except Exception:
            pass
        return ''

    @staticmethod 
    def cleanHtmlStr(str):
        return CParsingHelper.cleanHtmlStr(str)

    @staticmethod 
    def getStr(v, default=''):
        if type(v) == type(u''): return v.encode('utf-8')
        elif type(v) == type(''):  return v
        return default
            
    def getCurrList(self):
        return self.currList

    def setCurrList(self, list):
        self.currList = list
        
    def getCurrItem(self):
        return self.currItem

    def setCurrItem(self, item):
        self.currItem = item

    def addDir(self, params):
        params['type'] = 'category'
        self.currList.append(params)
        return self.currList
        
    def addMore(self, params):
        params['type'] = 'more'
        self.currList.append(params)
        return
        
    def addVideo(self, params):
        params['type'] = 'video'
        self.currList.append(params)
        return
        
    def addAudio(self, params):
        params['type'] = 'audio'
        self.currList.append(params)
        return
    
    def addPicture(self, params):
        params['type'] = 'picture'
        self.currList.append(params)
        return
        
    def addData(self, params):
        params['type'] = 'data'
        self.currList.append(params)
        return
  
    def addArticle(self, params):
        params['type'] = 'article'
        self.currList.append(params)
        return
    
    def addMarker(self, params):
        params['type'] = 'marker'
        self.currList.append(params)
        return
    
    def listsHistory(self, baseItem={'name': 'history', 'category': 'Wyszukaj'}, desc_key='plot', desc_base='' ):
        list = self.history.getHistoryList()
        for histItem in list:
            plot = ''
            try:
                if type(histItem) == type({}):
                    pattern     = histItem.get('pattern', '')
                    search_type = histItem.get('type', '')
                    if '' != search_type: plot = desc_base + _(search_type)
                else:
                    pattern     = histItem
                    search_type = None
                params = dict(baseItem)
                params.update({'title': pattern, 'search_type': search_type,  desc_key: plot})
                self.addDir(params)
            except Exception: printExc()
            
    def getFavouriteData(self, cItem):
        try:
            return json_dumps(cItem)
        except Exception: 
            printExc()
        return ''
        
    def getLinksForFavourite(self, fav_data):
        try:
            if self.MAIN_URL == None:
                self.selectDomain()
        except Exception: 
            printExc()
        links = []
        try:
            cItem = json_loads(fav_data)
            links = self.getLinksForItem(cItem)
        except Exception: printExc()
        return links
        
    def setInitListFromFavouriteItem(self, fav_data):
        try:
            if self.MAIN_URL == None:
                self.selectDomain()
        except Exception: 
            printExc()
        try:
            params = json_loads(fav_data)
        except Exception: 
            params = {}
            printExc()
            return False
        self.currList.append(params)
        return True
        
    def getLinksForItem(self, cItem):
        return self.getLinksForVideo(cItem)
    
    def handleService(self, index, refresh=0, searchPattern='', searchType=''):
        self.moreMode = False
        if 0 == refresh:
            if len(self.currList) <= index:
                return
            if -1 == index:
                self.currItem = { "name": None }
            else:
                self.currItem = self.currList[index]
        if 2 == refresh: # refresh for more items
            printDBG(">> endHandleService index[%s]" % index)
            # remove item more and store items before and after item more
            self.beforeMoreItemList = self.currList[0:index]
            self.afterMoreItemList = self.currList[index+1:]
            self.moreMode = True
            if -1 == index:
                self.currItem = { "name": None }
            else:
                self.currItem = self.currList[index]
    
    def endHandleService(self, index, refresh):
         
        self.TSaddDir(self.currList)
        if 2 == refresh: # refresh for more items
            currList = self.currList
            self.currList = self.beforeMoreItemList
            for item in currList:
                if 'more' == item['type'] or (item not in self.beforeMoreItemList and item not in self.afterMoreItemList):
                    self.currList.append(item)
            self.currList.extend(self.afterMoreItemList)
            self.beforeMoreItemList = []
            self.afterMoreItemList  = []
            
        self.moreMode = False
        
    
