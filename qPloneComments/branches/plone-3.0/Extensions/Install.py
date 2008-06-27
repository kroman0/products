from StringIO import StringIO
from Products.CMFCore.utils import getToolByName
from Products.CMFCore.DirectoryView import addDirectoryViews
from Products.CMFCore.permissions import ManagePortal, ReplyToItem

from plone.browserlayer.utils import register_layer, unregister_layer
from Products.qPloneComments.config import *
from Products.qPloneComments.interfaces import IPloneCommentsLayer

def install(self):
    out = StringIO()

    # Fire GenericSetup imports
    portal_setup = getToolByName(self, 'portal_setup')
    portal_setup.runAllImportStepsFromProfile('profile-Products.qPloneComments:default')

    # Register our browser layer
    register_layer(IPloneCommentsLayer, name='qPloneComments')

    # Add Property sheet to portal_properies
    pp = getToolByName(self, 'portal_properties')
    if not 'qPloneComments' in pp.objectIds():
        pp.addPropertySheet(id='qPloneComments', title='qPloneComments Properties')
        out.write("Adding %s property sheet to portal_properies\n" % 'qPloneComments')
    props_sheet = pp['qPloneComments']
    updateProperties(props_sheet, out, PROPERTIES)
    # Tern on Anonymous commenting
    self.manage_permission(ReplyToItem, ['Anonymous','Manager','Member'], 1)

    out.write("Updating properties of %s property sheet\n" % 'qPloneComments' )

    # Add Configlet. Delete old version before adding, if exist one.
    controlpanel_tool = getToolByName(self, 'portal_controlpanel')
    controlpanel_tool.unregisterConfiglet(CONFIGLET_ID)
    controlpanel_tool.registerConfiglet(id=CONFIGLET_ID, name=CONFIGLET_NAME, category='Products',
                                        action='string:${portal_url}/%s' % CONFIGLET_ID,
                                        appId=PROJECTNAME, permission=ManagePortal, imageUrl='group.gif')

    uf = getToolByName(self, 'acl_users')
    rmanager = uf.portal_role_manager
    existing = rmanager.listRoleIds()
    if not 'DiscussionManager' in existing:
        rmanager.addRole('DiscussionManager')
        out.write("Added DiscussionManager role top portal.\n")

    self.manage_permission('Moderate Discussion', ['DiscussionManager', 'Manager'])
    # Add 'DiscussionManagers' group
    gtool = getToolByName(self, 'portal_groups')
    existing = gtool.listGroupIds()
    if not 'DiscussionManager' in existing:
        gtool.addGroup('DiscussionManager', roles=['DiscussionManager'])
        out.write("Added DiscussionManager group to portal_groups with DiscussionManager role.\n")

    # Remove workflow-chain for Discussion Item
    wf_tool = getToolByName(self, 'portal_workflow')
    wf_tool.setChainForPortalTypes(('Discussion Item',), [])
    out.write("Removed workflow chain for Discussion Item type.\n")

    out.write('Installation successfully completed.\n')
    return out.getvalue()

def updateProperties(pp_ps, out, *args):
    for prop in args:
        for prop_id, prop_value, prop_type in prop:
            if not pp_ps.hasProperty(prop_id):
                pp_ps.manage_addProperty(prop_id, prop_value, prop_type)
                out.write("Adding %s property to %s property sheet\n" % (prop_id, 'qPloneComments'))

def uninstall(self):
    skinstool = getToolByName(self, 'portal_skins')
    # Remove skin
    for skinName in skinstool.getSkinSelections():
        old_path = skinstool.getSkinPath(skinName)
        old_path = [i.strip() for i in  old_path.split(',')]
        path = []
        for p in old_path:
            if not p.startswith(SKIN_NAME):
                path.append(p)
        path = ','.join(path)
        skinstool.addSkinSelection(skinName, path)

    # remove browser layer
    try:
        unregister_layer(name='qPloneComments')
    except KeyError:
        pass

    # Remove configlet
    controlpanel_tool = getToolByName(self, 'portal_controlpanel')
    controlpanel_tool.unregisterConfiglet(CONFIGLET_ID)

    # Remove Product's property sheet from portal_properties
    pp = getToolByName(self, 'portal_properties')
