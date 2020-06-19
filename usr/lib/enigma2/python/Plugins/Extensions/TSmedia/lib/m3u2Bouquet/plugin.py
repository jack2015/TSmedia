# Embedded file name: /usr/lib/enigma2/python/Plugins/Extensions/TSmedia/screens/tools/m3u2Bouquet/plugin.py
from Components.ActionMap import ActionMap
from Screens.MessageBox import MessageBox
from Tools.Directories import fileExists
from GlobalActions import globalActionMap
from keymapparser import readKeymap, removeKeymap
from os import environ
from Plugins.Plugin import PluginDescriptor
from Screens.Screen import Screen
from Components.Console import Console as iConsole
from Components.Language import language
from Components.config import config, getConfigListEntry, ConfigText, ConfigInteger, ConfigSubsection, configfile, ConfigSelection, ConfigPassword, NoSave
from Components.ConfigList import ConfigListScreen
from Tools.Directories import resolveFilename, SCOPE_PLUGINS, SCOPE_LANGUAGE
from Components.Sources.StaticText import StaticText
from Tools import Notifications
import os
import gettext
from os import environ
lang = language.getLanguage()
environ['LANGUAGE'] = lang[:2]
gettext.bindtextdomain('enigma2', resolveFilename(SCOPE_LANGUAGE))
gettext.textdomain('enigma2')
gettext.bindtextdomain('m2b', '%s%s' % (resolveFilename(SCOPE_PLUGINS), 'Extensions/m2b/locale/'))

def _(txt):
    t = gettext.dgettext('m2b', txt)
    if t == txt:
        t = gettext.gettext(txt)
    return t

dlocation=config.TSmedia.downloadlocation.value 
m2uPath=dlocation+"/TSmedia/iptv/"
def get_m3u_name():
    m3u_name = []
   
    try:
        dlocation=config.TSmedia.downloadlocation.value 
        m2uPath=dlocation+"/TSmedia/iptv/"
        if os.path.exists(m2uPath)==False:
           m2uPath="/media/hdd/TSmedia/iptv/" 
        dirs = os.listdir(m2uPath)
        for m3u_file in dirs:
            if m3u_file.endswith('.m3u'):
               
                    m3u_name.append(m3u_file)
                    
        if len(m3u_name)==0:
           m3u_name.append("No m3u files")
           
       
        return m3u_name
    except:
        m3u_name.append("code error")
        return m3u_name

def remove_line(filename, what):
    if os.path.isfile(filename):
        file_read = open(filename).readlines()
        file_write = open(filename, 'w')
        for line in file_read:
            if what not in line:
                file_write.write(line)

        file_write.close()


config.plugins.m2b = ConfigSubsection()
config.plugins.m2b.m3ufile = ConfigSelection(choices=get_m3u_name())
config.plugins.m2b.type = ConfigSelection(default='Gstreamer', choices=[('Gstreamer', _('Gstreamer')),
 ('LiveStreamerhls', _('LiveStreamer/hls')),
 ('LiveStreamerhlsvariant', _('LiveStreamer/hlsvariant')),
 ('Multicast', _('Multicast'))])
config.plugins.m2b.passw = ConfigPassword(default='', visible_width=50, fixed_size=False)

class TSmediam2b_setup(ConfigListScreen, Screen):

    def __init__(self, session,m3uFile=None):
        self.session = session
        Screen.__init__(self, session)
        self.skin = 'TSmediam2b_setup'
        self.setTitle(_('m3u/xml bouquet converter'))
        config.plugins.m2b.m3ufile = ConfigSelection(choices=get_m3u_name())
        if  m3uFile:
            config.plugins.m2b.m3ufile.value=m3uFile
            config.plugins.m2b.m3ufile.save()
        self.list = []
        self.converted=False
        self.list.append(getConfigListEntry(_('select m3u file from %s'%str(config.plugins.m2b.m3ufile.value)), config.plugins.m2b.m3ufile))
        self.list.append(getConfigListEntry(_('Select type'), config.plugins.m2b.type))
        self.list.append(getConfigListEntry(_('Input password (if needed)'), config.plugins.m2b.passw))
        ConfigListScreen.__init__(self, self.list, session=session)
        self['key_red'] = StaticText(_('Close'))
        self['key_green'] = StaticText(_('Convert'))
        self['setupActions'] = ActionMap(['SetupActions', 'ColorActions', 'EPGSelectActions'], {'red': self.cancel,
         'cancel': self.cancel,
         'green': self.convert,
         'ok': self.convert}, -2)


             
    def cancel(self):
        config.plugins.m2b.passw.save()
         
        
        config.save()
        if self.converted==True:
           self.session.openWithCallback(self.close, get_chlist)
        else:
            self.close()
    def convert(self):
        config.plugins.m2b.passw.save()
        config.plugins.m2b.type.save()
        config.plugins.m2b.m3ufile.save()
        config.save()
        
        
        self.session.openWithCallback(self.convertback,create_bouquet)
    def convertback(self,success=False):
        if success==True:
           self.converted=True 
        else:
           self.converted=False 
SKIN_DWN = '\n<screen name="get_chlist" position="center,140" size="625,35" title="Please wait">\n  <widget source="status" render="Label" position="10,5" size="605,22" zPosition="2" font="Regular; 20" halign="center" transparent="2" />\n</screen>'

class create_bouquet(Screen):

    def __init__(self, session, args = None):
        Screen.__init__(self, session)
        self.session = session
        self.skin = SKIN_DWN
        BFNAME = 'userbouquet.%s.tv' % config.plugins.m2b.m3ufile.value
        self.setTitle(_('Converting,Please wait'))
        self['status'] = StaticText()
        self.iConsole = iConsole()
        self.success=False
        self['status'].text = _('Converting %s' % config.plugins.m2b.m3ufile.value)
        desk_tmp = hls_opt = ''
        in_bouquets = 0
        self['setupActions'] = ActionMap(['SetupActions', 'ColorActions', 'EPGSelectActions'], {'red': self.cancel,
         'cancel': self.cancel,         
         'ok': self.cancel}, -2)

       

        self.converting=True
        if os.path.exists(m2uPath+config.plugins.m2b.m3ufile.value):
            try:
                    print config.plugins.m2b.type.value
                    if os.path.isfile('/etc/enigma2/%s' % BFNAME):
                        os.remove('/etc/enigma2/%s' % BFNAME)
                    if config.plugins.m2b.type.value is 'LiveStreamerhls':
                        hls_opt = 'hls'
                    elif config.plugins.m2b.type.value is 'LiveStreamerhlsvariant':
                        hls_opt = 'hlsvariant'
                    with open('/etc/enigma2/%s' % BFNAME, 'w') as outfile:
                        
                            outfile.write('#NAME %s\r\n' % config.plugins.m2b.m3ufile.value.capitalize())
                            for line in open(m2uPath+config.plugins.m2b.m3ufile.value):
                                print 'linexx', line
                                if line.startswith('http://') or line.startswith('rtmp://'):
                                    if config.plugins.m2b.type.value is 'LiveStreamerhls' or config.plugins.m2b.type.value is 'LiveStreamerhlsvariant':
                                        outfile.write('#SERVICE 1:0:1:1:0:0:0:0:0:0:http%%3a//127.0.0.1%%3a88/%s%%3a//%s' % (hls_opt, line.replace(':', '%3a')))
                                    elif config.plugins.m2b.type.value is 'Gstreamer':
                                        outfile.write('#SERVICE 4097:0:1:1:0:0:0:0:0:0:%s' % line.replace(':', '%3a'))
                                    elif config.plugins.m2b.type.value is 'Multicast':
                                        outfile.write('#SERVICE 1:0:1:1:0:0:0:0:0:0:%s' % line.replace(':', '%3a'))
                                    outfile.write('#DESCRIPTION %s' % desk_tmp)
                                elif line.startswith('#EXTINF'):
                                    desk_tmp = '%s' % line.split(',')[-1]
                                elif '<stream_url><![CDATA' in line:
                                    if config.plugins.m2b.type.value is 'LiveStreamerhls' or config.plugins.m2b.type.value is 'LiveStreamerhlsvariant':
                                        outfile.write('#SERVICE 1:0:1:1:0:0:0:0:0:0:http%%3a//127.0.0.1%%3a88/%s%%3a//%s\r\n' % (hls_opt, line.split('[')[-1].split(']')[0].replace(':', '%3a')))
                                    elif config.plugins.m2b.type.value is 'Gstreamer':
                                        outfile.write('#SERVICE 4097:0:1:1:0:0:0:0:0:0:%s\r\n' % line.split('[')[-1].split(']')[0].replace(':', '%3a'))
                                    elif config.plugins.m2b.type.value is 'Multicast':
                                        outfile.write('#SERVICE 1:0:1:1:0:0:0:0:0:0:%s\r\n' % line.split('[')[-1].split(']')[0].replace(':', '%3a'))
                                    outfile.write('#DESCRIPTION %s\r\n' % desk_tmp)
                                elif '<title>' in line:
                                    if '<![CDATA[' in line:
                                        desk_tmp = '%s\r\n' % line.split('[')[-1].split(']')[0]
                                    else:
                                        desk_tmp = '%s\r\n' % line.split('<')[1].split('>')[1]

                            outfile.close()

                            
                    if os.path.isfile('/etc/enigma2/bouquets.tv'):
                        for line in open('/etc/enigma2/bouquets.tv'):
                            if BFNAME in line:
                                in_bouquets = 1

                        if in_bouquets is 0:
                            if os.path.isfile('/etc/enigma2/%s' % BFNAME) and os.path.isfile('/etc/enigma2/bouquets.tv'):
                                remove_line('/etc/enigma2/bouquets.tv', BFNAME)
                                remove_line('/etc/enigma2/bouquets.tv', 'LastScanned')
                                with open('/etc/enigma2/bouquets.tv', 'a') as outfile:
                                    outfile.write('#SERVICE 1:7:1:0:0:0:0:0:0:0:FROM BOUQUET "%s" ORDER BY bouquet\r\n' % BFNAME)
                                    outfile.write('#SERVICE 1:7:1:0:0:0:0:0:0:0:FROM BOUQUET "userbouquet.LastScanned.tv" ORDER BY bouquet\r\n')
                                    outfile.close()

                        self['status'].text = _('m3u converted to %s'%str(config.plugins.m2b.m3ufile.value)+" bouquet")
                        self.success=True
                        
                        
                        self.converting=False 
                        self.iConsole.ePopen('sleep 3', self.cancel)
                        self.setTitle(_('Finished'))
                        
                                  
                    else:
                         self['status'].text = _('Not Found m3u file')
                         self.converting=False 
                         self.success=False
                        
                        
                    
                    

                    
                    #mymess=_("m3u converted successfully to %s"%str(config.plugins.m2b.m3ufile.value))
                    #Notifications.AddPopup(text=mymess, type=MessageBox.TYPE_INFO, timeout=3, id='success')

            except:
                self['status'].text = _('Failed to convert m3u file')
                self.success=False
                self.converting=False
                self.setTitle(_('Finished'))
                
                #Notifications.AddPopup(text=_('Failed to convert m3u file'), type=MessageBox.TYPE_INFO, timeout=3, id='failed')
                #self.close()
        else:
                self['status'].text = _('m3u file not found')
                self.success=False
                self.converting=False
                self.setTitle(_('Finished'))
                
    def cancel(self, result=None, retval=None, extra_args=[]):
        if self.converting==False:
           self.close(self.success)


class get_chlist(Screen):

    def __init__(self, session, args = None):
        Screen.__init__(self, session)
        self.session = session
        self.skin = SKIN_DWN
        self.setTitle(_('Please wait'))
        self['status'] = StaticText()
        self.iConsole = iConsole()
        self['status'].text = _('Reload servicelist')
        if config.plugins.m2b.passw.value is not '':
            config.plugins.m2b.passw.value = ':' + config.plugins.m2b.passw.value
        self.iConsole.ePopen('wget -q -O - http://root%s@127.0.0.1/web/servicelistreload?mode=0 && sleep 2' % config.plugins.m2b.passw.value, self.quit)

    def quit(self, result, retval, extra_args):
        config.plugins.m2b.passw.value = config.plugins.m2b.passw.value.lstrip(':')
        self.close(False)


def main(session, **kwargs):
    session.open(m2b_setup)


def Plugins(**kwargs):
    list = [PluginDescriptor(name=_('m3u/xml bouquet converter'), description=_('m3u to bouquet converter'), where=[PluginDescriptor.WHERE_PLUGINMENU], icon='m2b.png', fnc=main)]
    list.append(PluginDescriptor(name=_('m3u/xml bouquet converter'), description=_('m3u to bouquet converter'), where=[PluginDescriptor.WHERE_EXTENSIONSMENU], fnc=main))
    return list
