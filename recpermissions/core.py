## @namespace recpermissions.core
## @brief Core functions of the package
import datetime
import platform
import sys

if platform.system()=="Windows":
    print("This script only works on Linux")
    sys.exit(0)

import argparse
import gettext
import grp
import locale
import os
import pkg_resources
import pwd
import shutil

from colorama import Fore, Style, init as colorama_init
from recpermissions.version import __versiondate__, __version__
from stat import ST_MODE

try:
    t=gettext.translation('recpermissions',pkg_resources.resource_filename("recpermissions","locale"))
    _=t.gettext
except:
    _=str

## Returns a localized int
## @param value Integer to localize
## @return string
def localized_int(value):
    return locale.format_string("%d", value, True)

## Check if a directory is empty
## @param dir String with the directory to check
## @return boolean
def is_dir_empty(dir):
    if not os.listdir(dir):
        return True
    else:
        return False

## Gets octal string permissions from a file
## @param path String with the path. Can be a dir or a file
## @return string "644" or "755", for example
def get_octal_string_permissions(path):
    return oct(os.stat(path)[ST_MODE])[-3:]

## Sets octal string permissions to a file
## @param path String with the path. Can be a dir or a file
## @param octal String with octal permissions. "644" or "755" for example
## @return Boolean if file has been changed
def set_octal_string_permissions(path, octal):
    if octal==None:
        return False
    if get_octal_string_permissions(path)==octal:
        return False
    else:
        try:
            os.chmod(path, int(octal, 8))
            return True
        except:
            return False

## Returns if the octal string has valid octal permissions
## @param octal String with octal permissions. "644" or "755" for example
## @return Boolean if the octal string is valid
def is_octal_string_permissions_valid(octal):
    if len(octal)==3 and octal.isdigit()==True and octal.find("9")==-1:
         return True
    return False

## Gets user and root from a path
## @param path String with the path. Can be a dir or a file
## @return a tuple (root, root), for example. If uid of the file isn't in /etc/passwd, returns uid and gid
def get_file_ownership(path):
    try:
        return (pwd.getpwuid(os.stat(path).st_uid).pw_name, grp.getgrgid(os.stat(path).st_gid).gr_name)
    except:
        return (os.stat(path).st_uid, os.stat(path).st_gid)

## Set file user and grup
## @param path String with the path. Can be a dir or a file
## @param user String or None. If none it doesn't change the user
## @param group String or None. If none it doesn't change the group
## @return Boolean if file has been changed
def set_file_ownership(path, user, group):
    if (user, group)==(None, None):
        return False
    tuple=get_file_ownership(path)
    if tuple==(user, group):
        return False
    else:
        user=tuple[0] if user==None else user
        group=tuple[1] if group==None else group
        try:
            shutil.chown(path, user, group)
            return True
        except:
            return False

## recpermissions main script
## If arguments is None, launches with sys.argc parameters. Entry point is recpermissions:main
## You can call with main(['--pretend']). It's equivalento to os.system('recpermissions --pretend')
## @param arguments is an array with parser arguments. For example: ['--max_files_to_store','9']. 
def main(arguments=None):
    start=datetime.datetime.now()
    parser=argparse.ArgumentParser(prog='recpermissions', description=_('Change Linux permissions and ownership in one step. It can delete empty directories when necessary.'), epilog=_("Developed by Mariano Muñoz 2018-{}".format(__versiondate__.year)), formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument('--version', action='version', version=__version__)

    parser.add_argument('--user', help=_("File owner will be changed to this parameter. It does nothing if it's not set."), action="store", default=None)
    parser.add_argument('--group', help=_("File owner group will be changed to this parameter. It does nothing if it's not set."), action="store", default=None)
    parser.add_argument('--files', help=_("File permissions to set in all files. It does nothing if it's not set."), default=None, metavar='PERM')
    parser.add_argument('--directories', help=_("Directory permissions to set in all directories. It does nothing if it's not set."), default=None, metavar='PERM')
    parser.add_argument('--remove_emptydirs', help=_("If it's established, removes empty directories recursivily from current path."), action="store_true", default=False)
    parser.add_argument('--only', help=_("Only changes permissions to the file or directory passed in absolute_path parameter."), action="store_true", default=False)
    parser.add_argument('absolute_path', help=_("Directory who is going to be changed permissions and owner recursivily"), action="store")

    args=parser.parse_args(arguments)

    colorama_init(autoreset=True)

    # Sets locale to get integer format localized strings
    try:
        locale.setlocale(locale.LC_ALL, ".".join(locale.getlocale()))
    except:
        pass

    if os.path.isabs(args.absolute_path)==False:
        print(Fore.RED + Style.BRIGHT + _("Path parameter must be an absolute one") + Style.RESET_ALL)
        sys.exit(1)

    if not (is_octal_string_permissions_valid(args.files) and is_octal_string_permissions_valid(args.directories)):
        print(Fore.RED + Style.BRIGHT + _("Seems you gave a bad octal string in --files or --directories parameters. Use format 644 or 755 for example."))
        sys.exit(1)

    deleted_dirs=[]
    files=[]
    dirs=[]
    changed_dirs=[]
    changed_files=[]
    error_files=[]
    ignored_symlinks=[]

    #Generate list of files and directories
    if args.only==False:
        dirs.append(args.absolute_path)
        for (dirpath, dirnames, filenames) in os.walk(args.absolute_path):
            for d in dirnames:
                dirs.append(os.path.join(dirpath, d))
            for f in filenames:
                files.append(os.path.join(dirpath, f))
    else:
        if os.path.isdir(args.absolute_path):
            dirs.append(args.absolute_path)
        else:
            files.append(args.absolute_path)

    #Iterate list of dirs
    for dirname in dirs:
        if os.path.islink(dirname)==True:
            ignored_symlinks.append(dirname)
            continue
        if os.path.exists(dirname)==False:
            error_files.append(dirname)
            continue

        b_permissions=set_octal_string_permissions(dirname,args.directories)
        b_ownership=set_file_ownership(dirname, args.user, args.group)
        if b_permissions==True or b_ownership==True:
            changed_dirs.append(dirname)

        if args.remove_emptydirs==True:
            if is_dir_empty(dirname):
                os.rmdir(dirname)
                deleted_dirs.append(dirname)

    #Iterate list of files
    for filename in files:
        if os.path.islink(filename)==True:
            ignored_symlinks.append(filename)
            continue
        if os.path.exists(filename)==False:
            error_files.append(filename)
            continue

        b_permissions=set_octal_string_permissions(filename, args.files)
        b_ownership=set_file_ownership(filename, args.user, args.group)
        if b_permissions or b_ownership==True:
            changed_files.append(dirname)

    print( _("RecPermissions in {} set owner to {}:{}, files to {} and directories to {}.").format(Fore.GREEN + args.absolute_path + Fore.RESET, Fore.GREEN + args.user + Fore.RESET, Fore.GREEN + args.group + Fore.RESET, Fore.GREEN + args.files + Fore.RESET, Fore.GREEN + args.directories + Fore.RESET))
    print( Fore.GREEN + "  * " + Fore.RESET + _("Directories found: ") + Fore.YELLOW + localized_int(len(dirs)))
    print( Fore.GREEN + "  * " + Fore.RESET + _("Files found: ") + Fore.YELLOW + localized_int(len(files)))
    print( Fore.GREEN + "  * " + Fore.RESET + _("Directories changed: ") + Fore.YELLOW + localized_int(len(changed_dirs)))
    print( Fore.GREEN + "  * " + Fore.RESET + _("Files changed: ") + Fore.YELLOW + localized_int(len(changed_files)))
    print( Fore.GREEN + "  * " + Fore.RESET + _("Directories deleted: ") + Fore.YELLOW + localized_int(len(deleted_dirs)))
    print( Fore.GREEN + "  * " + Fore.RESET + _("Ignored symlinks: ") + Fore.YELLOW + localized_int(len(ignored_symlinks)))
    if len(error_files)>0:
        print( Fore.GREEN + "  * " + Fore.RESET +  _("{} error files:").format(Fore.RED + localized_int(len(error_files))+ Fore.RESET))
        for e in error_files:
            print( Fore.RED + "     + " + Style.RESET_ALL + e)
    print( _("Executed at {}, took {}.").format(Fore.GREEN + str(datetime.datetime.now()) + Fore.RESET, Fore.GREEN + str(datetime.datetime.now()-start) + Fore.RESET))
