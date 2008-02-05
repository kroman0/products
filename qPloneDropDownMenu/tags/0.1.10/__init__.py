from Products.CMFCore import utils
from Products.CMFCore.DirectoryView import registerDirectory

from Products.qPloneDropDownMenu.DropDownMenuTool import DropDownMenuTool
from Products.qPloneDropDownMenu.config import PROJECT_NAME, SKINS_DIR, GLOBALS, VIEW_PERMISSION

registerDirectory(SKINS_DIR, GLOBALS)
 
tools = (DropDownMenuTool,)
 
def initialize(context):
    utils.ToolInit( PROJECT_NAME,
                    tools = tools,
                    product_name = PROJECT_NAME,
                    icon='tool.gif'
                    ).initialize(context)