from Globals import package_home
from Products.Archetypes.public import process_types, listTypes
from Products.CMFCore import utils
from Products.CMFCore.DirectoryView import registerDirectory
import os, os.path
import TrackSpamTool 
from config import *

registerDirectory(SKINS_DIR, GLOBALS)

tools = ( TrackSpamTool.TrackSpamTool, )

def initialize(context):

    utils.ToolInit("TrackSpamTool",
                    tools=tools,
                    product_name=PROJECTNAME,
                    icon=TOOL_ICON,
                  ).initialize(context)

#     content_types, constructors, ftis = process_types(listTypes(PROJECTNAME), PROJECTNAME)
# 
#     utils.ContentInit(
#         PROJECTNAME + ' Content',
#         content_types      = content_types,
#         permission         = 'Manage Portal',
#         extra_constructors = constructors,
#         fti                = ftis,
#         ).initialize(context)

