#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright (c) 2011 Benoit HERVIER <khertan@khertan.net>
# Licenced under GPLv3

## This program is free software; you can redistribute it and/or modify
## it under the terms of the GNU General Public License as published
## by the Free Software Foundation; version 3 only.
##
## This program is distributed in the hope that it will be useful,
## but WITHOUT ANY WARRANTY; without even the implied warranty of
## MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
## GNU General Public License for more details.

from PySide.QtGui import QApplication
from PySide.QtCore import QUrl, Slot, QObject, Property, Signal
from PySide import QtDeclarative
from PySide.QtOpenGL import QGLWidget

import threading
import sys
import os
import markdown2
import re
import htmlentitydefs
try:
  from pygments import highlight
  from pygments.formatters import HtmlFormatter
  from pygments.lexers import get_lexer_for_filename
  from pygments.util import ClassNotFound
except:
  pass
  
import ConfigParser

__author__ = 'Benoit HERVIER (Khertan)'
__email__ = 'khertan@khertan.net'
__version__ = '0.4.2'

class Settings(QObject):
    '''Config object'''
    
    def __init__(self,):
        QObject.__init__(self,)
        self.config = ConfigParser.ConfigParser()
        if not os.path.exists(os.path.expanduser('~/.khtsimpletext.cfg')):
            self._write_default()
        else:
            self.config.read(os.path.expanduser('~/.khtsimpletext.cfg'))

    def _write_default(self):
        ''' Write the default config'''
        self.config.add_section('Display')
        self.config.set('Display', 'syntaxhighlighting', 'True')
        self.config.set('Display', 'textwrap', 'True')
        self.config.set('Display', 'fontsize', '18')
        self.config.set('Display', 'fontfamily', 'Nokia Pure Text')

        # Writing our configuration file to 'example.cfg'
        with open(os.path.expanduser('~/.khtsimpletext.cfg'), 'wb') as configfile:
            self.config.write(configfile)
    
    @Slot(unicode, result=unicode)
    def get(self,option):
        try:
            return self.config.get('Display',option)
        except:
            return ''
    
    def _get_textWrap(self,):
        return (self.get('textwrap').lower() == 'true')
    def _get_fontSize(self,):
        return int(self.get('fontsize'))
    def _get_fontFamily(self,):
        return self.get('fontfamily')
    def _get_syntaxHighlighting(self,):
        return (self.get('syntaxhighlighting').lower() == 'True')
        
    on_textWrap = Signal()
    on_fontSize = Signal()
    on_fontFamily = Signal()
    on_syntaxHighlighting = Signal()
    textWrap = Property(bool, _get_textWrap, notify=on_textWrap)
    fontSize = Property(int, _get_fontSize, notify=on_fontSize)
    fontFamily = Property(unicode, _get_fontFamily, notify=on_fontFamily)
    syntaxHighlighting = Property(bool, _get_syntaxHighlighting, notify=on_syntaxHighlighting)
    
class Document(QObject):
   '''Represent the text document'''

   def __init__(self,):
       QObject.__init__(self,)
       self._text = u''
       self._modified = False
       self._colored = False
       self._filepath = u''
       self._ready = False

   @Slot(unicode)
   def load(self,path):
       ''' Load the document from a path in a thread'''
       print 'def load:' + path
       self._set_ready(False)
#       self.thread = threading.Thread(target=self._load, args= (path, ))
#       self.thread.start()
       self._load(path)

   def _load(self,path):
        ''' Load the document from a path '''
        self.filepath = QUrl(path).path()
        print 'def _load:'+self.filepath
        try:
          with open(self.filepath, 'rb') as fh:
            try:
                text = unicode(fh.read(),'utf-8')
                if (Settings.syntaxHighlighting):
                    self._colorIt(text)
                else:
                    self._set_text(text)
                self._set_ready(True)
            except Exception, e:
                print e
                self._set_text('')
                self.on_error.emit(str(e))
                self._set_ready(True)
        except Exception, e:
          self._set_text('')
          self._set_ready(True)
          print e


   def _colorIt(self, text):
     ''' Syntax highlight a text in html'''
     try:
       lexer =  get_lexer_for_filename(self.filepath)
       if lexer == None:
            self._set_text(text)
            self._set_colored(False)
            return
       self._set_text(highlight(text, lexer, HtmlFormatter(full=True)))
       self._set_colored(True)
     except ClassNotFound:
       self._set_text(text)
       self._set_colored(False)
     except Exception, e:
       print e
       self.on_error.emit(str(e))
       self._set_text(text)
       self._set_colored(False)

   def _unescape(self,text):
     def fixup(m):
        text = m.group(0)
        if text[:2] == "&#":
            # character reference
            try:
                if text[:3] == "&#x":
                    return unichr(int(text[3:-1], 16))
                else:
                    return unichr(int(text[2:-1]))
            except ValueError, e:
                print e
        else:
            # named entity
            try:
                text = unichr(htmlentitydefs.name2codepoint[text[1:-1]])
            except KeyError, e:
                print e
        return text # leave as is
     return re.sub("&#?\w+;", fixup, text)

   @Slot(unicode, result=unicode)
   def recolorIt(self, text):
      ''' ReHighlight a text '''
      return self._colorIt(self._stripTags(text))

   @Slot(unicode, result=unicode)
   def previewMarkdown(self, text):
       ''' Generate a markdown preview'''
       try:
           return markdown2.markdown(self._stripTags(text))
       except:
           return text

   def _stripTags(self,content):
      ''' Remove html text formating from a text'''
      from BeautifulSoup import BeautifulSoup
      plainText = self._unescape(''.join(BeautifulSoup(content).body(text=True)))
      if (plainText.startswith('\n')):
        return plainText[1:]
      return plainText

   @Slot(unicode)
   def write(self, data):
       ''' Write the document to a file '''
       if self._colored:
          print data
          data = self._stripTags(data)


       try:
           with open(self.filepath, 'wb') as fh:
               fh.write(data.encode('utf-8'))
       except Exception, e:
           print e
           self.on_error.emit(str(e))

   def _get_text(self):
       return self._text
   def _set_text(self, text):
       self._text = text
       self.on_text.emit()
       print 'def _set_text:' + text.split('\n')[0]

   def _get_colored(self):
       return self._colored
   def _set_colored(self, b):
       self._colored = b
       self.on_colored.emit()
       print 'def _set_colored:' + str(b)

   def _get_ready(self):
       return self._ready
   def _set_ready(self, b):
       self._ready = b
       self.on_ready.emit()
       
       
   on_text = Signal()
   on_error = Signal(unicode)
   on_colored = Signal()
   on_ready = Signal()
   text = Property(unicode, _get_text, _set_text, notify=on_text)
   colored = Property(bool, _get_colored, _set_colored, notify=on_colored)
   ready = Property(bool, _get_ready, _set_ready, notify=on_ready)

class QmlDirReaderWriter(QObject):
   ''' A class for manipulating file and directory from Qml'''
   def __init__(self, ):
       QObject.__init__(self)

   @Slot(unicode,result=bool)
   def newFolder(self,path):
       ''' Create a new folder '''
       try:
           path = QUrl(path).path()
           os.makedirs(path)
           return True
       except:
          return False

   @Slot(unicode,unicode,unicode,result=bool)
   def rename(self,pathdir,oldname,newname):
       ''' Rename an existing file '''
       try:
           pathdir = os.path.dirname(QUrl(pathdir).path())
           #oldpath = QUrl(oldname).path()
           #newpath = QUrl(newname).path()
           os.rename(os.path.join(pathdir, oldname),os.path.join(pathdir, newname))
           return True
       except:
          return False

   @Slot(unicode,unicode,result=bool)
   def mv(self,oldpath,newpath):
       ''' Move a file to another folder '''
       try:
           import shutil
           oldpath = QUrl(oldpath).path()
           newpath = QUrl(newpath).path()
           shutil.move( oldpath, newpath)
           return True
       except:
          return False

   @Slot(unicode,unicode,result=bool)
   def cp(self,oldpath,newpath):
       ''' Copy a file '''
       try:
           import shutil
           oldpath = QUrl(oldpath).path()
           newpath = QUrl(newpath).path()
           shutil.copy2( oldpath, newpath)
           return True
       except:
          return False

   @Slot(unicode,result=bool)
   def rm(self,path):
       ''' Delete a file or a folder '''
       try:
           path = QUrl(path).path()
           if os.path.isdir(path):
                import shutil
                shutil.rmtree(path)
           else:
                os.remove(path)
           return True
       except Exception, e:
          print e
          return False



class KhtSimpleText(QApplication):
    ''' Application class '''
    def __init__(self):
        QApplication.__init__(self, sys.argv)
        self.setOrganizationName("Khertan Software")
        self.setOrganizationDomain("khertan.net")
        self.setApplicationName("KhtSimpleText")

        self.view = QtDeclarative.QDeclarativeView()
        self.glw = QGLWidget()
        self.view.setViewport(self.glw)
        self.aDocument = Document() 
        self.rootContext = self.view.rootContext()
        self.rootContext.setContextProperty("argv", sys.argv)
        self.rootContext.setContextProperty("__version__", __version__)
        self.rootContext.setContextProperty("Settings", Settings())
        self.rootContext.setContextProperty("QmlDirReaderWriter", QmlDirReaderWriter())
        self.rootContext.setContextProperty('Document', self.aDocument)
        self.view.setSource(QUrl.fromLocalFile(
                os.path.join(os.path.dirname(__file__), 'qml',  'main.qml')))
        self.rootObject = self.view.rootObject()
        self.aDocument.on_error.connect(self.rootObject.onError)
        self.view.showFullScreen()

if __name__ == '__main__':
    sys.exit(KhtSimpleText().exec_())  
