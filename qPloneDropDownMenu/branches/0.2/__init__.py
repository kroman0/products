from Products.CMFCore import utils
from Products.CMFCore.DirectoryView import registerDirectory

from Products.qPloneDropDownMenu.DropDownMenuTool import DropDownMenuTool
from Products.qPloneDropDownMenu.config import *

registerDirectory(SKINS_DIR, GLOBALS)

tools = (DropDownMenuTool,)

def initialize(context):
    utils.ToolInit(PROJECTNAME,
                   tools = tools,
                   product_name = PROJECTNAME,
                   icon='tool.gif'
                   ).initialize(context)