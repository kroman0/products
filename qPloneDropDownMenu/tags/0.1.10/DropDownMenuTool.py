from Globals import InitializeClass
from OFS.SimpleItem import SimpleItem
from AccessControl import ClassSecurityInfo
 
from Products.CMFCore.utils import UniqueObject, getToolByName

from Products.qPloneDropDownMenu.Extensions.Install import updateMenu
from config import VIEW_PERMISSION, PROJECT_NAME, UNIQUE_ID


class DropDownMenuTool(UniqueObject, SimpleItem):

    meta_type = 'DropDownMenu Tool'
    id = UNIQUE_ID
    title="DropDown Menu Tool"

    security = ClassSecurityInfo()

    security.declareProtected(VIEW_PERMISSION, 'regenerateMenu')
    def regenerateMenu(self):
        updateMenu(self)

InitializeClass(DropDownMenuTool)