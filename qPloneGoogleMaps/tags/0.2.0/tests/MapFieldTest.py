from AccessControl import ClassSecurityInfo
from Products.Archetypes.atapi import *
from Products.ATContentTypes.content.base import ATCTFolder

from Products.qPloneGoogleMaps.field import MapField, MapWidget
from Products.qPloneGoogleMaps.config import *

schema = Schema((
    MapField(
        name='location',
        widget=MapWidget(),
    ),
),)

MapFieldTest_schema = BaseSchema.copy() + \
    schema.copy()

class MapFieldTest(ATCTFolder):
    security = ClassSecurityInfo()
    __implements__ = (getattr(ATCTFolder,'__implements__',()),)

    archetype_name = 'MapFieldTest'

    meta_type = 'MapFieldTest'
    portal_type = 'MapFieldTest'
    allowed_content_types = []
    filter_content_types = 0
    global_allow = 0
    allow_discussion = False
    immediate_view = 'base_view'
    default_view = 'base_view'
    suppl_views = ()
    typeDescription = "MapFieldTest"
    typeDescMsgId = 'description_edit_mapfieldtest'

    schema = MapFieldTest_schema

registerType(MapFieldTest, PROJECTNAME)
