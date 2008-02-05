from Globals import package_home
from Products.Archetypes.public import process_types, listTypes
from Products.CMFCore import utils
from Products.CMFCore.DirectoryView import registerDirectory
import os, os.path
import PingInfo, PingTool 
from config import *





registerDirectory(SKINS_DIR, GLOBALS)

tools = ( PingTool.PingTool, )

def initialize(context):

    utils.ToolInit("PingTool", tools=tools, product_name=PROJECTNAME, icon=TOOL_ICON,
                  ).initialize(context)
    
    content_types, constructors, ftis = process_types(listTypes(PROJECTNAME), PROJECTNAME)

    utils.ContentInit(
        PROJECTNAME + ' Content',
        content_types      = content_types,
        permission         = ADD_PERMISSION,
        extra_constructors = constructors,
        fti                = ftis,
        ).initialize(context)

