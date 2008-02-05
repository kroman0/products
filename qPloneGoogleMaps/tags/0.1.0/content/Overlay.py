from AccessControl import ClassSecurityInfo
try:
    from Products.CMFCore.permissions import ModifyPortalContent, View
except ImportError:
    from Products.CMFCore.CMFCorePermissions import ModifyPortalContent, View

try:
  from Products.LinguaPlone.public import *
except ImportError:
  from Products.Archetypes.public import *

from Products.ATContentTypes.content.base import ATCTContent
from Products.ATReferenceBrowserWidget.ATReferenceBrowserWidget import ReferenceBrowserWidget

from Products.qPloneGoogleMaps.config import PROJECTNAME

OverlaySchema = BaseSchema.copy() + Schema((
    ReferenceField('markerssource',
                   accessor = 'getSource',
                   required = True,
                   multiValued=0,
                   allowed_types=('Folder', 'Topic', 'Large Plone Folder'),
                   relationship='markers',
                   widget=ReferenceBrowserWidget(label='Markers Source',
                                                 label_msgid='label_markers_source',
                                                 allow_search=1,
                                                 allow_browse=1,
                                                 startup_directory='/',
                                                 show_path=1,
                                                 description='Select source object for Markers.',
                   )
    ),
    StringField('markerscolor',
        accessor = 'getMarkersColor',
        vocabulary=('default', 'red', 'green', 'blue'),
        default='default',
        widget=SelectionWidget(
            label='Markers Color',
            label_msgid='label_markers_color',
            description_msgid='help_markers_color',
            i18n_domain='googlemaps',
        )
    ),
))


class Overlay(ATCTContent):
    """ Maps Overlay """

    schema          = OverlaySchema

    content_icon    = 'overlay_icon.gif'
    portal_type     = 'Overlay'
    meta_type       = 'Overlay'
    archetype_name  = 'Overlay'
    default_view    = 'overlay_view'
    immediate_view  = 'overlay_view'
    suppl_views     = ()
    typeDescription = 'Maps Overlay'
    typeDescMsgId   = 'overlay_description_edit'

    global_allow    = 0

    security       = ClassSecurityInfo()

    # Get the standard actions (tabs)
    #actions = ATCTContent.actions

    # Make sure we get title-to-id generation when an object is created
    _at_rename_after_creation = True

    security.declareProtected(View, 'getMarkers')
    def getMarkers(self):
        """ Get object or brains with geolocation properties from source object """
        container = self.getSource()
        if container and container.portal_type:
            contentsMethod = container.getFolderContents
            if container.portal_type == 'Topic': contentsMethod = container.queryCatalog
            return [el for el in contentsMethod() if el.geoLocation]
        return []

registerType(Overlay, PROJECTNAME)
