from Products.CMFCore.DirectoryView import registerDirectory
from config import GLOBALS
from AccessControl import allow_module

allow_module('Products.qPloneCaptchas.utils')
allow_module('Products.qPloneCaptchas.config')

registerDirectory('skins', GLOBALS)