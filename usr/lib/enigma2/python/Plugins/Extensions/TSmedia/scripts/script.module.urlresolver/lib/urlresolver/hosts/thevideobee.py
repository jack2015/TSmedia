def get_video_url(url, premium=False, user="", password="", video_password=""):
    import re
    import requests
    List_Vid = []
    s = requests.Session()
    r = s.get(url)
    htmldata2 = r.text
    Rgx = '''sources: \[\{src: "(.+?)"'''
    cline = re.findall(Rgx,htmldata2)
    if cline:
        w=('Cool_* thevideobee_',cline[0])
        List_Vid.append(w)
    else:
        w=('Ooops_* thevideobee','https://error')
        List_Vid.append(w)
    return List_Vid

href='https://thevideobee.to/embed-wvl1jid9bbuc.html'
AA = get_video_url(href)
print AA
