from Products.CMFCore.utils import getToolByName

def setupVarious(context):
    """Run the various non-Generic Setup profile import steps.
    """
    if context.readDataFile('qPloneComments-default.txt') is None:
        return

    portal = context.getSite()
    logger = context.getLogger('qPloneComments')

    # Add 'DiscussionManagers' group
    gtool = getToolByName(portal, 'portal_groups')
    existing = gtool.listGroupIds()
    if not 'DiscussionManager' in existing:
        gtool.addGroup('DiscussionManager', roles=['DiscussionManager'])
        logger.info('Added DiscussionManager group to portal_groups with DiscussionManager role.')

    # Remove workflow-chain for Discussion Item
    wf_tool = getToolByName(portal, 'portal_workflow')
    wf_tool.setChainForPortalTypes(('Discussion Item',), [])
    logger.info('Removed workflow chain for Discussion Item type.')
