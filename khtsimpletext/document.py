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

from PySide.QtCore import Slot, QObject, Property, Signal

import threading
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


def _stripTags(text):
    ''' Remove html text formating from a text'''
    from BeautifulSoup import BeautifulSoup
    plainText = _unescape(''.join(
        BeautifulSoup(
            text.replace('<p style=', '<pre style'))
        .body(text=True)))
    if (plainText.startswith('\n')):
        return plainText[1:]
    return plainText


def _colorIt(text, filepath):
    ''' Syntax highlight a text in html'''
    try:
        lexer = get_lexer_for_filename(filepath)
        if lexer is None:
            return (text, None)
        return (highlight(text, lexer, HtmlFormatter(full=True)), None)
    except ClassNotFound:
        return (text, None)
    except Exception, err:
        return (text, err)


def _unescape(text):
    ''' Unescape a text '''
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
        return text  # leave as is
    return re.sub("&#?\w+;", fixup, text)


class Document(QObject):
    def __init__(self, filepath):
        QObject.__init__(self,)
        self._filename = os.path.basename(filepath)
        self._filepath = os.path.realpath(filepath)
        self._isdir = os.path.isdir(filepath)
        self._data = None
        self._ready = False

    def _get_isdir(self,):
        return self._isdir

    def _get_filename(self,):
        return self._filename

    def _set_filename(self, value):
        self._filename = value
        self.onFilenameChanged.emit()

    def _get_filepath(self,):
        return self._filepath

    def _set_filepath(self, value):
        self._filepath = value
        self._set_filename(os.path.basename(value))
        self.onFilepathChanged.emit()

    def _get_data(self,):
        return self._data

    def _set_data(self, value):
        self._data = value
        self.onDataChanged.emit()

    @Slot()
    def load(self,):
        ''' Load the document from a path in a thread'''
        self._set_ready(False)
        self.thread = threading.Thread(target=self._load)
        self.thread.start()

    def _load(self, ):
        ''' Load the document from a path '''
        import codecs
        try:
            with codecs.open(self._filepath, 'r', 'utf_8') as fh:
                try:
                    text = fh.read()
                    if text.find('\0') > 0:
                        text = text.decode('utf-16')
                    text, err = _colorIt(text, self._filepath)
                    if err:
                        raise err
                    self._set_data(text)
                    self._set_ready(True)
                except Exception, err:
                    print type(err), err
                    self._set_data('')
                    self.onError.emit(unicode(err))
                    self._set_ready(True)
        except Exception, err:
            self._set_data('')
            self._set_ready(True)
            self.onError.emit(unicode(err))
            print err

    @Slot(unicode, result=unicode)
    def recolorIt(self, text):
        ''' ReHighlight a text '''
        text, err = _colorIt(_stripTags(text), self._filepath)
        if not err:
            self._set_data(text)
        else:
            self.onError.emit(unicode(err))

    @Slot(unicode, result=unicode)
    def previewMarkdown(self, text):
        ''' Generate a markdown preview'''
        try:
            return markdown2.markdown(self._stripTags(text))
        except:
            return text

    @Slot(unicode)
    def write(self, data):
        ''' Write the document to a file '''
        data = self._stripTags(data)
        try:
            with open(self.filepath, 'wb') as fh:
                fh.write(data.encode('utf-8'))
        except Exception, err:
            print err
            self.onError.emit(unicode(err))

    def _get_ready(self):
        return self._ready

    def _set_ready(self, value):
        self._ready = value
        self.onReadyChanged.emit()

    onIsdirChanged = Signal()
    onFilenameChanged = Signal()
    onFilepathChanged = Signal()
    onDataChanged = Signal()
    isdir = Property(bool, _get_isdir, notify=onIsdirChanged)
    filename = Property(unicode, _get_filename,
                        _set_filename, notify=onFilenameChanged)
    filepath = Property(unicode, _get_filepath,
                        _set_filepath, notify=onFilepathChanged)
    data = Property(unicode, _get_data,
                    _set_data, notify=onDataChanged)

    onError = Signal(unicode)
    onReadyChanged = Signal()
    ready = Property(bool, _get_ready, _set_ready, notify=onReadyChanged)
