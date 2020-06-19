import urllib,urllib2,re,os,json,requests,hashlib,time,jsunpack
from urlparse import urlparse



def scrape_sources(html, result_blacklist=None, scheme='http', patterns=None, generic_patterns=True):
    if patterns is None: patterns = []
    
    def __parse_to_list(_html, regex):
        _blacklist = ['.jpg', '.jpeg', '.gif', '.png', '.js', '.css', '.htm', '.html', '.php', '.srt', '.sub', '.xml', '.swf', '.vtt', '.mpd']
        _blacklist = set(_blacklist + result_blacklist)
        streams = []
        labels = []
        for r in re.finditer(regex, _html, re.DOTALL):
            match = r.groupdict()
            stream_url = match['url'].replace('&amp;', '&')
            file_name = urlparse(stream_url[:-1]).path.split('/')[-1] if stream_url.endswith("/") else urlparse(stream_url).path.split('/')[-1]
            blocked = not file_name or any(item in file_name.lower() for item in _blacklist)
            if stream_url.startswith('//'): stream_url = scheme + ':' + stream_url
            if '://' not in stream_url or blocked or (stream_url in streams) or any(stream_url == t[1] for t in source_list):
                continue
    
            label = match.get('label', file_name)
            if label is None: label = file_name
            labels.append(label)
            streams.append(stream_url)
            
        matches = zip(labels, streams)
        if matches:
            print "matches",matches
        return matches

    if result_blacklist is None:
        result_blacklist = []
    elif isinstance(result_blacklist, str):
        result_blacklist = [result_blacklist]
        
    html = html.replace("\/", "/")
    html += get_packed_data(html)

    source_list = []
    if generic_patterns or not patterns:
        source_list += __parse_to_list(html, '''["']?label\s*["']?\s*[:=]\s*["']?(?P<label>[^"',]+)["']?(?:[^}\]]+)["']?\s*file\s*["']?\s*[:=,]?\s*["'](?P<url>[^"']+)''')
        source_list += __parse_to_list(html, '''["']?\s*(?:file|src)\s*["']?\s*[:=,]?\s*["'](?P<url>[^"']+)(?:[^}>\]]+)["']?\s*label\s*["']?\s*[:=]\s*["']?(?P<label>[^"',]+)''')
        source_list += __parse_to_list(html, '''video[^><]+src\s*[=:]\s*['"](?P<url>[^'"]+)''')
        source_list += __parse_to_list(html, '''source\s+src\s*=\s*['"](?P<url>[^'"]+)['"](?:.*?res\s*=\s*['"](?P<label>[^'"]+))?''')
        source_list += __parse_to_list(html, '''["'](?:file|url)["']\s*[:=]\s*["'](?P<url>[^"']+)''')
        source_list += __parse_to_list(html, '''param\s+name\s*=\s*"src"\s*value\s*=\s*"(?P<url>[^"]+)''')
    for regex in patterns:
        source_list += __parse_to_list(html, regex)
        
    source_list = list(set(source_list))
    
   

    return source_list
def get_packed_data(html):
    packed_data = ''
    for match in re.finditer('(eval\s*\(function.*?)</script>', html, re.DOTALL | re.I):
        try:
            js_data = jsunpack.unpack(match.group(1))
            js_data = js_data.replace('\\', '')
            packed_data += js_data
        except:
            pass
        
    return packed_data
