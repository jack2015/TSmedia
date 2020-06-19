# Embedded file name: /usr/lib/enigma2/python/Plugins/Extensions/TSmedia/lib/syspath.py
import sys
import os
def checkproc(filename,proc):
    import ast
    def parse_ast(filename):
        with open(filename, "rt") as file:
            return ast.parse(file.read(), filename=filename)



    try:
        tree = parse_ast(filename)

        for func in (f for f in tree.body if isinstance(f, ast.FunctionDef)):
                
                 if proc== func.name:
                     
                     return True
        return False
    except:
        return False
def trace_error():
   
    import traceback
    try:
        #traceback.print_exc(file=sys.stdout)
        
        logfile = '/tmp/TSmedia_log'
        
        traceback.print_exc(file=open(logfile, 'a'))
    except:
        pass
scripts = '/usr/lib/enigma2/python/Plugins/Extensions/TSmedia/scripts'



try:
       for name in os.listdir(scripts):
              if "script." in name:
                      fold = scripts + "/" + name + "/lib"
                     
                      sys.path.append(fold)

      
except:
       pass



try:
       
    sys.argv[0]=sys.argv[0].replace("psyspath","default")
    try:
        sys.argv[2] = sys.argv[2].replace('AxNxD', '&').replace('ExQ', '=').strip()
    except:

        pass
    if checkproc(sys.argv[0],"start")==True:
       from default import start
       start()
    else:
       import default 
except:
    
    trace_error()
