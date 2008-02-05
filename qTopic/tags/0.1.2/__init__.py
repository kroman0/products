from Products.Archetypes.public import process_types, listTypes
from Products.CMFCore import utils
from Products.CMFCore.DirectoryView import registerDirectory, registerFileExtension

from config import *

registerDirectory(SKINS_DIR, GLOBALS)

def initialize(context):
    ##Import Types here to register them
    from qTopic import qTopic
    from zLOG import LOG

    content_types, constructors, ftis = process_types(
        listTypes(PROJECTNAME),
        PROJECTNAME)
    LOG('*',0, str(content_types), PROJECTNAME)

    utils.ContentInit(
        PROJECTNAME + ' Content',
        content_types      = content_types,
        permission         = ADD_TOPIC_PERMISSION,
        extra_constructors = constructors,
        fti                = ftis,
        ).initialize(context)

