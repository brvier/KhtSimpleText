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

import ConfigParser
from PySide.QtCore import Slot, QObject, Property, Signal

import os

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

    def reload(self, ):
        self.config.read(os.path.expanduser('~/.khtsimpletext.cfg'))

    def _write_default(self):
        ''' Write the default config'''
        self.config.add_section('Display')
        self.config.set('Display', 'syntaxhighlighting', 'True')
        self.config.set('Display', 'textwrap', 'True')
        self.config.set('Display', 'fontsize', '18')
        self.config.set('Display', 'fontfamily', 'Nokia Pure Text')
        self.config.add_section('General')
        self.config.set('General', 'lastopenedfolder', os.path.expanduser('~'))
        self.config.set('General', 'useLastopenedfolder', 'True')
        self.config.set('General', 'hideVKB', 'False')
        self.config.set('General', 'hideHeader', 'False')
        self._write()

    def _write(self):
        # Writing our configuration file to 'example.cfg'
        with open(os.path.expanduser('~/.khtsimpletext.cfg'),
                  'wb') as configfile:
            self.config.write(configfile)

    @Slot(unicode, unicode, result=bool)
    def set(self, option, value):
        try:
            if option in ('lastopenedfolder', 'hideVKB', 'hideHeader', 'useLastopenedfolder'):
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
            if option in ('lastopenedfolder', 'hideVKB', 'hideHeader', 'useLastopenedfolder'):
                return self.config.get('General', option)
            else:
                return self.config.get('Display', option)
        except:
            if option == 'lastopenedfolder':
                return os.path.expanduser('~')
            elif option == 'hideVKB':
                return 'False'
            elif option == 'useLastopenedfolder':
                return 'True'
            return ''

    def _get_textWrap(self,):
        return (self.get('textwrap').lower() == 'true')

    def _set_textWrap(self, value):
        self.set('textwrap', 'True' if value else 'False')
        self.on_textWrap.emit()

    def _get_fontSize(self,):
        return int(self.get('fontsize'))

    def _set_fontSize(self, value):
        return self.set('fontsize', unicode(value))
        self.on_fontSize.emit()

    def _get_fontFamily(self,):
        return self.get('fontfamily')

    def _set_fontFamily(self, value):
        self.set('fontfamily', value)
        self.on_fontFamily.emit()

    def _get_syntaxHighlighting(self,):
        print self.get('syntaxhighlighting')
        return (self.get('syntaxhighlighting').lower() == 'true')

    def _set_syntaxHighlighting(self, value):
        self.set('syntaxhighlighting', 'True' if value else 'False')
        self.on_syntaxHighlighting.emit()

    def _get_useLastOpenedFolder(self,):
        return (self.get('useLastopenedfolder').lower() == 'true')

    def _set_useLastOpenedFolder(self, value):
        self.set('useLastopenedfolder', 'True' if value else 'False')
        self.on_useLastOpenedFolder.emit()

    def _get_lastOpenedFolder(self, ):
        return self.get('lastopenedfolder')

    def _set_lastOpenedFolder(self, value):
        self.set('lastopenedfolder', value)
        self.on_lastOpenedFolder.emit()

    def _get_hideVKB(self, ):
        return (self.get('hideVKB').lower() == 'true')

    def _set_hideVKB(self, value):
        self.set('hideVKB', 'True' if value else 'False')
        self.on_hideVKB.emit()

    def _get_hideHeader(self, ):
        return (self.get('hideHeader').lower() == 'true')

    def _set_hideHeader(self, value):
        self.set('hideHeader', 'True' if value else 'False')
        self.on_hideHeader.emit()

    on_textWrap = Signal()
    on_fontSize = Signal()
    on_fontFamily = Signal()
    on_syntaxHighlighting = Signal()
    on_lastOpenedFolder = Signal()
    on_hideHeader = Signal()
    on_hideVKB = Signal()
    on_useLastOpenedFolder = Signal()

    textWrap = Property(bool, _get_textWrap,
                        _set_textWrap, notify=on_textWrap)
    fontSize = Property(int, _get_fontSize,
                        _set_fontSize, notify=on_fontSize)
    fontFamily = Property(unicode, _get_fontFamily,
                          _set_fontFamily, notify=on_fontFamily)
    syntaxHighlighting = Property(bool, _get_syntaxHighlighting,
                                  _set_syntaxHighlighting,
                                  notify=on_syntaxHighlighting)
    useLastOpenedFolder = Property(bool, _get_useLastOpenedFolder,
                                _set_useLastOpenedFolder, notify=on_useLastOpenedFolder)

    lastOpenedFolder = Property(unicode, _get_lastOpenedFolder,
                                _set_lastOpenedFolder, notify=on_lastOpenedFolder)
    hideHeader = Property(bool, _get_hideHeader,
                          _set_hideHeader,
                          notify=on_hideHeader)
    hideVKB = Property(bool, _get_hideVKB,
                       _set_hideVKB,
                       notify=on_hideVKB)         