import re
import jsbeautifier.unpackers.packer as packer
def get_video_url(url):
       
        list=[]
        from xbmctools import getnet,finddata
        data=getnet(url)
       
        regx='''<script type="text/javascript"(.*)</script>'''
        #print "jucie",_filter(data)
        #print"data1", data
        data2 =finddata(data.replace("\n",""),'eval(','</script')

       
        
        unpack = packer.unpack(data2)
        print 'unpack',unpack
       
        regx='''http://(.*?)mkv'''
       
        

        try:
                link='http://'+re.findall(regx,unpack, re.M|re.I)[0]+'mkv'
                
        except:
                regx='''http://(.*?)mp4'''
                link='http://'+re.findall(regx,unpack, re.M|re.I)[0]+'mp4'
        
        print 'link',link
        
        return link 
