# -*- coding: utf-8 -*-

import HTMLParser
import difflib
import os, re, string, urllib, urllib2


 
#from iTools import printD as log
def printE(msg=''):
    import traceback,sys
    printD("===============================================")
    printD("                   EXCEPTION                   ")
    printD("===============================================")
    msg = msg + ': \n%s' % traceback.format_exc()
    traceback.print_exc(file=sys.stdout)
    printD("Error",msg)
    printD("===============================================")
log_file='/tmp/subsscene2.log'    
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
        import traceback
    
   
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

main_url = "https://subscene.com"
debug_pretext = ""
log=printD
printD("start","start")


# Seasons as strings for searching
# Seasons as strings for searching
seasons = ["Specials", "First", "Second", "Third", "Fourth", "Fifth", "Sixth", "Seventh", "Eighth", "Ninth", "Tenth"]
seasons = seasons + ["Eleventh", "Twelfth", "Thirteenth", "Fourteenth", "Fifteenth", "Sixteenth", "Seventeenth",
                     "Eighteenth", "Nineteenth", "Twentieth"]
seasons = seasons + ["Twenty-first", "Twenty-second", "Twenty-third", "Twenty-fourth", "Twenty-fifth", "Twenty-sixth",
                     "Twenty-seventh", "Twenty-eighth", "Twenty-ninth"]

movie_season_pattern = ("<a href=\"(?P<link>/subtitles/[^\"]*)\">(?P<title>[^<]+)\((?P<year>\d{4})\)</a>\s+"
                        "</div>\s+<div class=\"subtle count\">\s+(?P<numsubtitles>\d+)")



import HTMLParser
import difflib
import os, re, string, urllib, urllib2
import string,urllib,re,requests

movie_season_pattern = ("<a href=\"(?P<link>/subtitles/[^\"]*)\">(?P<title>[^<]+)\((?P<year>\d{4})\)</a>\s+"
                        "</div>\s+<div class=\"subtle count\">\s+(?P<numsubtitles>\d+)")
subscene_languages = {
    'Chinese BG code': 'Chinese',
    'Brazillian Portuguese': 'Portuguese (Brazil)',
    'Serbian': 'SerbianLatin',
    'Ukranian': 'Ukrainian',
    'Farsi/Persian': 'Persian'
}
LANGUAGES = (
    ("Albanian", "29", "sq", "alb", "0", 30201),
    ("Arabic", "12", "ar", "ara", "1", 30202),
    ("Belarusian", "0", "hy", "arm", "2", 30203),
    ("Bosnian", "10", "bs", "bos", "3", 30204),
    ("Bulgarian", "33", "bg", "bul", "4", 30205),
    ("Catalan", "53", "ca", "cat", "5", 30206),
    ("Chinese", "17", "zh", "chi", "6", 30207),
    ("Croatian", "38", "hr", "hrv", "7", 30208),
    ("Czech", "7", "cs", "cze", "8", 30209),
    ("Danish", "24", "da", "dan", "9", 30210),
    ("Dutch", "23", "nl", "dut", "10", 30211),
    ("English", "2", "en", "eng", "11", 30212),
    ("Estonian", "20", "et", "est", "12", 30213),
    ("Persian", "52", "fa", "per", "13", 30247),
    ("Finnish", "31", "fi", "fin", "14", 30214),
    ("French", "8", "fr", "fre", "15", 30215),
    ("German", "5", "de", "ger", "16", 30216),
    ("Greek", "16", "el", "ell", "17", 30217),
    ("Hebrew", "22", "he", "heb", "18", 30218),
    ("Hindi", "42", "hi", "hin", "19", 30219),
    ("Hungarian", "15", "hu", "hun", "20", 30220),
    ("Icelandic", "6", "is", "ice", "21", 30221),
    ("Indonesian", "0", "id", "ind", "22", 30222),
    ("Italian", "9", "it", "ita", "23", 30224),
    ("Japanese", "11", "ja", "jpn", "24", 30225),
    ("Korean", "4", "ko", "kor", "25", 30226),
    ("Latvian", "21", "lv", "lav", "26", 30227),
    ("Lithuanian", "0", "lt", "lit", "27", 30228),
    ("Macedonian", "35", "mk", "mac", "28", 30229),
    ("Malay", "0", "ms", "may", "29", 30248),
    ("Norwegian", "3", "no", "nor", "30", 30230),
    ("Polish", "26", "pl", "pol", "31", 30232),
    ("Portuguese", "32", "pt", "por", "32", 30233),
    ("PortugueseBrazil", "48", "pb", "pob", "33", 30234),
    ("Romanian", "13", "ro", "rum", "34", 30235),
    ("Russian", "27", "ru", "rus", "35", 30236),
    ("Serbian", "36", "sr", "scc", "36", 30237),
    ("Slovak", "37", "sk", "slo", "37", 30238),
    ("Slovenian", "1", "sl", "slv", "38", 30239),
    ("Spanish", "28", "es", "spa", "39", 30240),
    ("Swedish", "25", "sv", "swe", "40", 30242),
    ("Thai", "0", "th", "tha", "41", 30243),
    ("Turkish", "30", "tr", "tur", "42", 30244),
    ("Ukrainian", "46", "uk", "ukr", "43", 30245),
    ("Vietnamese", "51", "vi", "vie", "44", 30246),
    ("BosnianLatin", "10", "bs", "bos", "100", 30204),
    ("Farsi", "52", "fa", "per", "13", 30247),
    ("English (US)", "2", "en", "eng", "100", 30212),
    ("English (UK)", "2", "en", "eng", "100", 30212),
    ("Portuguese (Brazilian)", "48", "pt-br", "pob", "100", 30234),
    ("Portuguese (Brazil)", "48", "pb", "pob", "33", 30234),
    ("Portuguese-BR", "48", "pb", "pob", "33", 30234),
    ("Brazilian", "48", "pb", "pob", "33", 30234),
    ("Español (Latinoamérica)", "28", "es", "spa", "100", 30240),
    ("Español (España)", "28", "es", "spa", "100", 30240),
    ("Spanish (Latin America)", "28", "es", "spa", "100", 30240),
    ("Español", "28", "es", "spa", "100", 30240),
    ("SerbianLatin", "36", "sr", "scc", "100", 30237),
    ("Spanish (Spain)", "28", "es", "spa", "100", 30240),
    ("Chinese (Traditional)", "17", "zh", "chi", "100", 30207),
    ("Chinese (Simplified)", "17", "zh", "chi", "100", 30207))
import requests
ses = requests.Session()
          
def geturl(url1, headers =None, params = None):
        print "exeurl",url1
        #from reqData import reqData
       
        print "exeurl2",url1
        #content=reqData(url1)
        #return content

        

        
        try:
            res = ses.get(url1, headers=headers, verify=False, timeout=5)
            print 'res.status_code',res.status_code
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

def prepare_search_string(s):
    s = string.strip(s)
    s = re.sub(r'\(\d\d\d\d\)$', '', s)  # remove year from title
    s = urllib.quote_plus(s)
    return s
def find_movie(content, title, year):
    
    url_found = None
    h = HTMLParser.HTMLParser()
    for matches in re.finditer(movie_season_pattern, content, re.IGNORECASE | re.DOTALL):
        found_title = matches.group('title')
        found_title = h.unescape(found_title)
        #log(__name__, "Found movie on search page: %s (%s)" % (found_title, matches.group('year')))
        printD(__name__, "Found movie on search page: %s (%s)" % (found_title, matches.group('year')))
        if string.find(string.lower(found_title), string.lower(title)) > -1:
            if matches.group('year') == year:
                printD(__name__, "Matching movie found on search page: %s (%s)" % (found_title, matches.group('year')))


                url_found = matches.group('link')
                break
    return url_found

def getSearchTitle(title,year=None):
    
    url='https://subscene.com/subtitles/searchbytitle?query=%s&l='%urllib.quote_plus(title)
    data=geturl(url)
   
    blocks=data.split('class="title"')
    blocks.pop(0)
    list1=[]
    for block in blocks:
        regx='''<a href="(.*?)">(.*?)</a>'''
        try:
            matches=re.findall(regx,block)
            name=matches[0][1]
            href=matches[0][0]
            print "hrefxxx",href
            print "yearxx",year
            href='https://subscene.com'+href
            if year and year=='':
              if "/subtitles/" in href:
                  return href
            if not year:
              if "/subtitles/" in href:
                  return href
            
            if year and str(year) in name:
                
                if "/subtitles/" in href:
                   print "href",href
                   
                   return href


        except:
            break
        
    return 'https://subscene.com/subtitles/'+urllib.quote_plus(title)   

    
def search_movie(title, year, languages, filename):
    
    try:
        printD("start2",title)
        title = string.strip(title)
        search_string = prepare_search_string(title)

        
        #url = main_url + "/subtitles/title?q=" + urllib.quote_plus(search_string) + '&r=true'
        #url='https://subscene.com/subtitles/venom'
        url=getSearchTitle(search_string,year)
        print "true url",url
        printD("true url",url)
        
        content = geturl(url)
              
        if content=='':
           
           if content is None:
               return []
        
       
        print "content",content
        if content !='':
            
            
                    list=getallsubs(content, languages, filename)
                    printD("allsubs",list)
                    return list
           
    except Exception as error:
           printE()
           print "error",error
           printD("error",error)
def getallsubs(content, allowed_languages, filename="", search_string=""):
    subtitle_pattern = ("<a href=\"(?P<link>/subtitles/[^\"]+)\">\s+"
                        "<span class=\"[^\"]+ (?P<quality>\w+-icon)\">\s+(?P<language>[^\r\n\t]+)\s+</span>\s+"
                        "<span>\s+(?P<filename>[^\r\n\t]+)\s+</span>\s+"
                        "</a>\s+</td>\s+"
                        "<td class=\"[^\"]+\">\s+(?P<numfiles>[^\r\n\t]*)\s+</td>\s+"
                        "<td class=\"(?P<hiclass>[^\"]+)\">"
                        "(?P<rest>.*?)</tr>")
    comment_pattern = "<td class=\"a6\">\s+<div>\s+(?P<comment>[^\"]+)&nbsp;\s*</div>"

    subtitles = []
    h = HTMLParser.HTMLParser()
    allmatches=re.finditer(subtitle_pattern, content, re.IGNORECASE | re.DOTALL)
    print 'allmatches',allmatches
   
    i=0
    for matches in re.finditer(subtitle_pattern, content, re.IGNORECASE | re.DOTALL):
        numfiles = 1
        print 'matches',matches
        
        if matches.group('numfiles') != "":
            numfiles = int(matches.group('numfiles'))
        languagefound = matches.group('language')
        language_info = get_language_info(languagefound)
        if language_info and language_info['name'] in allowed_languages:
            link = main_url + matches.group('link')
            subtitle_name = string.strip(matches.group('filename'))
            hearing_imp = (matches.group('hiclass') == "a41")
            rating = '0'
            comment = ''
            if matches.group('quality') == "bad-icon":
                continue
            if matches.group('quality') == "positive-icon":
                rating = '5'

            commentmatch = re.search(comment_pattern, matches.group('rest'), re.IGNORECASE | re.DOTALL);
            if commentmatch != None:
                comment = re.sub("[\r\n\t]+", " ", h.unescape(string.strip(commentmatch.group('comment'))))

            sync = False
            if filename != "" and string.lower(filename) == string.lower(subtitle_name):
                sync = True

            if search_string != "":
                if string.find(string.lower(subtitle_name), string.lower(search_string)) > -1:
                    subtitles.append({'rating': rating, 'filename': subtitle_name, 'sync': sync, 'link': link,
                                     'language_name':language_info['name'], 'lang': language_info, 'hearing_imp': hearing_imp, 'comment': comment})


                     
                    i=i+1
                elif numfiles > 2:
                    subtitle_name = subtitle_name + ' ' + ("%d files" % int(matches.group('numfiles')))
                    subtitles.append({'rating': rating, 'filename': subtitle_name, 'sync': sync, 'link': link,
                                     'language_name':language_info['name'], 'lang': language_info, 'hearing_imp': hearing_imp, 'comment': comment})

                    i=i+1


            else:
                subtitles.append({'rating': rating, 'filename': subtitle_name, 'sync': sync, 'link': link,
                                 'language_name':language_info['name'], 'lang': language_info, 'hearing_imp': hearing_imp, 'comment': comment})
                i=i+1

    subtitles.sort(key=lambda x: [not x['sync']])
    print "len",len(subtitles)
    return subtitles

def get_language_info(language):
    if language in subscene_languages:
        language = subscene_languages[language]

    for lang in LANGUAGES:
        if lang[0] == language:
            return {'name': lang[0], '2let': lang[2], '3let': lang[3]}


def find_tv_show_season(content, tvshow, season):
    url_found = None
    possible_matches = []
    all_tvshows = []

    h = HTMLParser.HTMLParser()
    for matches in re.finditer(movie_season_pattern, content, re.IGNORECASE | re.DOTALL):
        found_title = matches.group('title')
        found_title = h.unescape(found_title)

        log(__name__, "Found tv show season on search page: %s" % found_title)
        s = difflib.SequenceMatcher(None, string.lower(found_title + ' ' + matches.group('year')), string.lower(tvshow))
        all_tvshows.append(matches.groups() + (s.ratio() * int(matches.group('numsubtitles')),))
        if string.find(string.lower(found_title), string.lower(tvshow) + " ") > -1:
            if string.find(string.lower(found_title), string.lower(season)) > -1:
                log(__name__, "Matching tv show season found on search page: %s" % found_title)
                possible_matches.append(matches.groups())

    if len(possible_matches) > 0:
        possible_matches = sorted(possible_matches, key=lambda x:-int(x[3]))
        url_found = possible_matches[0][0]
        log(__name__, "Selecting matching tv show with most subtitles: %s (%s)" % (
            possible_matches[0][1], possible_matches[0][3]))
    else:
        if len(all_tvshows) > 0:
            all_tvshows = sorted(all_tvshows, key=lambda x:-int(x[4]))
            url_found = all_tvshows[0][0]
            log(__name__, "Selecting tv show with highest fuzzy string score: %s (score: %s subtitles: %s)" % (
                all_tvshows[0][1], all_tvshows[0][4], all_tvshows[0][3]))

    return url_found



 



def search_tvshow(tvshow, season, episode, languages, filename):
    tvshow = string.strip(tvshow)
    search_string = prepare_search_string(tvshow)
    search_string += " - " + seasons[int(season)] + " Season"

    log(__name__, "Search tvshow = %s" % search_string)
    url = main_url + "/subtitles/title?q=" + urllib.quote_plus(search_string) + '&r=true'
    content, response_url = geturl(url)

    if content is not None:
        log(__name__, "Multiple tv show seasons found, searching for the right one ...")
        tv_show_seasonurl = find_tv_show_season(content, tvshow, seasons[int(season)])
        if tv_show_seasonurl is not None:
            log(__name__, "Tv show season found in list, getting subs ...")
            url = main_url + tv_show_seasonurl
            content, response_url = geturl(url)
            if content is not None:
                search_string = "s%#02de%#02d" % (int(season), int(episode))
                return getallsubs(content, languages, filename, search_string)


def search_manual(searchstr, languages, filename):
    search_string = prepare_search_string(searchstr)
    url = main_url + "/subtitles/release?q=" + search_string + '&r=true'
    content, response_url = geturl(url)

    if content is not None:
        return getallsubs(content, languages, filename)

 

def search_subtitles(file_original_path, title, tvshow, year, season, episode, set_temp, rar, lang1, lang2, lang3, stack):  # standard input
    log(__name__ , "%s Search_subtitles = '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s'" % 
         (debug_pretext, file_original_path, title, tvshow, year, season, episode, set_temp, rar, lang1, lang2, lang3, stack))
    if lang1 == 'Farsi':
        lang1 = 'Persian'
    if lang2 == 'Farsi':
        lang2 = 'Persian'
    if lang3 == 'Farsi':
        lang3 = 'Persian'
    if tvshow:
        sublist = search_tvshow(tvshow, season, episode, [lang1, lang2, lang3], file_original_path)
    elif title :
        sublist = search_movie(title, year, [lang1, lang2, lang3], file_original_path)
    else:
        try:
          sublist = search_manual(title, [lang1, lang2, lang3], file_original_path)
        except:
            printE()
    return sublist, "", ""


def download_subtitles (subtitles_list, pos, zip_subs, tmp_sub_dir, sub_folder, session_id):  # standard input
    url = subtitles_list[pos][ "link" ]
    language = subtitles_list[pos][ "language_name" ]
    content = geturl(url)
    downloadlink_pattern = "...<a href=\"(.+?)\" rel=\"nofollow\" onclick=\"DownloadSubtitle"
    match = re.compile(downloadlink_pattern).findall(content)
    if match:
        downloadlink = "http://subscene.com" + match[0]
        log(__name__ , "%s Downloadlink: %s " % (debug_pretext, downloadlink))
        viewstate = 0
        previouspage = 0
        subtitleid = 0
        typeid = "zip"
        filmid = 0
        postparams = urllib.urlencode({ '__EVENTTARGET': 's$lc$bcr$downloadLink', '__EVENTARGUMENT': '' , '__VIEWSTATE': viewstate, '__PREVIOUSPAGE': previouspage, 'subtitleId': subtitleid, 'typeId': typeid, 'filmId': filmid})
        class MyOpener(urllib.FancyURLopener):
            version = 'User-Agent=Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.2.3) Gecko/20100401 Firefox/3.6.3 ( .NET CLR 3.5.30729)'
        my_urlopener = MyOpener()
        my_urlopener.addheader('Referer', url)
        log(__name__ , "%s Fetching subtitles using url '%s' with referer header '%s' and post parameters '%s'" % (debug_pretext, downloadlink, url, postparams))
        response = my_urlopener.open(downloadlink, postparams)
        local_tmp_file = zip_subs
        try:
            log(__name__ , "%s Saving subtitles to '%s'" % (debug_pretext, local_tmp_file))
            if not os.path.exists(tmp_sub_dir):
                os.makedirs(tmp_sub_dir)
            local_file_handle = open(local_tmp_file, "w" + "b")
            local_file_handle.write(response.read())
            local_file_handle.close()
            # Check archive type (rar/zip/else) through the file header (rar=Rar!, zip=PK)
            myfile = open(local_tmp_file, "rb")
            myfile.seek(0)
            if (myfile.read(1) == 'R'):
                typeid = "rar"
                packed = True
                log(__name__ , "Discovered RAR Archive")
            else:
                myfile.seek(0)
                if (myfile.read(1) == 'P'):
                    typeid = "zip"
                    packed = True
                    log(__name__ , "Discovered ZIP Archive")
                else:
                    typeid = "srt"
                    packed = False
                    subs_file = local_tmp_file
                    log(__name__ , "Discovered a non-archive file")
            myfile.close()
            log(__name__ , "%s Saving to %s" % (debug_pretext, local_tmp_file))
        except:
            printD("errortttt","error")
            log(__name__ , "%s Failed to save subtitle to %s" % (debug_pretext, local_tmp_file))
        if packed:
            subs_file = typeid
        log(__name__ , "%s Subtitles saved to '%s'" % (debug_pretext, local_tmp_file))
        printD('packed',packed)
        return packed, language, subs_file  # standard output
        
