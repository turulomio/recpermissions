from datetime import datetime
from gettext import translation
from importlib.resources import files

try:
    t=translation('recpermissions', files("recpermissions") / 'locale')
    def _(s):
        return t.gettext(s)
except:
    def _(s):
        return s



__versiondatetime__=datetime(2025,9,28,8,42)
__versiondate__ = __versiondatetime__.date()
__version__ = '2.0.0'

def epilog():
    return _("Developed by Mariano Muñoz 2018-{}").format(__versiondate__.year  )