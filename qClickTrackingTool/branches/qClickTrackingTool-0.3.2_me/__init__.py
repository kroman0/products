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
            [v for v in listTypes(PROJECTNAME) if v['name'] != 'Campaign'],
	    PROJECTNAME)

    utils.ContentInit( 
		PROJECTNAME + ' Content', 
		content_types      = content_types, 
		permission         = ADD_CAMPAIGN_PERMISSION, 
		extra_constructors = constructors, 
		fti                = ftis,
                ).initialize(context)

import sys
import Products.qClickTrackingTool.legacy.Campaign
 #change module alias
sys.modules['Products.qClickTrackingTool.Campaign'] = legacy.Campaign