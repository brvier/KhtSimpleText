#!/usr/bin/python
# -*- coding: utf-8 -*-

#KhtSimpleText Setup File
import khtsimpletext
import sys
reload(sys).setdefaultencoding("UTF-8")

changelog = '* Implement rename and delete feature in contextual menu * fix package display name'
buildversion = '1'

try:
    from sdist_maemo import sdist_maemo as _sdist_maemo
except:
    _sdist_maemo = None
    print 'sdist_maemo command not available'

from distutils.core import setup

#Remove pyc and pyo file
import glob,os
for fpath in glob.glob('*/*.py[c|o]'):
    os.remove(fpath)

for fpath in glob.glob('*/plugins/*.py[c|o]'):
    os.remove(fpath)
for fpath in glob.glob('*/syntax/*.py[c|o]'):
    os.remove(fpath)


setup(name='khtsimpletext',
      version=khtsimpletext.__version__,
      license='GNU GPLv3',
      description='A plain text editor.',
      long_description="A simple and easy to use plain text editor for Harmattan",
      author='Benoît HERVIER',
      author_email='khertan@khertan.net',
      maintainer=u'Benoît HERVIER',
      maintainer_email='khertan@khertan.net',
      url='http://www.khertan.net/khteditor',
      requires=['pyside',],
      packages= ['khtsimpletext', ],
      package_data = {'khtsimpletext': ['icons/*.png', 'syntax/*.xml', 'qml/*.js', 'qml/*.qml', 'qml/components/*.qml', ],},
      data_files=[('/usr/share/dbus-1/services', ['khtsimpletext.service']),
                  ('/usr/share/applications/', ['khtsimpletext.desktop']),
                  ('/usr/share/pixmaps', ['khtsimpletext.png']),
                  ('/usr/share/icons/blanco/80x80/apps', ['khtsimpletext.png']),
                  ],
      scripts=['khtsimpletext_launch.py'],
      cmdclass={'sdist_maemo': _sdist_maemo},
      options = { 'sdist_maemo':{
      'buildversion':buildversion,
      'depends':'python, python-pyside.qtdeclarative, python-pyside.qtcore, python-pyside.qtgui',
      'Maemo_Bugtracker':'https://github.com/khertan/KhtSimpleText/issues',
      'Maemo_Display_Name':'KhtSimpleText',
      'Maemo_Icon_26':'khtsimpletext.png',
      'Maemo_Flags':'visible',
      'MeeGo_Desktop_Entry_Filename':'/usr/share/applications/khtsimpletext.desktop',
      'section':'user/utilities',
      'changelog':changelog,
      'Maemo_Upgrade_Description':changelog,
      'architecture':'any',
      'postinst':"""#!/bin/sh
chmod +x /usr/local/bin/khtsimpletext_launch.py
""",
      'copyright':'gpl'},
      'bdist_rpm':{
      'requires':'python-pyside.qtdeclarative python-pyside.qtcore python-pyside.qtgui',
      'icon':'khtsimpletext.png',
      'group':'Development',}}
     )

