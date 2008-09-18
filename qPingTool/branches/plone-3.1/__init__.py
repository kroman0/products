from zope.i18nmessageid import MessageFactory
from Products.Archetypes.public import process_types, listTypes
from Products.CMFCore import utils

qPingToolMessageFactory = MessageFactory('qPingTool')

import PingInfo, PingTool
from config import *

tools = ( PingTool.PingTool, )

def initialize(context):
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

