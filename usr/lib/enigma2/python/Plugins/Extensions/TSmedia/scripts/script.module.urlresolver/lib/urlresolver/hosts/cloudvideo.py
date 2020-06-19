
def get_video_url(url, premium=False, user="", password="", video_password=""):
    import re
    import requests
    List_Vid = []
    s = requests.Session()
    r = s.get(url)
    htmldata2 = r.text
    Rgx = '''<source src="(.+?)"'''
    cline = re.findall(Rgx,htmldata2)
    if cline:
        cline = cline[0]
        w=('Cool_* cloudvideo',cline)
        List_Vid.append(w)
    else:
        w=('Ooops_* cloudvideo','https://error')
        List_Vid.append(w)
    return List_Vid

S1= 'https://cloudvideo.tv/embed-gamkpgelabef.html'
#print get_video_url(S1)
