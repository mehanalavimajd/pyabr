#######################################################################################
#  In the name of God, the Compassionate, the Merciful
#  Pyabr (c) 2020 Mani Jamali. GNU General Public License v3.0
#
#  Programmer & Creator:    Mani Jamali <manijamali2003@gmail.com>
#  Telegram or Gap channel: @pyabr
#  Telegram or Gap group:   @pyabr_community
#  Git source:              github.com/manijamali2003/pyabr
#
#######################################################################################

from buildlibs import pack_archives as pack
from buildlibs import control
import shutil, os, sys, hashlib,getpass

import shutil, os

## pre build ##

if not os.path.isdir ("app"):
	os.mkdir ("app")
	os.mkdir ("app/cache")
	os.mkdir ("app/cache/archives")
	os.mkdir ("app/cache/archives/data")
	os.mkdir ("app/cache/archives/control")
	os.mkdir ("app/cache/archives/code")
	os.mkdir ("app/cache/archives/build")
	os.mkdir ("app/cache/gets")

if not os.path.isdir ("stor"):
	os.mkdir ("stor")
	os.mkdir ("stor/app")
	os.mkdir ("stor/app/packages")

if not os.path.isdir ("build-packs"): os.mkdir ("build-packs")

for i in os.listdir('packs'):pack.manifest(i)
for i in os.listdir('packs'):pack.build(i)

shutil.rmtree('latest')
shutil.copytree('build-packs','latest')

import clean
clean.clean()