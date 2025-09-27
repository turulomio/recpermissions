from datetime import datetime
from platform import system as platform_system
from sys import exit, version_info

if platform_system()=="Windows":
    print("This script only works on Linux")
    exit(1)

from argparse import ArgumentParser, RawTextHelpFormatter
from grp import getgrgid
from locale import LC_ALL, format_string, getlocale, setlocale
from os import chmod, listdir, path, rmdir, stat, walk
from pwd import getpwuid
from shutil import chown
from colorama import Fore, Style, init as colorama_init
from recpermissions import __versiondate__, __version__, _, epilog
from stat import ST_MODE


## Returns a localized int
## @param value Integer to localize
## @return string
def localized_int(value):
    return format_string("%d", value, True)

## Check if a directory is empty
## @param dir String with the directory to check
## @return boolean
def is_dir_empty(dir):
    if not listdir(dir):
        return True
    else:
        return False

## Gets octal string permissions from a file
## @param path String with the path. Can be a dir or a file
## @return string "644" or "755", for example
def get_octal_string_permissions(path):
    return oct(stat(path)[ST_MODE])[-3:]

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
            chmod(path, int(octal, 8))
            return True
        except:
            return False

## Returns if the octal string has valid octal permissions
## @param octal String with octal permissions. "644" or "755" for example
## @return Boolean if the octal string is valid
def is_octal_string_permissions_valid(octal):
    if octal==None: #Is valid but set function just ignore it
         return True
    if len(octal)==3 and octal.isdigit()==True and octal.find("9")==-1:
         return True
    return False

## Gets user and root from a path
## @param path String with the path. Can be a dir or a file
## @return a tuple (root, root), for example. If uid of the file isn't in /etc/passwd, returns uid and gid
def get_file_ownership(path):
    try:
        return (getpwuid(stat(path).st_uid).pw_name, getgrgid(stat(path).st_gid).gr_name)
    except:
        return (stat(path).st_uid, stat(path).st_gid)

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
            chown(path, user, group)
            return True
        except:
            return False


## Returns if a string can be casted to integer. Used to detect if owner is a uid or gid
## @param s String
## @return boolean
def is_uid_or_gid(s):
    if s==None:
        return False
    try:
        int(s)
        return True
    except:
        return False


## recpermissions main script
## If arguments is None, launches with sys.argc parameters. Entry point is recpermissions:main
## You can call with main(['--pretend']). It's equivalento to os.system('recpermissions --pretend')
## @param arguments is an array with parser arguments. For example: ['--max_files_to_store','9']. 
def main_recpermissions():
    parser=ArgumentParser(prog='recpermissions', description=_('Change Linux permissions and ownership in one step. It can delete empty directories when necessary.'), epilog=epilog(), formatter_class=RawTextHelpFormatter)
    parser.add_argument('--version', action='version', version=__version__)

    parser.add_argument('--user', help=_("File owner will be changed to this parameter. It does nothing if it's not set."), action="store", required=True)
    parser.add_argument('--group', help=_("File owner group will be changed to this parameter. It does nothing if it's not set."), action="store", required=True)
    parser.add_argument('--files', help=_("File permissions to set in all files. It does nothing if it's not set."), required=True, metavar='PERM')
    parser.add_argument('--directories', help=_("Directory permissions to set in all directories. It does nothing if it's not set."), required=True, metavar='PERM')
    parser.add_argument('absolute_path', help=_("Directory who is going to be changed permissions and owner recursivily"), action="store")

    args=parser.parse_args()

    colorama_init(autoreset=True)

    recpermissions(args.user, args.group, args.files, args.directories, args.absolute_path)


def recpermissions(user,group,files,directories,absolute_path):
    start=datetime.now()

    # Sets locale to get integer format localized strings
    try:
        setlocale(LC_ALL, ".".join(getlocale()))
    except:
        pass

    if is_uid_or_gid(user)==True or is_uid_or_gid(group)==True:
        print(Fore.RED + Style.BRIGHT + _("Change owner by uid or gid is not allowed") + Style.RESET_ALL)
        exit(1)

    if path.isabs(absolute_path)==False:
        print(Fore.RED + Style.BRIGHT + _("Path parameter must be an absolute one") + Style.RESET_ALL)
        exit(1)

    if not (is_octal_string_permissions_valid(files) and is_octal_string_permissions_valid(directories)):
        print(Fore.RED + Style.BRIGHT + _("Seems you gave a bad octal string in --files or --directories parameters. Use format 644 or 755 for example."))
        exit(1)

    files=0
    dirs=0
    changed_dirs=0
    changed_files=0
    error_files=[]
    ignored_symlinks=0

    #Generate list of files and directories
    if set_octal_string_permissions(absolute_path,directories) and set_file_ownership(absolute_path, user, group):
        changed_dirs+=1

    #Change absolute path


    for dirpath, dirnames, filenames in walk(absolute_path):
        # Iterate directories
        for d in dirnames:
            p=path.join(dirpath, d)
            dirs+=1
            
            if path.islink(p):
                ignored_symlinks+=1
            elif not path.exists(p):
                error_files.append(p)
            else:
                if set_octal_string_permissions(p,directories) and set_file_ownership(p , user, group):
                    changed_dirs+=1
                else:
                    error_files.append(p)   

        #Iterate files
        for f in filenames:
            p=path.join(dirpath, f) 
            files+=1
            if path.islink(p):
                ignored_symlinks+=1
            elif not path.exists(p):
                error_files.append(p)   
            else:
                if set_octal_string_permissions(p,files) and set_file_ownership(p, user, group):
                    changed_dirs+=1
                else:
                    error_files.append(p)   

    print( _("RecPermissions in {}:").format(Fore.GREEN + absolute_path + Fore.RESET))
    print( Fore.GREEN + "  * " + Fore.RESET + _("Directories found: ") + Fore.YELLOW + localized_int(dirs))
    print( Fore.GREEN + "  * " + Fore.RESET + _("Files found: ") + Fore.YELLOW + localized_int(files))
    print( Fore.GREEN + "  * " + Fore.RESET + _("Directories changed: ") + Fore.YELLOW + localized_int(changed_dirs))
    print( Fore.GREEN + "  * " + Fore.RESET + _("Files changed: ") + Fore.YELLOW + localized_int(changed_files))
    print( Fore.GREEN + "  * " + Fore.RESET + _("Ignored symlinks: ") + Fore.YELLOW + localized_int(ignored_symlinks))
    if len(error_files)>0:
        print( Fore.GREEN + "  * " + Fore.RESET +  _("{} error files:").format(Fore.RED + localized_int(len(error_files))+ Fore.RESET))
        for e in error_files:
            print( Fore.RED + "     + " + Style.RESET_ALL + e)
    print( _("Executed at {}, took {}.").format(Fore.GREEN + str(datetime.now()) + Fore.RESET, Fore.GREEN + str(datetime.now()-start) + Fore.RESET))


def main_remove_empty_directories():
    parser=ArgumentParser(prog='recpermissions', description=_('Removes empty directories'), epilog=epilog(), formatter_class=RawTextHelpFormatter)
    parser.add_argument('--version', action='version', version=__version__)
    parser.add_argument('--pretend', help=_("Only changes permissions to the file or directory passed in absolute_path parameter."), action="store_true", default=False)
    parser.add_argument('absolute_path', help=_("Directory who is going to be changed permissions and owner recursivily"), action="store")

    args=parser.parse_args()

    colorama_init(autoreset=True)

    recpermissions(args.pretend, args.absolute_path)


def remove_empty_directories(pretend,absolute_path):
    start=datetime.now()

    # Sets locale to get integer format localized strings
    try:
        setlocale(LC_ALL, ".".join(getlocale()))
    except:
        pass

    if path.isabs(absolute_path)==False:
        print(Fore.RED + Style.BRIGHT + _("Path parameter must be an absolute one") + Style.RESET_ALL)
        exit(1)


    deleted_dirs=0
    error_directories=[]
    ignored_symlinks=0

    #Generate list of files and directories

    #Iterate list of dirs
    for dirpath, dirnames, filenames in walk(absolute_path):
        for d in dirnames:
            p = path.join(dirpath,  d)
            if path.islink(d)==True:
                ignored_symlinks+=1
                continue
            if path.exists(d)==False:
                error_directories.append(d)
                continue

        if pretend is False:
            if is_dir_empty(d):
                rmdir(d)
                deleted_dirs+=1


    print( _("RecPermissions in {}:").format(Fore.GREEN + absolute_path + Fore.RESET))
    print( Fore.GREEN + "  * " + Fore.RESET + _("Directories deleted: ") + Fore.YELLOW + localized_int(len(deleted_dirs)))
    print( Fore.GREEN + "  * " + Fore.RESET + _("Ignored symlinks: ") + Fore.YELLOW + localized_int(len(ignored_symlinks)))
    if len(error_directories)>0:
        print( Fore.GREEN + "  * " + Fore.RESET +  _("{} error files:").format(Fore.RED + localized_int(len(error_directories))+ Fore.RESET))
        for e in error_directories:
            print( Fore.RED + "     + " + Style.RESET_ALL + e)
    print( _("Executed at {}, took {}.").format(Fore.GREEN + str(datetime.now()) + Fore.RESET, Fore.GREEN + str(datetime.now()-start) + Fore.RESET))
