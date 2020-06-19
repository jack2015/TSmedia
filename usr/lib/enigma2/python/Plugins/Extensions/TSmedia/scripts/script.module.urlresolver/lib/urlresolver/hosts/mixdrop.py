import warnings
from requests.packages.urllib3.exceptions import InsecureRequestWarning
warnings.simplefilter('ignore',InsecureRequestWarning)
import requests,re
from random import choice
from jsunpack import unpack
def _default_get_url(host, media_id, template=None):
    if template is None: template = 'http://{host}/embed-{media_id}.html'
    return template.format(host=host, media_id=media_id)
def get_url(host, media_id):
    return _default_get_url(host, media_id, template='https://{host}/embed-{media_id}.html')
def get_packed_data(html):
    packed_data = ''
    for match in re.finditer('(eval\s*\(function.*?)</script>', html, re.DOTALL | re.I):
        try:
            js_data = unpack(match.group(1))
            js_data = js_data.replace('\\', '')
            packed_data += js_data
        except:
            pass
    return packed_data
def get_video_url(host, media_id):
    web_url = get_url(host, media_id)
    headers = {'Origin': 'https://{}'.format(host),
               'Referer': 'https://{}/'.format(host),
               'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:61.0) Gecko/20100101 Firefox/61.0'}
    html = requests.get('https://mixdrop.co/e/'+str(media_id)+'?download', headers=headers).content
    if '(p,a,c,k,e,d)' in html:
        html = get_packed_data(html)
    r = re.search(r'(?:vsr|wurl|surl)[^=]*=\s*"([^"]+)', html)
    if r:
        return "https:" + r.group(1)
##url = "https://mixdrop.co/f/4qlicoowiuv"
#url1= "https://mixdrop.co/e/26wluvk35ne"
#print get_video_url('mixdrop.co', '26wluvk35ne')
