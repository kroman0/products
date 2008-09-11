from Acquisition import aq_base, aq_inner, aq_parent
from Products.CMFCore.utils import getToolByName

def isDefaultPage(context):
    plone_utils = getToolByName(context, 'plone_utils')
    return plone_utils.isDefaultPage(context)

def getDefaultPage(context):
    plone_utils = getToolByName(context, 'plone_utils')
    return plone_utils.getDefaultPage(context)

def isStructuralFolder(context):
    plone_utils = getToolByName(context, 'plone_utils')
    return plone_utils.isStructuralFolder(context)

def getParentObject(context):
    return aq_parent(aq_inner(context))

def getCurrentFolder(context):
    if isStructuralFolder(context) and not isDefaultPage(context):
        return context
    return getParentObject(context)

def isFolderOrFolderDefaultPage(context):
    if isStructuralFolder(context) or isDefaultPage(context):
        return True
    return False

def isPortalOrPortalDefaultPage(context):
    portal = getToolByName(context, 'portal_url').getPortalObject()
    if aq_base(context) is aq_base(portal) or \
        (aq_base(getParentObject(context)) is aq_base(portal) and
        isDefaultPage(context)):
        return True
    return False