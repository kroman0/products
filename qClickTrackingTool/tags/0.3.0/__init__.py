from Products.Archetypes.public import *
from Products.CMFCore import utils
from Products.CMFCore.DirectoryView import registerDirectory
from config import *

from ClickTracker import ClickTracker

registerDirectory(SKINS_DIR, GLOBALS)

tools=(ClickTracker,)

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
		permission         = ADD_CONTENT_PERMISSION, 
		extra_constructors = constructors, 
		fti                = ftis,
                ).initialize(context)

