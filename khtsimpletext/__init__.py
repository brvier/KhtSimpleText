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
from PySide.QtOpenGL import QGLWidget, QGLFormat
import sys
import os

import ConfigParser

__author__ = 'Benoit HERVIER (Khertan)'
__email__ = 'khertan@khertan.net'
__version__ = '2.2.1'
__upgrade__ = '''0.4.1 :
 * Implement MarkDown preview
 * Syntax Highlighting (not in realtime due to qml limitation)
 * Fix loading of large text (But can appear frozen sometime due to qml limitations)
 * Add a busy cursor when loading text
0.4.2 :
 * Fix creation of new file
 * Remove threading, seems to slow donw more things and make some sync problem on signals
0.4.3 :
 * Reactivate threading, fix removal of space bugs on syntax highlighted text, improve signals
1.0.0 :
 * Giant bump number release just to conform to nokia ovi rules
1.0.1 :
 * fix missing package beautifulsoup in the package dependencies
1.1.0 :
 * fix reading of highlighting setting, and add support for decoding utf-16 file
1.1.1:
 * fix the 1.1.0 fix :)
1.1.2:
 * fix the 1.1.1 fix :p
1.1.3:
 * Deal a problem with harmattan invoker
1.1.4:
 * Fix packaging
1.2.0:
 * Improve text flickering
 * ensure new written text visible on horizontal flickering (Fork and improve qml qt component TextArea
2.0.0:
 * Mostly rewritten, fix some bugs due to implementation
2.1.0:
 * Fix delete feature
 * Fix new file feature
 * Add changelog in about screen
2.1.1:
 * Adaptation for MeeGo Mer/Nemoi
2.1.2:
 * Add missing import of QGLFormat
2.1.3:
 * Fix for Nemomobile/Mer to use real user path
2.1.4:
 * Add 64x64 icon for nemo mobile, clean make.py
2.2.0:
 * Open by default the last opened folder
2.2.1:
 * Fix unsaved dialog which appear when there is none modification'''


class Settings(QObject):
    '''Config object'''

    def __init__(self,):
        QObject.__init__(self,)
        self.config = ConfigParser.ConfigParser()
        if not os.path.exists(os.path.expanduser('~/.khtsimpletext.cfg')):
            self._write_default()
        else:
            self.config.read(os.path.expanduser('~/.khtsimpletext.cfg'))
        try:
            self.config.add_section('General')
        except:
            pass

    def _write_default(self):
        ''' Write the default config'''
        self.config.add_section('Display')
        self.config.set('Display', 'syntaxhighlighting', 'True')
        self.config.set('Display', 'textwrap', 'True')
        self.config.set('Display', 'fontsize', '18')
        self.config.set('Display', 'fontfamily', 'Nokia Pure Text')
        self.config.add_section('General')
        self.config.set('General', 'lastopenedfolder', os.path.expanduser('~'))
        self._write()

    def _write(self):
        # Writing our configuration file to 'example.cfg'
        with open(os.path.expanduser('~/.khtsimpletext.cfg'),
                  'wb') as configfile:
            self.config.write(configfile)

    @Slot(unicode, unicode, result=bool)
    def set(self, option, value):
        try:
            if option in ('lastopenedfolder', ):
                self.config.set('General', option, value)
            else:
                self.config.set('Display', option, value)
            self._write()
            return True
        except Exception, err:
            print err
            return False

    @Slot(unicode, result=unicode)
    def get(self, option):
        try:
            if option in ('lastopenedfolder', ):
                return self.config.get('General', option)
            else:
                return self.config.get('Display', option)
        except:
            if option == 'lastopenedfolder':
                return os.path.expanduser('~')
            return ''

    def _get_textWrap(self,):
        return (self.get('textwrap').lower() == 'true')

    def _get_fontSize(self,):
        return int(self.get('fontsize'))

    def _get_fontFamily(self,):
        return self.get('fontfamily')

    def _get_syntaxHighlighting(self,):
        return (self.get('syntaxhighlighting').lower() == 'true')

    on_textWrap = Signal()
    on_fontSize = Signal()
    on_fontFamily = Signal()
    on_syntaxHighlighting = Signal()
    textWrap = Property(bool, _get_textWrap, notify=on_textWrap)
    fontSize = Property(int, _get_fontSize, notify=on_fontSize)
    fontFamily = Property(unicode, _get_fontFamily, notify=on_fontFamily)
    syntaxHighlighting = Property(bool, _get_syntaxHighlighting,
                                  notify=on_syntaxHighlighting)

from documentsModel import DocumentsModel
from document import Document


class KhtSimpleText(QApplication):
    ''' Application class '''
    def __init__(self):
        QApplication.__init__(self, sys.argv)
        self.setOrganizationName("Khertan Software")
        self.setOrganizationDomain("khertan.net")
        self.setApplicationName("KhtSimpleText")

        self.view = QtDeclarative.QDeclarativeView()

        #Are we on mer ? So don't use opengl
        #As it didn't works on all devices
        if not os.path.exists('/etc/mer-release'):
            self.glformat = QGLFormat().defaultFormat()
            self.glformat.setSampleBuffers(False)
            self.glw = QGLWidget(self.glformat)
            self.glw.setAutoFillBackground(False)
            self.view.setViewport(self.glw)

        self.document = Document('~')
        self.settings = Settings()
        self.documentsModel = DocumentsModel(currentDoc=self.document, settings=self.settings)

        self.rootContext = self.view.rootContext()
        self.rootContext.setContextProperty("argv", sys.argv)
        self.rootContext.setContextProperty("__version__", __version__)
        self.rootContext.setContextProperty("__upgrade__", __upgrade__
                                            .replace('\n', '<br>'))
        self.rootContext.setContextProperty("Settings", self.settings)
        self.rootContext.setContextProperty("DocumentsModel",
                                            self.documentsModel)
        self.rootContext.setContextProperty("Document",
                                            self.document)
        self.view.setSource(QUrl.fromLocalFile(
            os.path.join(os.path.dirname(__file__), 'qml',  'main.qml')))
        self.rootObject = self.view.rootObject()
        self.view.showFullScreen()

if __name__ == '__main__':
    sys.exit(KhtSimpleText().exec_())
