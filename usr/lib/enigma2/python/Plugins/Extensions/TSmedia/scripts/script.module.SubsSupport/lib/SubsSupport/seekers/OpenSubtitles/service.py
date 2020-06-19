# -*- coding: utf-8 -*-

import os
from ..utilities import log, hashFile
#from os_utilities import OSDBServer

import xmlrpclib

def printE(msg=''):
    printD("===============================================")
    printD("                   EXCEPTION                   ")
    printD("===============================================")
    msg = msg + ': \n%s' % traceback.format_exc()
    traceback.print_exc(file=sys.stdout)
    printD("Error",msg)
    printD("===============================================")
log_file='/tmp/opensubtitles2.log'    
def getcaller_name():
    try:
        import inspect
        import os
        frame = inspect.currentframe()
        frame = frame.f_back.f_back
        code = frame.f_code
        calling_module = os.path.basename(code.co_filename)
        return calling_module
    except:
        return ''
def printD(label='', Ddata='' ):
        return
        Ddata=str(Ddata)
        label=str(label)
    
   
        try:
            caller_name = getcaller_name() 
            f = open(log_file, 'a')
            
            f.write(caller_name+":"+label+'->'+Ddata + '\n')
            f.close
        except Exception:
            print("======================EXC printDBG======================")
            print("Log: %s" % traceback.format_exc())
            print("========================================================")
            try:
                msg = '%s' % traceback.format_exc()
                f = open(log_file, 'a')
                f.write(Ddata + '\n')
                f.close
            except Exception:
                print("======================EXC printDBG======================")
                print("logII: %s" % traceback.format_exc())
                print("========================================================")

printD('opensubtitles-service8xxx', 'mahmoud')

from ..utilities import languageTranslate, log

__scriptname__ = 'XBMC Subtitles'
__version__ = '3.9.18'

BASE_URL_XMLRPC = u"http://api.opensubtitles.org/xml-rpc"

class OSDBServer:

    def __init__(self, *args, **kwargs):
        self.server = xmlrpclib.Server(BASE_URL_XMLRPC, verbose=0)
        #login = self.server.LogIn("", "", "en", "%s_v%s" % (__scriptname__.replace(" ", "_"), __version__))
        login = self.server.LogIn('mfaraj25', 'docray57', 'en', 'tsmediauseragent')
        printD('login',login)
        self.osdb_token = login[ "token" ]
        printD('self.osdb_token',self.osdb_token)

    def mergesubtitles(self):
        self.subtitles_list = []
        if(len (self.subtitles_hash_list) > 0):
            for item in self.subtitles_hash_list:
                if item["format"].find("srt") == 0 or item["format"].find("sub") == 0:
                    self.subtitles_list.append(item)

        if(len (self.subtitles_list) > 0):
            self.subtitles_list.sort(key=lambda x: [not x['sync'], x['lang_index']])

    def searchsubtitles(self, srch_string , lang1, lang2, lang3, hash_search, _hash="000000000", size="000000000"):
        msg = ""
        printD('self.osdb_token2',self.osdb_token)
        lang_index = 3
        searchlist = []
        self.subtitles_hash_list = []
        self.langs_ids = [languageTranslate(lang1, 0, 2), languageTranslate(lang2, 0, 2), languageTranslate(lang3, 0, 2)]
        language = languageTranslate(lang1, 0, 3)
        if lang1 != lang2:
            language += "," + languageTranslate(lang2, 0, 3)
        if lang3 != lang1 and lang3 != lang2:
            language += "," + languageTranslate(lang3, 0, 3)
        log(__name__ , "Token:[%s]" % str(self.osdb_token))
        try:
            if (self.osdb_token) :
                if hash_search:
                    searchlist.append({'sublanguageid':language, 'moviehash':_hash, 'moviebytesize':str(size) })
                searchlist.append({'sublanguageid':language, 'query':srch_string })
                printD('opensubtitlesearchlist23xxxxx',searchlist)
                search = self.server.SearchSubtitles(self.osdb_token, searchlist)
                printD("opensubtitlessearch24xxxxx",search)
                if search["data"]:
                    for item in search["data"]:
                        if item["ISO639"]:
                            lang_index = 0
                            for user_lang_id in self.langs_ids:
                                if user_lang_id == item["ISO639"]:
                                    break
                                lang_index += 1
                            flag_image = "flags/%s.gif" % item["ISO639"]
                        else:
                            flag_image = "-.gif"

                        if str(item["MatchedBy"]) == "moviehash":
                            sync = True
                        else:
                            sync = False
                        self.subtitles_hash_list.append({
                            'lang_index':lang_index,
                            'filename':item["SubFileName"],
                            'link':item["ZipDownloadLink"],
                            'language_name':item["LanguageName"],
                            'language_flag':flag_image,
                            'language_id':item["SubLanguageID"],
                            'ID':item["IDSubtitleFile"],
                            'rating':str(int(item["SubRating"][0])),
                            'format':item["SubFormat"],
                            'sync':sync,
                            'hearing_imp':int(item["SubHearingImpaired"]) != 0,
                            'fps':item.get('MovieFPS')
                        })

        except Exception as e:
            msg = "Error Searching For Subs: %s" % str(e)
            printD("searching error",e)

        self.mergesubtitles()
        return self.subtitles_list, msg

    def download(self, ID, dest, token):
        try:
            import zlib, base64
            down_id = [ID, ]
            result = self.server.DownloadSubtitles(self.osdb_token, down_id)
            if result["data"]:
                local_file = open(dest, "w" + "b")
                d = zlib.decompressobj(16 + zlib.MAX_WBITS)
                data = d.decompress(base64.b64decode(result["data"][0]["data"]))
                local_file.write(data)
                local_file.close()
                return True
            return False
        except:
            return False

def search_subtitles(file_original_path, title, tvshow, year, season, episode, set_temp, rar, lang1, lang2, lang3, stack):  # standard input
    hash_search = False
    printD('file_original_path',file_original_path)
    printD('title',title)
    printD('tvshow',tvshow)
    printD('year',year)
    printD('season',season)
    printD('episode',episode)
    printD('set_temp',set_temp)
    printD(' rar', rar)
    printD('lang1',lang1)
    printD('lang2',lang2)
    printD('lang3, stack',lang3)
    printD('stack', stack)




    
    if len(tvshow) > 0:  # TvShow
        OS_search_string = ("%s S%.2dE%.2d" % (tvshow,
                                             int(season),
                                               int(episode),)
                                              ).replace(" ", "+")
    else:  # Movie or not in Library
        if str(year) == "":  # Not in Library
            title, year = title, ""  # xbmc.getCleanMovieTitle( title )
        else:  # Movie in Library
            year = year
            title = title
        OS_search_string = title.replace(" ", "+")

    printD('OS_search_string8xxx', OS_search_string)    
    log(__name__ , "Search String [ %s ]" % (OS_search_string,))

    if set_temp :
        hash_search = False
        file_size = "000000000"
        SubHash = "000000000000"
    else:
        try:
            file_size, SubHash = hashFile(file_original_path, rar)
            log(__name__ , "xbmc module hash and size")
            hash_search = True
        except:
            file_size = ""
            SubHash = ""
            hash_search = False
    printD('file_size', file_size)
    printD('SubHash', SubHash)
    if file_size != "" and SubHash != "":
        log(__name__ , "File Size [%s]" % file_size)
        log(__name__ , "File Hash [%s]" % SubHash)

    log(__name__ , "Search by hash and name %s" % (os.path.basename(file_original_path),))


    #printD('hash_search222', hash_search)
    #printD('OS_search_string', OS_search_string)
    
    try:
        cb=OSDBServer()
        subtitles_list, msg = cb.searchsubtitles(OS_search_string, lang1, lang2, lang3, hash_search, SubHash, file_size)
    except Exception as error:
        printD("errorMMMM",error)
        printE()

    printD('open-subtitles-subtitles_listxxx21', subtitles_list)
    return subtitles_list, "", msg  # standard output

def download_subtitles (subtitles_list, pos, zip_subs, tmp_sub_dir, sub_folder, session_id):  # standard input

    destination = os.path.join(tmp_sub_dir, "%s.srt" % subtitles_list[pos][ "ID" ])
    result = OSDBServer().download(subtitles_list[pos][ "ID" ], destination, session_id)
    if not result:
        import urllib
        urllib.urlretrieve(subtitles_list[pos][ "link" ], zip_subs)

    language = subtitles_list[pos][ "language_name" ]
    return not result, language, destination  # standard output
