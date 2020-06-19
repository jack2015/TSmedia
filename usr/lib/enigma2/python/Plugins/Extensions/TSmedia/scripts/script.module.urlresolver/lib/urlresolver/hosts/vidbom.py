import requests,re
sgn = requests.Session()
def decode1(text):
    text = re.sub(r"\s+|/\*.*?\*/", "", text)
    data = text.split("+(ﾟДﾟ)[ﾟoﾟ]")[1]
    chars = data.split("+(ﾟДﾟ)[ﾟεﾟ]+")[1:]
    txt = ""
    for char in chars:
        char = char \
            .replace("(oﾟｰﾟo)","u") \
            .replace("c", "0") \
            .replace("(ﾟДﾟ)['0']", "c") \
            .replace("ﾟΘﾟ", "1") \
            .replace("!+[]", "1") \
            .replace("-~", "1+") \
            .replace("o", "3") \
            .replace("_", "3") \
            .replace("ﾟｰﾟ", "4") \
            .replace("(+", "(")
        char = re.sub(r'\((\d)\)', r'\1', char)
        c = ""; subchar = ""
        for v in char:
            c+= v
            try: x = c; subchar+= str(eval(x)); c = ""
            except: pass
        if subchar != '': txt+= subchar + "|"
    txt = txt[:-1].replace('+','')
    txt_result = "".join([ chr(int(n, 8)) for n in txt.split('|') ])
    return toStringCases(txt_result)
def toStringCases(txt_result):
    sum_base = ""
    m3 = False
    if ".toString(" in txt_result:
        if "+(" in  txt_result:
            m3 = True
            sum_base = "+"+find_single_match(txt_result,".toString...(\d+).")
            txt_pre_temp = find_multiple_matches(txt_result,"..(\d),(\d+).")
            txt_temp = [ (n, b) for b ,n in txt_pre_temp ]
        else:
            txt_temp = find_multiple_matches(txt_result, '(\d+)\.0.\w+.([^\)]+).')
        for numero, base in txt_temp:
            code = toString( int(numero), eval(base+sum_base) )
            if m3:
                txt_result = re.sub( r'"|\+', '', txt_result.replace("("+base+","+numero+")", code) )
            else:
                txt_result = re.sub( r"'|\+", '', txt_result.replace(numero+".0.toString("+base+")", code) )
    return txt_result
def toString(number,base):
    string = "0123456789abcdefghijklmnopqrstuvwxyz"
    if number < base:
        return string[number]
    else:
        return toString(number//base,base) + string[number%base]
def find_single_match(data,patron,index=0):
    try:
        matches = re.findall( patron , data , flags=re.DOTALL )
        return matches[index]
    except:
        return ""
def find_multiple_matches(text,pattern):
    return re.findall(pattern,text,re.DOTALL)
def get_eval_function(data,sPattern):
    r = re.search(sPattern, data, re.DOTALL + re.IGNORECASE)
    return r
def get_video_url(url):
    Urlo = ''
    video_urls = []
    hdr = {'Host': 'vidbm.com',
           'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:74.0) Gecko/20100101 Firefox/74.0',
           'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
           'Accept-Language': 'fr,fr-FR;q=0.8,en-US;q=0.5,en;q=0.3',
           'Accept-Encoding': 'gzip, deflate',
           'Connection': 'keep-alive',
           'Upgrade-Insecure-Requests': '1'}
    data = sgn.get(url,headers=hdr,verify=False).content
    sPattern = '''\ﾟω\ﾟ\ﾉ=(.+?)</script>'''
    code = get_eval_function(data,sPattern).group(1)
    code = decode1(code)
    if code:
        sPattern = '''file:"(.+?)",label:"(.+?)"'''
        code = get_eval_function(code,sPattern)
        a,b = code.group(1),code.group(2)
        b = b.replace('/','_')
        w = ('Cool_* vidbom [ '+b+' ]',a)
        video_urls.append(w)
    else:
        w = ('Ooops_* vidbom ','http://error')
        video_urls.append(w)
    return video_urls
#S1="https://www.vidbom.com/embed-wdjvucsc9wyf.html"
#print get_video_url(S1)
