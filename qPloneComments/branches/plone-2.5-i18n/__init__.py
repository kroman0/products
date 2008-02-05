from Products.CMFCore.DirectoryView import registerDirectory
from AccessControl import allow_module, Permission

from  config import *
import patch

registerDirectory(SKINS_DIR, GLOBALS)

allow_module('Products.qPloneComments.config')
allow_module('Products.qPloneComments.utils')

Permission.registerPermissions((('Moderate Discussion', (), ('Manager',)),))