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

import os
import sys
from glob import glob

import khtsimpletext
import pypackager

__build__ = '1'
__author__ = "Benoît HERVIER (khertan)"
__mail__ = "khertan@khertan.net"
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
1.1.1: fix the 1.1.0 fix :)
1.1.2: fix the 1.1.1 fix :p
1.1.3: Deal a problem with harmattan invoker
1.1.4: Fix packaging
1.2.0: Improve text flickering and ensure new written text visible on horizontal flickering (Fork and improve qml qt component TextArea'''

if __name__ == "__main__":
    try:
        os.chdir(os.path.dirname(sys.argv[0]))
    except:
        pass

    p=pypackager.PyPackager("khtsimpletext")
    p.display_name = 'KhtSimpleText'
    p.version = khtsimpletext.__version__
    p.buildversion = __build__
    p.description="A plain text editor for Harmattan devices (n950, n9) with basic syntax highlighting feature"
    p.upgrade_description=__upgrade__
    p.author=__author__
    p.maintainer=__author__
    p.email=__mail__
    p.depends = "python, python-pyside.qtgui, python-pyside.qtdeclarative, python-pyside.qtcore, python-pyside.qtopengl, python-beautifulsoup"
    p.suggests = ""
    p.section="user/office"
    p.arch="armel"
    p.urgency="low"
    p.icon='khtsimpletext.png'
    p.distribution="harmattan"
    p.repository="Khertan Repository"
    p.bugtracker = 'http://github.com/khertan/KhtSimpleText/issues'
    p.changelog =  p.upgrade_description
    p.maemo_flags = 'visible'
    p.meego_desktop_entry_filename = '/usr/share/applications/khtsimpletext.desktop'
    p.createDigsigsums = True
    files = []
    p.postinst = '''#!/bin/sh
chmod +x /opt/khtsimpletext/__init__.py'''


    #Src
    #Src
    for root, dirs, fs in os.walk(os.path.join(os.path.dirname(__file__), p.name)):
      for f in fs:
        files.append(os.path.join(root, f))


    p['/usr/share/dbus-1/services'] = ['khtsimpletext.service',]
    #p['/usr/share/pixmaps'] = ['khtsimpletext.png',] #Removed due to stupid nokia store qa rules
    p['/usr/share/icons/blanco/80x80/apps'] = ['khtsimpletext.png',]
    p['/usr/share/applications'] = ['khtsimpletext.desktop',]
    p["/opt"] = files

    print p.generate(build_binary=True,build_src=True)
    if not os.path.exists('dists'):
        os.mkdir('dists')
    for filepath in glob(p.name+'_'+p.version+'-'+p.buildversion+'*'):
        os.rename(filepath, os.path.join(os.path.dirname(filepath), 'dists', os.path.basename(filepath)))



