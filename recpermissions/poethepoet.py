from recpermissions import _, __version__
from os import system


def pytest():
    system("pytest")
    
def coverage():
    system("coverage run --omit='recpermissions/tests/*' -m pytest && coverage report && coverage html")




def release():
    print(_("New Release:"))
    print(_("  * Change version and date in version.py"))
    print(_("  * Edit Changelog in README"))
    print("  * python setup.py doc")
    print("  * mcedit locale/es.po")
    print("  * python setup.py doc")
    print("  * python setup.py install")
    print("  * python setup.py doxygen")
    print("  * mcedit doc/ttyrec/howto.py")
    print("  * python setup.py video" + ". " + _("If changed restart from first python setup.py doc"))
    print("  * git commit -a -m 'recpermissions-{}'".format(__version__))
    print("  * git push")
    print(_("  * Make a new tag in github"))
    print("  * python setup.py sdist upload -r pypi")
    print("  * python setup.py uninstall")
    print(_("  * Create a new gentoo ebuild with the new version and install it"))
    print(_("  * Upload to portage repository")) 

# class Uninstall(Command):
#     description = "Uninstall installed files with install"
#     user_options = []

#     def initialize_options(self):
#         pass

#     def finalize_options(self):
#         pass

#     def run(self):
#         if platform.system()=="Linux":
#             system("rm -Rf {}/recpermissions*".format(site.getsitepackages()[0]))
#             system("rm /usr/bin/recpermissions")
#             system("rm /usr/share/man/man1/recpermissions.1")
#             system("rm /usr/share/man/es/man1/recpermissions.1")
#         else:
#             print(_("Uninstall command only works in Linux"))

def translate():
    #es
    system("xgettext -L Python --no-wrap --no-location --from-code='UTF-8' -o recpermissions/locale/recpermissions.pot recpermissions/*.py")
    system("msgmerge -N --no-wrap -U recpermissions/locale/es.po recpermissions/locale/recpermissions.pot")
    system("msgmerge -N --no-wrap -U recpermissions/locale/fr.po recpermissions/locale/recpermissions.pot")
    system("msgfmt -cv -o recpermissions/locale/es/LC_MESSAGES/recpermissions.mo recpermissions/locale/es.po")
    system("msgfmt -cv -o recpermissions/locale/fr/LC_MESSAGES/recpermissions.mo recpermissions/locale/fr.po")


# def mangenerator():
#     for language in ["en", "es", "fr"]:
#         self.mangenerator(language)

#     def mangenerator_(self, language):
#         """
#             Create man pages for parameter language
#         """
#         from mangenerator import Man
#         if language=="en":
#             lang1=gettext.install('recpermissions', 'badlocale')
#             man=Man("man/man1/recpermissions")
#         else:
#             lang1=gettext.translation('recpermissions', 'recpermissions/locale', languages=[language])
#             lang1.install()
#             man=Man("man/{}/man1/recpermissions".format(language))
#         print("  - DESCRIPTION in {} is {}".format(language, _("DESCRIPTION")))

#         man.setMetadata("RecPermissions",  1,   datetime.date.today(), "Mariano Muñoz", _("Change files and directories owner and permissions recursively."))
#         man.setSynopsis("""usage: recpermissions [-h] [--version] [--user USER] [--group GROUP]
#                       [--files PERM] [--directories PERM] [--remove_emptydirs]
#                       [--only]
#                       absolute_path""")
#         man.header(_("DESCRIPTION"), 1)
#         man.paragraph(_("This app has the following mandatory parameters:"), 1)
#         man.paragraph("--user", 2, True)
#         man.paragraph(_("User used to change files owner.") + " " + _("It does nothing if it's not set"), 3)
#         man.paragraph("--group", 2, True)
#         man.paragraph(_("Group used to change files owner group.") + " " + _("It does nothing if it's not set"), 3)
#         man.paragraph("--files", 2, True)
#         man.paragraph(_("File permissions in octal to be used.") + " " + _("It does nothing if it's not set"), 3)
#         man.paragraph("--directories", 2, True)
#         man.paragraph(_("Directory permissions in octal to be used.") + " " + _("It does nothing if it's not set"), 3)
#         man.paragraph("--remove_emptydirs", 2, True)
#         man.paragraph(_("When used in script, removes all empty dirs recursively from path."), 3)
#         man.paragraph("--only", 2, True)
#         man.paragraph(_("Only changes permissions to the file or directory passed in absolute_path parameter."), 3)
#         man.paragraph("absolute_path", 2, True)
#         man.paragraph(_("To avoid errors and wrong changes, path must be an absolute one."), 3)  
#         man.header(_("EXAMPLES"), 1)
#         man.paragraph(_("Null Example"), 2, True)
#         man.paragraph(_("recpermissions /home/user/"), 3)
#         man.paragraph(_("This comand does nothing"), 3)
#         man.paragraph(_("Partial Example"), 2, True)
#         man.paragraph(_("recpermissions --user user --files 644 /home/user/"), 3)
#         man.paragraph(_("This command only changes user permissions and files permissions to 644. Group and directory permissions are not changed:"), 3)
#         man.paragraph(_("Full Example"), 2, True)
#         man.paragraph(_("recpermissions --user root --group root --files 640 --directories 750 --remove_emptydirs /home/user/"), 3)
#         man.paragraph(_("This command will change user and group to root user and group. Files will have rw-r----- permisions and directories rwxr-x--- permisions. If the script finds empty dirs it will remove them:"), 3)
#         man.paragraph(_("Only Example"), 2, True)
#         man.paragraph(_("recpermissions --user user /home/user/README.txt --only"), 3)
#         man.paragraph(_("This command will change user ownership to the file /home/usr/README.txt only"),  3)
#         man.save()

# def video():
#     print(_("You need ttyrecgenerator installed to generate videos"))
#     os.chdir("doc/ttyrec")
#     system("ttyrecgenerator --output recpermissions_howto_es 'python3 howto.py' --lc_all es_ES.UTF-8")
#     system("ttyrecgenerator --output recpermissions_howto_en 'python3 howto.py' --lc_all C")
#     os.chdir("../..")

    ########################################################################

