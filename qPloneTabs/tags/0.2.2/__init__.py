from AccessControl import allow_module
from Products.CMFCore.DirectoryView import registerDirectory

from Products.qPloneTabs.config import SKINS_DIR, GLOBALS

allow_module('Products.qPloneTabs.utils')
registerDirectory(SKINS_DIR, GLOBALS)

from Products.qPloneTabs.utils import getPortalTabs
from Products.qPloneTabs.utils import getRootTabs