from AccessControl import ClassSecurityInfo
try:
    from Products.CMFCore.permissions import ModifyPortalContent, View
except ImportError:
    from Products.CMFCore.CMFCorePermissions import ModifyPortalContent, View
from Products.CMFCore.utils import getToolByName

try:
  from Products.LinguaPlone.public import *
except ImportError:
  from Products.Archetypes.public import *

from Products.ATContentTypes.content.base import ATCTFolder, updateActions
from Products.ATContentTypes.content.schemata import finalizeATCTSchema

#from Products.CMFPlone.interfaces.NonStructuralFolder import INonStructuralFolder

from Products.qPloneGoogleMaps.field import *
from Products.qPloneGoogleMaps.config import *

zoom_vocaburary = range(18)
zoom_vocaburary.reverse()

MapSchema = ATCTFolder.schema.copy() + Schema((
    MapField('location',
        default=None,
        required=True,
        validators=('isLocation',),
        widget=MapWidget(
            label='Map Center',
            label_msgid='label_map_center',
            description='Here you can choose map center point on the map by mouse clicking',
            description_msgid='help_map_center',
            i18n_domain='googlemaps',
        )
    ),

    StringField('auto',
        vocabulary=('None', 'Zoom', 'Center', 'Full'),
        default='None',
        widget=SelectionWidget(
            label='Auto Control',
            label_msgid='label_auto_control',
            description_msgid='help_auto_control',
            i18n_domain='googlemaps',
            format = 'radio',
        )
    ),

    IntegerField('height',
        default="480",
        required=True,
        widget=IntegerWidget(
            label='Height',
            label_msgid='label_height',
            description_msgid='help_height',
            i18n_domain='googlemaps',
        )
    ),

    IntegerField('zoom',
        default=3,
        vocabulary=zoom_vocaburary,
        widget=SelectionWidget(
            label='Zoom',
            label_msgid='label_zoom',
            description_msgid='help_zoom',
            i18n_domain='googlemaps',
        )
    ),

    StringField('mapControl',
        vocabulary=('large', 'small', 'nothing'),
        default='large',
        widget=SelectionWidget(
            label='Map Control',
            label_msgid='label_map_control',
            description_msgid='help_map_control',
            i18n_domain='googlemaps',
        )
    ),

    StringField('mapType',
        vocabulary=('map', 'satellite', 'hybrid'),
        default='hybrid',
        widget=SelectionWidget(
            label='Map Type',
            label_msgid='label_map_type',
            description_msgid='help_map_type',
            i18n_domain='googlemaps',
        )
    ),

    BooleanField('typeControl',
        default=1,
        widget=BooleanWidget(
            label='Type Control',
            label_msgid='label_type_control',
            description_msgid='help_type_control',
            i18n_domain='googlemaps',
        )
    ),

    BooleanField('overviewControl',
        default=1,
        widget=BooleanWidget(
            label='Overview Control',
            label_msgid='label_overview_control',
            description_msgid='help_overview_control',
            i18n_domain='googlemaps',
        )
    ),
),
)

finalizeATCTSchema(MapSchema)

class Map(ATCTFolder):
    """Google Map class"""

    schema          = MapSchema

    content_icon    = 'map_icon.gif'
    portal_type     = 'Map'
    meta_type       = 'Map'
    archetype_name  = 'Map'
    default_view    = 'map_view'
    immediate_view  = 'map_view'
    suppl_views     = ()
    typeDescription = 'Maps Folder'
    typeDescMsgId   = 'map_description_edit'

    security        = ClassSecurityInfo()

    # Get the standard actions (tabs)
    actions = updateActions(ATCTFolder,
        ({'id'          : 'edit',
          'name'        : 'Edit',
          'action'      : 'string:${object_url}/map_edit',
          'permissions' : (ModifyPortalContent,)
         },
        )
    )

    #__implements__ = (ATCTFolder.__implements__, INonStructuralFolder)

    allowed_content_types = ['Marker', 'Overlay']

    # Make sure we get title-to-id generation when an object is created
    _at_rename_after_creation = True

    def canSetDefaultPage(self):
        return False

    security.declareProtected(View, 'geoLocation')
    def geoLocation(self):
        """ Return geolocation tuple """
        return self.getLocation()

    security.declareProtected(View, 'getOverlayMarkers')
    def getOverlayMarkers(self):
        """ Return markers of the contained overlays """
        catalog = getToolByName(self, 'portal_catalog')
        result = {}
        for el in self.folderlistingFolderContents():
            if el.portal_type == 'Overlay':
                color = el.getMarkersColor()
                markers =  el.getMarkers()
            elif el.portal_type == 'Marker':
                color = el.getColor()
                markers = list(catalog(path='/'.join(el.getPhysicalPath())))
            else: continue
            result[(el.getId(),color)] = result.get(el.getId(), []) + markers
        return result

registerType(Map, PROJECTNAME)
