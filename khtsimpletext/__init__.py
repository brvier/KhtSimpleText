#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright (c) 2011 Benoît HERVIER
# Licenced under GPLv3

from PySide.QtGui import QApplication
from PySide.QtCore import QUrl, QDir, Slot, QObject
from PySide import QtDeclarative

import sys
import os.path

__author__ = 'Benoît HERVIER (Khertan)'
__email__ = 'khertan@khertan.net'
__version__ = '0.2.0'

class QmlFileReaderWriter(QObject):

   @Slot(unicode, result=unicode)
   def read(self,path):
       print QUrl(path).path()
       with open(QUrl(path).path(), 'rb') as fh:
           return unicode(fh.read(), 'utf-8')
       return u''

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
