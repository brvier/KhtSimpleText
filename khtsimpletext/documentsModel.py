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

from PySide.QtCore import Slot, Signal, \
    QAbstractListModel, QModelIndex, \
    Property

import os
import os.path

from document import Document

class DocumentsModel(QAbstractListModel):
    COLUMNS = ('filename', 'index', 'data',
               'filepath', 'isdir', 'ready', 'document')

    def __init__(self, currentDoc=None,
                       settings=None):
        self._documents = {}
        self.settings = settings
        self._currentPath = settings.lastOpenedFolder
        if ((not os.path.exists(self._currentPath)) or 
            (not settings.useLastOpenedFolder)):
            self._currentPath = os.path.expanduser('~')
        QAbstractListModel.__init__(self)
        self.setRoleNames(dict(enumerate(DocumentsModel.COLUMNS)))
        self.currentDoc = currentDoc

    @Slot()
    def loadDir(self, ):
        self._documents = [Document(os.path.join(self._currentPath,
                                                 filename))
                           for filename in os.listdir(self._currentPath)]
        self._documents.append(Document(os.path.join(self._currentPath,
                                                     '..')))
        self._sortData()

    def _sortData(self,):
        self._documents.sort(key=lambda document: (document.filename, ),
                             reverse=False)

    def rowCount(self, parent=QModelIndex()):
        return len(self._documents)

    def data(self, index, role):
        if index.isValid() \
                and role == DocumentsModel.COLUMNS.index('filename'):
            return self._documents[index.row()].filename
        elif index.isValid() \
                and role == DocumentsModel.COLUMNS.index('index'):
            return index.row()
        elif index.isValid() \
                and role == DocumentsModel.COLUMNS.index('data'):
            return self._documents[index.row()].data
        elif index.isValid() \
                and role == DocumentsModel.COLUMNS.index('filepath'):
            return self._documents[index.row()].filepath
        elif index.isValid() \
                and role == DocumentsModel.COLUMNS.index('isdir'):
            return self._documents[index.row()].isdir
        elif index.isValid() \
                and role == DocumentsModel.COLUMNS.index('ready'):
            return self._documents[index.row()].ready
        elif index.isValid() \
                and role == DocumentsModel.COLUMNS.index('document'):
            return self._documents[index.row()]
        return None

    @Slot()
    def reload(self):
        self.beginResetModel()
        self.loadDir()
        self.endResetModel()

    @Slot(unicode, result=int)
    def newFile(self, filename):
        self.beginResetModel()
        filepath = os.path.join(self._currentPath,
                                filename)
        print 'New file:', filepath
        if os.path.exists(filepath):
            isnewindex = -1
        else:
            new_document = Document(filepath)
            new_document.ready = True
            new_document.write(' ')
            self._documents.append(new_document)
            self._sortData()
            isnewindex = len(self._documents) - 1
        self.endResetModel()
        return isnewindex

    @Slot(int)
    def duplicate(self, idx):
        self.beginResetModel()
        newfilepath = os.path.join(
            os.path.dirname(self._documents[idx].filepath),
            os.path.splitext(os.path.basename(
                self._documents[idx].filepath))[0] +
            ' Copy' +
            os.path.splitext(os.path.basename(
            self._documents[idx].filepath))[1])
        new_document = self._documents[idx].copy(newfilepath)
        self._documents.append(new_document)
        self._sortData()
        self.endResetModel()

    @Slot(int, unicode, result=bool)
    def copyFile(self, idx, newfilepath):
        copied = self._documents[idx].copyFile(newfilepath)
        self.reload()
        return copied

    @Slot(int, result=bool)
    def remove(self, idx):
        self.beginResetModel()
        deleted = self._documents[idx].delete()
        self._documents.remove(self._documents[idx])
        self._sortData()
        self.endResetModel()
        return deleted

    @Slot(int, unicode, result=bool)
    def rename(self, idx, newfilename):
        self.beginResetModel()
        renammed = self._documents[idx].rename(newfilename)
        self._sortData()
        self.endResetModel()
        return renammed

    @Slot(int, unicode, result=bool)
    def move(self, idx, newfilepath):
        renammed = self._documents[idx].rename(newfilepath)
        if renammed:
            self.reload()
        return renammed

    def _get_currentpath(self):
        return self._currentPath

    def _set_currentpath(self, value):
        self._currentPath = os.path.realpath(value)
        self.onCurrentpathChanged.emit()
        self.settings.set('lastopenedfolder', value)
        self.reload()

    onCurrentpathChanged = Signal()

    currentpath = Property(unicode, _get_currentpath,
                           _set_currentpath, notify=onCurrentpathChanged)        