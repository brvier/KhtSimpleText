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

__build__ = '3'
__author__ = "Benoît HERVIER (khertan)"
__mail__ = "khertan@khertan.net"
if __name__ == "__main__":
    try:
        os.chdir(os.path.dirname(sys.argv[0]))
    except:
        pass

    p = pypackager.PyPackager("khtsimpletext")
    p.display_name = 'KhtSimpleText'
    p.version = khtsimpletext.__version__
    p.buildversion = __build__
    p.summary = 'A text editor'
    p.description = "A text editor for Harmattan devices (n950, n9)" \
        + " and MeeGo/Mer device with basic syntax highlighting feature"
    p.upgrade_description = khtsimpletext.__upgrade__
    p.author = __author__
    p.maintainer = __author__
    p.email = __mail__
    p.depends = "python, python-pyside.qtgui, python-pyside.qtdeclarative, " \
        + "python-pyside.qtcore, python-pyside.qtopengl, python-beautifulsoup"
    p.rpm_depends = "python, python-pyside, python-beautifulsoup"
    p.suggests = ""
    p.section = "user/office"
    p.arch = "armel"
    p.urgency = "low"
    p.icon = 'khtsimpletext.png'
    p.distribution = "harmattan"
    p.repository = "Khertan Repository"
    p.bugtracker = 'http://github.com/khertan/KhtSimpleText/issues'
    p.changelog = p.upgrade_description
    p.maemo_flags = 'visible'
    p.meego_desktop_entry_filename = ('/usr/share/applications/'
                                      'khtsimpletext.desktop')
    p.createDigsigsums = True
    files = []
    p.postinst = '''#!/bin/sh
echo "Giving permissions for apps to execute"
chmod +x /opt/khtsimpletext/__init__.py
exit 0'''

    #Include byte compiled files, so do not remove it at packaging
    #time : selinux / obs spec packaging can require them
    from compileall import compile_dir
    compile_dir(os.path.join(os.path.dirname(__file__), p.name))
    os.system('python -O -m compileall '
              + os.path.join(os.path.dirname(__file__), p.name))

    #Src
    for root, dirs, fs in os.walk(os.path.join(os.path.dirname(__file__),
                                  p.name)):
        for f in fs:
            files.append(os.path.join(root, f))

    p['/usr/share/dbus-1/services'] = ['khtsimpletext.service', ]
    p['/usr/share/icons/hicolor/80x80/apps'] = ['khtsimpletext.png', ]
    p['/usr/share/icons/hicolor/scalable/apps'] = ['khtsimpletext.svg', ]
    p['/usr/share/applications'] = ['khtsimpletext.desktop', ]
    p["/opt"] = files

    print p.generate(build_binary=True, build_src=True)
    if not os.path.exists('dists'):
        os.mkdir('dists')
    for filepath in glob(p.name + '_' + p.version
                         + '-' + p.buildversion + '*'):
        os.rename(filepath, os.path.join(os.path.dirname(filepath),
                  'dists', os.path.basename(filepath)))
