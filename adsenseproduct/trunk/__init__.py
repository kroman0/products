from Products.CMFCore.DirectoryView import registerDirectory
from config import GLOBALS

registerDirectory('skins', GLOBALS)

def initialize(context):
    from AccessControl import allow_module
    allow_module('Products.adsenseproduct.util')