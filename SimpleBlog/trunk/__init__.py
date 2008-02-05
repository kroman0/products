from Globals import package_home
from Products.Archetypes.public import process_types, listTypes
from Products.CMFCore import utils
from Products.CMFCore.DirectoryView import registerDirectory
import os, os.path, sys, content

from Products.CMFCore.utils import ContentInit
from Products.CMFCore.utils import ToolInit

from config import SKINS_DIR, GLOBALS, PROJECTNAME

from Globals import InitializeClass

registerDirectory(SKINS_DIR, GLOBALS)

from Products.SimpleBlog.Permissions import wireAddPermissions

# Module aliases - we don't always get it right on the first try, but and we
# can't move modules around because things are stored in the ZODB with the
# full module path. However, we can create aliases for backwards compatability.

sys.modules['Products.SimpleBlog.Blog'] = content.blog
sys.modules['Products.SimpleBlog.BlogEntry'] = content.blogentry
sys.modules['Products.SimpleBlog.BlogFolder'] = content.blogfolder
sys.modules['Products.SimpleBlog.TrackBack'] = content.trackback

def initialize(context):

    ## Allow module utils
    from AccessControl import ModuleSecurityInfo, allow_module
    ModuleSecurityInfo('Products.SimpleBlog.util').declarePublic('addTrackBack')
    ModuleSecurityInfo('Products.SimpleBlog.util').declarePublic('encodeURLData')

    from content import BlogEntry
    from content import Blog
    from content import BlogFolder
    from content import TrackBack


    listOfTypes = listTypes(PROJECTNAME)

    content_types, constructors, ftis = process_types(
        listOfTypes,
        PROJECTNAME)

    from Products.SimpleBlog.Permissions import permissions
    
    allTypes = zip(content_types, constructors)
    wireAddPermissions()
    for atype, constructor in allTypes:
        kind = "%s: %s" % (PROJECTNAME, atype.archetype_name)
        ContentInit(
            kind,
            content_types      = (atype,),
            permission         = permissions[atype.portal_type],
            extra_constructors = (constructor,),
            fti                = ftis,
            ).initialize(context)

        
    from SimpleBlogTool import SimpleBlogManager
    utils.ToolInit(
        'SimpleBlog manager', 
        tools=(SimpleBlogTool.SimpleBlogManager,),  
        product_name='SimpleBlog', 
        icon='tool.gif', ).initialize(context)
    

    