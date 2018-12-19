#!/usr/bin/python3
import argparse
import time
import colorama
import os
import subprocess
import gettext
from ttyrecgenerator import RecSession
import pkg_resources
gettext.install('recpermissions', pkg_resources.resource_filename('recpermissions', 'locale'))

#We change permissions for the howto
os.system("mkdir -p directory")
os.system("touch directory/prueba.txt")
os.system("mkdir -p directory_empty")
os.system("chown -R apache:apache *")
os.system("chmod -R  777 *")

r=RecSession()
r.comment("# " + _("This is a video to show how to use 'recpermissions' command"))
r.comment("# " + _("We list files with permissions and owners"))
r.command("ls -la")

r.comment("# " + _("We want to change them to root:root owner. Files to 640 permissions, directories to 750. We want to remove empty directories too, so we use:"))
r.command("recpermissions --user root --group root --files 640 --directories 750 --remove_emptydirs " + os.getcwd())
r.comment("# " + _("We check the result"))
r.command("ls -la")
r.comment("# " + _("That's all"))
time.sleep(30)
r.comment("# ")

#We remove example
os.system("rm -Rf directory")
