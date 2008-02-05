from AccessControl import allow_module
from Products.CMFCore import utils
from Products.CMFCore.DirectoryView import registerDirectory

from Products.Archetypes.public import process_types, listTypes

from Products.qSiloGroup.config import *

registerDirectory(SKINS_DIR, GLOBALS)

allow_module('Products.qSiloGroup.utils')

def initialize(context):
    ##Import Types here to register them
    from Products.qSiloGroup import SiloSiteMap

    content_types, constructors, ftis = process_types(
        listTypes(PROJECTNAME),
        PROJECTNAME)

    utils.ContentInit(
        PROJECTNAME + ' Content',
        content_types      = content_types,
        permission         = VIEW_PERMISSION,
        extra_constructors = constructors,
        fti                = ftis,
        ).initialize(context)