What is RecPermissions?
=======================
It's a script to change Linux permissions and ownership in one step. It can delete empty directories when necessary.

This script doesn't work on Windows.

Usage
=====

Here you have a console video example:

![English howto](https://raw.githubusercontent.com/Turulomio/recpermissions/master/doc/ttyrec/recpermissions_howto_en.gif)

Once installed, you can see man documentation with

`man recpermissions`

Links
=====

Doxygen documentation:
    http://turulomio.users.sourceforge.net/doxygen/recpermissions/

Pypi web page:
    https://pypi.org/project/recpermissions/

Gentoo ebuild
    If you use Gentoo you can find a ebuild in https://github.com/Turulomio/myportage/tree/master/app-admin/recpermissions

Dependencies
============
* https://www.python.org/, as the main programming language.
* https://pypi.org/project/colorama/, to give console colors.

Changelog
=========
1.9.0
-----
  * Solved bug when using Default None arguments.

1.8.0
-----
  * Improved colorized output.

1.7.0
-----
  * Fixed critical bug with symlinks

1.6.0
-----
  * Octal permissions string is now validated in --files and --directories
  * #15 Absoute path directory given as a paramater changes its permissios too

1.5.0
-----
  * Added frech translation

1.4.0
-----
  * Improved man pages
  * If recpermissions is executed on Windows, just exists script, instead of crash.
  * mangenerator is not needed for setup.py main script

1.3.0
-----
  * If file owner isn't in /etc/passwd now remains its uid, and desn't crash
  * Code of conduct is added to the project
  * Added localized integers in summary
  * Added files to french translation
  * Added --only parameter funcionality to allow change ownership and permissions of one file or directory

1.2.0
-----
  * Due to a boolean logic error, some changes didn't took place

1.1.0
-----
  * Added 30 seconds to reload video in howto.py
  * Nothing is changed if --user --group --files or --directories is not set.

1.0.0
-----
  * Version fully operational
  * Added howto video in English and Spanish
  * Man pages and spanish translation have been improved
  * Added summary and added io error exception catching

0.2.1
-----
  * Solved critical bug. Directory now is set tu absolut_path parameter

0.2.0
-----
  * Added absolute path parameter to avoid errors and wrong changes

0.1.1
-----
  * Solved bug in current path directory

0.1.0
-----
  * Creating infrastructure
