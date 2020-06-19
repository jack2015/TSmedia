# -*- coding: utf-8 -*-
#!/usr/bin/env python
import re
import base64
from base64 import b64encode, b64decode
from jjdecode import *
class strwithmeta(str):
    def __new__(cls,value,meta={}):
        obj = str.__new__(cls, value)
        obj.meta = {}
        if isinstance(value, strwithmeta):
            obj.meta = dict(value.meta)
        else:
            obj.meta = {}
        obj.meta.update(meta)
        return obj
class cParser:
    def parseSingleResult(self, sHtmlContent, sPattern):     
        aMatches = re.compile(sPattern).findall(sHtmlContent)
        if (len(aMatches) == 1):
            aMatches[0] = self.__replaceSpecialCharacters(aMatches[0])
            return True, aMatches[0]
        return False, aMatches
    def __replaceSpecialCharacters(self, sString):
        return sString.replace('\\/','/').replace('&amp;','&').replace('\xc9','E').replace('&#8211;', '-').replace('&#038;', '&').replace('&rsquo;','\'').replace('\r','').replace('\n','').replace('\t','').replace('&#039;',"'").replace('&quot;','"').replace('&gt;','>').replace('&lt;','<').replace('&nbsp;','')
    def parse(self, sHtmlContent, sPattern, iMinFoundValue = 1):
        sHtmlContent = self.__replaceSpecialCharacters(str(sHtmlContent))
        aMatches = re.compile(sPattern, re.IGNORECASE).findall(sHtmlContent)
        if (len(aMatches) >= iMinFoundValue):                
            return True, aMatches
        return False, aMatches
    def replace(self, sPattern, sReplaceString, sValue):
         return re.sub(sPattern, sReplaceString, sValue)
    def escape(self, sValue):
        return re.escape(sValue)
    def getNumberFromString(self, sValue):
        sPattern = "\d+"
        aMatches = re.findall(sPattern, sValue)
        if (len(aMatches) > 0):
            return aMatches[0]
        return 0
    def titleParse(self, sHtmlContent, sPattern):
        sHtmlContent = self.__replaceSpecialCharacters(str(sHtmlContent))
        aMatches = re.compile(sPattern, re.IGNORECASE)
        try: 
            [m.groupdict() for m in aMatches.finditer(sHtmlContent)]              
            return m.groupdict()
        except:
            return {'title': sHtmlContent}
    def abParse(self,sHtmlContent,start,end,startoffset=''):
        #usage oParser.abParse(sHtmlContent,"start","end")
        #startoffset (int) décale le début pour ne pas prendre en compte start dans le résultat final si besoin
        #usage2 oParser.abParse(sHtmlContent,"start","end",6)
        #ex youtube.py
        if startoffset:
            return sHtmlContent[startoffset + sHtmlContent.find(start):sHtmlContent.find(end)]
        else:
            return sHtmlContent[sHtmlContent.find(start):sHtmlContent.find(end)]
def decode22(urlcoded,a,b,c):
	TableauTest = {}
	key = ''
	l = a
	n = "0123456789"
	h = b
	j = 0
	while j < len(l) :
		k = 0
		while k < len(n):
			TableauTest[l[j] + n[k]] = h[int(j + k)]
			k+=1
		j+=1
	hash = c
	i = 0
	while i < len(hash):
		key = key + TableauTest[hash[i] + hash[i + 1]]
		i+= 2
	chain = base64.b64decode(urlcoded)
	secretKey = {}
	y = 0
	temp = ''
	url = ""
	x = 0
	while x < 256:
		secretKey[x] = x
		x += 1
	x = 0
	while x < 256:
		y = (y + secretKey[x] + ord(key[x % len(key)])) % 256
		temp = secretKey[x]
		secretKey[x] = secretKey[y]
		secretKey[y] = temp
		x += 1
	x = 0
	y = 0
	i = 0
	while i < len(chain):
		x += 1 % 256
		y = (y + secretKey[x]) % 256
		temp = secretKey[x]
		secretKey[x] = secretKey[y]
		secretKey[y] = temp
		url = url + (chr(ord(chain[i]) ^ secretKey[(secretKey[x] + secretKey[y]) % 256]))
		i += 1
	return url
def Cdecode(sHtmlContent,encodedC):
	oParser = cParser()
	sPattern =  '<([0-9a-zA-Z]+)><script>([^<]+)<\/script>'
	aResult = oParser.parse(sHtmlContent, sPattern)
	print "========000000000=========",aResult[0]
	z = []
	y = []
	if (aResult[0] == True):
		for aEntry in aResult[1]:
			print "yyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyy===============",JJDecoder(aEntry[1]).decode()
			z.append(JJDecoder(aEntry[1]).decode())
			#print "ZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZ********************************",z
			#z.append(aEntry[1])
		#######VSlog(z)
		for x in z:
			r1 = re.search("atob\(\'([^']+)\'\)", x, re.DOTALL | re.UNICODE)
			print "R1R1R1R1R1R1R1R1R1R1R1R1R1R1////////////////______",r1.group(1)
			if r1:
				y.append(base64.b64decode(r1.group(1)))
				print "YYYYYYYYYYYYYYYYYYYYYYYYYYYYY===============",y
		for w in y:
			print "WWWWWWWWWWW==============",w
			N =w.split('|')
			print "NNNNNNNNNNNNNNNNNN===============",N
			return N[1]
			# print "encodedCencodedCencodedCencodedCencodedC***",encodedC
			# #r2 = re.search(encodedC + "|", w)
			# r2 = re.search(encodedC + "='([^']+)'", w, re.DOTALL | re.UNICODE)
			# print "r2r2r2r2r2r2r2r2r2r2r2r2r2r2===============",r2
			# if r2:
			    # print "coucoucoucou====="
			    # return "o4d4c1r6b0g9j8m0y7x6w9e2"#r2.group(1)
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
