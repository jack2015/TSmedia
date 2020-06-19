# -*- coding: utf-8 -*-
#!/usr/bin/env python
Agent = {'User-agent': 'Mozilla/5.0 (Windows NT 10.0; …) Gecko/20100101 Firefox/65.0'}
import urllib2
import re
def temp_decode(data):
    startpos = data.find('"\\""+') + 5
    endpos = data.find('"\\"")())()')
    first_group = data[startpos:endpos]
    l = re.search("(\(!\[\]\+\"\"\)\[.+?\]\+)", first_group, re.DOTALL)
    if l:
        first_group = first_group.replace(l.group(1), 'l').replace('$.__+', 't').replace('$._+', 'u').replace('$._$+', 'o')
        tmplist = []
        js = re.search('(\$={.+?});', data, re.DOTALL)
        if js:
            js_group = js.group(1)[3:][:-1]
            second_group = js_group.split(',')
            i = -1
            for x in second_group:
                a, b = x.split(':')
                if b == '++$':
                    i += 1
                    tmplist.append(("{}{}{}".format('$.', a, '+'), i))
                elif b == '(![]+"")[$]':
                    tmplist.append(("{}{}{}".format('$.', a, '+'), 'false'[i]))
                elif b == '({}+"")[$]':
                    tmplist.append(("{}{}{}".format('$.', a, '+'), '[object Object]'[i]))
                elif b == '($[$]+"")[$]':
                    tmplist.append(("{}{}{}".format('$.',a,'+'),'undefined'[i]))
                elif b == '(!""+"")[$]':
                    tmplist.append(("{}{}{}".format('$.', a, '+'), 'true'[i]))
            tmplist = sorted(tmplist, key=lambda x: x[1])
            for x in tmplist:
                first_group = first_group.replace(x[0], str(x[1]))
            first_group = first_group.replace(r'\\"' , '\\').replace("\"\\\\\\\\\"", "\\\\").replace('\\"', '\\').replace('"', '').replace("+", "")
    try:
        final_data = unicode(first_group, encoding = 'unicode-escape')
        return final_data
    except:
        return False
def find_single_match(data,patron,index=0):
    try:
        matches = re.findall( patron , data , flags=re.DOTALL )
        return matches[index]
    except:
        return ""
def get_video_url(url):
    listServers= []
    request = urllib2.Request(url, None, Agent)
    data2 = urllib2.urlopen(request).read()
    sPattern =  '([$]=.+?\(\)\)\(\);)'
    aResult = re.findall(sPattern, data2, re.DOTALL)
    if aResult:
        for i in aResult:
            decoded = temp_decode(i)
            #print decoded
            if decoded:
                r = re.search("setAttribute\(\'src\', *\'([^']+)\'\)", decoded, re.DOTALL)
                if r:
                    api_call = r.group(1)
                    w = ('Cool_Mystream',api_call)
                    listServers.append(w)
            else:
                w = ('Oops_Mystream','Error')
                listServers.append(w)
    else:
        w = ('Oops_Mystream','Error')
        listServers.append(w)
    return listServers
#url ="https://embed.mystream.to/qy30ud28dngj?Key=nOsmVoM4kFjvq084xlRTLQ&Expires=1587318637====https://mycima.vip/%d9%85%d8%b4%d8%a7%d9%87%d8%af%d8%a9-%d9%81%d9%8a%d9%84%d9%85-bad-trip-2020-%d9%85%d8%aa%d8%b1%d8%ac%d9%85/"
#print get_video_url(url)
