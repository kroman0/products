from Products.qPingTool.config import SITES_LIST

def setupVarious(context):

    # Ordinarily, GenericSetup handlers check for the existence of XML files.
    # Here, we are not parsing an XML file, but we use this text file as a
    # flag to check that we actually meant for this import step to be run.
    # The file is found in profiles/default.

    if context.readDataFile('qPingTool_various.txt') is None:
        return

    # Add additional setup code here
    portal = context.getSite()
    existent_sites = portal.portal_pingtool.objectIds()
    for site in SITES_LIST:
        if not site[0] in existent_sites:
            portal.portal_pingtool.invokeFactory(id = site[0], type_name = "PingInfo", title = site[1],url = site[2])

