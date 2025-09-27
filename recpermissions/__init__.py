from datetime import datetime
from gettext import translation
from importlib.resources import files

try:
    t=translation('toomanyfiles', files("toomanyfiles/") / 'locale')
    def _(s):
        return t.gettext(s)
except:
    _=str


__versiondatetime__=datetime.now()
__versiondate__ = __versiondatetime__.date()
__version__ = '1.10.1'

def epilog():
    return _("Developed by Mariano Muñoz 2018-{}").format(__versiondate__.year  )