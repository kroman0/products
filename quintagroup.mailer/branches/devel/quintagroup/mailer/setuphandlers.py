from Products.CMFCore.utils import getToolByName
from quintagroup.mailer.config import GROUP_ID


def setupVarious(context):
    if context.readDataFile('quintagroup.mailer_various.txt') is None:
        return
    site = context.getSite()

    # setup 'Alert subscribers' group
    gtool = getToolByName(site, "portal_groups")
    if GROUP_ID not in gtool.getGroupIds():
        gtool.addGroup(GROUP_ID)
