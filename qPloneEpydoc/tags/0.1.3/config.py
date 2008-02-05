# Author: Melnychuk Taras
# Contact: fenix@quintagroup.com
# Date: $Date: 2005-11-23 12:34:55
# Copyright: quintagroup.com

from Products.CMFCore.CMFCorePermissions import AddPortalContent, ManagePortal
import os

SKINS_DIR = 'skins'
DOCUMENTATION_DIR = 'documentation'
GLOBALS = globals()
PROJECTNAME = 'qPloneEpydoc'
TOOL_PERMISSION = AddPortalContent
MANAGE_TOOL_PERMISSION = ManagePortal
ARCHETYPENAME = 'portal_epydoc'
TOOLID = 'portal_documentation'
INSTANCE_HOME = os.environ.get("INSTANCE_HOME")
DOCUMENTATION_PATH = "%s/Products/%s/documentation/" %(INSTANCE_HOME, PROJECTNAME)
PRODUCTS_HOME = INSTANCE_HOME+'/Products/'