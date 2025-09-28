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


def translate():
    #es
    system("xgettext -L Python --no-wrap --no-location --from-code='UTF-8' -o recpermissions/locale/recpermissions.pot recpermissions/*.py")
    system("msgmerge -N --no-wrap -U recpermissions/locale/es.po recpermissions/locale/recpermissions.pot")
    system("msgmerge -N --no-wrap -U recpermissions/locale/fr.po recpermissions/locale/recpermissions.pot")
    system("msgfmt -cv -o recpermissions/locale/es/LC_MESSAGES/recpermissions.mo recpermissions/locale/es.po")
    system("msgfmt -cv -o recpermissions/locale/fr/LC_MESSAGES/recpermissions.mo recpermissions/locale/fr.po")

