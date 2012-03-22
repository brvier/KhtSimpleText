#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright (c) 2011 Benoît HERVIER <khertan@khertan.net>
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
from PySide.QtCore import QUrl, QDir, Slot, QObject
from PySide import QtDeclarative

import sys
import os

__author__ = 'Benoît HERVIER (Khertan)'
__email__ = 'khertan@khertan.net'
__version__ = '0.3.0'

class QmlFileReaderWriter(QObject):

   @Slot(unicode, result=unicode)
   def read(self,path):
       print QUrl(path).path()
       with open(QUrl(path).path(), 'rb') as fh:
           return unicode(fh.read(), 'utf-8')
       return u''

   @Slot(unicode,result=bool)
   def newFolder(self,path):
       try:
           path = QUrl(path).path()
           os.makedirs(path)
           return True
       except:
          return False       

   @Slot(unicode,unicode,result=bool)
   def rename(self,oldpath,newpath):
       try:
           oldpath = QUrl(oldpath).path()
           newpath = QUrl(newpath).path()
           os.rename(oldpath,newpath)
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

   @Slot(unicode, unicode)
   def write(self, path, data):
       with open(QUrl(path).path(), 'wb') as fh:
           fh.write(data.encode('utf-8'))

class KhtSimpleText(QApplication):

    def __init__(self):
        QApplication.__init__(self, sys.argv)
        self.setOrganizationName("Khertan Software")
        self.setOrganizationDomain("khertan.net")
        self.setApplicationName("KhtSimpleText")

        self.view = QtDeclarative.QDeclarativeView()
        self.view.rootContext().setContextProperty("argv", sys.argv)
        self.view.rootContext().setContextProperty("__version__", __version__)
        
        aQmlFileReaderWriter = QmlFileReaderWriter()
        self.view.rootContext().setContextProperty("QmlFileReaderWriter", aQmlFileReaderWriter)
        self.view.setSource(QUrl.fromLocalFile(
                os.path.join(os.path.dirname(__file__), 'qml',  'main.qml')))
        self.view.showFullScreen()

if __name__ == '__main__':
    sys.exit(KhtSimpleText().exec_())
