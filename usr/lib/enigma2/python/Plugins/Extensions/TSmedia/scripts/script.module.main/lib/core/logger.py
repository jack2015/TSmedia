# Embedded file name: /usr/lib/enigma2/python/Plugins/Extensions/TSmedia/scripts/script.module.pelisresolver/lib/core/logger.py
import inspect
import os
import xbmc
from core import config
loggeractive = True

def log_enable(active):
    global loggeractive
    loggeractive = False


def encode_log(message = ''):
    if type(message) == unicode:
        message = message.encode('utf8')
    elif type(message) == str:
        message = unicode(message, 'utf8', errors='replace').encode('utf8')
    else:
        message = str(message)
    return message


def get_caller(message = None):
    module = inspect.getmodule(inspect.currentframe().f_back.f_back)
    if module is None:
        module = '.'.join(os.path.splitext(inspect.currentframe().f_back.f_back.f_code.co_filename.split('streamondemand')[1])[0].split(os.path.sep))[1:]
    else:
        module = module.__name__
    function = inspect.currentframe().f_back.f_back.f_code.co_name
    if module == '__main__':
        module = 'streamondemand'
    else:
        module = 'streamondemand.' + module
    if message:
        if module not in message:
            if function == '<module>':
                return module + ' ' + message
            else:
                return module + ' [' + function + '] ' + message
        else:
            return message
    else:
        if function == '<module>':
            return module
        return module + '.' + function
    return


def info(texto = ''):
    return
    if loggeractive:
        xbmc.log(get_caller(encode_log(texto)), xbmc.LOGNOTICE)


def debug(texto = ''):
    return
    if loggeractive:
        texto = '    [' + get_caller() + '] ' + encode_log(texto)
        xbmc.log('######## DEBUG #########', xbmc.LOGNOTICE)
        xbmc.log(texto, xbmc.LOGNOTICE)


def error(texto = ''):
    texto = '    [' + get_caller() + '] ' + encode_log(texto)
    xbmc.log('######## ERROR #########', xbmc.LOGERROR)
    xbmc.log(texto, xbmc.LOGERROR)
