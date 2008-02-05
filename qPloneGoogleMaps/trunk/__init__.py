from AccessControl import allow_module

from Products.CMFCore.DirectoryView import registerDirectory
from Products.CMFCore import utils

from Products.Archetypes.public import process_types
from Products.Archetypes import listTypes

from Products.qPloneGoogleMaps.config import *

from Products.validation import validation

from Products.qPloneGoogleMaps.validator import MapFieldValidator
validation.register(MapFieldValidator('isLocation'))

allow_module('Products.qPloneGoogleMaps.config')
allow_module('Products.qPloneGoogleMaps.utility')

registerDirectory(SKINS_DIR, GLOBALS)

def initialize(context):
    from content import Map, Marker, Overlay

    content_types, constructors, ftis = process_types(listTypes(PROJECTNAME), PROJECTNAME)

    utils.ContentInit(PROJECTNAME + ' Content',
        content_types      = content_types,
        permission         = DEFAULT_ADD_CONTENT_PERMISSION,
        extra_constructors = constructors,
        fti                = ftis).initialize(context)
