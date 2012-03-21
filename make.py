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
import shutil
import time
import string
from glob import glob
from datetime import datetime
import socket

import khtsimpletext
import pypackager

__build__ = '6'
__author__ = "khertan"
__mail__ = "khertan@khertan.net"

if __name__ == "__main__":
    try:
        os.chdir(os.path.dirname(sys.argv[0]))
    except:
        pass

    p=pypackager.PyPackager("khtsimpletext")
    p.display_name = 'KhtSimpleText'
    p.version = khtsimpletext.__version__
    p.buildversion = __build__
    p.description="A plain text editor for Harmattan"
    p.upgrade_description="Support now invoker"
    p.author=__author__
    p.maintainer=__author__    
    p.email=__mail__
    p.depends = "python, python-pyside.qtgui, python-pyside.qtdeclarative, python-pyside.qtcore"
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
    files = []
    p.postinst = """#!/bin/sh
chmod +x /usr/local/bin/khtsimpletext_launch.py
"""

    #Src
    srcpath = '/home/user/MyDocs/Projects/khtsimpletext/khtsimpletext'
    for root, dirs, fs in os.walk(srcpath):
      for f in fs:
        prefix = os.path.relpath(os.path.join(root,f),(os.path.dirname(srcpath)))
        print root, prefix
        files.append(prefix)
#    print files

    p['/usr/share/dbus-1/services'] = ['khtsimpletext.service',]
    p['/usr/share/pixmaps'] = ['khtsimpletext.png',]
    p['/usr/share/icons/blanco/80x80/apps'] = ['khtsimpletext.png',]
    p['/usr/local/bin'] = ['khtsimpletext_launch.py',]

    p['/usr/share/applications'] = ['khtsimpletext.desktop',]
    p["/usr/lib/pymodules/python2.6"] = files
    
    #print p.generate(build_binary=False,build_src=True)
    print p.generate(build_binary=True,build_src=False)
