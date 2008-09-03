from Products.Archetypes.public import process_types, listTypes
from Products.CMFCore import utils
import PingInfo, PingTool
from config import *

tools = ( PingTool.PingTool, )

def initialize(context):
    from AccessControl import allow_module
    allow_module('Products.qPingTool.util')

    utils.ToolInit("PingTool", tools=tools, icon=TOOL_ICON,
                  ).initialize(context)

    content_types, constructors, ftis = process_types(listTypes(PROJECTNAME), PROJECTNAME)

    utils.ContentInit(
        PROJECTNAME + ' Content',
        content_types      = content_types,
        permission         = ADD_PERMISSION,
        extra_constructors = constructors,
        fti                = ftis,
        ).initialize(context)

