from StringIO import StringIO
from Products.Archetypes.public import listTypes
from Products.Archetypes.Extensions.utils import installTypes, install_subskin
from Products.CMFCore.CMFCorePermissions import ManagePortal
from Products.CMFCore.utils import getToolByName
from Products.qPingTool.config import *
from Products.qPingTool import PingTool
from Products.CMFCore.TypesTool import ContentFactoryMetadata
from Products.CMFCore.utils import getToolByName
from Products.CMFPlone.migrations.migration_util import safeEditProperty



def install(self):
    out = StringIO()

    installTypes(self, out, listTypes(PROJECTNAME), PROJECTNAME)
    portal = getToolByName(self, 'portal_url').getPortalObject()
    if not hasattr(portal, TOOL_ID):
        portal.invokeFactory(id=TOOL_ID, type_name='PingTool')

    # Add PortalActions Tool Configlet. Delete old version before adding, if exist one.
    controlpanel_tool = getToolByName(self, 'portal_controlpanel')
    controlpanel_tool.unregisterConfiglet(TOOL_ID)
    controlpanel_tool.registerConfiglet(id=TOOL_ID, name='Ping Tool', category='Products',
                                        action='string:${portal_url}/'+TOOL_ID+'/folder_contents',
                                        appId=PROJECTNAME,  permission=ManagePortal, imageUrl='group.gif')

    # Add 'portal_actionstool' to action provider list, if not yet exist
    action_tool = getToolByName(portal, 'portal_actions')
    if TOOL_ID not in action_tool.listActionProviders():
        action_tool.addActionProvider(TOOL_ID)


    install_subskin(self,out,GLOBALS)
   

    for site in SITES_LIST:
        portal.portal_pingtool.invokeFactory(id = site[0], type_name = "PingInfo", title = site[1],url = site[2])

    pp = getToolByName(self,'portal_properties')
    np = getattr(pp,'navtree_properties')
    meta_types = list(np.getProperty('metaTypesNotToList'))
    if 'PingTool' not in meta_types:
        meta_types.append('PingTool')
    safeEditProperty(np,'metaTypesNotToList', meta_types, 'lines')


    
    print >> out, "\nSuccessfully installed %s." % PROJECTNAME
    return out.getvalue()

def uninstall(portal):
    action_tool = getToolByName(portal, 'portal_actions')
    # Delete ActionProvider
    action_tool.deleteActionProvider(TOOL_ID)

    controlpanel_tool = getToolByName(portal, 'portal_controlpanel')
    controlpanel_tool.unregisterConfiglet(TOOL_ID)

    removeSkin(portal, ('ping_tool.pt',))

    #wf_tool=getToolByName(self, 'portal_workflow')
    #wf=wf_tool.plone_workflow
    #tdef = wf.transitions['publish']
    #tdef.after_script_name=None


    return '%s actionProvider successfully uninstalled' % TOOL_ID

def removeSkin(self, skins = []):
    if skins:
        skinstool = getToolByName(self, 'portal_skins')
        for skinName in skinstool.getSkinSelections():
            path = skinstool.getSkinPath(skinName)
            path = [i.strip() for i in  path.split(',')]
            for s in skins:
                if s in path:
                    path.remove(s)
            path = ','.join(path)
            skinstool.addSkinSelection(skinName, path)
