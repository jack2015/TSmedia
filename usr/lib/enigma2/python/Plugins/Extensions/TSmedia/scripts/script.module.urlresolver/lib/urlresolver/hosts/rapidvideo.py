def get_video_url(url, premium=False, user="", password="", video_password=""):
    import re
    import requests
    List_Vid = []
    s = requests.Session()
    r = s.get(url)
    htmldata2 = r.text
    Rgx = '''<source src="(.+?)" type=".+?" label="(.+?)" data-res.+?/>'''
    cline = re.findall(Rgx,htmldata2)
    if cline:
        for url,qlt in cline:
            w=('Cool_* rapidvideo_'+qlt,url)
            List_Vid.append(w)
    else:
        w=('Ooops_* rapidvideo','https://error')
        List_Vid.append(w)
    return List_Vid

href='https://www.rapidvideo.com/e/G3HWV5XPDR'
AA = get_video_url(href)
print AA
