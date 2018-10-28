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

class Video(Command):
    description = "Create video/GIF from console ouput"
    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        os.chdir("doc/ttyrec")
        os.system("ttyrecgenerator --output recpermissions_howto_es 'python3 howto.py' --lc_all es_ES.UTF-8")
        os.system("ttyrecgenerator --output recpermissions_howto_en 'python3 howto.py' --lc_all C")
        os.chdir("../..")


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
        os.system("xgettext -L Python --no-wrap --no-location --from-code='UTF-8' -o locale/recpermissions.pot *.py recpermissions/*.py doc/ttyrec/*.py")
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

        man.setMetadata("recpermissions",  1,   datetime.date.today(), "Mariano Muñoz", _("Remove innecesary files or directories with a date and time pattern in the current directory."))
        man.setSynopsis("""[-h] [--version] (--create_example | --remove | --pretend)
                        [--pattern PATTERN] [--disable_log]
                        [--remove_mode {RemainFirstInMonth,RemainLastInMonth}]
                        [--too_young_to_delete TOO_YOUNG_TO_DELETE]
                        [--max_files_to_store MAX_FILES_TO_STORE]""")
        man.header(_("DESCRIPTION"), 1)
        man.paragraph(_("This app has the following mandatory parameters:"), 1)
        man.paragraph("--create_example", 2, True)
        man.paragraph(_("Create two directories called 'example' and 'example_directories' in the current working directory and fill it with example files with date and time patterns."), 3)
        man.paragraph("--pretend", 2, True)
        man.paragraph(_("Makes a simulation selecting which files will be deleted when --remove parameter is used."), 3)
        man.paragraph("--remove", 2, True)
        man.paragraph(_("Deletes files. Be careful, This can't be unmade. Use --pretend before."), 3)
        
        man.paragraph(_("With --pretend and --remove you can use this parameters:"), 1)
        man.paragraph("--pattern", 2, True)
        man.paragraph(_("Sets the date and time pattern to search in the current directory filenames. It uses python strftime function format."), 3)
        man.paragraph("--disable_log", 2, True)
        man.paragraph("--remove_mode", 2, True)
        man.paragraph("--too_young_to_delete", 2, True)
        man.paragraph("--max_files_to_store", 2, True)
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
               'video': Video, 
             },
    zip_safe=False,
    include_package_data=True
    )

_=gettext.gettext#To avoid warnings
