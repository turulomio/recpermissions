import argparse
from colorama import Fore, Style, init as colorama_init
from recpermissions.version import __versiondate__, __version__
from stat import ST_MODE
import gettext
import grp
import os
import pwd
import shutil
import sys

try:
    t=gettext.translation('recpermissions',pkg_resources.resource_filename("recpermissions","locale"))
    _=t.gettext
except:
    _=str


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


## Gets user and root from a path
## @param path String with the path. Can be a dir or a file
## @return a tuple (root, root), for example
def get_file_ownership(path):
    return (
        pwd.getpwuid(os.stat(path).st_uid).pw_name,
        grp.getgrgid(os.stat(path).st_gid).gr_name
)


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
    parser=argparse.ArgumentParser(prog='recpermissions', description=_('Search date and time patterns to delete innecesary files or directories'), epilog=_("Developed by Mariano Muñoz 2018-{}".format(__versiondate__.year)), formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument('--version', action='version', version=__version__)

    parser.add_argument('--user', help=_("File owner will be changed to this parameter. It does nothing if it's not set."), action="store", default=None)
    parser.add_argument('--group', help=_("File owner group will be changed to this parameter. It does nothing if it's not set."), action="store", default=None)
    parser.add_argument('--files', help=_("File permissions to set in all files. It does nothing if it's not set."), default=None, metavar='PERM')
    parser.add_argument('--directories', help=_("Directory permissions to set in all directories. It does nothing if it's not set."), default=None, metavar='PERM')
    parser.add_argument('--remove_emptydirs', help=_("If it's established, removes empty directories recursivily from current path."), action="store_true", default=False)
    parser.add_argument('absolute_path', help=_("Directory who is going to be changed permissions and owner recursivily"), action="store")

    args=parser.parse_args(arguments)

    colorama_init(autoreset=True)

    if os.path.isabs(args.absolute_path)==False:
        print(Fore.RED + Style.BRIGHT + _("Path parameter must be an absolute one") + Style.RESET_ALL)
        sys.exit(1)

    deleted_dirs=[]
    found_files=0
    found_dirs=0
    changed_dirs=[]
    changed_files=[]
    error_files=[]

    for (dirpath, dirnames, filenames) in os.walk(args.absolute_path):
        for d in dirnames:
            found_dirs=found_dirs+1
            dirname= os.path.join(dirpath, d)

            if os.path.exists(dirname)==False:
                error_files.append(dirname)
                continue

            if (set_octal_string_permissions(dirname,args.directories) or set_file_ownership(dirname, args.user, args.group))==True:
                changed_dirs.append(dirname)

            if args.remove_emptydirs==True:
                if is_dir_empty(dirname):
                    os.rmdir(dirname)
                    deleted_dirs.append(dirname)

        for f in filenames:
            found_files=found_files+1
            filename= os.path.join(dirpath, f)

            if os.path.exists(filename)==False:
                error_files.append(filename)
                continue
            
            if (set_octal_string_permissions(filename, args.files) or set_file_ownership(filename, args.user, args.group))==True:
                changed_files.append(dirname)


    print(Style.BRIGHT + _("RecPermissions summary:"))
    print(Style.BRIGHT + Fore.GREEN + "  * " + Fore.RESET + _("Directories found: ") + Fore.YELLOW + str(found_dirs))
    print(Style.BRIGHT + Fore.GREEN + "  * " + Fore.RESET + _("Files found: ") + Fore.YELLOW + str(found_files))
    print(Style.BRIGHT + Fore.GREEN + "  * " + Fore.RESET + _("Directories changed: ") + Fore.YELLOW + str(len(changed_dirs)))
    print(Style.BRIGHT + Fore.GREEN + "  * " + Fore.RESET + _("Files changed: ") + Fore.YELLOW + str(len(changed_files)))
    print(Style.BRIGHT + Fore.GREEN + "  * " + Fore.RESET + _("Directories deleted: ") + Fore.YELLOW + str(len(deleted_dirs)))
    if len(error_files)>0:
        print(Style.BRIGHT + Fore.GREEN + "  * " + Fore.RESET +  _("{} error files:").format(Fore.RED + str(len(error_files))+ Fore.RESET))
        for e in error_files:
            print(Style.BRIGHT + Fore.RED + "     + " + Style.RESET_ALL + e)
