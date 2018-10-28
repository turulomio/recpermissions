What is RecPermissions
======================
It's a script to change permissions and owner recursivily from current directory. It can delete empty directories when necessary.

Usage
=====

Basic Example
-------------

This command will change user and group to current user and to current user main group. Files will have rw-r--r-- permisions and directories rwxr-xr-x permisions. If the script finds empty dirs it will NOT remove them:

`recpermissions --path /home/user/`

Full Example
------------

This command will change user and group to root user and group. Files will have rw-r----- permisions and directories rwxr-x--- permisions. If the script finds empty dirs it will remove them:

`recpermissions --user root --group root --files 640 --directories 750 --remove_emptydirs --path /home/user/`

License
=======
GPL-3

Links
=====

Source code & Development:
    https://github.com/Turulomio/recpermissions

Doxygen documentation:
    http://turulomio.users.sourceforge.net/doxygen/recpermissions/

Main developer web page:
    http://turulomio.users.sourceforge.net/en/proyectos.html
    
Pypi web page:
    https://pypi.org/project/recpermissions/

Gentoo ebuild
    You can find a Gentoo ebuild in https://sourceforge.net/p/xulpymoney/code/HEAD/tree/myportage/app-admin/recpermissions/


Dependencies
============
* https://www.python.org/, as the main programming language.
* https://pypi.org/project/colorama/, to give console colors.

Changelog
=========
0.2.1
  * Solved critical bug. Directory now is set tu absolut_path parameter

0.2.0
  * Added absolute path parameter to avoid errors and wrong changes

0.1.1
  * Solved bug in current path directory

0.1.0
  * Creating infrastructure
