from StringIO import StringIO
from Products.CMFCore.utils import getToolByName
from Products.CMFCore.permissions import ManagePortal, ReplyToItem

from Products.qPloneComments.config import *

def install(self):
    out = StringIO()

    # Fire GenericSetup imports
    portal_setup = getToolByName(self, 'portal_setup')
    portal_setup.runAllImportStepsFromProfile('profile-Products.qPloneComments:default')

    # Tern on Anonymous commenting
    self.manage_permission(ReplyToItem, ['Anonymous','Manager','Member'], 1)

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

def uninstall(self):

    # Remove configlet
    controlpanel_tool = getToolByName(self, 'portal_controlpanel')
    controlpanel_tool.unregisterConfiglet(CONFIGLET_ID)
