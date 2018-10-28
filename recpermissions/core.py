import argparse
from colorama import Fore, Style, init as colorama_init
from recpermissions.version import __versiondate__, __version__
import gettext
import os
import pwd
import shutil
import grp


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

## recpermissions main script
## If arguments is None, launches with sys.argc parameters. Entry point is recpermissions:main
## You can call with main(['--pretend']). It's equivalento to os.system('recpermissions --pretend')
## @param arguments is an array with parser arguments. For example: ['--max_files_to_store','9']. 
def main(arguments=None):
    parser=argparse.ArgumentParser(prog='recpermissions', description=_('Search date and time patterns to delete innecesary files or directories'), epilog=_("Developed by Mariano Muñoz 2018-{}".format(__versiondate__.year)), formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument('--version', action='version', version=__version__)

    parser.add_argument('--user', help=_("File owner will be changed to this parameter. Default user is '%(default)s'"), action="store", default=os.environ['USER'])
    parser.add_argument('--group', help=_("File owner group will be changed to this parameter. The default value is '%(default)s'."), action="store", default=grp.getgrgid(os.getgid()).gr_name)
    parser.add_argument('--files', help=_("File permissions to set in all files. The default value is '%(default)s'."), default='644', metavar='PERM')
    parser.add_argument('--directories', help=_("Directory permissions to set in all directories. The default value is '%(default)s'."), default='755', metavar='PERM')
    parser.add_argument('--remove_emptydirs', help=_("If it's established, removes empty directories recursivily from current path."), action="store_true", default=False)

    args=parser.parse_args(arguments)

    colorama_init(autoreset=True)

    changedOwners=0
    changedPermissions=0
    deletedDirs=0

    decimal_value_files=int(args.files,8)
    decimal_value_dirs=int(args.directories,8)
    print(decimal_value_files, args.files)

    uid = pwd.getpwnam(args.user).pw_uid
    gid = grp.getgrnam(args.group).gr_gid

    for (dirpath, dirnames, filenames) in os.walk(os.getcwd()+"/recpermissions"):
        for d in dirnames:
            dirname= os.path.join(dirpath, d)
            shutil.chown(dirname, args.user, args.group)
            os.chmod(dirname, decimal_value_dirs)
            if is_dir_empty(dirname):
                os.rmdir(dirname)
                deletedDirs=deletedDirs+1
        for f in filenames:
            filename= os.path.join(dirpath, f)
            shutil.chown(filename, args.user, args.group)
            os.chmod(filename, decimal_value_files)

    if deletedDirs>0:
        print(_("{} empty dirs were removed").format(deletedDirs))