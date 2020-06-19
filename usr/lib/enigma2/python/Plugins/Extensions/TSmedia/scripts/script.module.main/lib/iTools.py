# -*- coding: utf-8 -*-
# @file  ihost.py
#

###################################################
# E2 GUI COMMPONENTS 
###################################################
import os,re,sys,urllib,urllib2,traceback,ast
import xml.etree.cElementTree
import cookielib
import time
############################

from urlparse import urljoin
from time import sleep as time_sleep

from urllib2 import Request, urlopen, URLError, HTTPError
import stat
import codecs
import datetime
from urlparse import urlparse, urlunparse, parse_qs
import gettext
from cStringIO import StringIO
from vstream.requestHandler import cRequestHandler

import gzip
###############TSmedia stuff######################
def getAppPath():
    return __file__.split("/scripts")[0]
AppPath=getAppPath()
plugin_path=AppPath
def getos():
    if AppPath.startswith('/usr'):
        return 'enigma2'
    else:
        return 'windows'

if getos()=='enigma2':
   data_file='/tmp/TSmedia/data.json'
   log_file='/tmp/TSmedia/TSmedia.log'
   searchtext_file='/tmp/TSmedia/searchSTR'
else:
   data_file=AppPath+'/tmp/json.txt'
   log_file=AppPath+'/tmp/TSmedia/TSmedia2.log'
   searchtext_file=AppPath+'/tmp/xbmc_search.txt'
def enigmaos():
    if os.path.exists('/var/lib/dpkg/status'):
        return 'oe2.2'
    else:
        return 'oe2.0'
log_file='/tmp/TSmedia/TSmedia.log'    
##############iptvtools
SERVER_DOMAINS = {'vline':'http://addonsParser.vline.pl/', 'gitlab':'http://www.addonsParser.gitlab.io/', 'private':'http://www.e2iplayer.gitlab.io/'}
SERVER_UPDATE_PATH = {'vline':'download/update2/', 'gitlab':'update2/', 'private':'update2/'}
def getAppPath():
    return __file__.split("/scripts")[0]

def getDownloadPath():
    try:downloadDir=open("/tmp/TSmedia/downloadDir").read()
    except:downloadDir="/media/hdd"
    return downloadDir
def getCachePath():
    return getAppPath()+"/media/hdd"
def getAppTmp():
    return getAppPath()+"/tmp"
def getAppDukPath():
    return getAppPath()+"/bin/duk"
#config.plugins.addonsParser.SciezkaCache = ConfigText(default = "/hdd/IPTVCache")
SCOPE_PLUGINS=getAppPath()+"/scripts/script.module.urlresolver/lib/"
cookieDir=getAppPath()+"/media/hdd/IPTVCache"
from os.path import join as resolveFilename

gE2iPlayerTempCookieDir = None
def SetTmpCookieDir():
    global gE2iPlayerTempCookieDir
    gE2iPlayerTempCookieDir = getAppPath()+'/tmp/TSmedia_cookies/'
    mkdirs(gE2iPlayerTempCookieDir)
    
def ClearTmpCookieDir():
    global gE2iPlayerTempCookieDir
    if gE2iPlayerTempCookieDir != None:
        try:
            for file in os.listdir( gE2iPlayerTempCookieDir ):
                rm(gE2iPlayerTempCookieDir + '/' + file)
        except Exception:
            printExc()
    
    gE2iPlayerTempCookieDir = None

def TestTmpCookieDir():
    path = GetCookieDir(forceFromConfig=True)
    if not os.path.isdir(path):
        mkdirs(path, True)
    with open(path + ".rw_test", 'w') as f:
        f.write("test")

def GetCookieDir(file = '', forceFromConfig=False):
    global gE2iPlayerTempCookieDir
    
    cookieDir =getCachePath()+"/cookie"
    print 'cookieDirxxx',cookieDir
    try:
        if not os.path.isdir(cookieDir):
            mkdirs(cookieDir)
    except Exception: printExc()
    return cookieDir +"/"+ file

###########################
gE2iPlayerTempJSCache = None
def SetTmpJSCacheDir():
    global gE2iPlayerTempJSCache
    gE2iPlayerTempJSCache = getAppPath()+'/tmp/TSmedia_js_cache/'
    mkdirs(gE2iPlayerTempJSCache)

def ClearTmpJSCacheDir():
    global gE2iPlayerTempJSCache
    if gE2iPlayerTempJSCache != None:
        try:
            for file in os.listdir( gE2iPlayerTempJSCache ):
                rm(gE2iPlayerTempJSCache + '/' + file)
        except Exception:
            printExc()
    gE2iPlayerTempJSCache = None

def TestTmpJSCacheDir():
    path = GetJSCacheDir(forceFromConfig=True)
    if not os.path.isdir(path):
        mkdirs(path, True)
    with open(path + ".rw_test", 'w') as f:
        f.write("test")

def GetJSCacheDir(file = '', forceFromConfig=False):
    global gE2iPlayerTempJSCache
    
    cookieDir=getAppPath()+"/media/hdd/IPTVCache"
    if gE2iPlayerTempJSCache == None or forceFromConfig: cookieDir = cookieDir + '/JSCache/'
    else: cookieDir = gE2iPlayerTempJSCache
    try:
        if not os.path.isdir(cookieDir):
            mkdirs(cookieDir)
    except Exception: printExc()
    return cookieDir + file
##############################

def GetTmpDir(file = ''):
    path = getAppTmp()#config.plugins.addonsParser.NaszaTMP.value
    path = path.replace('//', '/')
    mkdirs(path)
    return path + '/' + file

def GetE2iPlayerRootfsDir(file = ''):
    return '/addonsParser_rootfs/' + file

def GetE2iPlayerVKLayoutDir(file = ''):
    return GetE2iPlayerRootfsDir('etc/vk/' + file)
    
def CreateTmpFile(filename, data=''):
    sts = False
    filePath = GetTmpDir(filename)
    try:
        with open(filePath, 'w') as f:
            f.write(data)
            sts = True
    except Exception:
        printExc()
    return sts, filePath
    
def GetCacheSubDir(dir, file = ''):
    path = getCachePath()+ "/" + dir#config.plugins.addonsParser.SciezkaCache.value + "/" + dir
    path = path.replace('//', '/')
    mkdirs(path)
    return path + '/' + file

def getDebugMode():
    DBG=''

    return DBG


def IsValidFileName(name, NAME_MAX=255):
    prohibited_characters = ['/', "\000", '\\', ':', '*', '<', '>', '|', '"']
    if isinstance(name, basestring) and (1 <= len(name) <= NAME_MAX):
        for it in name:
            if it in prohibited_characters:
                return False
        return True
    return False
def unicode_escape(s):
    decoder = codecs.getdecoder('unicode_escape')
    return re.sub(r'\\u[0-9a-fA-F]{4,}', lambda m: decoder(m.group(0))[0], s).encode('utf-8')
    
def RemoveDisallowedFilenameChars(name, replacment='.'):
    prohibited_characters = ['/', "\000", '\\', ':', '*', '<', '>', '|', '"']
    for item in prohibited_characters:
        name = name.replace(item, replacment).replace(replacment+replacment, replacment)
    return name    
def touch(fname, times=None):
    try:
        with open(fname, 'a'):
            os.utime(fname, times)
        return True
    except Exception:
        printExc()
        return False
        
        
def mkdir(newdir):
    """ Wrapper for the os.mkdir function
        returns status instead of raising exception
    """
    try:
        os.mkdir(newdir)
        sts = True
        msg = 'Katalog "%s" został utworzony poprawnie.' % newdir
    except Exception:
        sts = False
        msg = 'Katalog "%s" nie może zostać utworzony.' % newdir
        printExc()
    return sts,msg

def mkdirs(newdir, raiseException=False):
    """ Create a directory and all parent folders.
        Features:
        - parent directories will be created
        - if directory already exists, then do nothing
        - if there is another filsystem object with the same name, raise an exception
    """
    printDBG('mkdirs: "%s"' % newdir)
    try:
        if os.path.isdir(newdir):
            pass
        elif os.path.isfile(newdir):
            raise OSError("cannot create directory, file already exists: '%s'" % newdir)
        else:
            head, tail = os.path.split(newdir)
            if head and not os.path.isdir(head) and not os.path.ismount(head) and not os.path.islink(head):
                mkdirs(head)
            if tail:
                os.mkdir(newdir)
        return True
    except Exception, e:
        printDBG('Exception mkdirs["%s"]' % e)
        if raiseException:
            raise e
    return False
        
def rm(fullname):
    try:
        os.remove(fullname)
        return True
    except Exception: printExc()
    return False

def rmtree(path, ignore_errors=False, onerror=None):
    """Recursively delete a directory tree.
    If ignore_errors is set, errors are ignored; otherwise, if onerror
    is set, it is called to handle the error with arguments (func,
    path, exc_info) where func is os.listdir, os.remove, or os.rmdir;
    path is the argument to that function that caused it to fail; and
    exc_info is a tuple returned by sys.exc_info(). If ignore_errors
    is false and onerror is None, an exception is raised.
    """
    if ignore_errors:
        def onerror(*args):
            pass
    elif onerror is None:
        def onerror(*args):
            raise
    try:
        if os.path.islink(path):
            # symlinks to directories are forbidden, see bug #1669
            raise OSError("Cannot call rmtree on a symbolic link")
    except OSError:
        onerror(os.path.islink, path)
        # can't continue even if onerror hook returns
        return
    names = []
    try:
        names = os.listdir(path)
    except os.error, err:
        onerror(os.listdir, path)
    for name in names:
        fullname = os.path.join(path, name)
        try:
            mode = os.lstat(fullname).st_mode
        except os.error:
            mode = 0
        if stat.S_ISDIR(mode):
            rmtree(fullname, ignore_errors, onerror)
        else:
            try:
                os.remove(fullname)
            except os.error, err:
                onerror(os.remove, fullname)
    try:
        os.rmdir(path)
    except os.error:
        onerror(os.rmdir, path) 
        
def GetFileSize(filepath):
    try:
        return os.stat(filepath).st_size
    except Exception:
        return -1
       
def DownloadFile(url, filePath):
    printDBG('DownloadFile [%s] from [%s]' % (filePath, url) )
    try:
        downloadFile = urllib2.urlopen(url)
        output = open(filePath, 'wb')
        output.write(downloadFile.read())
        output.close()
        try:
            os.system('sync')
        except Exception:
            printExc('DownloadFile sync exception')
        return True
    except Exception:
        printExc()
        try:
            if os.path.exists(filePath):
                os.remove(filePath)
            return False
        except Exception:
            printExc()
            return False
def GetLastDirNameFromPath(path):
    path = os.path.normcase(path)
    if path[-1] == '/':
        path = path[:-1]
    dirName = path.split('/')[-1]
    return dirName

def formatBytes(bytes, precision = 2):
    import math
    units = ['B', 'KB', 'MB', 'GB', 'TB'] 
    bytes = max(bytes, 0); 
    if bytes:
        pow = math.log(bytes)
    else:
        pow = 0
    pow = math.floor(pow / math.log(1024)) 
    pow = min(pow, len(units) - 1) 
    bytes /= math.pow(1024, pow);
    return ("%s%s" % (str(round(bytes, precision)),units[int(pow)])) 
    
def remove_html_markup(s, replacement=''):
    tag = False
    quote = False
    out = ""
    for c in s:
            if c == '<' and not quote:
                tag = True
            elif c == '>' and not quote:
                tag = False
                out += replacement
            elif (c == '"' or c == "'") and tag:
                quote = not quote
            elif not tag:
                out = out + c
    return re.sub('&\w+;', ' ',out)

def ReadTextFile(filePath, encode='utf-8', errors='ignore'):
    sts, ret = False, ''
    try:
        file = codecs.open(filePath, 'r', encode, errors)
        ret = file.read().encode(encode, errors)
        file.close()
        if ret.startswith(codecs.BOM_UTF8):
            ret = ret[3:]
        sts = True
    except Exception:
        printExc()
    return sts, ret

def WriteTextFile(filePath, text, encode='utf-8', errors='ignore'):
    sts = False
    try:
        toSave = text if type(u'') == type(text) else text.decode('utf-8', errors)
        file = codecs.open(filePath, 'w', encode, errors)
        file.write(toSave)
        file.close()
        sts = True
    except Exception:
        printExc()
    return sts
def byteify(input, noneReplacement=None, baseTypesAsString=False):
    if isinstance(input, dict):
        return dict([(byteify(key, noneReplacement, baseTypesAsString), byteify(value, noneReplacement, baseTypesAsString)) for key, value in input.iteritems()])
    elif isinstance(input, list):
        return [byteify(element, noneReplacement, baseTypesAsString) for element in input]
    elif isinstance(input, unicode):
        return input.encode('utf-8')
    elif input == None and noneReplacement != None:
        return noneReplacement
    elif baseTypesAsString:
        return str(input)
    else:
        return input
def IsHttpsCertValidationEnabled():
    return False#config.plugins.addonsParser.httpssslcertvalidation.value
    
def IsWebInterfaceModuleAvailable(chekInit=False):
    if chekInit:
        file = '__init__'
    else:
        file = 'initiator'
    if (fileExists(resolveFilename(SCOPE_PLUGINS, '/addonsParser/Web/%s.py'  % file)) or
        fileExists(resolveFilename(SCOPE_PLUGINS, '/addonsParser/Web/%s.pyo' % file)) or
        fileExists(resolveFilename(SCOPE_PLUGINS, '/addonsParser/Web/%s.pyc' % file))):
        return True
    else:
        return False
    
def printExc(msg=''):
    printDBG("===============================================")
    printDBG("                   EXCEPTION                   ")
    printDBG("===============================================")
    msg = msg + ': \n%s' % traceback.format_exc()
    traceback.print_exc(file=sys.stdout)
    printDBG(msg)
    printDBG("===============================================")



##################ddonsParser.components.addonsParserinit
PluginLanguageDomain = "TSmedia"
PluginLanguagePath = "Extensions/TSmedia/locale"
    
def TranslateTXT(txt):
    t = gettext.dgettext(PluginLanguageDomain, txt)
    if t == txt:
        t = gettext.gettext(txt)
    return t
_=TranslateTXT
#####################addonsParser.tools.iptvtypes
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
def DecodeGzipped(data):
    buf = StringIO(data)
    f = gzip.GzipFile(fileobj=buf)
    return f.read()

def EncodeGzipped(data):
    f = StringIO()
    gzf = gzip.GzipFile(mode="wb", fileobj=f, compresslevel=1)
    gzf.write(data)
    gzf.close()
    encoded = f.getvalue()
    f.close()
    return encoded
######################ph
NONE=0
START_E=1
START_S=2
END_E=4
END_S=8
IGNORECASE=16
I=16

# pre-compiled regular expressions
IFRAME_SRC_URI_RE = re.compile(r'''<iframe[^>]+?src=(['"])([^>]*?)(?:\1)''', re.I)
IMAGE_SRC_URI_RE = re.compile(r'''<img[^>]+?src=(['"])([^>]*?\.(?:jpe?g|png)(?:\?[^\1]*?)?)(?:\1)''', re.I)
A_HREF_URI_RE = re.compile(r'''<a[^>]+?href=(['"])([^>]*?)(?:\1)''', re.I)
STRIP_HTML_COMMENT_RE = re.compile("<!--[\s\S]*?-->")

# add short aliases
IFRAME = IFRAME_SRC_URI_RE
IMG = IMAGE_SRC_URI_RE
A = A_HREF_URI_RE

def getattr(data, attrmame, flags=0):
    if flags & IGNORECASE:
        sData = data.lower() 
        m = '%s=' % attrmame.lower() 
    else:
        sData = data
        m = '%s=' % attrmame
    sidx = 0
    while True:
        sidx = sData.find(m, sidx)
        if sidx == -1:
            return ''
        if data[sidx - 1] in ('\t', ' ', '\n', '\r'):
            break
        sidx += len(m)
    sidx += len(m)
    z = data[sidx]
    if z not in ('"', "'"):
        return ''
    eidx = sidx + 1
    while eidx < len(data):
        if data[eidx] == z:
            return data[sidx+1:eidx]
        eidx += 1
    return ''

def search(data, pattern, flags=0, limits=-1):
    tab = []
    if isinstance(pattern, basestring):
        reObj = re.compile(pattern, re.IGNORECASE if flags & IGNORECASE else 0)
    else:
        reObj = pattern
    if limits == -1:
        limits = reObj.groups
    match = reObj.search(data)
    for idx in range(limits):
        try:    value = match.group(idx + 1)
        except Exception: value = ''
        tab.append(value)
    return tab

def all(tab, data, start, end):
    for it in tab:
        if data.find(it, start, end) == -1:
            return False
    return True

def any(tab, data, start, end):
    for it in tab:
        if data.find(it, start, end) != -1:
            return True
    return False

def none(tab, data, start, end):
    return not any(tab, data, start, end)

# example: findall(data, ('<a', '>', check(any, ('articles.php', 'readarticle.php'))), '</a>')
def check(arg1, arg2=None):
    if arg2 == None and isinstance(arg1, basestring):
        return lambda data, ldata, s, e: ldata.find(arg1, s, e) != -1
    
    return lambda data, ldata, s, e: arg1(arg2, ldata, s, e)

def findall(data, start, end=('',), flags=START_E|END_E, limits=-1):

    start = start if isinstance(start, tuple) or isinstance(start, list) else (start,)
    end = end if isinstance(end, tuple) or isinstance(end, list) else (end,)

    if len(start) < 1 or len(end) < 1:
        return []

    itemsTab = []

    n1S = start[0]
    n1E = start[1] if len(start) > 1 else ''
    match1P = start[2] if len(start) > 2 else None
    match1P = check(match1P) if isinstance(match1P, basestring) else match1P

    n2S = end[0]
    n2E = end[1] if len(end) > 1 else ''
    match2P = end[2] if len(end) > 2 else None
    match2P = check(match2P) if isinstance(match2P, basestring) else match2P

    lastIdx = 0
    search = 1
    
    if not (flags & IGNORECASE):
        sData = data
    else:
        sData = data.lower()
        n1S = n1S.lower()
        n1E = n1E.lower()
        n2S = n2S.lower()
        n2E = n2E.lower()

    while True:
        if search == 1:
            # node 1 - start
            idx1 = sData.find(n1S, lastIdx)
            if -1 == idx1: return itemsTab
            lastIdx = idx1 + len(n1S)
            idx2 = sData.find(n1E, lastIdx)
            if -1 == idx2: return itemsTab
            lastIdx = idx2 + len(n1E)

            if match1P and not  match1P(data, sData, idx1 + len(n1S), idx2):
                continue

            search = 2
        else:
            # node 2 - end
            tIdx1 = sData.find(n2S, lastIdx)
            if -1 == tIdx1: return itemsTab
            lastIdx = tIdx1 + len(n2S)
            tIdx2 = sData.find(n2E, lastIdx)
            if -1 == tIdx2: return itemsTab
            lastIdx = tIdx2 + len(n2E)

            if match2P and not  match2P(data, sData, tIdx1 + len(n2S), tIdx2):
                continue

            if flags & START_S:
                itemsTab.append(data[idx1:idx2 + len(n1E)])

            idx1 = idx1 if flags & START_E else idx2 + len(n1E)
            idx2 = tIdx2 + len(n2E) if flags & END_E else tIdx1

            itemsTab.append(data[idx1:idx2])

            if flags & END_S:
                itemsTab.append(data[tIdx1:tIdx2 + len(n2E)])

            search = 1

        if limits > 0 and len(itemsTab) >= limits:
            break
    return itemsTab

def rfindall(data, start, end=('',), flags=START_E|END_E, limits=-1):

    start = start if isinstance(start, tuple) or isinstance(start, list) else (start,)
    end = end if isinstance(end, tuple) or isinstance(end, list) else (end,)

    if len(start) < 1 or len(end) < 1:
        return []

    itemsTab = []

    n1S = start[0]
    n1E = start[1] if len(start) > 1 else ''
    match1P = start[2] if len(start) > 2 else None
    match1P = check(match1P) if isinstance(match1P, basestring) else match1P

    n2S = end[0]
    n2E = end[1] if len(end) > 1 else ''
    match2P = end[2] if len(end) > 2 else None
    match2P = check(match2P) if isinstance(match2P, basestring) else match2P

    lastIdx = len(data)
    search = 1
    
    if not (flags & IGNORECASE):
        sData = data
    else:
        sData = data.lower()
        n1S = n1S.lower()
        n1E = n1E.lower()
        n2S = n2S.lower()
        n2E = n2E.lower()

    while True:
        if search == 1:
            # node 1 - end
            idx1 = sData.rfind(n1S, 0, lastIdx)
            if -1 == idx1: return itemsTab
            lastIdx = idx1
            idx2 = sData.find(n1E, idx1+len(n1S))
            if -1 == idx2: return itemsTab

            if match1P and not  match1P(data, sData, idx1 + len(n1S), idx2):
                continue

            search = 2
        else:
            # node 2 - start
            tIdx1 = sData.rfind(n2S, 0, lastIdx)
            if -1 == tIdx1: return itemsTab
            lastIdx = tIdx1
            tIdx2 = sData.find(n2E, tIdx1+len(n2S), idx1)
            if -1 == tIdx2: return itemsTab

            if match2P and not  match2P(data, sData, tIdx1 + len(n2S), tIdx2):
                continue

            if flags & START_S:
                itemsTab.insert(0, data[idx1:idx2 + len(n1E)])

            s1 = tIdx1 if flags & START_E else tIdx2 + len(n2E)
            s2 = idx2 + len(n1E) if flags & END_E else idx1

            itemsTab.insert(0, data[s1:s2])

            if flags & END_S:
                itemsTab.insert(0, data[tIdx1:tIdx2 + len(n2E)])

            search = 1

        if limits > 0 and len(itemsTab) >= limits:
            break
    return itemsTab


def find(data, start, end=('',), flags=START_E|END_E):
    ret = findall(data, start, end, flags, 1)
    if len(ret): return True, ret[0]
    else: return False, ''

def rfind(data, start, end=('',), flags=START_E|END_E):
    ret = rfindall(data, start, end, flags, 1)
    if len(ret): return True, ret[0]
    else: return False, ''

def strip_doubles(data, pattern):
    while -1 < data.find(pattern+pattern) and '' != pattern:
        data = data.replace(pattern+pattern, pattern)
    return data 

STRIP_HTML_TAGS_C = None
def clean_html(str):
    global STRIP_HTML_TAGS_C
    if None == STRIP_HTML_TAGS_C:
        STRIP_HTML_TAGS_C = False
        try:
            from Plugins.Extensions.addonsParser.libs.iptvsubparser import _subparser as p
            if 'strip_html_tags' in dir(p):
                STRIP_HTML_TAGS_C = p
        except Exception:
            printExc()

    if STRIP_HTML_TAGS_C and type(u' ') != type(str):
        return STRIP_HTML_TAGS_C.strip_html_tags(str)

    str = str.replace('<', ' <')
    str = str.replace('&nbsp;', ' ')
    str = str.replace('&nbsp', ' ')
    str = yt_clean_html(str)
    str = str.replace('\n', ' ').replace('\r', ' ').replace('\t', ' ')
    return strip_doubles(str, ' ').strip()



class NoRedirection(urllib2.HTTPRedirectHandler):
    def http_error_302(self, req, fp, code, msg, headers):
        infourl = urllib.addinfourl(fp, headers, req.get_full_url())
        infourl.status = code
        infourl.code = code
        return infourl
    http_error_300 = http_error_302
    http_error_301 = http_error_302
    http_error_303 = http_error_302
    http_error_307 = http_error_302

class MultipartPostHandler(urllib2.BaseHandler):
    handler_order = urllib2.HTTPHandler.handler_order - 10

    def http_request(self, request):
        data = request.get_data()
        if data is not None and type(data) != str:
            content_type, data = self.encode_multipart_formdata( data )
            request.add_unredirected_header('Content-Type', content_type)
            request.add_data(data)
        return request
        
    def encode_multipart_formdata(self, fields):
        LIMIT = '-----------------------------14312495924498'
        CRLF = '\r\n'
        L = []
        for (key, value) in fields:
            L.append('--' + LIMIT)
            L.append('Content-Disposition: form-data; name="%s"' % key)
            L.append('')
            L.append(value)
        L.append('--' + LIMIT + '--')
        L.append('')
        body = CRLF.join(L)
        content_type = 'multipart/form-data; boundary=%s' % LIMIT
        return content_type, body
    
    https_request = http_request

##################    
class Item(object):
    def __init__(self,module_path=None):

        self.list=[]
        self.spath=sys.argv[0]
        self.addon_id=self.spath.split("/")[-2]
        self.section_id=self.spath.split("/")[-3]
        self.addonSPath=self.section_id+"/"+self.addon_id
        #self.__dict__ = self.toutf8(self.__dict__)
    def addDir(self,name='', url='', mode=0, image='',category='',page=1,maintitle = False, link = False,desc='', extra={},show='', searchall = None,type='',dialog=None,parseM3u8=True,headers=None,mediaType='video'):
            category=str(category)

           
           
            m3u8=False
            if name and  name.startswith("Error") :
                mode=-1
                if not dialog:
                   dialog="error"
            if url and name and ("error" in url or "error" in name.lower()) and mode==0 :
                mode=-1
                if not dialog:
                   dialog="error"
                name="Error:"+name               
            if name and mode==-1 :
                if not dialog:
                   dialog="error"
                name="Error:"+name
               
            if name and  (name.startswith("Message") or str(url).startswith("Message")):
                mode=-2
                if not dialog:
                   dialog='message'
                name=name.replace("Message:","")
            if name and mode==-2 and not name.startswith("Message"):
                if not dialog:
                    dialog='message'
                name="Message:"+name 
                
            if mode==-5 :
                m3u8=True
                mode=0


                
            if url and ('m3u8' in url) :
               m3u8=True 
            if mode==-6:
                m3u8=False 
                mode=0       
            if link==True:
                mode=0
            if mode==0:
                link=True
          
                
            if mode==503:
                if not dialog:
                   dialog="input"
            if mode==903:
                if not dialog:
                   dialog="login"                
            if mode==103 or mode==603 or mode==703 or mode==803 or mode==1003 or mode==2003:
                if not dialog:
                   dialog="search"                  
            if (url.startswith('plugin://plugin.video.youtube') or 'https://www.youtube.com/watch?v=' in url):
                             link=True
                             mode=0
            if image.startswith("img/"):
                image=AppPath+"/addons/"+self.addonSPath+"/"+image
               
            if not image.startswith("http") and not os.path.exists(image):
               image=AppPath+"/addons/"+self.addonSPath+"/icon.png"  
            imageBasename=getimage_basename(image)



                  

            
            try:
                name = name.encode('utf-8', 'ignore')
                name=name.replace("'",'').replace("&"," ")
               
            except:
                pass             
            try:
                category = category.encode('utf-8', 'ignore')
                category=category.replace("'",'').replace("&"," ")
            except:
                pass              
            try:
                desc = desc.encode('utf-8', 'ignore')
                desc=desc.replace("'",'').replace("&"," ")
            except:
                pass                
            

            try:image = image.encode('utf-8', 'ignore')
            except:pass 
            try:url = url.encode('utf-8', 'ignore')
            except:pass

            cParams={}   
            cParams['name']=name
            cParams['title']=name
            cParams['url']=url
            cParams['mode']=mode
            cParams['image']=image
            cParams['category']=category
            cParams['page']=page
            cParams['maintitle']=maintitle
            cParams['desc']=desc
            cParams['extra']=extra
            cParams['type']=type
            cParams['show']=show
            cParams['caddon_id']=self.addon_id
            cParams['csection_id']=self.section_id
            cParams['dialog']=dialog
            cParams['imageBasename']=imageBasename
            cParams['mediaType']=mediaType
            if headers:
               cParams['headers']=headers

            self.list.append(cParams)

            
            if searchall is not None and dialog=='search':
                try: 
                    dirname = os.path.split(searchall)[0]
                    addon_name = os.path.basename(dirname)
                    search_file = searchall.replace('default.pyc', 'searchall').replace('default.pyo', 'searchall').replace('default.py', 'searchall')
                    afile = open(search_file, 'w')
                    
                    afile.write(addon_name + ';;' + str(cParams))
                    afile.close()
                except:
                    pass            

           
            if m3u8==True and parseM3u8==True :
                try:
                    
                    from m3u8player import getm3u8playlist
                    list = getm3u8playlist(url)
                    printD("list",list)
                    for item in list:
                            url = str(item[1])
                            
                            try:             
                                title ='quality'+"-"+ str(item[0]).encode('utf-8', 'replace')
                                
                            except:
                                title=item[0]
                            printD("title",title)
                            printD("url",url)
                            cParams={}   
                            cParams['name']=title
                            cParams['title']=title
                            cParams['url']=url
                            cParams['mode']=0
                            cParams['image']=image
                            cParams['category']=category
                            cParams['page']=page
                            cParams['maintitle']=maintitle
                            cParams['desc']=desc
                            cParams['extra']=extra
                            cParams['type']=type
                            cParams['show']=show
                            cParams['caddon_id']=self.addon_id
                            cParams['csection_id']=self.section_id
                            cParams['dialog']=dialog
                            cParams['imageBasename']=imageBasename
                            if headers:
                               cParams['headers']=headers
                            


                            
                            self.list.append(cParams)
                           
                                                
                       



                except:
                        
                        pass
            

            


    def getsearchtext(self,marker = '+'):
            import os
            if os.path.exists(searchtext_file):
                file = open(searchtext_file, 'r')
                sstr = file.read().replace(' ', marker)
                file.close()
            else:
                sstr = None
            return sstr
    
    def getHostName(self, url, nameOnly = True):
        hostName = strwithmeta(url).meta.get('host_name', '')
        print "hostName",hostName
        if not hostName:
            match = re.search('https?://(?:www.)?(.+?)/', url)
            if match:
                hostName = match.group(1)
                if (nameOnly):
                    n = hostName.split('.')
                    try: hostName = n[-2]
                    except Exception: printExc()
            hostName = hostName.lower()
        printDBG("_________________getHostName: [%s] -> [%s]" % (url, hostName))
        return hostName
    def getDomain(self,url):###
        hostName=self.getHostName(url)  
        
        
        issupported=supported(hostName)
        image=getserver_image(hostName)
        
        return hostName,image,issupported        

    def endDir(self):

            datalist=self.list
            try:
                printD("datalist-itools",datalist[0])
            except:
                printD("No returned data",self.list)
            self.list=[]
            try:                 
                debugmode=sys.argv[3]
            except:
                
                debugmode='user'
                
            if debugmode=="SearchAll":
                f=open(data_file,"w")
                f.close()

                
   

                
            self.list=[]
            return datalist 

                   
       
    def resolvehost(self,name=None,url=None,headers=None):
                 
        from urlresolver import resolve

        
            
        if name=='':
               name='play'
        if "youtube" in url:
            stream_link=get_youtube_link(url)
        else:    
            stream_link=resolve(url)        
        
        if not stream_link :
            
            self.addDir("Error:invalid stream_link","Error:invalid stream_link",-1,"",name,1,headers=headers)
            return stream_link
        
        if  type(stream_link)==type([]):
          
           
           for ditem in stream_link:

               
               name=str(ditem[0])
               url=str(ditem[1])
               self.addDir(name,url,0,"",name,1,link=True,headers=headers)
           return  stream_link

        if stream_link.startswith("Error") or name.startswith("Error"):
           self.addDir(stream_link,stream_link,-1,"",name,1,headers=headers)
           return stream_link
            
        
        try:self.addDir(name,stream_link,0,'',name,1,headers=headers)
        except: printE()
        return stream_link	                  

    def removeunicode(self,data):##mfaraj
        try:
            try:
                data = data.encode('utf', 'ignore')
            except:
                pass

            data = data.decode('unicode_escape').encode('ascii', 'replace').replace('?', '').strip()
        except:
            pass

        return data
        
    def get_params(self,params=None):
        if params and isinstance(params,dict):
            return params
        item=sys.argv[2]
        params={}
        try:
            item=item.replace('"','')
            params=ast.literal_eval(item)
            
            return params
        except:
           printE() 
           pass

        
        item = item.replace('AxNxD', '&').replace('ExQ', '=')
        paramstring = item
        if len(paramstring) >= 2:
            
            cleanedparams = paramstring.replace('?', '&')

            pairsofparams = cleanedparams.split('&')
            
            for i in range(len(pairsofparams)):
                splitparams = {}
                splitparams = pairsofparams[i].split('=')
                if len(splitparams) == 2:
                    p=splitparams[1]  
                    if isinstance(splitparams[1], basestring) :
                        p=urllib.unquote_plus(splitparams[1])
                    
                           
                    params[splitparams[0]] = p
        return params            



###################################################    
'''
CHostBase implements some typical methods
          from IHost interface
'''

    

class CBaseAddonClass(Item):
    def __init__(self, params={}):
        Item.__init__(self)
        self.ItemClass=Item()
        #self.sessionEx = MainSessionWrapper() 
        #self.up = urlparser()
        
        proxyURL = params.get('proxyURL', '')
        useProxy = params.get('useProxy', False)
        self.cm = common(proxyURL, useProxy)

        self.currList = []
        self.currItem = {}
        if '' != params.get('cookie', ''):
            self.COOKIE_FILE = GetCookieDir(params['cookie'])
        self.moreMode = False
        
    def getTorrentInfo(self,torrentFile=None,tHash=None,extra={}):
            try:
                if getos()=="windows":
                    target="E://"+"tmp.torrent"
                else:
                    target="/tmp/"+"tmp.torrent"
                ret=downloadfile(torrentFile,target)
                print "ret",ret
                from bencode import torrent_parser as tp
                import bencode, hashlib
                
                data = tp.parse_torrent_file(target)
                #print "['info']",data['info']
                files=[]
                try:
                    files=data['info']['files']
                except:
                        printE()
                        files=[]
                    
 
                        name=data['info'].get('name',None)
                        length=data['info'].get('length','0')
                        if name:
                           files.append({'path':name,'length':length})
                           
                           




                try:
                    info_hash = hashlib.sha1(bencode.bencode(data[b"info"])).hexdigest()
                except:
                    printE()
                    info_hash=''
                

                extra['tHash']=info_hash
                extra['files']=files
                
                newfiles=[]
                
                for tfile in files:
                    path=str(tfile.get('path','')).replace("u'",'').replace("'","").replace("[","").replace("]","")
                    length=str(tfile.get('length',''))
                    try:
                        filestr=str(path)+" "+getmb(float(length))
                    except:
                        printE()
                        continue
                    newfiles.append(filestr)
                extra.update({'files':newfiles})    
                return extra
            except:
                printE()
                return extra        

    def getSubsapiLink(self,imdb_id='',sub_lng_id=''):
           log_file="/tmp/TSmedia/subsapitools.log"
           try:
               if imdb_id!='':
                  if sub_lng_id=='': 
                     sub_lng_id=open("/tmp/TSmedia/sublngID").read()
                  
                  from subsapi import getmovie_sub
                  
                  
                  sts,srtFile,localFile=getmovie_sub(imdb_id,sub_lng_id=sub_lng_id)
                 
                  if sts:
                     return srtFile,localFile
                  else:
                     return "",""     
                  
               else:
                       return '',''
           except Exception as error:
                 
                 printE()
                 return "",""

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

#####################################        
    def getDN(self,data, marker1, marker2, withMarkers = True):

        sts,NodesData=self.cm.ph.getDataBeetwenNodes(data, marker1, marker2, withMarkers)
        if sts:
            return NodesData
        else:
          printE()
          return ''
    def getSM(self,data, patron, index=0):
        try:
            matches = re.findall(patron, data, flags=re.DOTALL)
            return matches[index]
        except:
            return ""

    def getMM(self,text, pattern):
        return re.findall(pattern, text, re.DOTALL)
    def getDM(self,data, marker1, marker2, withMarkers=False, caseSensitive=True):
        
        flags = 0
        if withMarkers: flags |= START_E|END_E
        if not caseSensitive: flags |= IGNORECASE
        sts,rdata=find(data, marker1, marker2, flags)
        return rdata                    

    def getAIN(self,data, node1, node2, withNodes=True, numNodes=-1, caseSensitive=True):
      return self.cm.ph.getAllItemsBeetwenNodes(data, node1, node2, withNodes, numNodes, caseSensitive)

    def getSG(self,data, pattern, grupsNum=1, ignoreCase=False):
        return self.cm.ph.getSearchGroups(data, pattern, grupsNum=grupsNum, ignoreCase=ignoreCase)

    
    def getDRM(self,data, pattern1, pattern2, withMarkers=True):
        return self.cm.ph.getDataBeetwenReMarkers(data, pattern1, pattern2, withMarkers=withMarkers)

    def getDM2(self,data, marker1, marker2, withMarkers=True, caseSensitive=True):
            sts,makersData=self.cm.ph.getDataBeetwenMarkers(data, marker1, marker2, withMarkers=withMarkers, caseSensitive=caseSensitive)
            if sts:
                return makersData
            else:
              printE()
              return ''
    def getAIM(self,data, marker1, marker2, withMarkers=True, caseSensitive=True):
          return self.cm.ph.getAllItemsBeetwenMarkers(data, marker1, marker2, withMarkers=withMarkers, caseSensitive=caseSensitive)
        
    def colorize(self,txt,selcolor='magenta',marker1="(",marker2=")"):
        
         if getos()=="windows" or enigmaos()=="oe2.2" or  is_ascii(txt)==False:
            return txt
        
         
         
         colors={'black':'\c00000000','white':'\c00??????','grey':'\c00808080',
                           
         'blue':'\c000000??','green':'\c0000??00','red':'\c00??0000','ivory':"\c0???????",
         'yellow':'\c00????00','cyan':'\\c0000????','magenta':'\c00??00??'}
         color=colors.get(selcolor,'\c0000????') 
         try:
            if not marker1 in txt :
                return color+" "+txt
            txtparts=txt.split(marker1)
            txt1=txtparts[0]
            txt2=txtparts[1]
            if marker2 in txt:
                txt3=txt2.split(marker2)[0]
            else:
                txt3=txt2 
            
            ftxt=txt1+" "+color+marker1+txt3+marker2
           
            return ftxt
         except:
             printE()
             return txt
    def getcfPage(self, baseUrl, addParams = None, post_data = None):
        from CloudflareScraper import CloudflareScraper
        scraper=CloudflareScraper()
        try:
            if post_data :
                data=scraper.post(baseUrl,headers=addParams,data=post_data,verify=False).content
                sts=True
            else:
                 if addParams:
                    data=scraper.get(baseUrl,headers=addParams,verify=False).content
                 else:
                    data=scraper.get(baseUrl,verify=False).content 
                 sts=True
        except:
           printE()
           sts=False
           data=''
        printDBG("++++++++++++++++++++++++++++++++++++++++")
        printDBG("url: %s" % baseUrl)
        printDBG("sts: %s" % sts)
       
        printDBG("++++++++++++++++++++++++++++++++++++++++")
        return data

    def reqData(self,url, headers =None, params = None):
        import requests
        ses = requests.Session()
          
        if headers is None:
            headers=self.HEADER   
        if params:
            try:
                print 'heades', headers
                res = ses.post(url, headers=headers, params=params, verify=False, timeout=5)
                print 'res.status_code', res.status_code
                if res.status_code == 200:
                    printD("download ok","download ok")
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
            print "url",url
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

    def removeUnicode(self,data):##mfaraj
        try:
            try:
                data = data.encode('utf', 'ignore')
            except:
                pass

            data = data.decode('unicode_escape').encode('ascii', 'replace').replace('?', '').strip()
        except:
            pass

        return data



    
    def getPageCFProtection2(self,baseUrl, addParams = {}, post_data = None):
                
                import requests
                r=requests.session()
                data=r.get(baseUrl).content
               
                
                
                try:
                    if "'jschl-answer'" in data:
                        import cookielib
                        import time
                        import cfscrape      
                        scraper = cfscrape.create_scraper()
                        data = scraper.get(baseUrl).content
                        tokens, user_agent=cfscrape.get_tokens(self.MAIN_URL)
                        sts = True
                        cj = self.cm.getCookie(self.COOKIE_FILE)
                       
                        cook_dat=re.findall("'(.*?)'.*?'(.*?)'", str(tokens), re.S)          
                        for (cookieKey,cookieValue) in cook_dat:
                            cookieItem = cookielib.Cookie(version=0, name=cookieKey, value=cookieValue, port=None, port_specified=False, domain='.'+self.cm.getBaseUrl(baseUrl, True), domain_specified=True, domain_initial_dot=True, path='/', path_specified=True, secure=False, expires=time.time()+3600*48, discard=True, comment=None, comment_url=None, rest={'HttpOnly': None}, rfc2109=False)
                            cj.set_cookie(cookieItem)      

                        cj.save(self.COOKIE_FILE, ignore_discard = True)
                        return True,data
                except:
                     
                    printE()
                return  False,None


    def getPage2(self, baseUrl, addParams = {}, post_data = None,cloudflare=False):
        if addParams == {}:
            addParams = dict(self.defaultParams)
        print "addParams",addParams
        origBaseUrl = baseUrl
        baseUrl = self.cm.iriToUri(baseUrl)
        if cloudflare:
            addParams['cloudflare_params'] = {'cookie_file':self.COOKIE_FILE, 'User-Agent':self.USER_AGENT}
            sts, data = self.getPageCFProtection2(baseUrl, addParams, post_data)

        else:
            
            sts, data = self.cm.getPage(baseUrl, addParams, post_data)



            
        printDBG("++++++++++++++++++++++++++++++++++++++++")
        printDBG("url: %s" % baseUrl)
        printDBG("sts: %s" % sts)
       
        printDBG("++++++++++++++++++++++++++++++++++++++++")
        if sts:
            return data
        else:
            return ''
        
    def getPageCFProtection(self,baseUrl, addParams = {}, post_data = None,cloudflare=True):
                
		
		if cloudflare=="auto":
                    data=self.getPage(baseUrl,addParams,post_data)
                    sts=True
                    if not '!![]+!![]' in data:
                        if data=='':
                            sts=False
                        return sts,data

                if cloudflare==False:
                   sts,data=self.getPage(baseUrl,addParams,post_data)
                   return sts,data
                
		if not post_data: post_data=(None,None)
		sts=False
		
                try:
                        printD("start resolving by anti-cf")
                        oRequestHandler = cRequestHandler(baseUrl)
                        if post_data:
                                oRequestHandler.setRequestType(cRequestHandler.REQUEST_TYPE_POST)
                                oRequestHandler.addParametersLine(post_data[0])			
                        data = oRequestHandler.request()
                        print "data1",data
                        sts = True
                        cook = GestionCookie().Readcookie('www_dpstream_top')
                        self.cookieHeader=str(cook)
                        if ';' in cook: cook_tab = cook.split(';')
                        else: cook_tab = cook
                        cj = self.cm.getCookie(self.COOKIE_FILE)
                        import time
                        for item in cook_tab:
                                if '=' in item:			
                                        cookieKey, cookieValue = item.split('=')
                                        cookieItem = cookielib.Cookie(version=0, name=cookieKey, value=cookieValue, port=None, port_specified=False, domain='.'+self.cm.getBaseUrl(baseUrl, True), domain_specified=True, domain_initial_dot=True, path='/', path_specified=True, secure=False, expires=time.time()+3600*48, discard=True, comment=None, comment_url=None, rest={'HttpOnly': None}, rfc2109=False)
                                        cj.set_cookie(cookieItem)
                        cj.save(self.COOKIE_FILE, ignore_discard = True)

                        
                        sts=True
                except Exception, e:
                        printDBG('ERREUR:'+str(e))
                        printD("cloudflare falied")
                               
                        printE()       
                       
                        data=''
                        sts=False       
		return sts, data
		


    def getPage(self, baseUrl, addParams = {}, post_data = None,cloudflare=False):
        if addParams == {}:
            try:addParams = dict(self.defaultParams)
            except:addParams={}
        print "addParams",addParams
        origBaseUrl = baseUrl
        baseUrl = self.cm.iriToUri(baseUrl)
        if cloudflare==True or cloudflare=="auto":
            addParams['cloudflare_params'] = {'cookie_file':self.COOKIE_FILE, 'User-Agent':self.USER_AGENT}
            sts, data = self.getPageCFProtection(baseUrl, addParams, post_data,cloudflare)
        else:
            
            sts, data = self.cm.getPage(baseUrl, addParams, post_data)



            
        printDBG("++++++++++++++++++++++++++++++++++++++++")
        printDBG("url: %s" % baseUrl)
        printDBG("sts: %s" % sts)
       
        printDBG("++++++++++++++++++++++++++++++++++++++++")
        if sts:
            return data
        else:
            return ''
        



###################################################                               


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
            return getAppPath()+"/addons/"+self.DEFAULT_ICON_URL
           
        except Exception:
            pass
        return ''

    @staticmethod 
    def cleanhtml(str,withSpace=False):

            try:
                txt=cleanhtml2(str,withSpace)
                #txt=txt.replace('&nbsp;',' ').replace('&bull;',' ').replace('&nbsp',' ').replace('&amp;','&')   

            except:
                return str

       

            return txt 
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

    def addDir2(self, params):
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
        print 'self.currListmmm',self.currList
        
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
####
class Addon:

    def __init__(self, id = None):
        
        
           
           self.plugin_path=AppPath+"/addons/"+id
           print "self.plugin_path",self.plugin_path
           self.path=self.plugin_path


    def getLocalizedString(self, idx = ' '):
        if True:
            xfile = self.path + '/resources/language/English/strings.xml'
            if os.path.exists(xfile) == False:
                xfile = self.path + '/resources/language/english/strings.xml'
                if os.path.exists(xfile) == False:
                    xfile = self.plugin_path + '/resources/defaults/strings.xml'
            tree = xml.etree.cElementTree.parse(xfile)
            root = tree.getroot()
        try:
            for string in root.iter('string'):
                id = string.get('id')
                text = string.text
                if int(id) == int(idx):
                    xtxt = text
                    return xtxt

        except:
            for string in root.getiterator('string'):
                id = string.get('id')
                text = string.text
                if int(id) == int(idx):
                    xtxt = text
                    return xtxt

    def getSetting(self, id = None):
        item = id
        xfile = self.path + '/resources/settings.xml'
        print "xfile2",xfile
        if not os.path.exists(xfile):
            return None
        else:
            f = open(xfile, 'r')
            xfile2 = f.read()
            f.close()
            if '&' in xfile2:
                xfile2 = xfile2.replace('&', 'AxNxD')
                f2 = open('/tmp/TSmedia/temp.xml', 'w')
                f2.write(xfile2)
                f2.close()
                cmd = "mv '/tmp/TSmedia/temp.xml' " + xfile
                os.system(cmd)
            try:
                tree = xml.etree.cElementTree.parse(xfile)
            except:
                printE()
                return None

            root = tree.getroot()
            
            try:
                for setting in root.iter('setting'):
                    
                    type = setting.get('type')
                    print "type2",type
                    print "id2",id
                    
                    if type == 'bool':
                        idx = setting.get('id')
                        default = setting.get('default')
                        if idx == item:
                            xtxt = default
                            return xtxt
                    elif type == 'action':
                        idx = setting.get('label')
                        action = setting.get('action')
                        if idx == item:
                            xtxt = action
                            return xtxt
                    elif type == 'text':
                        idx = setting.get('id')
                        default = setting.get('default')
                        if idx == item:
                            xtxt = default
                            return xtxt
                    elif type == 'enum':
                        idx = setting.get('id')
                        default = setting.get('default')
                        if idx == item:
                            ix = default
                            return ix
                    elif type == 'folder':
                        idx = setting.get('id')
                        default = setting.get('default')
                        if idx == item:
                            xtxt = default
                            return xtxt
                    elif type == 'labelenum':
                        idx = setting.get('id')
                        print "idx2",idx
                        print "item2",item
                        default = setting.get('default')
                        values = setting.get('values')
                        if idx == item:
                            vals = values.split('|')
                            
                            #xtxt = vals[-1]
                            return default
                    elif type == 'number':
                        idx = setting.get('id')
                        default = setting.get('default')
                        if idx == item:
                            xtxt = default
                            return xtxt
                    elif type == 'select':
                        idx = setting.get('id')
                        default = setting.get('default')
                        if idx == item:
                            xtxt = default
                            return xtxt

            except:
                for setting in root.getiterator('setting'):
                    type = setting.get('type')
                    if type == 'bool':
                        idx = setting.get('id')
                        default = setting.get('default')
                        if idx == item:
                            xtxt = default
                            return xtxt
                    elif type == 'action':
                        idx = setting.get('label')
                        action = setting.get('action')
                        if idx == item:
                            xtxt = action
                            return xtxt
                    elif type == 'text':
                        idx = setting.get('id')
                        default = setting.get('default')
                        if idx == item:
                            xtxt = default
                            return xtxt
                    elif type == 'enum':
                        idx = setting.get('id')
                        default = setting.get('default')
                        if idx == item:
                            ix = default
                            return ix
                    elif type == 'folder':
                        idx = setting.get('id')
                        default = setting.get('default')
                        if idx == item:
                            xtxt = default
                            return xtxt
                    elif type == 'labelenum':
                        idx = setting.get('id')
                        values = setting.get('values')
                        if idx == item:
                            vals = values.split('|')
                            n = len(vals) - 1
                            xtxt = vals[n]
                            return xtxt
                    elif type == 'number':
                        idx = setting.get('id')
                        default = setting.get('default')
                        if idx == item:
                            xtxt = default
                            return xtxt
                    elif type == 'select':
                        idx = setting.get('id')
                        default = setting.get('default')
                        if idx == item:
                            xtxt = default
                            return xtxt

            
            return None

    def getSetting1(self, id = id):
        xfile = self.path + '/resources/settings.xml'
        if not os.path.exists(xfile):
            return ''
        
        
        xmlText = open(xfile).read()       
       
        if '&' in xmlText:
            xmlText = xmlText.replace('&', 'AxNxD')
            f2 = open(plugin_path+'/tmp/TSmedia/temp.xml', 'w')
            f2.write(xmlText)
            f2.close()
            cmd = "mv '/tmp/TSmedia/temp.xml' " + xfile
            os.system(cmd)
        try:
            tree = xml.etree.cElementTree.parse(xfile)
            root = tree.getroot()
            
        except Exception as error:
            printE()
            print "error",str(error)
            return ''       
        
        i = 0
       
        for setting in root.iter('setting'):
            sid=setting.attrib.get("id",'')
            if sid==id:
                return setting.attrib.get("default",'')
            
                    



    def getSetting2(self, id = id):
        xfile = self.path + '/resources/settings.xml'
        if not os.path.exists(xfile):
            return '',''
        
        
        xmlText = open(xfile).read()       
       
        if '&' in xmlText:
            xmlText = xmlText.replace('&', 'AxNxD')
            f2 = open(plugin_path+'/tmp/TSmedia/temp.xml', 'w')
            f2.write(xmlText)
            f2.close()
            cmd = "mv '/tmp/TSmedia/temp.xml' " + xfile
            os.system(cmd)
        try:
            tree = xml.etree.cElementTree.parse(xfile)
            root = tree.getroot()
            
        except Exception as error:
            printE()
            print "error",str(error)
            return '',''       
        
        i = 0
       
        for setting in root.iter('setting'):
            sid=setting.attrib.get("id",'')
            if sid==id:
                return setting.attrib.get('label',''),setting.attrib.get("default",'')
            
            

    def setSetting(self, setting_id, value):
        """Sets a script setting."""
        if value is None:
            return False
        else:
            settings_xml = self.path + '/resources/settings.xml'
            if settings_xml is None:
                return False
            tree = xml.etree.cElementTree.parse(settings_xml)
            root = tree.getroot()
            for setting in root.iter('setting'):
                id = setting.get('id')
                if setting_id == id:
                    try:
                        setting.set('default', value)
                        tree.write(settings_xml)
                        return True
                    except:
                        return False

            return False
            return

    def openSettings(self, arg = None):
        """get all settings."""
        settings_xml = self.path + '/resources/settings.xml'
        tree = xml.etree.cElementTree.parse(settings_xml)
        root = tree.getroot()
        i = 0
        list = []
        for setting in root.iter('setting'):
            list.append((i, setting.attrib))
            i = i + 1

        return list

    def getAddonInfo(self, item):
        cachefold = None
        try:
            myfile = file('/tmp/TSmedia/xbmc.txt')
            icount = 0
            for line in myfile.readlines():
                cachefold = line
                break

        except:
            pass

        if cachefold is None:
            try:
                cachefold = sys.argv[3]
            except:
                cachefold = '/media/hdd'

        profile = cachefold + '/xbmc/profile/addon_data/' + str(self.id)
        cmd = 'mkdir -p ' + profile
        os.system(cmd)
        xfile = self.path + '/addon.xml'
        if not os.path.exists(xfile):
            return
        else:
            tree = xml.etree.cElementTree.parse(xfile)
            root = tree.getroot()
            version = str(root.get('version'))
            author = str(root.get('provider-name'))
            name = str(root.get('name'))
            id = str(root.get('id'))
            if item == 'path':
                return self.path
            if item == 'Path':
                return self.path
            if item == 'version':
                return version
            if item == 'author':
                return author
            if item == 'name':
                return name
            if item == 'id':
                return id
            if item == 'profile':
                return profile
            return 'xxx'
###new classes
class CParsingHelper:
    @staticmethod
    def listToDir(cList, idx):
        cTree = {'dat':''}
        deep = 0 
        while (idx+1) < len(cList):
            if cList[idx].startswith('<ul') or cList[idx].startswith('<li'):
                deep += 1
                nTree, idx, nDeep = CParsingHelper.listToDir(cList, idx+1)
                if 'list' not in cTree: cTree['list'] = []
                cTree['list'].append(nTree)
                deep += nDeep
            elif cList[idx].startswith('</ul>') or cList[idx].startswith('</li>'):
                deep -= 1
                idx += 1
            else:
                cTree['dat'] += cList[idx]
                idx += 1
            if deep < 0:
                break
        return cTree, idx, deep

    @staticmethod
    def getSearchGroups(data, pattern, grupsNum=1, ignoreCase=False):
        return  search(data, pattern, IGNORECASE if ignoreCase else 0, grupsNum)

    @staticmethod
    def getDataBeetwenReMarkers(data, pattern1, pattern2, withMarkers=True):
        match1 = pattern1.search(data)
        if None == match1 or -1 == match1.start(0): return False, ''
        match2 = pattern2.search(data[match1.end(0):])
        if None == match2 or -1 == match2.start(0): return False, ''
        
        if withMarkers:
            return True, data[match1.start(0): (match1.end(0) + match2.end(0)) ]
        else:
            return True, data[match1.end(0): (match1.end(0) + match2.start(0)) ]

    @staticmethod
    def getDataBeetwenMarkers(data, marker1, marker2, withMarkers=True, caseSensitive=True):
        
        flags = 0
        if withMarkers: flags |= START_E|END_E
        if not caseSensitive: flags |= IGNORECASE
        return find(data, marker1, marker2, flags)

    @staticmethod
    def getAllItemsBeetwenMarkers(data, marker1, marker2, withMarkers=True, caseSensitive=True):
        flags = 0
        if withMarkers: flags |= START_E|END_E
        if not caseSensitive: flags |= IGNORECASE
        return findall(data, marker1, marker2, flags)

    @staticmethod
    def rgetAllItemsBeetwenMarkers(data, marker1, marker2, withMarkers=True, caseSensitive=True):
        flags = 0
        if withMarkers: flags |= START_E|END_E
        if not caseSensitive: flags |= IGNORECASE
        return rfindall(data, marker1, marker2, flags)

    @staticmethod
    def rgetDataBeetwenMarkers2(data, marker1, marker2, withMarkers=True, caseSensitive=True):
        flags = 0
        if withMarkers: flags |= START_E|END_E
        if not caseSensitive: flags |= IGNORECASE
        return rfind(data, marker1, marker2, flags)

    @staticmethod
    def rgetDataBeetwenMarkers(data, marker1, marker2, withMarkers = True):
        # this methods is not working as expected, but is is used in many places
        # so I will leave at it is, please use rgetDataBeetwenMarkers2
        idx1 = data.rfind(marker1)
        if -1 == idx1: return False, ''
        idx2 = data.rfind(marker2, idx1 + len(marker1))
        if -1 == idx2: return False, ''
        if withMarkers:
            idx2 = idx2 + len(marker2)
        else:
            idx1 = idx1 + len(marker1)
        return True, data[idx1:idx2]

    @staticmethod
    def getDataBeetwenNodes(data, node1, node2, withNodes=True, caseSensitive=True):
        flags = 0
        if withNodes: flags |= START_E|END_E
        if not caseSensitive: flags |= IGNORECASE
        return find(data, node1, node2, flags)

    @staticmethod
    def getAllItemsBeetwenNodes(data, node1, node2, withNodes=True, numNodes=-1, caseSensitive=True):
        flags = 0
        if withNodes: flags |= START_E|END_E
        if not caseSensitive: flags |= IGNORECASE
        return findall(data, node1, node2, flags, limits=numNodes)

    @staticmethod
    def rgetDataBeetwenNodes(data, node1, node2, withNodes=True, caseSensitive=True):
        flags = 0
        if withNodes: flags |= START_E|END_E
        if not caseSensitive: flags |= IGNORECASE
        return rfind(data, node1, node2, flags)
        
    @staticmethod
    def rgetAllItemsBeetwenNodes(data, node1, node2, withNodes=True, numNodes=-1, caseSensitive=True):
        flags = 0
        if withNodes: flags |= START_E|END_E
        if not caseSensitive: flags |= IGNORECASE
        return rfindall(data, node1, node2, flags, limits=numNodes)

    # this method is useful only for developers 
    # to dump page code to the file
    @staticmethod
    def writeToFile(file, data, mode = "w"):
        #helper to see html returned by ajax
        file_path = file
        text_file = open(file_path, mode)
        text_file.write(data)
        text_file.close()
    
    @staticmethod
    def getNormalizeStr(txt, idx=None):
        POLISH_CHARACTERS = {u'ą':u'a', u'ć':u'c', u'ę':u'ę', u'ł':u'l', u'ń':u'n', u'ó':u'o', u'ś':u's', u'ż':u'z', u'ź':u'z',
                             u'Ą':u'A', u'Ć':u'C', u'Ę':u'E', u'Ł':u'L', u'Ń':u'N', u'Ó':u'O', u'Ś':u'S', u'Ż':u'Z', u'Ź':u'Z',
                             u'á':u'a', u'é':u'e', u'í':u'i', u'ñ':u'n', u'ó':u'o', u'ú':u'u', u'ü':u'u',
                             u'Á':u'A', u'É':u'E', u'Í':u'I', u'Ñ':u'N', u'Ó':u'O', u'Ú':u'U', u'Ü':u'U',
                            }
        txt = txt.decode('utf-8')
        if None != idx: txt = txt[idx]
        nrmtxt = unicodedata.normalize('NFC', txt)
        ret_str = []
        for item in nrmtxt:
            if ord(item) > 128:
                item = POLISH_CHARACTERS.get(item)
                if item: ret_str.append(item)
            else: # pure ASCII character
                ret_str.append(item)
        return ''.join(ret_str).encode('utf-8')

    @staticmethod
    def isalpha(txt, idx=None):
        return CParsingHelper.getNormalizeStr(txt, idx).isalpha()

    @staticmethod 
    def cleanHtmlStr(str):
        return clean_html(str)


class common:
    HOST   = 'Mozilla/5.0 (Windows NT 6.1; rv:17.0) Gecko/20100101 Firefox/17.0'
    HEADER = None
    ph = CParsingHelper
    
    @staticmethod
    def getDefaultHeader(browser='firefox'):
        if browser == 'firefox': ua = 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:46.0) Gecko/20100101 Firefox/46.0'
        elif browser == 'iphone_3_0': ua = 'Mozilla/5.0 (iPhone; U; CPU iPhone OS 3_0 like Mac OS X; en-us) AppleWebKit/528.18 (KHTML, like Gecko) Version/4.0 Mobile/7A341 Safari/528.16'
        else: ua = 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36'
        
        HTTP_HEADER = { 'User-Agent':ua,
                        'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                        'Accept-Encoding':'gzip, deflate',
                        'DNT':1 
                      }
        return dict(HTTP_HEADER)
    
    @staticmethod
    def getParamsFromUrlWithMeta(url, baseHeaderOutParams=None):
        from Plugins.Extensions.addonsParser.iptvdm.iptvdh import DMHelper
        HANDLED_HTTP_HEADER_PARAMS = DMHelper.HANDLED_HTTP_HEADER_PARAMS #['Host', 'User-Agent', 'Referer', 'Cookie', 'Accept',  'Range']
        outParams = {}
        tmpParams = {}
        postData = None
        if isinstance(url, strwithmeta):
            if None != baseHeaderOutParams: tmpParams['header'] = baseHeaderOutParams
            else: tmpParams['header'] = {}
            for key in url.meta:
                if key in HANDLED_HTTP_HEADER_PARAMS:
                    tmpParams['header'][key] = url.meta[key]
            if 0 < len(tmpParams['header']):
                outParams = tmpParams
            if 'iptv_proxy_gateway' in url.meta:
                outParams['proxy_gateway'] = url.meta['iptv_proxy_gateway']
            if 'iptv_http_proxy' in url.meta:
                outParams['http_proxy'] = url.meta['iptv_http_proxy']
        return outParams, postData
        
    @staticmethod
    def getBaseUrl(url, domainOnly=False):
        parsed_uri = urlparse( url )
        if domainOnly:
            domain = '{uri.netloc}'.format(uri=parsed_uri)
        else:
            domain = '{uri.scheme}://{uri.netloc}/'.format(uri=parsed_uri)
        return domain
        
    @staticmethod
    def getFullUrl(url, mainUrl='http://fake/'):
        if not url: return ''
        if url.startswith('./'):
            url = url[1:]

        currUrl = mainUrl
        mainUrl = common.getBaseUrl(currUrl)

        if url.startswith('//'):
            proto = mainUrl.split('://', 1)[0]
            url = proto + ':' + url
        elif url.startswith('://'):
            proto = mainUrl.split('://', 1)[0]
            url = proto + url
        elif url.startswith('/'):
            url = mainUrl + url[1:]
        elif 0 < len(url) and '://' not in url:
            if currUrl == mainUrl:
                url =  mainUrl + url
            else:
                url = urljoin(currUrl, url)
        return url

    @staticmethod
    def isValidUrl(url):
        return url.startswith('http://') or url.startswith('https://')

    @staticmethod
    def buildHTTPQuery(query):
        def _process(query, data, key_prefix):
            if isinstance(data, dict):
                for key, value in data.iteritems():
                    key = '%s[%s]' % (key_prefix, key) if key_prefix else key
                    _process(query, value, key)
            elif isinstance(data, list):
                for idx in range(len(data)):
                    _process(query, data[idx], '%s[%s]' % (key_prefix, idx))
            else:
                query.append((key_prefix, data))
        _query = []
        _process(_query, query, '')
        return _query

    def __init__(self, proxyURL= '', useProxy = False, useMozillaCookieJar=True):
        self.proxyURL = proxyURL
        self.useProxy = useProxy
        self.geolocation = {}
        self.meta = {} # metadata from previus request
        
        self.curlSession = None
        self.pyCurlAvailable = None
        if not useMozillaCookieJar:
            raise Exception("You should stop use parameter useMozillaCookieJar it change nothing, because from only MozillaCookieJar can be used")
    
    def reportHttpsError(self, type, url, msg):
        domain = self.getBaseUrl(url, True)
        messages = []
        messages.append(_('HTTPS connection error "%s"\n') % msg)
        messages.append(_('It looks like your current configuration do not allow to connect to the https://%s/.\n') % domain)
        
        if type == 'verify' and IsHttpsCertValidationEnabled():
            messages.append(_('You can disable HTTPS certificates validation in the E2iPlayer configuration to suppress this problem.'))
        else:
            pyCurlInstalled = False
            try:
                verInfo = pycurl.version_info()
                printDBG("usePyCurl VERSION: %s" % [verInfo])
                if verInfo[4] & (1<<7) and verInfo[1].startswith('7.6') and verInfo[5] == 'wolfSSL/3.15.3':
                    pyCurlInstalled = True
            except Exception:
                printExc()
            if pyCurlInstalled:
                if not UsePyCurl():
                    messages.append(_('You can enable PyCurl in the E2iPlayer configuration to fix this problem.'))
                else:
                    messages.append(_('Please report this problem to the developer %s.') % 'addonsParsere2@gmail.com')
            else:
                messages.append(_('You can install PyCurl package from %s to fix this problem.') % 'http://www.addonsParser.gitlab.io/')
        #GetIPTVNotify().push('\n'.join(messages), 'error', 40, type + domain, 40)
        printD("error", messages+":url"+url)       
    

        
    def getCountryCode(self, lower=True):
        if 'countryCode' not in self.geolocation:
            sts, data = self.getPage('http://ip-api.com/json')
            if sts:
                try:
                    self.geolocation['countryCode'] = json_loads(data)['countryCode']
                except Exception:
                    printExc()
        return self.geolocation.get('countryCode', '').lower()
        

        
    def clearCookie(self, cookiefile, leaveNames=[], removeNames=None, ignoreDiscard=True, ignoreExpires=False):
        try:
            toRemove = []
            if self.usePyCurl():
                cj = self._pyCurlLoadCookie(cookiefile, ignoreDiscard, ignoreExpires)
            else:
                cj = cookielib.MozillaCookieJar()
            cj.load(cookiefile, ignore_discard = ignoreDiscard)
            for cookie in cj:
                if cookie.name not in leaveNames and (None == removeNames or cookie.name in removeNames):
                    toRemove.append(cookie)
            for cookie in toRemove:
                cj.clear(cookie.domain, cookie.path, cookie.name)
            cj.save(cookiefile, ignore_discard = ignoreDiscard)
        except Exception:
            printExc()
            return False
        return True
        
    def getCookieItem(self, cookiefile, item):
        cookiesDict = self.getCookieItems(cookiefile)
        return cookiesDict.get(item, '')
        
    def getCookie(self, cookiefile, ignoreDiscard=True, ignoreExpires=False):
        cj = None
        try:
            if False:#self.usePyCurl():
                cj = self._pyCurlLoadCookie(cookiefile, ignoreDiscard, ignoreExpires)
            else:
                cj = cookielib.MozillaCookieJar()
                cj.load(cookiefile, ignore_discard = ignoreDiscard)
        except Exception:
            printExc()
        return cj

    def getCookieItems(self, cookiefile, ignoreDiscard=True, ignoreExpires=False):
        cookiesDict = {}
        try:
            cj = self.getCookie(cookiefile, ignoreDiscard, ignoreExpires)
            for cookie in cj:
                cookiesDict[cookie.name] = cookie.value
        except Exception:
            printExc()
        return cookiesDict
        
    def getCookieHeader(self, cookiefile, allowedNames=[], unquote=True, ignoreDiscard=True, ignoreExpires=False):
        ret = ''
        try:
            cookiesDict = self.getCookieItems(cookiefile, ignoreDiscard, ignoreExpires)
            for name in cookiesDict:
                if 0 < len(allowedNames) and name not in allowedNames: continue
                value = cookiesDict[name]
                if unquote: value = urllib.unquote(value)
                ret += '%s=%s; ' % (name, value)
        except Exception:
            printExc()
        return ret




    def fillHeaderItems(self, metadata, responseHeaders, camelCase=False, collectAllHeaders=False):
        returnKeys = ['content-type', 'content-disposition', 'content-length', 'location']
        if camelCase: sourceKeys = ['Content-Type', 'Content-Disposition', 'Content-Length', 'Location']
        else: sourceKeys = returnKeys
        for idx in range(len(returnKeys)):
            if sourceKeys[idx] in responseHeaders:
                metadata[returnKeys[idx]] = responseHeaders[sourceKeys[idx]]

        if collectAllHeaders:
            for header, value in responseHeaders.iteritems():
                metadata[header.lower()] = responseHeaders[header]

    def getPage(self, url, addParams = {}, post_data = None):
        ''' wraps getURLRequestData '''
        try:url=url.encode("utf-8","ignore")
        except:pass
        # if curl should be used and can be used
        #if addParams.get('return_data', True) and self.usePyCurl():
            #553return self.getPageWithPyCurl(url, addParams, post_data)
        
        try:
            addParams['url'] = url
            if 'return_data' not in addParams:
                addParams['return_data'] = True
            response = self.getURLRequestData(addParams, post_data)
            status = True
        except urllib2.HTTPError, e:
            printE()
            printD("url",url)
            try:
                printExc()
                status = False
                response = e
                if addParams.get('return_data', False):
                    self.meta = {}
                    metadata = self.meta
                    metadata['url'] = e.fp.geturl()
                    metadata['status_code'] = e.code
                    self.fillHeaderItems(metadata, e.fp.info(), True, collectAllHeaders=addParams.get('collect_all_headers'))
                    
                    data = e.fp.read(addParams.get('max_data_size', -1))
                    if e.fp.info().get('Content-Encoding', '') == 'gzip':
                        data = DecodeGzipped(data)
                    
                    data, metadata = self.handleCharset(addParams, data, metadata)
                    response = strwithmeta(data, metadata)
                    e.fp.close()
            except Exception:
                printExc()
                printE()
        except urllib2.URLError, e:
            printExc()
            errorMsg = str(e) 
            if 'ssl_protocol' not in addParams and 'TLSV1_ALERT_PROTOCOL_VERSION' in errorMsg:
                    try:
                        newParams = dict(addParams)
                        newParams['ssl_protocol'] = 'TLSv1_2'
                        return self.getPage(url, newParams, post_data)
                    except Exception: 
                        pass
            if 'VERSION' in errorMsg:
                self.reportHttpsError('version', url, errorMsg)
            elif 'VERIFY_FAILED' in errorMsg:
                self.reportHttpsError('verify', url, errorMsg)
            elif 'SSL' in errorMsg or 'unknown url type: https' in errorMsg: #GET_SERVER_HELLO
                self.reportHttpsError('other', url, errorMsg)
            
            response = None
            status = False
                
        except Exception:
            printExc()
            response = None
            status = False
        
        if addParams['return_data'] and status and not isinstance(response, basestring):
            status = False
            
        return (status, response)
    
    def getPageCFProtection(self, baseUrl, params={}, post_data=None):
        cfParams = params.get('cloudflare_params', {})
        
        def _getFullUrl(url, baseUrl):
            if 'full_url_handle' in cfParams:
                return cfParams['full_url_handle'](url)
            return self.getFullUrl(url, baseUrl)
        
        def _getFullUrl2(url, baseUrl):
            if 'full_url_handle2' in cfParams:
                return cfParams['full_url_handle2'](url)
            return url
        
        url = baseUrl
        header = {'Referer':url, 'User-Agent':cfParams.get('User-Agent', ''), 'Accept-Encoding':'text'}
        header.update(params.get('header', {}))
        params.update({'with_metadata':True, 'use_cookie': True, 'save_cookie': True, 'load_cookie': True, 'cookiefile': cfParams.get('cookie_file', ''), 'header':header})
        sts, data = self.getPage(url, params, post_data)
        
        current = 0
        while current < 5:
            #if True:
            if not sts and None != data:
                start_time = time.time()
                current += 1
                doRefresh = False
                try:
                    domain = self.getBaseUrl(data.meta['url'])
                    verData = data
                    printDBG("------------------")
                    printDBG(verData)
                    printDBG("------------------")
                    if 'sitekey' not in verData and 'challenge' not in verData: break
                    
                    printDBG(">>")
                    printDBG(verData)
                    printDBG("<<")
                    
                    sitekey = self.getSearchGroups(verData, 'data-sitekey="([^"]+?)"')[0]
                    id = self.getSearchGroups(verData, 'data-ray="([^"]+?)"')[0]
                    if sitekey != '':
                        from  addonsParser.libs.recaptcha_v2 import UnCaptchaReCaptcha
                        # google captcha
                        recaptcha = UnCaptchaReCaptcha(lang=GetDefaultLang())
                        recaptcha.HTTP_HEADER['Referer'] = baseUrl
                        if '' != cfParams.get('User-Agent', ''): recaptcha.HTTP_HEADER['User-Agent'] = cfParams['User-Agent']
                        token = recaptcha.processCaptcha(sitekey)
                        if token == '': return False, None
                        
                        sts, tmp = self.getDataBeetwenMarkers(verData, '<form', '</form>', caseSensitive=False)
                        if not sts: return False, None
                        
                        url = self.getSearchGroups(tmp, 'action="([^"]+?)"')[0]
                        if url != '': url = _getFullUrl( url, domain )
                        else: url = data.meta['url']
                        actionType = self.getSearchGroups(tmp, 'method="([^"]+?)"', 1, True)[0].lower()
                        post_data2 = dict(re.findall(r'<input[^>]*name="([^"]*)"[^>]*value="([^"]*)"[^>]*>', tmp))
                        #post_data2['id'] = id
                        if '' != token:
                            post_data2['g-recaptcha-response'] = token
                        else:
                            continue
                        params2 = dict(params)
                        params2['header']= dict(params['header'])
                        params2['header']['Referer'] = baseUrl
                        if actionType == 'get':
                            if '?' in url:
                                url += '&'
                            else:
                                url += '?'
                            url += urllib.urlencode(post_data2)
                            post_data2 = None
                            
                        sts, data = self.getPage(url, params2, post_data2)
                        printDBG("+++++++++++++")
                        printDBG(sts)
                        printDBG("-------------")
                        printDBG(data)
                        printDBG("++++++++++++++")
                    else:
                        dat = findall(verData, ('<script', '>'), '</script>', flags=0)
                        for item in dat:
                            if 'setTimeout' in item and 'submit()' in item:
                                dat = item
                                break
                        decoded = ''
                        pathcf=AppPath +'/addonsParser/tsiplayer/' + 'cf.byte'
                        js_params = [{'path':pathcf}]
                        js_params.append({'code':"var location = {hash:''}; var iptv_domain='%s';\n%s\niptv_fun();" % (domain, dat)}) #cfParams['domain']
                        ret = js_execute_ext( js_params )
                        decoded = json_loads(ret['data'].strip())
                        
                        verData = find(verData, ('<form', '>', 'id="challenge-form"'), '</form>')[1]
                        printDBG(">>")
                        printDBG(verData)
                        printDBG("<<")
                        verUrl =  _getFullUrl( getattr(verData, 'action'), domain)
                        get_data = dict(re.findall(r'<input[^>]*name="([^"]*)"[^>]*value="([^"]*)"[^>]*>', verData))
                        get_data['jschl_answer'] = decoded['answer']
                        verUrl += '?'
                        for key in get_data:
                            verUrl += '%s=%s&' % (key, get_data[key])
                        verUrl = _getFullUrl( getattr(verData, 'action'), domain) + '?s=%s&jschl_vc=%s&pass=%s&jschl_answer=%s' % (urllib.quote(get_data['s'], ''), urllib.quote(get_data['jschl_vc']), urllib.quote(get_data['pass']), urllib.quote(get_data['jschl_answer']))
                        verUrl = _getFullUrl2( verUrl, domain)
                        params2 = dict(params)
                        params2['load_cookie'] = True
                        params2['save_cookie'] = True
                        params2['Accept-Encoding'] = '*'
                        params2['header'] = dict(params.get('header', {}))
                        params2['header'].update({'Referer':url, 'User-Agent':cfParams.get('User-Agent', ''), 'Accept-Encoding':'text'})
                        printDBG("Time spent: [%s]" % (time.time() - start_time))
                        if current == 1:
                            GetIPTVSleep().Sleep(1 + (decoded['timeout'] / 1000.0)-(time.time() - start_time))
                        else:
                            GetIPTVSleep().Sleep((decoded['timeout'] / 1000.0))
                        printDBG("Time spent: [%s]" % (time.time() - start_time))
                        printDBG("Timeout: [%s]" % decoded['timeout'])
                        sts, data = self.getPage(verUrl, params2, post_data)
                except Exception:
                    printExc()
                    break
            else:
                break
        return sts, data
    

    
    def saveWebFile(self, file_path, url, addParams = {}, post_data = None):
        addParams = dict(addParams)
        
        outParams, postData = self.getParamsFromUrlWithMeta(url)
        addParams.update(outParams)
        if 'header' not in addParams and 'host' not in addParams:
            host = 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.2.18) Gecko/20110621 Mandriva Linux/1.9.2.18-0.1mdv2010.2 (2010.2) Firefox/3.6.18'
            header = {'User-Agent': host, 'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'}
            addParams['header'] = header
        addParams['return_data'] = False
        
        # if curl should and can be used
        if self.usePyCurl():
            return self.saveWebFileWithPyCurl(file_path, url, addParams, post_data)
    
        bRet = False
        downDataSize = 0
        dictRet = {}
        try:
            sts, downHandler = self.getPage(url, addParams, post_data)

            if addParams.get('ignore_content_length', False):
                meta = downHandler.info()
                contentLength = int(meta.getheaders("Content-Length")[0])
            else:
                contentLength = None
            
            checkFromFirstBytes = addParams.get('check_first_bytes', [])
            OK = True
            if 'maintype' in addParams and addParams['maintype'] != downHandler.headers.maintype:
                printDBG("common.getFile wrong maintype! requested[%r], retrieved[%r]" % (addParams['maintype'], downHandler.headers.maintype))
                if 0 == len(checkFromFirstBytes):
                    downHandler.close()
                OK = False
            
            if OK and 'subtypes' in addParams:
                OK = False
                for item in addParams['subtypes']:
                    if item == downHandler.headers.subtype:
                        OK = True
                        break
            
            if OK or len(checkFromFirstBytes):
                blockSize = addParams.get('block_size', 8192)
                fileHandler = None
                while True:
                    buffer = downHandler.read(blockSize)
                    
                    if len(checkFromFirstBytes):
                        OK = False
                        for item in checkFromFirstBytes:
                            if buffer.startswith(item):
                                OK = True
                                break
                        if not OK:
                            break
                        else:
                            checkFromFirstBytes = []
                    
                    if not buffer:
                        break
                    downDataSize += len(buffer)
                    if len(buffer):
                        if fileHandler == None:
                            fileHandler = file(file_path, "wb")
                        fileHandler.write(buffer)
                if fileHandler != None:
                    fileHandler.close()
                downHandler.close()
                if None != contentLength:
                    if contentLength == downDataSize:
                        bRet = True
                elif downDataSize > 0:
                    bRet = True
        except Exception:
            printExc("common.getFile download file exception")
        dictRet.update( {'sts': bRet, 'fsize': downDataSize} )
        return dictRet
        
    def getUrllibSSLProtocolVersion(self, protocolName):
        if not isinstance(protocolName, basestring):
            GetIPTVNotify().push('getUrllibSSLProtocolVersion error. Please report this problem to addonsParsere2@gmail.com', 'error', 40)
            return protocolName
        if protocolName == 'TLSv1_2':
            return ssl.PROTOCOL_TLSv1_2
        elif protocolName == 'TLSv1_1':
            return ssl.PROTOCOL_TLSv1_1
        return None

    
    def getURLRequestData(self, params = {}, post_data = None):
        
        def urlOpen(req, customOpeners, timeout):
            if len(customOpeners) > 0:
                opener = urllib2.build_opener( *customOpeners )
                if timeout != None:
                    response = opener.open(req, timeout=timeout)
                else:
                    response = opener.open(req)
            else:
                if timeout != None:
                    response = urllib2.urlopen(req, timeout=timeout)
                else:
                    response = urllib2.urlopen(req)
            return response
        

            
        if 'max_data_size' in params and not params.get('return_data', False):
            raise Exception("return_data == False is not accepted with max_data_size.\nPlease also note that return_data == False is deprecated and not supported with PyCurl HTTP backend!")
        
        cj = cookielib.MozillaCookieJar()
        response = None
        req      = None
        out_data = None
        opener   = None
        self.meta = {}
        metadata = self.meta
        
        timeout = params.get('timeout', None)
        
        if 'host' in params:
            host = params['host']
        else:
            host = self.HOST

        if 'header' in params:
            headers = params['header']
        elif None != self.HEADER:
            headers = self.HEADER
        else:
            headers = { 'User-Agent' : host }
            
        if 'User-Agent' not in headers:
            headers['User-Agent'] = host
        
        printDBG('pCommon - getURLRequestData() -> params: ' + str(params))
        printDBG('pCommon - getURLRequestData() -> headers: ' + str(headers)) 

        customOpeners = []
        #cookie support
        if 'use_cookie' not in params and 'cookiefile' in params and ('load_cookie' in params or 'save_cookie' in params):
            params['use_cookie'] = True 
        
        if params.get('use_cookie', False):
            if params.get('load_cookie', False):
                try:
                    cj.load(params['cookiefile'], ignore_discard = True)
                except IOError:
                    printDBG('Cookie file [%s] not exists' % params['cookiefile'])
                except Exception:
                    printExc()
            try:
                for cookieKey in params.get('cookie_items', {}).keys():
                    printDBG("cookie_item[%s=%s]" % (cookieKey, params['cookie_items'][cookieKey]))
                    cookieItem = cookielib.Cookie(version=0, name=cookieKey, value=params['cookie_items'][cookieKey], port=None, port_specified=False, domain='', domain_specified=False, domain_initial_dot=False, path='/', path_specified=True, secure=False, expires=None, discard=True, comment=None, comment_url=None, rest={'HttpOnly': None}, rfc2109=False)
                    cj.set_cookie(cookieItem)
            except Exception:
                printExc()
            customOpeners.append( urllib2.HTTPCookieProcessor(cj) )
            
        if params.get('no_redirection', False):
            customOpeners.append( NoRedirection() )
        
        if None != params.get('ssl_protocol', None):
            sslProtoVer = self.getUrllibSSLProtocolVersion(params['ssl_protocol'])
        else:
            sslProtoVer = None
        # debug 
        #customOpeners.append(urllib2.HTTPSHandler(debuglevel=1))
        #customOpeners.append(urllib2.HTTPHandler(debuglevel=1))
        if not IsHttpsCertValidationEnabled():
            try:
                if sslProtoVer != None:
                    ctx = ssl._create_unverified_context( sslProtoVer )
                else:
                    ctx = ssl._create_unverified_context()
                customOpeners.append(urllib2.HTTPSHandler(context=ctx))
            except Exception: pass
        elif sslProtoVer != None:
            ctx = ssl.SSLContext( sslProtoVer )
            customOpeners.append(urllib2.HTTPSHandler(context=ctx))
        
        #proxy support
        if self.useProxy:
            http_proxy = self.proxyURL
        else:
            http_proxy = ''
        #proxy from parameters (if available) overwrite default one
        if 'http_proxy' in params:
            http_proxy = params['http_proxy']
        if '' != http_proxy:
            printDBG('getURLRequestData USE PROXY')
            customOpeners.append( urllib2.ProxyHandler({"http":http_proxy}) )
            customOpeners.append( urllib2.ProxyHandler({"https":http_proxy}) )
        
        pageUrl = params['url']
        proxy_gateway = params.get('proxy_gateway', '')
        if proxy_gateway != '':
            pageUrl = proxy_gateway.format(urllib.quote_plus(pageUrl, ''))
        printDBG("pageUrl: [%s]" % pageUrl)

        if None != post_data:
            printDBG('pCommon - getURLRequestData() -> post data: ' + str(post_data))
            if params.get('raw_post_data', False):
                dataPost = post_data
            elif params.get('multipart_post_data', False):
                customOpeners.append( MultipartPostHandler() )
                dataPost = post_data
            else:
                dataPost = urllib.urlencode(post_data)
            req = urllib2.Request(pageUrl, dataPost, headers)
        else:
            req = urllib2.Request(pageUrl, None, headers)

        if not params.get('return_data', False):
            out_data = urlOpen(req, customOpeners, timeout)
        else:
            gzip_encoding = False
            try:
                response = urlOpen(req, customOpeners, timeout)
                if response.info().get('Content-Encoding') == 'gzip':
                    gzip_encoding = True
                try: 
                    metadata['url'] = response.geturl()
                    metadata['status_code'] = response.getcode()
                    self.fillHeaderItems(metadata, response.info(), True, collectAllHeaders=params.get('collect_all_headers'))
                except Exception: pass
                
                data = response.read(params.get('max_data_size', -1))
                response.close()
            except urllib2.HTTPError, e:
                ignoreCodeRanges = params.get('ignore_http_code_ranges', [(404, 404), (500, 500)])
                ignoreCode = False
                metadata['status_code'] = e.code
                for ignoreCodeRange in ignoreCodeRanges:
                    if e.code >= ignoreCodeRange[0] and e.code <= ignoreCodeRange[1]:
                        ignoreCode = True
                        break
                
                if ignoreCode:
                    printDBG('!!!!!!!! %s: getURLRequestData - handled' % e.code)
                    if e.fp.info().get('Content-Encoding', '') == 'gzip':
                        gzip_encoding = True
                    try: 
                        metadata['url'] = e.fp.geturl()
                        self.fillHeaderItems(metadata, e.fp.info(), True, collectAllHeaders=params.get('collect_all_headers'))
                    except Exception: pass
                    data = e.fp.read(params.get('max_data_size', -1))
                    #e.msg
                    #e.headers
                elif e.code == 503:
                    if params.get('use_cookie', False):
                        new_cookie = e.fp.info().get('Set-Cookie', '')
                        printDBG("> new_cookie[%s]" % new_cookie)
                        cj.save(params['cookiefile'], ignore_discard = True)
                    raise e
                else:
                    if e.code in [300, 302, 303, 307] and params.get('use_cookie', False) and params.get('save_cookie', False):
                        new_cookie = e.fp.info().get('Set-Cookie', '')
                        printDBG("> new_cookie[%s]" % new_cookie)
                        #for cookieKey in params.get('cookie_items', {}).keys():
                        #    cj.clear('', '/', cookieKey)
                        cj.save(params['cookiefile'], ignore_discard = True)
                    raise e
            try:
                if gzip_encoding:
                    printDBG('Content-Encoding == gzip')
                    out_data = DecodeGzipped(data)
                else:
                    out_data = data
            except Exception as e:
                printExc()
                if params.get('max_data_size', -1) == -1: 
                    msg1 = _("Critical Error – Content-Encoding gzip cannot be handled!")
                    msg2 = _("Last error:\n%s" % str(e))
                    #GetIPTVNotify().push('%s\n\n%s' % (msg1, msg2), 'error', 20)
                    printD('error','%s\n\n%s' % (msg1, msg2))
                out_data = data
 
        if params.get('use_cookie', False) and params.get('save_cookie', False):
            try:
                cj.save(params['cookiefile'], ignore_discard = True)
            except Exception as e:
                printExc()
                raise e
        
        out_data, metadata = self.handleCharset(params, out_data, metadata)
        if params.get('with_metadata', False) and params.get('return_data', False):
            out_data = strwithmeta(out_data, metadata)
        
        return out_data 
        
    def handleCharset(self, params, data, metadata):
        try:
            if params.get('return_data', False) and params.get('convert_charset', True) :
                encoding = ''
                if 'content-type' in metadata:
                    encoding = self.ph.getSearchGroups(metadata['content-type'], '''charset=([A-Za-z0-9\-]+)''', 1, True)[0].strip().upper()
                
                if encoding == '' and params.get('search_charset', False):
                    encoding = self.ph.getSearchGroups(data, '''(<meta[^>]+?Content-Type[^>]+?>)''', ignoreCase=True)[0]
                    encoding = self.ph.getSearchGroups(encoding, '''charset=([A-Za-z0-9\-]+)''', 1, True)[0].strip().upper()
                if encoding not in ['', 'UTF-8']:
                    printDBG(">> encoding[%s]" % encoding)
                    try:
                        data = data.decode(encoding).encode('UTF-8')
                    except Exception:
                        printExc()
                    metadata['orig_charset'] = encoding
        except Exception:
            printExc()
        return data, metadata

    def urlEncodeNonAscii(self, b):
        return re.sub('[\x80-\xFF]', lambda c: '%%%02x' % ord(c.group(0)), b)

    def iriToUri(self, iri):
        try:
            parts = urlparse(iri.decode('utf-8'))
            encodedParts = []
            for parti, part in enumerate(parts):
                newPart = part
                try:
                    if parti == 1: newPart = part.encode('idna')
                    else: newPart = self.urlEncodeNonAscii(part.encode('utf-8'))
                except Exception:
                    printExc()
                encodedParts.append(newPart)
            return urlunparse(encodedParts)
        except Exception:
            printExc()
        return iri

    def makeABCList(self, tab = ['0 - 9']):
        strTab = list(tab)
        for i in range(65,91):
            strTab.append(str(unichr(i)))    
        return strTab
class GestionCookie():
    PathCache = GetCookieDir('')

    def DeleteCookie(self,Domain):
        Name = ''.join([self.PathCache, "cookie_%s.txt"]) % (Domain)
        os.remove(Name)

    def SaveCookie(self,Domain,data):
        Name = ''.join([self.PathCache, "cookie_%s.txt"]) % (Domain)
        f = open(Name, 'w')
        f.write(data)
        f.close()

    def Readcookie(self,Domain):
        Name = ''.join([self.PathCache, "cookie_%s.txt"]) % (Domain)

        try:
            f = open(Name,'r')
            data = f.read()
            f.close()
        except:
            return ''

        return data

    def AddCookies(self):
        cookies = self.Readcookie(self.__sHosterIdentifier)
        return 'Cookie=' + cookies
##############################        
###################################################


def printE(msg=''):
    import traceback,sys
    printD("===============================================")
    printD("                   EXCEPTION                   ")
    printD("===============================================")
    msg = msg + ': \n%s' % traceback.format_exc()
    traceback.print_exc(file=sys.stdout)
    printD("Error",msg)
    printD("===============================================")
  
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

def printDBG( DBGtxt ):
        try:DBGtxt=DBGtxt.encode("utf-8",'replace')
        except:pass
        print DBGtxt

        try:
            f = open(log_file, 'a')
            
            f.write(DBGtxt + '\n')
            f.close
        except Exception:
            print("======================EXC printDBG======================")
            print("printDBG(I): %s" % traceback.format_exc())
            print("========================================================")
            try:
                msg = '%s' % traceback.format_exc()
                
                f = open(log_file, 'a')
                f.write(DBGtxt + '\n')
                f.close
            except Exception:
                print("======================EXC printDBG======================")
                print("printDBG(II): %s" % traceback.format_exc())
                print("========================================================")

                
########################################



def getimage_basename(webfile):
           try:
                if webfile.startswith('http'):
       
                        image_basenames = webfile.split("/")
                        image_basename=image_basenames[-2]+image_basenames[-1]
                        if not image_basename.endswith("jpg") and not image_basename.endswith("png") and not image_basename.endswith("jpeg"):
                            
                            image_basename=image_basename+".jpg"
                       
                     
                else:
                    image_basename = webfile
                   
                   
                return image_basename
           except:
                return webfile

def getmainitem_image():
    try:
        imagefile='/tmp/TSmedia/mimage'
        image=open(imagefile).read()
        return image

    except:
        return ''
def supported(hostname):##mfaraj
    hostname=hostname.lower()
    try:
        from urlresolver.supservers import supported_servers  
        
        if supported_servers.has_key(hostname):
            supported=True
        else:
            supported =False
        return supported    
   
    except:
        printE()
        return False
def getserver_image(server):
    default_path=sys.argv[0]
    
    try:
        
        image_dir=os.path.dirname(default_path)
        image=os.path.join(image_dir, "img")
        image=image+"/"+server+".png"
        if  os.path.exists(image):
           
            pass
        else:
            image=plugin_path+"/interface/servers/"+server+".png"
            if  os.path.exists(image):
                pass
            else:            
               image=os.path.join(image_dir,'icon.png')
    except:
         image=os.path.join(image_dir,'icon.png')
    return image    
def cleanhtml2(raw_html,withSpace=False):

    def replaceSpecialCharacters(sString):
        return sString.replace('\\/','/').replace('&amp;','&').replace('\xc9','E').replace('&#8211;', '-').replace('&#038;', '&').replace('&rsquo;','\'').replace('\r','').replace('\n','').replace('\t','').replace('&#039;',"'").replace('&quot;','"').replace('&gt;','>').replace('&lt;','<').replace('&nbsp;','').replace('&bull;','')

    
    cleanr = re.compile('<.*?>')
    if withSpace:
       cleantext = re.sub(cleanr, ' ', raw_html)
    else:
       cleantext = re.sub(cleanr, '', raw_html) 
    return replaceSpecialCharacters(cleantext)

def cleanTitle(title):
    title = title.replace('&lt;', '<').replace('&gt;', '>').replace('&amp;', '&').replace('&#039;', "'").replace('&quot;', '"').replace('&szlig;', '\xc3\x9f').replace('&ndash;', '-')
    title = title.replace('&Auml;', '\xc3\x84').replace('&Uuml;', '\xc3\x9c').replace('&Ouml;', '\xc3\x96').replace('&auml;', '\xc3\xa4').replace('&uuml;', '\xc3\xbc').replace('&ouml;', '\xc3\xb6')
    title = title.strip()
    return title
    
def getdebug_mode():
    debugmode='user'
    debugmode_file = '/tmp/TSmedia/debugmode'
    if os.path.exists(debugmode_file):
        try:
            debugmode = open(debugmode_file).read()
            return debugmode
        except:
            pass
    else:
        return debugmode
    return debugmode

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
def cfresolve(url_page = None):
    
    if url_page:
        CBaseAddon=CBaseAddonClass({'cookie':'cooke.cookie'})
        sts,data = CBaseAddon.getPageCFProtection(url_page, addParams = {}, post_data = None)
        return data
def cfdownloadImage(url = None,images_cachepath=None,localfile=None):
    ofile=''
   
    if url is None or url.strip() == '':
        return ''
    else:
        if 'ExQ' in url:
            url.replace('ExQ', '=')
        if getos() == 'windows':
            path = 'd:\\tmp'
        else:
            path = images_cachepath
        
        if url and url.startswith('http'):
            try:
                if localfile is None:
                    filename = url.split('/')[-1]
                    ofile = os.path.join(path, filename)

                else:
                    ofile=localfile
                if os.path.exists(ofile):
                    return ofile
                try:
                    r = cfresolve(url)
                    with open(ofile, 'wb') as f:
                        f.write(r)
                    f.close()
                    return ofile
                except:
                    printE()
                    pass

            except:
                printE()

        return ofile
        


def downloadImage(url = None,images_cachepath=None,localfile=None):
    ofile=True

    if url is None or url.strip() == '':
        return ''
    else:
        if 'ExQ' in url:
            url.replace('ExQ', '=')
        if getos() == 'windows':
            path = 'd:\\tmp'
        else:
            path = images_cachepath
       
       
        if url and url.startswith('http'):
            try:
                if localfile is None:
                    filename = url.split('/')[-1]
                    ofile = os.path.join(path, filename)

                else:
                    ofile=localfile

                if os.path.exists(ofile):
                     
                    return ofile
                r = requests.get(url, timeout=0.5,verify=False)
                if r.status_code == 200:
                    with open(ofile, 'wb') as f:
                        f.write(r.content)
                    f.close()
                    
                    return ofile
            except:
                printE()
            
        return ofile
        return


def get_youtube_link(value):
    """
    Examples:
    - http://youtu.be/SA2iWivDJiE
    - http://www.youtube.com/watch?v=_oPAwA_Udwc&feature=feedu
    - http://www.youtube.com/embed/SA2iWivDJiE
    - http://www.youtube.com/v/SA2iWivDJiE?version=3&amp;hl=en_US
    -'plugin://plugin.video.youtube/?action=play_video&amp;videoid=FBBLhRgrw0o'
    """
    from urlparse import urlparse
    vid = None
    if value is None:
        return
    else:
        value = value.strip()
        if value.startswith('plugin://'):
            try:
                vid = value.split('=')[value.count('=')]
            except:
                return

        else:
            query = urlparse(value)
            if query.hostname == 'youtu.be':
                vid = query.path[1:]
            elif query.hostname in ('www.youtube.com', 'youtube.com'):
                if query.path == '/watch':
                    p = parse_qs(query.query)
                    vid = p['v'][0]
                if query.path[:7] == '/embed/':
                    vid = query.path.split('/')[2]
                if query.path[:3] == '/v/':
                    vid = query.path.split('/')[2]
                    
        if vid is not None:            
           return 'plugin://plugin.video.youtube/?action=play_video&videoid=%s' % vid
        else:
           return        
def is_ascii(s):
    try:
        s.decode('ascii')
    except UnicodeDecodeError:
        return False
    else:
        return True
def downloadfile(url = None, target = ''):
    try:
        import requests
        s=requests.Session()
        r = s.get(url, timeout=10, verify=False)
        if r.status_code == 200:
            with open(target, 'wb') as f:
                f.write(r.content)
            f.close()
            return True
    except:
        printE()
        return False  
def getmb(b):##torrent
    try:
      return str(round(b/(1024*1024),2))+"MB"
    except:
        printE()
        return ''
#####################
def decorateUrl(url, metaParams={}):
    retUrl = strwithmeta( url )
    retUrl.meta.update(metaParams)
    urlLower = url.lower()
    if 'iptv_proto' not in retUrl.meta:
        if urlLower.startswith('merge://'):
            retUrl.meta['iptv_proto'] = 'merge'
        elif urlLower.split('?')[0].endswith('.m3u8'):
            retUrl.meta['iptv_proto'] = 'm3u8'
        elif urlLower.split('?')[0].endswith('.f4m'):
            retUrl.meta['iptv_proto'] = 'f4m'
        elif 'protocol=hls' in urlLower:
            retUrl.meta['iptv_proto'] = 'm3u8'
        elif urlLower.split('?')[0].endswith('.mpd'):
            retUrl.meta['iptv_proto'] = 'mpd'
        elif urlLower.startswith('rtmp'):
            retUrl.meta['iptv_proto'] = 'rtmp'
        elif urlLower.startswith('https'):
            retUrl.meta['iptv_proto'] = 'https'
        elif urlLower.startswith('http'):
            retUrl.meta['iptv_proto'] = 'http'
        elif urlLower.startswith('file'):
            retUrl.meta['iptv_proto'] = 'file'
        elif urlLower.startswith('rtsp'):
            retUrl.meta['iptv_proto'] = 'rtsp'
        elif urlLower.startswith('mms'):
            retUrl.meta['iptv_proto'] = 'mms'
        elif urlLower.startswith('mmsh'):
            retUrl.meta['iptv_proto'] = 'mmsh'
    return retUrl
ph = CParsingHelper

def  yt_clean_html(html):
    """Clean an HTML snippet into a readable string"""
    if type(html) == type(u''):
        strType = 'unicode'
    elif type(html) == type(''):
        strType = 'utf-8'
        html = html.decode("utf-8", 'ignore')
        
    # Newline vs <br />
    html = html.replace('\n', ' ')
    html = re.sub(r'\s*<\s*br\s*/?\s*>\s*', '\n', html)
    html = re.sub(r'<\s*/\s*p\s*>\s*<\s*p[^>]*>', '\n', html)
    # Strip html tags
    html = re.sub('<.*?>', '', html)
    # Replace html entities
    html = unescapeHTML(html)
    
    if strType == 'utf-8': 
        html = html.encode("utf-8")
    
    return html.strip()

try:
    compat_str = unicode # Python 2
except NameError:
    compat_str = str

try:
    compat_chr = unichr # Python 2
except NameError:
    compat_chr = chr

def compat_ord(c):
    if type(c) is int: return c
    else: return ord(c)

    
def unescapeHTML(s):
    if s is None:
        return None
    assert type(s) == compat_str

    return re.sub(r'&([^;]+);', lambda m: htmlentity_transform(m.group(1)), s)
def htmlentity_transform(entity):
    """Transforms an HTML entity to a character."""
    # Known non-numeric HTML entity
    try:
        if entity in compat_html_entities.name2codepoint:
            return compat_chr(compat_html_entities.name2codepoint[entity])
    except Exception: pass

    mobj = re.match(r'#(x?[0-9A-Fa-f]+)', entity)
    if mobj is not None:
        numstr = mobj.group(1)
        if numstr.startswith(u'x'):
            base = 16
            numstr = u'0%s' % numstr
        else:
            base = 10
        try:
            ret = compat_chr(int(numstr, base))
            return ret
        except Exception:
            printExc()
    # Unknown entity in name, return its literal representation
    return (u'&%s;' % entity)
def saveSession(S,name=''):
    try:
        import pickle
        if name=='':
            return
        with open(AppPath+"/media/hdd/%s.ses"%name, 'wb') as f:
            pickle.dump(S, f)
    except:
        pass
def getSession(name=''):
    try:
        import pickle,requests
        if name=='':
            return None    
        try:
            with open(AppPath+"/media/hdd/%s.ses"%name, 'rb') as f:
                S = pickle.load(f)
        except IOError:
                S = requests.session()
        return S
    except:
        printE()
        return requests.session()

def unzipFile(zipFile, dstDir):
    try:
        from zipfile import ZipFile
        with ZipFile(zipFile, 'r') as zipObj:
            zipObj.extractall(dstDir)
            listOfiles = zipObj.namelist()
        printD('unzopped succ', zipFile)
        printD('unzopped succ-dstDir', dstDir)
        return listOfiles
    except:
        printE()
        return []    
def DownloadUnzipSRT(webZIP,path):
        
        from zipfile import ZipFile
        zipBasename = os.path.basename(webZIP)
        localZIP=path+"/"+zipBasename
        sts=downloadZIP(webFile,localZIP )
        if not sts: return False
        if localZIP.endswith('.zip'):
            filesList=unzipFile(localZIP, path)
        try:
            srtFile=''
            for zFile in filesList:
                if zFile.endswith(".srt"):
                    srtFile=zFile
                    break
            if srtFile!='' :
                os.rename(path + '/' + srtFile, path+"/"+zipBasename)
            
        except:
            
            printE()
            srtFiles = []
def downloadZIP(url = None, target = ''):
    try:
        if os.path.exists(target):
            return
        import requests
        session = requests.Session()
        r = session.get(url, timeout=5, verify=False)
        if r.status_code == 200:
            with open(target, 'wb') as f:
                f.write(r.content)
            f.close()
            printD('zipfiledownloaded success', target)
            return True
        printD('zipfiledownloaded failed', r.status_code)
        return False
    except:
        printE()
        printD('zipfiledownloaded success', target)
        return False
def getIMDBParams(imdbTrailer='',imdb_id=''):
  import os,json,requests  
  videoURL=''
  try:
    if imdb_id=='':  
        if imdbTrailer.startswith("http"):
            vid=os.path.basename(os.path.normpath(imdbTrailer))
        else:
            vid=imdbTrailer
        jsLink='https://www.imdb.com/_json/video/%s'%vid

        jData=requests.get(jsLink).json()
        imdb_id=jData["videoMetadata"][vid].get('primaryConst','')
        imdbTrailer='https://www.imdb.com/videoembed/%s'%vid
        videos=jData["videoMetadata"][vid]['encodings']
        vidoescount= len(videos)
        for i in range(vidoescount):
            definition= videos[i]['definition']
            videoURL= videos[i]['videoUrl']
            if definition=="720p":
                return imdbTrailer,imdb_id,videoURL
            
        return imdbTrailer,imdb_id,videoURL   




        
    else:
        jsLink='https://m.imdb.com/_json/video/%s'%imdb_id
        jData=requests.get(jsLink).json()
        items=jData["videoMetadata"]
        vid=items.keys()[0]
        imdbTrailer='https://www.imdb.com/videoembed/%s'%vid
        videos=jData["videoMetadata"][vid]['encodings']
        vidoescount= len(videos)
        for i in range(vidoescount):
            definition= videos[i]['definition']
            videoURL= videos[i]['videoUrl']
            if definition=="720p":
                return imdbTrailer,imdb_id,videoURL
            
        return imdbTrailer,imdb_id,videoURL        
        
    
    

  except Exception as error:
      print str(error)
      printE()
  return imdbTrailer,imdb_id,videoURL

#trailerURL="https://www.imdb.com/videoembed/vi2935144217/"
#imdb_id='tt8972256'
#print getIMDBParams(trailerURL,imdb_id)

