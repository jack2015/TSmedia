# -*- coding: utf-8 -*-
# StreamOnDemand Community Edition - Kodi Addon

from core import httptools, scrapertools
from platformcode import logger


def test_video_exists(page_url):
    logger.info("(page_url='%s')" % page_url)

    data = httptools.downloadpage(page_url).data

    if "File was deleted" in data:
        return False, "[speedvideo] Il file non esiste oppure è stato cancellato"

    return True, ""
def get_video_url(url):
        import re
        from xbmctools import readnet
        
        data=readnet(url)
        regx="file: '(.*?)'"
        match=re.findall(regx,data, re.M|re.I)
        print "match",match
        list1=[]
        for href in match:
                if not ".mp4" in href:
                        continue
                list1.append(("link",href))
        return list1 
def get_video_url2(page_url,
                  premium=False,
                  user="",
                  password="",
                  video_password=""):
    logger.info("url=" + page_url)
    video_urls = []

    data = httptools.downloadpage(page_url).data

    media_urls = scrapertools.find_multiple_matches(data, r"file:[^']'([^']+)',\s*label:[^\"]\"([^\"]+)\"")

    for media_url, label in media_urls:
        media_url = httptools.downloadpage(media_url, only_headers=True, follow_redirects=False).headers.get("location", "")

        if media_url:
            video_urls.append([label + " " + media_url.rsplit('.', 1)[1] + ' [speedvideo]', media_url])

    return video_urls
