import sys,os,json,io,ast
print "************************wsyspath-sending params to the host module*******************"
cParams=None
######################################

dpath=__file__.split("addons")[0]

def trace_error():
                  import sys,traceback
                  traceback.print_exc(file = sys.stdout)
                  traceback.print_exc(file=open(dpath+"/tmp/wTSmedia_log","w"))
          
######################################
Params=sys.argv[2]
if Params.startswith("'file_"):
         Params=Params.replace("'","").replace('"','')       
         filename=Params.split(",")[0]
         index=int(Params.split(",")[1])
         jfile=dpath+"/tmp/"+filename+".json"
         sys.argv=[]

         try:
             
             with io.open(jfile, 'r', encoding="utf8") as json_file:
                jdata = json.load(json_file)
                cParams=jdata[index]
                try:
                   name=cParams['name']
                   cParams.update({'name':name.encode("utf-8")})
                except:
                                   pass

                try:
                   desc=cParams['desc']
                   cParams.update({'desc':desc.encode("utf-8")})
                except:
                                   pass
                try:
                   url=cParams['Url']
                   cParams.update({'Url':url.encode("utf-8")})
                except:
                                   pass

                try:
                   url=cParams['url']
                   cParams.update({'url':url.encode("utf-8")})
                except:
                                   pass 

                                
                sys.argv=[]
                sys.argv.append(__file__)
                sys.argv.append("1")
                sys.argv.append(cParams)
              
         except:
              trace_error()
              print "wsyspath>>-failed to get json params,check error<<"
else:
    
    Params=Params[1:]
    Params=Params[:-1] 
    sys.argv=[]
    print "Params222",Params
    cParams=ast.literal_eval(Params)
    image=cParams.get('icon',"")
    cParams.update({"icon":image})
    sys.argv.append(__file__)
    sys.argv.append("1")
    sys.argv.append(cParams) 
log_file=dpath+"/tmp/Kodi_log"
log_file1=dpath+"/tmp/Kodi_log1"
xbmclog_file=dpath+"/tmp/TSmedia_log"

#############################################


from os import listdir as os_listdir
import sys
import os


scripts =dpath+"/scripts"

if "Kodi" in scripts:
       scripts=open(__file__.replace("wsyspath.py","appPath")).read()+"\scripts"
      
      
for name in os_listdir(scripts):
       if "script." in name:
               fold = scripts + "/" + name + "/lib"
               sys.path.append(fold)
#############################################
       

try:
    
    sys.argv[0]=sys.argv[0].replace("wsyspath.py","default.py")
    sys.modules["__main__"].__file__=sys.argv[0]

   
   
    if not isinstance(sys.argv[2],dict):

        sys.argv[2]=sys.argv[2].replace('"','')
    

              
    
     
    
    print "wsyspath>>params<<<"
    print "wsyspath:>>sent params-starting host module<<<",cParams
    section_id=cParams.get("csection_id","")
    if section_id=="TSiplayer":
        from default import TSIPHost
        tsi=TSIPHost()
        type=cParams.get("type","")
        resolver=cParams.get("resolver",None)
        need_resolve=cParams.get("need_resolve",None)
        print "resolver",resolver
        print "type",type
        print "need_resolve",need_resolve
        mode=cParams.get('mode',"00")
        cParams.update({"mode":mode})
 

        cimport=cParams.get("import","")
      
        cParams.update({"import":cimport})
        

        
        if type=="video":

           urltabs=tsi.get_links(cParams)
           
           for urltab in urltabs:
               title=urltab.get("title",'')
               title=urltab.get("name",title)
               urltab.update({"title":title})
               tsi.addDir(urltab)
           tsi.endHandleService(0,1)   
        elif need_resolve and need_resolve==1:
            if url.startswith("hst#"):
               url=url.split("#")[2]
            try:   
              urltabs=tsi.getVideos(url)

            except:
             url=cParams.get("url",None)
             
             if url :
                 from iTools import Item
                 item=Item()
                 
                 item.resolvehost("play",url)
                 
             urltabs=[]                              
            for urltab in urltabs:
                mode=int(urltab[1])
                
                url=urltab[0]
                host=tsi.getHostName(url)
                tsi.addDir({"title":host,"url":url,"mode":mode,'resolver':"iTools"})
            tsi.endHandleService(0,1)     
        elif resolver and resolver=="iTools":
             url=cParams.get("url",None)
             mode=cParams.get("mode",None)
             if not mode is None:
                 mode=int(mode)
             if url and mode is not None:
                 from iTools import Item
                 item=Item()
                 if mode==1:
                     item.resolvehost("play",url)
                 elif mode==0:
                      
                    item.addDir("play",url,0,"","",1)
              
             item.endDir()

            
                                
        else:   
           tsi.start(cParams)
        tsi.endHandleService(0,1)   
    else:
        from default import start
        try:
          
          start(cParams)#start(params)
        except:
               trace_error()
               start()
    
except:
    trace_error()

print """end processing"""

