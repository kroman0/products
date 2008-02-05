try:
    from Products.CMFCore.permissions import setDefaultRoles
except ImportError:
    from Products.CMFCore.CMFCorePermissions import setDefaultRoles

PROJECTNAME = 'qPloneGoogleMaps'

DEFAULT_ADD_CONTENT_PERMISSION = "Add portal content"
GLOBALS = globals()
SKINS_DIR = 'skins'

NEW_PORTAL_TYPES = ['Map', 'Marker', 'Overlay']
MAP_API_KEYS = ["http://localhost.com:8888/map|ABQIAAAAPKXXAksH6LF9wD3-iB3Z9hR-_Derz1M-sZYUdeXG3J1uZOMrKxT98efydo7fhYu6kuaFv5ESjlw4mw", ]

MAP_PORTLETS = ['here/portlet_maps/macros/portlet', 'here/portlet_overlays/macros/portlet',]
PROPERTY_SHEET = 'maps_properties'
PROPERTY_FIELD = 'map_api_keys'
GEO_INDEX = 'geoLocation'

setDefaultRoles(DEFAULT_ADD_CONTENT_PERMISSION, ('Manager', 'Owner',))