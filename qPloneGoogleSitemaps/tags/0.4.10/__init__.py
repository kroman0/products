import Globals

from Products.CMFCore.DirectoryView import registerDirectory
from AccessControl import allow_module

registerDirectory('skins', globals())
qPGS_globals = globals()

allow_module('Products.qPloneGoogleSitemaps.utils.py')
allow_module('Products.qPloneGoogleSitemaps.config.py')