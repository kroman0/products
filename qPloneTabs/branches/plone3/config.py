from Products.CMFCore import CMFCorePermissions

VIEW_PERMISSION = CMFCorePermissions.ManagePortal

PROJECTNAME = 'qPloneTabs'
SKINS_DIR = 'skins'

GLOBALS = globals()

PROPERTY_SHEET = 'tabs_properties'
SHEET_TITLE    = 'Portal Tabs Properties'
FIELD_NAME = 'titles'
PROPERTY_FIELD = ['portal_tabs|Portal Tabs Configuration', 'portal_footer|Portal Footer Configuration']