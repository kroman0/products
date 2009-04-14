import Globals
from Products.CMFCore.DirectoryView import registerDirectory
from AccessControl import allow_module

allow_module('Products.qSEOptimizer.util')

qSEO_globals = globals()
registerDirectory('skins', qSEO_globals)
