# Author: Melnychuk Taras
# Contact: fenix@quintagroup.com
# Date: $Date: 2005-11-23 12:34:02
# Copyright: quintagroup.com

import epydoc_patch
from Products.Archetypes.public import *
from Products.CMFCore import utils
from Products.CMFCore.DirectoryView import registerDirectory
from config import *

from PloneEpydoc import PloneEpydoc

registerDirectory(SKINS_DIR, GLOBALS)
registerDirectory(DOCUMENTATION_DIR, GLOBALS)

tools=(PloneEpydoc,)

def initialize(context):
    utils.ToolInit(PROJECTNAME,
                   tools=tools,
                   product_name=PROJECTNAME,
                   icon= "tool.gif",
                  ).initialize(context)

    content_types, constructors, ftis = process_types(
        listTypes(PROJECTNAME),
        PROJECTNAME)

    utils.ContentInit( 
        PROJECTNAME + ' Content', 
        content_types      = content_types, 
        permission         = TOOL_PERMISSION, 
        extra_constructors = constructors, 
        fti                = ftis,
                ).initialize(context)