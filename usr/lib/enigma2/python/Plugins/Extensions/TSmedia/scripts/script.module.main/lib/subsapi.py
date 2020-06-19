# Embedded file name: /usr/lib/enigma2/python/Plugins/Extensions/TSmedia/lib/subsapi.py
import requests, json, sys, os
import zipfile

os_platform = sys.platform
print 'Os Platform: ' + os_platform
if os_platform == 'win32':
    sub_path = os.getcwd()
if os_platform == 'linux':
    sub_path = '/tmp/'
sub_path = '/tmp/'
hdr = {'User-Agent': 'okhttp/3.10.0',
 'Accept-Encoding': 'gzip'}
print 'SUB PATH: ' + sub_path

##########################################parsing tools
def printE(msg=''):
    import traceback,sys
    printD("===============================================")
    printD("                   EXCEPTION                   ")
    printD("===============================================")
    msg = msg + ': \n%s' % traceback.format_exc()
    traceback.print_exc(file=sys.stdout)
    printD("Error",msg)
    printD("===============================================")
log_file='/tmp/TSmedia/subsid.log'    
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
            print("======================EXC printD======================")
            print("Log: %s" % traceback.format_exc())
            print("========================================================")
            try:
                msg = '%s' % traceback.format_exc()
                f = open(log_file, 'a')
                f.write(Ddata + '\n')
                f.close
            except Exception:
                print("======================EXC printD======================")
                print("logII: %s" % traceback.format_exc())
                print("========================================================")
########################################

printD('subsapi', 'subsapi')

def getSupportedSub_ids(imdb_id = '',default_languages=False):
    printD('movie_imdb', imdb_id)
    s = requests.Session()
    try:
        GetSub = False


        data = s.get('http://sub.apiumadomain.com/list?hash=' + '&imdb=' + imdb_id, headers=hdr, verify=False)
        jsdata = data.json()
        subitems = jsdata['subs']
        print 'subitems', len(subitems)
        printD('subitems', subitems)
        if subitems == []:
            return (False, [])
        count = 0
        sub_id = None
        sub_url = None
        sub_ids = []
        sts = False
        for item in subitems:
            langName = langs.get(item, '')
            if langName == '':
                continue
            lang1=open("/tmp/TSmedia/sublngID").read()
            
            if item in lang1 :
               sub_ids.append((langName, item))
               sts = True

        printD('sub_ids', sub_ids)
        return (sts, sub_ids)
    except:
        printE()
        return (False, [])

    return


def getmovie_sub(torrent_imdb = '', sub_lng_id = '', rename_srt = True, torrent_hash = ''):
    s = requests.Session()
    try:
        GetSub = False
        data = s.get('http://sub.apiumadomain.com/list?hash=' + torrent_hash + '&imdb=' + torrent_imdb, headers=hdr, verify=False)
        jsdata = data.json()
        subitems = jsdata['subs']
        #print 'subitems', subitems
        if subitems == []:
            return (False, None, None)
        count = 0
        sub_id = None
        sub_url = None
        item = subitems.get(sub_lng_id, None)
        if item:
            print 'Sub Lng: ' + str(item)
            sub_rating = item[0]['rating']
            sub_id = str(item[0]['id'])
            sub_url = item[0]['url']
            print '****************************************************************************'
            print 'Sub IMDB ID               : ' + torrent_imdb
            print 'Sub ID                    : ' + sub_id
            print 'Sub Torrent Hash          : ' + torrent_hash
            print 'Sub Best Available Rating : ' + str(sub_rating)
            print 'Sub Url    : ' + sub_url
        else:
            return (False, None, None)
        if sub_id:
            zip_fname = os.path.join(sub_path, sub_id + '.zip')
        else:
            zip_fname = None
        print 'sub_url', sub_url
        if sub_url:
            sub_data = s.get(sub_url, headers=hdr, verify=False)
        else:
            sub_data = None
            return (False, None, None)
        print 'sub_dataxx', sub_data
        subPath = None
        if sub_data and sub_data.status_code == 200:
            with open(zip_fname, 'wb') as f:
                f.write(sub_data.content)
            with zipfile.ZipFile(zip_fname, 'r') as zip_sub:
                zip_sub.extractall(sub_path)
                unzip_sub_name = ''.join(zip_sub.namelist())
                subPath = os.path.join(sub_path, unzip_sub_name)
                print 'Sub Srt Path              : ' + subPath
                print '****************************************************************************'
                if rename_srt:
                    try:
                        os.rename(os.path.join(sub_path, unzip_sub_name), os.path.join(sub_path, rename_srt + '.srt'))
                    except:
                        pass

            zip_sub.close
            os.remove(zip_fname)
            GetSub = True
        else:
            print 'sub_data.status_code', sub_data.status_code
            return (False, None, None)
    except Exception as e:
        printD("error",e)
        printE()
        GetSub = False
        sub_url = None
        sub_id = None
        sub_rating = None
        unzip_sub_name = None
        subPath = None
        print str(e)

    print '######finished########'
    subName=os.path.basename(subPath)
    if sub_lng_id !="":
       subName=subName.replace(".srt","-"+sub_lng_id+".srt")
    return (GetSub, sub_url, subName)


langs = {'gu': 'Gujarati',
 'lb': 'Luxembourgish',
 'lo': 'Lao',
 'tt': 'Tatar',
 'tr': 'Turkish Q',
 'tn': 'Setswana',
 'lt': 'Lithuanian Standard',
 'tk': 'Turkmen',
 'th': 'Thai Pattachote ',
 'tg': 'Tajik',
 'te': 'Telugu',
 'ta': 'Tamil',
 'yo': 'Yoruba',
 'de': 'Swiss German',
 'da': 'Danish',
 'dv': 'Divehi Typewriter',
 'lv': 'Latvian ',
 'el': 'Greek Polytonic',
 'en': 'United States-International',
 'zh': 'Chinese ',
 'et': 'Estonian',
 'es': 'Spanish Variation',
 'ru': 'Russian ',
 'ro': 'Romanian ',
 'hsb': 'Sorbian Standard ',
 'be': 'Belarusian',
 'bg': 'Bulgarian ',
 'ba': 'Bashkir',
 'wo': 'Wolof',
 'bn': 'Bengali - INSCRIPT ',
 'bo': 'Tibetan ',
 'bs': 'Bosnian ',
 'ja': 'Japanese',
 'syr': 'Syriac Phonetic',
 'or': 'Oriya',
 'nso': 'Sesotho sa Leboa',
 'cy': 'United Kingdom Extended',
 'cs': 'Czech Programmers',
 'ps': 'Pashto ',
 'pt': 'Portuguese ',
 'pa': 'Punjabi',
 'pl': 'Polish ',
 'hy': 'Armenian Western',
 'hr': 'Croatian',
 'hu': 'Hungarian 101-key',
 'hi': 'Hindi Traditional',
 'ha': 'Hausa',
 'he': 'Hebrew',
 'uz': 'Uzbek Cyrillic',
 'ml': 'Malayalam',
 'mn': 'Mongolian Cyrillic',
 'mi': 'Maori',
 'mk': 'Macedonian ',
 'ur': 'Urdu',
 'mt': 'Maltese 48-Key',
 'uk': 'Ukrainian ',
 'mr': 'Marathi',
 'ug': 'Uyghur ',
 'sah': 'Yakut',
 'vi': 'Vietnamese',
 'is': 'Icelandic',
 'iu': 'Inuktitut - Naqittaut',
 'it': 'Italian ',
 'kn': 'Kannada',
 'as': 'Assamese - INSCRIPT',
 'ar': 'Arabic ',
 'az': 'Azeri Latin',
 'ig': 'Igbo',
 'nl': 'Dutch',
 'nb': 'Norwegian',
 'ne': 'Nepali',
 'fr': 'Swiss French',
 'fa': 'Persian',
 'fi': 'Finnish',
 'fo': 'Faeroese',
 'ka': 'Georgian ',
 'kk': 'Kazakh',
 'sr': 'Serbian ',
 'sq': 'Albanian',
 'ko': 'Korean',
 'sv': 'Swedish',
 'km': 'Khmer',
 'kl': 'Greenlandic',
 'sk': 'Slovak ',
 'si': 'Sinhala - Wij 9',
 'sl': 'Slovenian',
 'ky': 'Kyrgyz Cyrillic',
 'se': 'Swedish with Sami'}
langsList=[]
for item in langs.keys():
   langsList.append((item,langs[item]))
langsList = sorted(langsList, key=lambda x:x[1])                    
#imdb_id='tt0111161'
#print getSupportedSub_ids(imdb_id)

#print getmovie_sub(imdb_id,sub_lng_id="ar")
