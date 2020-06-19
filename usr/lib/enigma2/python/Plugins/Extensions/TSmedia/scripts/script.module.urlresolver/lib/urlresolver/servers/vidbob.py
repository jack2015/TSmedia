#
import re
import jsbeautifier.unpackers.packer as packer
def get_video_url(url):
       
        list=[]
        from xbmctools import getnet,finddata
        data=getnet(url)
       
        
      
        regx='''file:"(.*?)m3u8"'''
        try:
                m3u8=re.findall(regx,data, re.M|re.I)[0]+'m3u8'
                list.append(('m3u8',m3u8))
                addDir('m3u8',m3u8,0,'','',1,link=True)
        except:
                            pass

        regx='''},{file:"(.*?)mp4"'''
        try:
                mp4=re.findall(regx,data, re.M|re.I)[0]+'mp4'
                list.append(('mp4',mp4))
                addDir('mp4',mp4,0,'','',1,link=True)
        except:
                            pass
        print "list",list
        
        return list
        Pre_Stream_URL = re.search('file:"(.*)"', unpack).group(1)
        print 'Pre_Stream_URL1',Pre_Stream_URL
        Pre_Stream_URL = re.search('file:"(.*)",label', unpack).group(1)
        
        print 'Pre_Stream_URL2',Pre_Stream_URL
        sys.exit(0)
        return Pre_Stream_URL        
       





