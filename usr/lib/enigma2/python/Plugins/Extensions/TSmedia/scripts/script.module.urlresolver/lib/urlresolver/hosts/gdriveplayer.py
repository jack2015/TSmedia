# -*- coding: utf8 -*-
Agent = {'User-agent': 'Mozilla/5.0 (Windows NT 10.0; …) Gecko/20100101 Firefox/65.0'}
from binascii import unhexlify
from hashlib import md5
from Crypto.Cipher import AES
import requests,re,urllib2,json,base64
from jsunpack import unpack
def cryptoJS_AES_decrypt(encrypted, password, salt):
    def derive_key_and_iv(password, salt, key_length, iv_length):
        d = d_i = ''
        while len(d) < key_length + iv_length:
            d_i = md5(d_i + password + salt).digest()
            d += d_i
        return d[:key_length], d[key_length:key_length+iv_length]
    bs = 16
    key, iv = derive_key_and_iv(password, salt, 32, 16)
    cipher = AES.new(key= key, mode= AES.MODE_CBC,iv= iv)
    return cipher.decrypt(encrypted)
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
def get_video_url(url):
    #url = url.replace('embed-','')
    listServers= []
    request = urllib2.Request(url, None, Agent)
    data2 = urllib2.urlopen(request).read()
    if '(p,a,c,k,e,d)' in data2:
        data2 = get_packed_data(data2.strip())
    result = re.findall('data=.*?(\{.*?}).*?null.*?[\'"](.*?)[\'"]',data2, re.S)
    if result:
        code_ = json.loads(result[0][0])
        data1 = result[0][1].strip().replace('\\','')
        lst = re.compile("[A-Za-z]{1,}").split(data1)
        script = ''
        for elm in lst:
            script = script+chr(int(elm))
        result = re.findall('pass.*?[\'"](.*?)[\'"]',script, re.S)
        if result:
            pass_ = result[0]
            ciphertext = base64.b64decode(code_['ct'])
            iv = unhexlify(code_['iv'])
            salt = unhexlify(code_['s'])
            b = pass_
            decrypted = cryptoJS_AES_decrypt(ciphertext, pass_, salt)
            data2 = decrypted[1:-1]
            data2 = unpack(data2)
            url_list = re.findall('sources:(\[.*?\])',data2, re.S)
            data3= url_list[0]
            data3 = data3.replace('\\','').replace('"+countcheck+"','')
            src_lst = json.loads(data3)
            for elm in src_lst:
                _url   = elm['file']
                if _url.startswith('//'):_url = "https:"+_url
                _label = elm.get('label','Google')
                w = ('Cool_gdriveplayer ['+str(_label)+']',_url)
                listServers.append(w)
        else:
            w = ('Ooops_gdriveplayer','Error')
            listServers.append(w)
    else:
        w = ('Ooops_gdriveplayer','Error')
        listServers.append(w)
    return listServers
                
#S1 = "https://gdriveplayer.me/embed2.php?link=%2BlpQwhEF2owb8p433J4CUgLML3AZqZqP0n9P2kmfwpYY03LIt4a1TV411LztHCk%2FNrGVeXJUOLCQiTzzhflw6HCOWLERxowF9S3iqL0%2FZH2xz37CSt5dizXkNqdw4s9rEhO5zwhTZGCXXl3KII1hRvPKle%2FEZFo2EXl963qs3GKAx7kVWQsaYf0KaVuG%2FHtxg%3D"
#S2 = "https://gdriveplayer.me/embed2.php?link=fyh5C652fH%2BKp%2F831fW1eQHQnp1FThikzQsiSy4vtSQu2CD8T%2Bqgl%2B%2FliAAptHLmdlas%2FBW1nZl9lLQKY%2FtMfYoesSdq93STy64qjgAAK1xXrHCfDnGeow9iNx3FCRf7f3U%2BArcwLlf%2FETPzPJKKWNAmbIms5LK9AKlD7oZm1No8KqPhYaYD64MVh2Ac0ycBE%3D"
#S3 = "https://gdriveplayer.me/embed2.php?link=SoJJi0zgTDFDfPUDMz%252Bi9QhWT%252FSlMrB0c5%252FNUnEyb9tVyqqJoFxgotLxcUUUyu%252Bj98REwwvtVEe0WutlAmP6usLV57DxakUFF52W14h%252BcNUrDxU65%252BsxKXHqepCxkRMLzCkFKS3Aa%252BmG%252BRVsirXzFkRAmwQTJvvOjfvhDd4jOfH1jtp1Du%252FApdFMLIxQOGKR0%253D"
#print get_video_url(S1)
