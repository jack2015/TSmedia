def get_video_url(url):
    import re
    import requests
    from requests.auth import HTTPBasicAuth
    import urllib
    ListVid = []
    s = requests.Session()
    r = s.get(url)
    htmldata2 = r.text
    Rgx = '''sources: \["(.+?)"\]'''
    cline = re.findall(Rgx,htmldata2)
    if cline:
        cline = cline[0]
    else:
        cline = 'nada'
    return [("play",cline)]
S1= 'https://govid.me/embed-843xtgt48att.html'
print get_video_url(S1)
