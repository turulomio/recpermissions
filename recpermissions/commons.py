from grp import getgrgid
from os import chmod, path, stat, scandir
from pwd import getpwuid
from shutil import chown
from recpermissions import __versiondate__, __version__
from recpermissions.i18n import _ # Import the translation function
from recpermissions.types import Returns
from stat import ST_MODE



def epilog():
    return _("Developed by Mariano Muñoz 2018-{}").format(__versiondate__.year  )

## Check if a directory is empty
## @param dir String with the directory to check
## @return boolean
def is_dir_empty(dir):
    """Check if the given directory path is empty."""
    # os.scandir returns an iterator. any() checks if the iterator yields any item.
    # The 'with' statement ensures the iterator is properly closed.
    if not path.isdir(dir):
        # Handle cases where the path is not a directory or doesn't exist
        return False
                        
    with scandir(dir) as entries:
        return not any(entries)

## Gets octal string permissions from a file
## @param path String with the path. Can be a dir or a file
## @return string "644" or "755", for example
def get_octal_string_permissions(path):
    try:
        return oct(stat(path)[ST_MODE])[-3:]
    except:
        return None


## Sets octal string permissions to a file
## @param path String with the path. Can be a dir or a file
## @param octal String with octal permissions. "644" or "755" for example
## @return Boolean if file has been changed
def set_octal_string_permissions(o, octal):
    if octal==None:        
        o["permissions_change"]=Returns.Error
        o["permissions_text"]= _("Octal string is None")
        return o
    if o["permissions"]==octal: 
        o["permissions_change"]=Returns.Ignored
        o["permissions_text"]=  _("Permissions haven't changed")
        return o
    else:   
        try:
            chmod(o["path"], int(octal, 8))
            o["permissions_change"]=Returns.Changed
            o["permissions_text"]= _("Permissions have changed")   
            return o
        except Exception as e:
            o["permissions_change"]=Returns.Error
            o["permissions_text"]= _("Error changing permissions: {}").format(e)   
            return o



## Returns if the octal string has valid octal permissions
## @param octal String with octal permissions. "644" or "755" for example
## @return Boolean if the octal string is valid
def is_octal_string_permissions_valid(octal):
    if octal==None: #Is valid but set function just ignore it
         return True
    if len(octal)==3 and octal.isdigit()==True and octal.find("9")==-1:
         return True
    return False

## Gets user and root from a path
## @param path String with the path. Can be a dir or a file
## @return a tuple (root, root), for example. If uid of the file isn't in /etc/passwd, returns uid and gid
def get_file_ownership(p):
    try:
        return (getpwuid(stat(p).st_uid).pw_name, getgrgid(stat(p).st_gid).gr_name)
    except:
        return (None,None)

## Set file user and grup
## @param path String with the path. Can be a dir or a file
## @param user String or None. If none it doesn't change the user
## @param group String or None. If none it doesn't change the group
## @return Boolean if file has been changed
def set_file_ownership(o, user, group):
    if (user, group)==(None, None):
        o["ownership_change"]=Returns.Error
        o["ownership_text"]=_("User and group are None")
        return o
    if (o["user"], o["group"])==(user, group):
        o["ownership_change"]=Returns.Ignored
        o["ownership_text"]=_("Ownership hasn't changed")
        return o
    else:
        # user=tuple[0] if user==None else user
        # group=tuple[1] if group==None else group
        try:
            chown(o["path"], user, group)
            o["ownership_change"]=Returns.Changed
            o["ownership_text"]=_("Ownership has changed")
            return o
        except Exception as e:        
            o["ownership_change"]=Returns.Error
            o["ownership_text"]=_("Error changing ownership: {}").format(e)
            return o


def process(o,user,group,files,directories):
    o=set_file_ownership(o, user, group)
    if o["type"]=="dir":
        o=set_octal_string_permissions(o, directories)
    elif o["type"]=="file":
        o=set_octal_string_permissions(o, files)
    return o


## Returns if a string can be casted to integer. Used to detect if owner is a uid or gid
## @param s String
## @return boolean
def is_uid_or_gid(s):
    if s==None:
        return False
    try:
        int(s)
        return True
    except:
        return False
    




def path_object(p):
    """
        Gets path atributes to be reused
    """
    if p is None:
        type_= None
    elif not path.exists(p):
        type_= None
    elif path.islink(p):
        type_= "link"
    elif path.isdir(p):
        type_= "dir"
    elif path.isfile(p):
        type_= "file"
    else:
        type_= "unknown"

    user, group=get_file_ownership(p)


    return {
        "path": p,
        "type": type_,
        "permissions": get_octal_string_permissions(p),
        "user": user,
        "group": group,
        "ownership_change": None,
        "permissions_change": None,
        "ownership_text": None,
        "permissions_text": None,
    }
