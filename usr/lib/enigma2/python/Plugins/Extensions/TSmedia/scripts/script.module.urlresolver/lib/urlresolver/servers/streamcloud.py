# -*- coding: utf-8 -*-
# StreamOnDemand Community Edition - Kodi Addon

from platformcode import logger
from core import scrapertools


def test_video_exists(page_url):
    logger.info("page_url='%s')" % page_url)

    data = scrapertools.cache_page(url=page_url)
    if "<h1>404 Not Found</h1>" in data:
        return False,"Video non trovato"
    else:
        return True, ""


def get_video_url(page_url, premium=False, user="", password="", video_password=""):
    logger.info("url=" + page_url)

    # Lo pide una vez
    headers = [
        ['User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.8.1.14) Gecko/20080404 Firefox/2.0.0.14']]
    data = scrapertools.cache_page(page_url, headers=headers)

    try:
        media_url = scrapertools.get_match(data, 'file\: "([^"]+)"')
    except:
        post = ""
        matches = scrapertools.find_multiple_matches(data, '<input.*?name="([^"]+)".*?value="([^"]*)">')
        for inputname, inputvalue in matches:
            post += inputname + "=" + inputvalue + "&"
        post = post.replace("op=download1", "op=download2")
        data = scrapertools.cache_page(page_url, post=post)

        if 'id="justanotice"' in data:
            logger.info("data=" + data)
            logger.info("Ha saltado el detector de adblock")
            return []

        # Extrae la URL
        media_url = scrapertools.get_match(data, 'file\: "([^"]+)"')

    video_urls = []
    video_urls.append([scrapertools.get_filename_from_url(media_url)[-4:] + " [streamcloud]", media_url])

    for video_url in video_urls:
        logger.info("%s - %s" % (video_url[0], video_url[1]))

    return video_urls
