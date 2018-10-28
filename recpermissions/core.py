import argparse
from colorama import Fore, Style
import os

## TooManyFiles main script
## If arguments is None, launches with sys.argc parameters. Entry point is toomanyfiles:main
## You can call with main(['--pretend']). It's equivalento to os.system('toomanyfiles --pretend')
## @param arguments is an array with parser arguments. For example: ['--max_files_to_store','9']. 
def main(arguments=None):
    parser=argparse.ArgumentParser(prog='toomanyfiles', description=_('Search date and time patterns to delete innecesary files or directories'), epilog=_("Developed by Mariano Muñoz 2018-{}".format(__versiondate__.year)), formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument('--version', action='version', version=__version__)

    parser.add_argument('--user', help=_("File owner will be changed to this user"), action="store", default=os.getlogin())
    parser.add_argument('--group', help=_("Disable log generation. The default value is '%(default)s'."),action="store_true", default=False)
    parser.add_argument('--files', help=_("Remove mode. The default value is '%(default)s'."), choices=['RemainFirstInMonth','RemainLastInMonth'], default='RemainFirstInMonth')
    parser.add_argument('--directories', help=_("Number of days to respect from today. The default value is '%(default)s'."), default=30)
    parser.add_argument('--remove_empty_directories', help=_("Maximum number of files to remain in directory. The default value is '%(default)s'."), default=100000000)

    args=parser.parse_args(arguments)

    colorama.init(autoreset=True)



    if args.create_examples==True:
        create_examples()
        sys.exit(ExitCodes.Success)
