from Products.CMFCore import utils
from Products.Archetypes.atapi import process_types, listTypes

from config import PROJECTNAME
from config import ADD_PERMISSION

def initialize(context):

    import field
    import validator

    content_types, constructors, ftis = process_types(listTypes(PROJECTNAME), PROJECTNAME)

    utils.ContentInit(
        PROJECTNAME + ' Content',
        content_types      = content_types,
        permission         = ADD_PERMISSION,
        extra_constructors = constructors,
        fti                = ftis,
        ).initialize(context)
