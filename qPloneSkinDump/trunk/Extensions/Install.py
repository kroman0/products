from Products.Archetypes.Extensions.utils import install_subskin
from Products.CMFCore.utils import getToolByName
try:
    from Products.CMFCore.permissions import ManagePortal
except:
    from Products.CMFCore.CMFCorePermissions import ManagePortal

from Products.qPloneSkinDump.config import *
from StringIO import StringIO

def install(self):
    out=StringIO()

    controlpanel_tool = getToolByName(self, 'portal_controlpanel')

    controlpanel_tool.unregisterConfiglet(CONFIGURATION_CONFIGLET)
    controlpanel_tool.registerConfiglet(id=CONFIGURATION_CONFIGLET, name='qPloneSkinDump Configuration', category='Products',
                                        action='string:${portal_url}/qploneskindump_config',
                                        appId=PROJECTNAME,  permission=ManagePortal, imageUrl='skins_icon.gif')

    install_subskin(self, out, GLOBALS)

    out.write('Installation qPloneSkinDump successfully completed.\n')
    return out.getvalue()

def uninstall(self) :
    controlpanel_tool = getToolByName(self, 'portal_controlpanel')
#    controlpanel_tool.unregisterConfiglet(TOOL_ID)
    controlpanel_tool.unregisterConfiglet(CONFIGURATION_CONFIGLET)

    skinstool = getToolByName(self, 'portal_skins')
    skinLayer = PROJECTNAME.lower()
    for skinName in skinstool.getSkinSelections():
        path = skinstool.getSkinPath(skinName)
        path = [i.strip() for i in  path.split(',')]
        if skinLayer in path:
            path.remove(skinLayer)
            path = ','.join(path)
            skinstool.addSkinSelection(skinName, path)

