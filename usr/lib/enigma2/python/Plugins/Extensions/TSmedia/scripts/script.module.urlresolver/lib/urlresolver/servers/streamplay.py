# -*- coding: utf-8 -*-
# StreamOnDemand Community Edition - Kodi Addon

import re

from core import httptools
from platformcode import logger
from core import scrapertools
from lib import jsunpack

headers = [['User-Agent', 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:53.0) Gecko/20100101 Firefox/53.0']]
host = "http://streamplay.to/"


def test_video_exists(page_url):
    logger.info("(page_url='%s')" % page_url)
    referer = re.sub(r"embed-|player-", "", page_url)[:-5]
    data = httptools.downloadpage(page_url, headers={'Referer': referer}).data
    if data == "File was deleted":
        return False, "[Streamplay] Il video è stato cancellato"
    elif "Video is processing now" in data:
        return False, "[Streamplay] Il video è in conversione"
    return True, ""


def get_video_url(page_url, premium=False, user="", password="", video_password=""):
    logger.info("(page_url='%s')" % page_url)
    referer = re.sub(r"embed-|player-", "", page_url)[:-5]
    data = httptools.downloadpage(page_url, headers={'Referer': referer}).data

    matches = scrapertools.find_single_match(data, "<script type=[\"']text/javascript[\"']>(eval.*?)</script>")
    data = jsunpack.unpack(matches).replace("\\", "")

    data = scrapertools.find_single_match(data.replace('"', "'"), "sources\s*=[^\[]*\[([^\]]+)\]")
    matches = scrapertools.find_multiple_matches(data, "[src|file]:'([^']+)'")
    video_urls = []
    for video_url in matches:
        _hash = scrapertools.find_single_match(video_url, '[A-z0-9\_\-]{40,}')
        hash = _hash[::-1]
        hash = hash.replace(hash[1:2],"",1)
        video_url = video_url.replace(_hash, hash)

        filename = scrapertools.get_filename_from_url(video_url)[-4:]
        if video_url.startswith("rtmp"):
            rtmp, playpath = video_url.split("vod/", 1)
            video_url = "%svod/ playpath=%s swfUrl=%splayer6/jwplayer.flash.swf pageUrl=%s" % \
                        (rtmp, playpath, host, page_url)
            filename = "RTMP"
        elif video_url.endswith("/v.mp4"):
            video_url_flv = re.sub(r'/v.mp4', '/v.flv', video_url)
            video_urls.append(["flv [streamplay]", video_url_flv])

        video_urls.append([filename + " [streamplay]", video_url])

    video_urls.sort(key=lambda x: x[0], reverse=True)
    for video_url in video_urls:
        logger.info(" %s - %s" % (video_url[0], video_url[1]))

    return video_urls


def decrypt(h, k):
    import base64

    if len(h) % 4:
        h += "=" * (4 - len(h) % 4)
    sig = []
    h = base64.b64decode(h.replace("-", "+").replace("_", "/"))
    for c in range(len(h)):
        sig += [ord(h[c])]

    sec = []
    for c in range(len(k)):
        sec += [ord(k[c])]

    dig = range(256)
    g = 0
    v = 128
    for b in range(len(sec)):
        a = (v + (sec[b] & 15)) % 256
        c = dig[(g)]
        dig[g] = dig[a]
        dig[a] = c
        g += 1

        a = (v + (sec[b] >> 4 & 15)) % 256
        c = dig[g]
        dig[g] = dig[a]
        dig[a] = c
        g += 1

    k = 0
    q = 1
    p = 0
    n = 0
    for b in range(512):
        k = (k + q) % 256
        n = (p + dig[(n + dig[k]) % 256]) % 256
        p = (k + p + dig[n]) % 256
        c = dig[k]
        dig[k] = dig[n]
        dig[n] = c

    q = 3
    for a in range(v):
        b = 255 - a
        if dig[a] > dig[b]:
            c = dig[a]
            dig[a] = dig[b]
            dig[b] = c

    k = 0
    for b in range(512):
        k = (k + q) % 256
        n = (p + dig[(n + dig[k]) % 256]) % 256
        p = (k + p + dig[n]) % 256
        c = dig[k]
        dig[k] = dig[n]
        dig[n] = c

    q = 5
    for a in range(v):
        b = 255 - a
        if dig[a] > dig[b]:
            c = dig[a]
            dig[a] = dig[b]
            dig[b] = c

    k = 0
    for b in range(512):
        k = (k + q) % 256
        n = (p + dig[(n + dig[k]) % 256]) % 256
        p = (k + p + dig[n]) % 256
        c = dig[k]
        dig[k] = dig[n]
        dig[n] = c

    q = 7
    k = 0
    u = 0
    d = []
    for b in range(len(dig)):
        k = (k + q) % 256
        n = (p + dig[(n + dig[k]) % 256]) % 256
        p = (k + p + dig[n]) % 256
        c = dig[k]
        dig[k] = dig[n]
        dig[n] = c
        u = dig[(n + dig[(k + dig[(u + p) % 256]) % 256]) % 256]
        d += [u]

    c = []
    for f in range(len(d)):
        try:
            c += [(256 + (sig[f] - d[f])) % 256]
        except:
            break

    h = ""
    for s in c:
        h += chr(s)

    return h
