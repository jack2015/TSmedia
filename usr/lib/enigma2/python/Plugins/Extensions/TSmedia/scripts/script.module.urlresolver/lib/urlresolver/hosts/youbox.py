
def get_video_url(host, media_id):
    import requests,re
    
    html = requests.get(S1).content
    r = re.search(r'(?:source src)[^=]*=\s*"([^"]+)', html)
    return r.group(1)
##url = S1 = "https://youdbox.com/embed-nawatrcczbp7.html"
#url1= "https://mixdrop.co/e/26wluvk35ne"
#print get_video_url('mixdrop.co', '26wluvk35ne')
