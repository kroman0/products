from AccessControl import ClassSecurityInfo
try:
    from Products.CMFCore.permissions import ModifyPortalContent, View
except ImportError:
    from Products.CMFCore.CMFCorePermissions import ModifyPortalContent, View
try:
  from Products.LinguaPlone.public import *
except ImportError:
  from Products.Archetypes.public import *

#from Products.ATContentTypes.content.base import ATCTContent
from Products.ATContentTypes.content.document import ATDocumentSchema
from Products.ATContentTypes.content.document import ATDocument
from Products.ATContentTypes.content.schemata import finalizeATCTSchema

from Products.qPloneGoogleMaps.field import *
from Products.qPloneGoogleMaps.config import *

MarkerSchema = ATDocumentSchema.copy() + Schema((
    MapField('location',
        default=None,
        required=True,
        validators=('isLocation',),
        widget=MapWidget(
            label='Marker Location',
            label_msgid='label_marker_center',
            description='Here you can choose marker location on the map by mouse clicking',
            description_msgid='help_marker_center',
            i18n_domain='googlemaps',
        )
    ),

    StringField('color',
        vocabulary=('default', 'red', 'green', 'blue'),
        default='default',
        widget=SelectionWidget(
            label='Marker Color',
            label_msgid='label_marker_color',
            description_msgid='help_marker_color',
            i18n_domain='googlemaps',
        )
    ),

),
)

finalizeATCTSchema(MarkerSchema)

class Marker(ATDocument):
    """ Map Marker """

    schema          = MarkerSchema

    content_icon    = 'marker_icon.gif'
    portal_type     = 'Marker'
    meta_type       = 'Marker'
    archetype_name  = 'Marker'
    default_view    = 'marker_view'
    immediate_view  = 'marker_view'
    suppl_views     = ()
    typeDescription = 'Marker document'
    typeDescMsgId   = 'marker_description_edit'

    security        = ClassSecurityInfo()

    # Get the standard actions (tabs)
    #actions = ATCTContent.actions

    # Make sure we get title-to-id generation when an object is created
    _at_rename_after_creation = True

    security.declareProtected(View, 'geoLocation')
    def geoLocation(self):
        return self.getLocation()

registerType(Marker, PROJECTNAME)
