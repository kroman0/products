from Products.CMFCore.CMFCorePermissions import AddPortalContent, ManagePortal

PROJECTNAME = "qClickTrackingTool"
GLOBALS = globals()
TOOLID = "portal_clicktracker"
SKINS_DIR = 'skins'
ADD_CAMPAIGN_PERMISSION = AddPortalContent
MANAGE_CLICKTRACKINGTOOL_PERMISSION = ManagePortal
C_WORKFLOWID='campaign_workflow'
TYPE_NAME = 'Campaign'