# -*- coding: utf8 -*-
#from __future__ import unicode_literals 
import sys
import urllib,urllib2,re,os,ast
from iTools import CBaseAddonClass,printD,printE,_
from youtubeparser import YouTubeParser
extra={}
################''
def gettytul():
    return 'https://youtube.com/'

##########################################parsing tools
sortBy="video_avg_rating"

class E2youtube(CBaseAddonClass,YouTubeParser):
    
        def __init__(self,cParams={}):
                
                CBaseAddonClass.__init__(self,{'cookie':'E2youtube.cookie','module_path':__file__})
                YouTubeParser.__init__(self)
                self.cParams=cParams
                self.USER_AGENT = 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:40.0) Gecko/20100101 Firefox/40.0'
                self.MAIN_URL = 'https://youtube.com/'
                self.HEADER = {'User-Agent': self.USER_AGENT, 'DNT':'1', 'Accept': 'text/html', 'Accept-Encoding':'gzip, deflate', 'Referer':self.getMainUrl(), 'Origin':self.getMainUrl()}
                self.AJAX_HEADER = dict(self.HEADER)
                self.AJAX_HEADER.update( {'X-Requested-With': 'XMLHttpRequest', 'Accept-Encoding':'gzip, deflate', 'Content-Type':'application/x-www-form-urlencoded; charset=UTF-8', 'Accept':'application/json, text/javascript, */*; q=0.01'} )
                self.cacheLinks  = {}
                self.defaultParams = {'header':self.HEADER, 'raw_post_data':True, 'use_cookie': True, 'load_cookie': True, 'save_cookie': True, 'cookiefile': self.COOKIE_FILE}
                self.module_path=__file__
                #self.getPage=self.cm.getPage#(self, url, addParams = {}, post_data = None)
               
        def showmenu(self):
                baseurl=self.getMainUrl()


                self.addDir("Favorites",'video',-20,"img/favorites.png",'video',1,dialog='favorites')

                self.addDir("Search",'video',103,"img/search.png",'video',1,dialog='search')
                #self.addDir("Search channels",'channel',603,"img/svideos.png",'channel',1,dialog='search')
                #self.addDir("Search playlists",'playlist',703,"img/svideos.png",'playlist',1,dialog='search')
                #self.addDir("Search live",'live',803,"img/svideos.png",'playlist',1,dialog='search')
                #self.addDir("Search movies",'movie',803,"img/svideos.png",'movies',1,dialog='search')


                self.addDir("Channels",'channel',100,"img/channel.png",'channel',1)

                self.addDir("Playlists",'playlists',101,"img/playlist.png",'playlists',1)
                
                self.addDir("Live channels",'livechannels',102,"img/live.png",'livechannels',1)

                self.addDir("Movies",'movies',200,"img/movies.png",'movies',1)

                self.addDir("Music",'music',201,"img/music.png",'music',1)

                #self.addDir("Recommended",'recommended',202,"img/recommended.png",'music',1)

                
                


                                
        ###################################movies
                                  
        def searchVideos(self,name,sterm,page,searchType,pamode):##may pastte code of getmovies here
            pattern=sterm
            
            nextPageCategory=searchType
            
            print "searchType",searchType
            
            currList=self.getSearchResult( pattern, searchType, page, nextPageCategory, sortBy=sortBy)
            print "currList",currList
            for item in currList:
                title=item.get('title',None)
                href=item.get('url',None)
                category=item.get('category','video')
                if href is None or title is None:
                    continue
                image=item.get('icon','')
                desc=item.get('desc','')
                
                if category=='video':
                    mode=0
                   
                elif category=='channel':
                    mode=1
                    
                elif category=='playlist':
                    mode=1
                    
                elif category=='movie':
                    mode=0
                   

                elif category=='live':
                    mode=0
                    
                elif category=='music':
                    mode=1
                    

                    
                    
                self.addDir(title,href,mode,image,category,1)

            print 'currList-1',currList[-1]
            
            title=currList[-1].get('title',None)
            if not title or not title=='Next page':
                return
            sterm=currList[-1].get('pattern',' ')
            searchType=currList[-1].get('search_type','' )
            self.addDir('Next page',sterm,pamode,"img/next.png",category,str(page+1),dialog='nosearch')                       
        def searchChannels(self,name,sterm,page,searchType,pamode):##may pastte code of getmovies here
            pattern=sterm
            
            nextPageCategory=searchType
            
            print "searchType",searchType
            
            currList=self.getSearchResult( pattern, searchType, page, nextPageCategory, sortBy=sortBy)
            print "currList0",currList[0]
            
            for item in currList:
                title=item.get('title',None)
                if not title:
                   title=item.get('name',None) 
                href=item.get('url',None)
                category=item.get('category','video')
                print "title",title
                print "href",href
               
                if href is None or title is None:
                    continue
                image=item.get('icon','')
                desc=item.get('desc','')
                
                if category=='video':
                    mode=0
                    
                elif category=='channel':
                    mode=1
                     
                elif category=='playlist':
                    mode=1
                    
                    
                self.addDir(title,href,1,image,category,1)

            print 'currList-1',currList[-1]
            title=currList[-1].get('name','Next page')
            sterm=currList[-1].get('pattern',' ')
            searchType=currList[-1].get('search_type','' )
            self.addDir('Next nage',sterm,pamode,"img/next.png",'channel',str(page+1),dialog='nosearch')                       
                                                
        def searchPlaylist(self,name,sterm,page,searchType,pamode):##may pastte code of getmovies here
            pattern=sterm
            
            nextPageCategory=searchType
            
            print "searchType",searchType
           
            currList=self.getSearchResult( pattern, searchType, page, nextPageCategory, sortBy=sortBy)
            print "currList0",currList[0]
            
            for item in currList:
                title=item.get('title',None)
                if not title:
                   title=item.get('name',None) 
                href=item.get('url',None)
                category=item.get('category','video')
                print "title",title
                print "href",href
               
                if href is None or title is None:
                    continue
                image=item.get('icon','')
                desc=item.get('desc','')
                
                if category=='video':
                    mode=0
                    nextmode=103
                elif category=='channel':
                    mode=1
                    nextmode=603
                elif category=='playlist':
                    mode=1
                    nextmode=703
                    
                self.addDir(title,href,1,image,category,1)

            print 'currList-1',currList[-1]
            title=currList[-1].get('name','Next page')
            sterm=currList[-1].get('pattern',' ')
            searchType=currList[-1].get('search_type','' )
            self.addDir('Next Page',sterm,pamode,"img/next.png",'channel',str(page+1),dialog='nosearch')                       
                                                
                
                
                                
     
        def searchMovie(self,name,sterm,page,searchType):##may pastte code of getmovies here
            pattern=sterm
            
            nextPageCategory=searchType
           
            print "searchType",searchType
            
            currList=self.getSearchResult( pattern, searchType, page, nextPageCategory, sortBy=sortBy)
            print "currList",currList
            for item in currList:
                title=item.get('title',None)
                href=item.get('url',None)
                category=item.get('category','video')
                if href is None or title is None:
                    continue
                image=item.get('icon','')
                desc=item.get('desc','')
                
                if category=='video':
                    mode=0
                    nextmode=103
                elif category=='channel':
                    mode=1
                    nextmode=603
                elif category=='playlist':
                    mode=1
                    nextmode=703
                    
                self.addDir(title,href,mode,image,category,1)

            print 'currList-1',currList[-1]
            title=currList[-1].get('name','Next page')
            sterm=currList[-1].get('pattern',' ')
            searchType=currList[-1].get('search_type','' )
            self.addDir('More',sterm,nextmode,"img/next.png",category,str(page+1),dialog='nosearch')                          


            
        def getVideos(self,name,url,img,page,category,pamode):

            printD('Youtube.getVideos name[%s]' % (name))
            
            
           
            
            #category='channel'
            print 'category',category
            
            if "channel" == category or 'browse_ajax' in  url:
                if -1 == url.find('browse_ajax'):
                    if url.endswith('/videos'): 
                        url = url + '?flow=list&view=0&sort=dd'
                    else:
                        url = url + '/videos?flow=list&view=0&sort=dd'
                category='channel'        
                self.currList = self.getVideosFromChannelList(url, category, page, {})
                print 'self.currList-1',self.currList[-1]
                
                
            elif "playlist" == category:
                self.currList = self.getVideosFromPlaylist(url, category, page, {})   
            elif "traylist" == category:
                self.currList = self.getVideosFromTraylist(url, category, page, cItem)
            else:
                printD('YTlist.getVideos Error unknown category[%s]' % category)
              
            self.displayList(self.currList,category,page,pamode)               
                
        def displayList(self,currList,pcategory,page,pamode):

            for item in currList:
                title=item.get('title',None)
                href=item.get('url',None)
                category=item.get('category','video')
                if href is None or title is None:
                    continue
                image=item.get('icon','')
                desc=item.get('desc','')
                page=item.get('page',1)
                
                if category=='video':
                    mode=0
                    nextmode=103
                elif category=='channel':
                    mode=1
                    nextmode=603
                elif category=='playlist':
                    mode=1
                    nextmode=703
                elif category=='live':
                    mode=0
                    nextmode=803

                    
                if 'next page' in title.lower():
                    mode=1
                self.addDir(title,href,mode,image,category,page)

           
            nextPage=False
            nextPage=currList[-1].get('title',False)
            if nextPage=='Next page':
                nextPage=True
                
            sterm=currList[-1].get('pattern',' ')
            
            url=currList[-1].get('url',' ')
            searchType=currList[-1].get('search_type','' )
##############################3   
        def get_recommended(self, cParams):
            main_title = cParams.get('name', '')
            url = 'https://www.youtube.com/'
            data = self.getPage(url)
            printD('data', data)
            if data == '':
                return self.youtube_error('Download error')
            blocks = data.split('class="yt-lockup-title')
            i = 0
            list1 = []
            print 'blaocks', len(blocks)
            printD('blaocks', len(blocks))
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

                self.addDir(name, href, 0, image, main_title, '', desc='', extra={})
        
        def run(self,cParams):
                self.cParams=cParams
                if self.cParams is None:
                        self.cParams=self.get_params()
                url=self.cParams.get('url','')
                name=self.cParams.get('name','')
                try:mode=int(self.cParams.get('mode',None))
                except:mode=None
                page=int(self.cParams.get('page',1))
                category=self.cParams.get('category','')
                extra=self.cParams.get("extra",{})
                try:extra=ast.literal_eval(extra)
                except:pass
                show=self.cParams.get('show','')
                image=self.cParams.get('image','')
                sterm=self.cParams.get('sterm','')
                dialog=self.cParams.get('dialog','')
                print "Mode: "+str(mode)
                print "URL: "+str(url)
                print "Name: "+str(name)
                print "sterm: "+str(sterm)
                print "page: "+str(page)
                print "cacategory: "+str(category)
                print "extra: "+str(extra)
                print "show: "+str(show)
                print "image: "+str(image.encode("utf-8","ignore"))

                if mode==None:
                        print ""
                        self.showmenu()
                elif mode==1:
                        print ""+url
                        #print self.getVideosFromChannelList( url, "channel", 2, {})
                        #return
                        self.getVideos(name,url,image,page,category,mode)
                elif mode==2:
                        print ""+url
                        self.resolve_host(name,url)        

                        
                elif mode==100:
                        print ""+url
                        
                        self.searchChannels("Channels",'channel',page,'channel',mode)
                elif mode==101:
                        print ""+url
                        
                        self.searchPlaylist("Playlists",'playlist',page,'playlist',mode)

                elif mode==102:
                        print ""+url
                        
                        self.searchVideos("Search",'live',page,'live',mode)  

                elif mode==200:
                        print ""+url
                        
                        self.searchVideos("Search",'',page,'movie',mode)
                elif mode==201:
                        print ""+url
                        
                        self.searchVideos("Search",'music',page,'video',mode)  

                elif mode==202:
                        print ""+url
                        self.get_recommended(self.cParams)
                        #self.searchVideos("Search",'music',page,'video',mode)  


                        
                        
                elif mode==103:
                        if  not dialog=='nosearch':
                           sterm = self.getsearchtext()      
                        else:
                            sterm=url
                        sterm= urllib.quote_plus(sterm) 
                        self.searchVideos("Search",sterm,page,category,mode)
                elif mode==104:
                        if  not dialog=='nosearch':
                           sterm = self.getsearchtext()      
                        else:
                            sterm=url
                        sterm= urllib.quote_plus(sterm) 
                        self.searchVideos("Search",'',page,'movie',mode)




                        
                elif mode==603:
                        if  not dialog=='nosearch':
                           sterm = self.getsearchtext()      
                        else:
                            sterm=url
                        sterm= urllib.quote_plus(sterm) 
                        self.searchChannels("Search",sterm,page,'channel',mode)  


                elif mode==703:
                        if  not dialog=='nosearch':
                           sterm = self.getsearchtext()      
                        else:
                            sterm=url
                        sterm= urllib.quote_plus(sterm) 
                        self.searchPlaylist("Search",sterm,page,'playlist',mode)  


                elif mode==903:
                        if  not dialog=='nosearch':
                           sterm = self.getsearchtext()      
                        else:
                            sterm=url
                        sterm= urllib.quote_plus(sterm) 
                        self.searchVideos("Search",sterm,page,'live',mode)  
                                                
                elif mode==803:
                        if  not dialog=='nosearch':
                           sterm = self.getsearchtext()      
                        else:
                            sterm=url
                        sterm= urllib.quote_plus(sterm) 
                        self.searchVideos("Search",sterm,page,'live',mode)  
                                                

               
                return self.endDir()

def start(cParams=None):
    addon=E2youtube(cParams)
    return addon.run(cParams)               
