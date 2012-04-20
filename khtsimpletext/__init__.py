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

import threading
import sys
import os
import markdown2
import re
import htmlentitydefs
from pygments import highlight
from pygments.formatters import HtmlFormatter
from pygments.lexers import get_lexer_for_filename
from pygments.utils import ClassNotFound
import ConfigParser

__author__ = 'Benoit HERVIER (Khertan)'
__email__ = 'khertan@khertan.net'
__version__ = '0.4.1'

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
       print 'Loading %s' % path
       self._set_ready(False)
       self.thread = threading.Thread(target=self._load, args= (path, ))
       self.thread.start()


   def _load(self,path):
        print 'Thread started'
        self.filepath = QUrl(path).path()
        try:
          with open(self.filepath, 'rb') as fh:
            try:
                if (Settings.syntaxHighlighting):
                    self._colorIt(unicode(fh.read(), 'utf-8'))
                else:
                    self._set_text(unicode(fh.read(), 'utf-8'))
                self._set_ready(True)
            except Exception, e:
                print e
                self.on_error.emit(str(e))
                self._set_ready(True)
        except:
          self._text = u''
          self._set_ready(True)


   def _colorIt(self, text):
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
            except ValueError:
                pass
        else:
            # named entity
            try:
                text = unichr(htmlentitydefs.name2codepoint[text[1:-1]])
            except KeyError:
                pass
        return text # leave as is
     return re.sub("&#?\w+;", fixup, text)

   @Slot(unicode, result=unicode)
   def recolorIt(self, text):
      return self._colorIt(self._stripTags(text))

   @Slot(unicode, result=unicode)
   def previewMarkdown(self, text):
       try:
           return markdown2.markdown(self._stripTags(text))
       except:
           return text

   def _stripTags(self,content):
      from BeautifulSoup import BeautifulSoup
      plainText = self._unescape(''.join(BeautifulSoup(content).body(text=True)))
      if (plainText.startswith('\n')):
        return plainText[1:]
      return plainText

   @Slot(unicode)
   def write(self, data):
       if self._colored:
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

   def _get_colored(self):
       return self._colored
   def _set_colored(self, b):
       self._colored = b
       self.on_colored.emit()

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

   def __init__(self, ):
       QObject.__init__(self)

   @Slot(unicode,result=bool)
   def newFolder(self,path):
       try:
           path = QUrl(path).path()
           os.makedirs(path)
           return True
       except:
          return False

   @Slot(unicode,unicode,unicode,result=bool)
   def rename(self,pathdir,oldname,newname):
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

    def __init__(self):
        QApplication.__init__(self, sys.argv)
        self.setOrganizationName("Khertan Software")
        self.setOrganizationDomain("khertan.net")
        self.setApplicationName("KhtSimpleText")

        self.view = QtDeclarative.QDeclarativeView()
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
