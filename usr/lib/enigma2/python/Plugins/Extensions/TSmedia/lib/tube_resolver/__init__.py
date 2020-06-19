import sys, os
from Plugins.Extensions.TSmedia.lib.pltools import logtmpdata as log, trace_error,get_youtube_video_id

def getvideo(url = None):
    error = None
    log('starting url', url)

    if ":" in url:
       video_id = get_youtube_video_id(url)
    else:
        video_id=url
    video_url = None
    try:
        from youtubedl.YouTubeVideoUrl import YouTubeVideoUrl
        ytdl = YouTubeVideoUrl()
        video_url = ytdl.extract(video_id)
        log('error,video_url', str(video_url))
        if video_url.startswith('Error'):
            return video_url
        if video_url is None:
            return ('Error :', ' video_url ' + str(video_url))
        if video_url is not None and video_url.startswith('http') and not video_url.startswith('Error') and not video_url.strip() == '':
            return video_url
        return 'Error:check /tmp/TSmedia.log'
    except Exception as e:
        trace_error()
        return 'Error:' + str(e)

    return
