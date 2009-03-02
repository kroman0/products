from Acquisition import aq_base

from Products.SiteAccess.AccessRule import AccessRule
from Products.Five.component import *
from Products.Five.site.localsite import *

from Products.CMFCore.utils import getToolByName

def turnOnBRT(self):
    portal = getToolByName(self, 'portal_url').getPortalObject()

    obj = aq_base(portal)
    hook = AccessRule(HOOK_NAME)
    registerBeforeTraverse(obj, hook, HOOK_NAME, 1)

    if not hasattr(obj, HOOK_NAME):
        setattr(obj, HOOK_NAME, LocalSiteHook())

    return "REGISTERED"     

def turnOffBRT(self):
    portal = getToolByName(self, 'portal_url').getPortalObject()

    obj = aq_base(portal)
    unregisterBeforeTraverse(obj, HOOK_NAME)
    if hasattr(obj, HOOK_NAME):
        delattr(obj, HOOK_NAME)

    return "UNREGISTERED"     
