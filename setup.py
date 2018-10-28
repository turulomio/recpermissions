from setuptools import setup, Command
from mangenerator import Man

import datetime
import gettext
import os
import platform
import site

class Doxygen(Command):
    description = "Create/update doxygen documentation in doc/html"
    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        print("Creating Doxygen Documentation")
        os.system("""sed -i -e "41d" doc/Doxyfile""")#Delete line 41
        os.system("""sed -i -e "41iPROJECT_NUMBER         = {}" doc/Doxyfile""".format(__version__))#Insert line 41
        os.system("rm -Rf build")
        os.chdir("doc")
        os.system("doxygen Doxyfile")
        os.system("rsync -avzP -e 'ssh -l turulomio' html/ frs.sourceforge.net:/home/users/t/tu/turulomio/userweb/htdocs/doxygen/recpermissions/ --delete-after")
        os.chdir("..")


class Uninstall(Command):
    description = "Uninstall installed files with install"
    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        if platform.system()=="Linux":
            os.system("rm -Rf {}/recpermissions*".format(site.getsitepackages()[0]))
            os.system("rm /usr/bin/recpermissions")
            os.system("rm /usr/share/man/man1/recpermissions.1")
            os.system("rm /usr/share/man/es/man1/recpermissions.1")
        else:
            print(_("Uninstall command only works in Linux"))

class Doc(Command):
    description = "Update man pages and translations"
    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        #es
        os.system("xgettext -L Python --no-wrap --no-location --from-code='UTF-8' -o locale/recpermissions.pot *.py recpermissions/*.py")
        os.system("msgmerge -N --no-wrap -U locale/es.po locale/recpermissions.pot")
        os.system("msgfmt -cv -o recpermissions/locale/es/LC_MESSAGES/recpermissions.mo locale/es.po")

        for language in ["en", "es"]:
            self.mangenerator(language)

    def mangenerator(self, language):
        """
            Create man pages for parameter language
        """
        if language=="en":
            gettext.install('recpermissions', 'badlocale')
            man=Man("man/man1/recpermissions")
        else:
            lang1=gettext.translation('recpermissions', 'recpermissions/locale', languages=[language])
            lang1.install()
            man=Man("man/es/man1/recpermissions")
        print("  - DESCRIPTION in {} is {}".format(language, _("DESCRIPTION")))

        man.setMetadata("RecPermissions",  1,   datetime.date.today(), "Mariano Muñoz", _("Change files and directories owner and permissions recursively."))
        man.setSynopsis("""usage: recpermissions [-h] [--version] [--user USER] [--group GROUP]
                      [--files FILES] [--directories DIRECTORIES]
                      [--remove_empty_directories] path""")
        man.header(_("DESCRIPTION"), 1)
        man.paragraph(_("This app has the following mandatory parameters:"), 1)
        man.paragraph("--user", 2, True)
        man.paragraph(_("User used to change files owner."), 3)
        man.paragraph("--group", 2, True)
        man.paragraph(_("Group used to change files owner group."), 3)
        man.paragraph("--files", 2, True)
        man.paragraph(_("File permissions in octal to be used. 644 by default."), 3)
        man.paragraph("--directories", 2, True)
        man.paragraph(_("Directory permissions in octal to be used. 755 by default."), 3)
        man.paragraph("--remove_emptydirs", 2, True)
        man.paragraph(_("When used in script, removes all empty dirs recursively from path."), 3)  
        man.paragraph("absolute_path", 2, True)
        man.paragraph(_("To avoid errors and wrong changes, path must be an absolute one."), 3)  
        man.save()

    ########################################################################


## Version of modele captured from version to avoid problems with package dependencies
__version__= None
with open('recpermissions/version.py', encoding='utf-8') as f:
    for line in f.readlines():
        if line.find("__version__ =")!=-1:
            __version__=line.split("'")[1]


with open('README.md', encoding='utf-8') as f:
    long_description = f.read()

if platform.system()=="Linux":
    data_files=[('/usr/share/man/man1/', ['man/man1/recpermissions.1']), 
                ('/usr/share/man/es/man1/', ['man/es/man1/recpermissions.1'])
               ]
else:
    data_files=[]

setup(name='recpermissions',
    version=__version__,
    description='Change files and directories permisions and owner recursivily from current directory',
    long_description=long_description,
    long_description_content_type='text/markdown',
    classifiers=['Development Status :: 4 - Beta',
              'Intended Audience :: Developers',
              'Topic :: Software Development :: Build Tools',
              'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
              'Programming Language :: Python :: 3',
             ], 
    keywords='change permissions ownner files directories',
    url='https://github.com/Turulomio/recpermissions',
    author='Turulomio',
    author_email='turulomio@yahoo.es',
    license='GPL-3',
    packages=['recpermissions'],
    entry_points = {'console_scripts': ['recpermissions=recpermissions.core:main',
                                       ],
                   },
    install_requires=['colorama','setuptools'],
    data_files=data_files,
    cmdclass={ 'doxygen': Doxygen,
               'doc': Doc,
               'uninstall':Uninstall, 
             },
    zip_safe=False,
    include_package_data=True
    )

_=gettext.gettext#To avoid warnings
