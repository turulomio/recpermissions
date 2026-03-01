from datetime import datetime
from platform import system as platform_system
from sys import exit, version_info
from argparse import ArgumentParser, RawTextHelpFormatter
from locale import LC_ALL, getlocale, setlocale
from os import chmod, path, rmdir, walk
from colorama import Fore, Style, init as colorama_init # type: ignore
from recpermissions import __versiondate__, __version__, epilog
from recpermissions.i18n import _ # Import the translation function
from recpermissions.commons import is_dir_empty, is_uid_or_gid, is_octal_string_permissions_valid, path_object, process
from recpermissions.types import Returns


if platform_system()=="Windows":
    print("This script only works on Linux")
    exit(1)


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
        
        
    processed=[]

    #Process absolute path
    processed.append(process(path_object(absolute_path), user, group, files, directories))
    for dirpath, dirnames, filenames in walk(absolute_path):
        # Process directories
        for d in dirnames:
            p=path.join(dirpath, d) # Full path to the directory
            processed.append(process(path_object(p), user, group, files, directories))

        #Iterate files
        for f in filenames:
            p=path.join(dirpath, f) 
            # print(p)
            processed.append(process(path_object(p), user, group, files, directories))


    dirs=sum(1 for item in  processed if item.get('type') == 'dir')
    files=sum(1 for item in processed if item.get('type') == 'file')
    changed_dirs_ownership=sum(1 for item in processed if item.get('ownership_change') == Returns.Changed and item.get('type') =="dir") 
    changed_dirs_permissions=sum(1 for item in processed if item.get('permissions_change') == Returns.Changed and item.get('type') =="dir") 
    changed_files_ownership=sum(1 for item in processed if item.get('ownership_change') == Returns.Changed and item.get('type') =="file") 
    changed_files_permissions=sum(1 for item in processed if item.get('permissions_change') == Returns.Changed and item.get('type') =="file")
    ignored_symlinks=sum(1 for item in processed if item.get('type') == 'link')
    print( _("RecPermissions in {}:").format(Fore.GREEN + absolute_path + Fore.RESET))
    print( Fore.GREEN + "  * " + Fore.RESET + _("Directories found: ") + Fore.YELLOW + str(dirs))
    print( Fore.GREEN + "  * " + Fore.RESET + _("Files found: ") + Fore.YELLOW + str(files))
    print( Fore.GREEN + "  * " + Fore.RESET + _("Directories ownership changed: ") + Fore.YELLOW + str(changed_dirs_ownership))
    print( Fore.GREEN + "  * " + Fore.RESET + _("Files ownership changed: ") + Fore.YELLOW + str(changed_files_ownership))
    print( Fore.GREEN + "  * " + Fore.RESET + _("Directories permissions changed: ") + Fore.YELLOW + str(changed_dirs_permissions))
    print( Fore.GREEN + "  * " + Fore.RESET + _("Files permissions changed: ") + Fore.YELLOW + str(changed_files_permissions))
    print( Fore.GREEN + "  * " + Fore.RESET + _("Ignored symlinks: ") + Fore.YELLOW + str(ignored_symlinks))


    errors=[]
    for o in processed:
        if o["ownership_change"]==Returns.Error:
            errors.append(o["ownership_text"])
        if o["permissions_change"]==Returns.Error:
            errors.append(o["permissions_text"])


    if len(errors)>0:
        print( Fore.GREEN + "  * " + Fore.RESET +  _("{} error files:").format(Fore.RED + str(len(errors))+ Fore.RESET))
        for e in errors:
            print( Fore.RED + "     + " + Style.RESET_ALL + e)
    print( _("Executed at {}, took {}.").format(Fore.GREEN + str(datetime.now()) + Fore.RESET, Fore.GREEN + str(datetime.now()-start) + Fore.RESET))


def main_remove_empty_directories():
    parser=ArgumentParser(prog='recpermissions', description=_('Removes empty directories'), epilog=epilog(), formatter_class=RawTextHelpFormatter)
    parser.add_argument('--version', action='version', version=__version__)
    parser.add_argument('--pretend', help=_("Only changes permissions to the file or directory passed in absolute_path parameter."), action="store_true", default=False)
    parser.add_argument('absolute_path', help=_("Directory who is going to be changed permissions and owner recursivily"), action="store")

    args=parser.parse_args()

    colorama_init(autoreset=True)

    remove_empty_directories(args.pretend, args.absolute_path)


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


    deleted_dirs=[]
    error_directories=[]
    ignored_symlinks=0

    #Generate list of files and directories

    #Iterate list of dirs
    for dirpath, dirnames, files in walk(absolute_path):
        for d in dirnames:
            p = path.join(dirpath,  d)
            if path.islink(p)==True:
                ignored_symlinks+=1
                continue
            if path.exists(p)==False:
                error_directories.append(p)
                continue

            if is_dir_empty(p):
                if pretend:
                    deleted_dirs.append(p) # Add to list for reporting in pretend mode
                else:
                    try:
                        rmdir(p)
                        deleted_dirs.append(p) # Add to list only if successfully deleted
                    except:
                        error_directories.append(p)                


    print( _("RecPermissions in {}:").format(Fore.GREEN + absolute_path + Fore.RESET))
    print( Fore.GREEN + "  * " + Fore.RESET + _("Directories deleted: ") + Fore.YELLOW + str(len(deleted_dirs)))
    print( Fore.GREEN + "  * " + Fore.RESET + _("Ignored symlinks: ") + Fore.YELLOW + str(ignored_symlinks))
    if len(deleted_dirs)>0:
        if (pretend):
            print( Fore.GREEN + "  * " + Fore.RESET +  _("{} deleted dirs (pretend):").format(Fore.GREEN + str(len(deleted_dirs))+ Fore.RESET))
        else:
            print( Fore.GREEN + "  * " + Fore.RESET +  _("{} deleted dirs:").format(Fore.GREEN + str(len(deleted_dirs))+ Fore.RESET))
        for d in deleted_dirs:
            print( Fore.GREEN + "     + " + Style.RESET_ALL + d)
    if len(error_directories)>0:
        print( Fore.GREEN + "  * " + Fore.RESET +  _("{} errors:").format(Fore.RED + str(len(error_directories))+ Fore.RESET))
        for e in error_directories:
            print( Fore.RED + "     + " + Style.RESET_ALL + e)
    print( _("Executed at {}, took {}.").format(Fore.GREEN + str(datetime.now()) + Fore.RESET, Fore.GREEN + str(datetime.now()-start) + Fore.RESET))
