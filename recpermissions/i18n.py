from gettext import translation
from importlib.resources import files

try:
    # Attempt to load translations
    t = translation('recpermissions', files("recpermissions") / 'locale')
    def _(s):
        return t.gettext(s)
except:
    # Fallback if translations are not found (e.g., during development or if locale files are missing)
    def _(s):
        return s