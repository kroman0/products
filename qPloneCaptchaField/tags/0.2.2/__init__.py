from Products.CMFCore import utils
from Products.CMFCore.interfaces import ISiteRoot
from Products.CMFCore.DirectoryView import registerDirectory
from Products.Archetypes.atapi import process_types, listTypes
from Products.GenericSetup import EXTENSION, profile_registry

from permissions import ADD_PERMISSION
from config import *
import validators
import content

registerDirectory(SKINS_DIR, GLOBALS)

def initialize(context):

    content_types, constructors, ftis = process_types(listTypes(PROJECTNAME), PROJECTNAME)

    utils.ContentInit(
        PROJECTNAME + ' Content',
        content_types      = content_types,
        permission         = ADD_PERMISSION,
        extra_constructors = constructors,
        fti                = ftis,
        ).initialize(context)

    profile_desc = "Installs CaptchaField content type."
    profile_registry.registerProfile('default',
                                      PROJECTNAME,
                                      profile_desc,
                                     'profiles/default',
                                      PROJECTNAME,
                                      EXTENSION,
                                      for_=ISiteRoot,
                                    )