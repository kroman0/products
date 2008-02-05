from Products.Archetypes.public import *
from Products.CMFCore import utils
from Products.CMFCore.DirectoryView import registerDirectory
from config import *

#registerDirectory(SKINS_DIR, GLOBALS)

def initialize(context):

    import ShortMessage

    content_types, constructors, ftis = process_types(
                   listTypes(PROJECTNAME),
                   PROJECTNAME)

    utils.ContentInit(
                PROJECTNAME ,
                content_types      = content_types,
                permission         = ADD_CONTENT_PERMISSION,
                extra_constructors = constructors,
                fti                = ftis,
                ).initialize(context)