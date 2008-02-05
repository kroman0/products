import string
from StringIO import StringIO
from Products.CMFCore.utils import getToolByName
from Products.Archetypes.Extensions.utils import install_subskin
from Products.CMFCore.permissions import ManagePortal
from Products.adsenseproduct.config import *

def registerConfiglet(self, out):
    controlpanel_tool = getToolByName(self, 'portal_controlpanel')
    controlpanel_tool.unregisterConfiglet('prefs_adsense')
    controlpanel_tool.registerConfiglet(id='prefs_adsense', name='Adsense Properties' \
        ,category='Products', action='string:${portal_url}/prefs_adsense' \
        ,appId=PRODUCT_NAME,  permission=ManagePortal, imageUrl='group.gif')
    out.write("'prefs_adsense' configlet registered\n")

def unregisterConfiglet(self):
    controlpanel_tool = getToolByName(self, 'portal_controlpanel')
    controlpanel_tool.unregisterConfiglet('prefs_adsense')

def addProperties(self, out):
    pp = getToolByName(self, 'portal_properties')
    if not 'adsense_properties' in pp.objectIds():
        pp.addPropertySheet(id='adsense_properties', title= 'adsense_properties')
        print >> out, "Added 'portal_properties.adsense_properties' PropertySheet."
    ads_ps = pp.adsense_properties
    if not ads_ps.hasProperty('customer_id'):
        ads_ps.manage_addProperty('customer_id','','string')
        out.write("'customer_id' property added to portal_properties/adsense_properties\n")

def removeProperties(self):
    pp = getToolByName(self, 'portal_properties')
    if 'adsense_properties' in pp.objectIds():
        pp.manage_delObjects(ids=['adsense_properties',])


def install(self):
    out = StringIO()
    install_subskin(self,out,GLOBALS)
    registerConfiglet(self, out)
    addProperties(self, out)
    return out.getvalue()

def uninstall(self):
    unregisterConfiglet(self)
    removeProperties(self)