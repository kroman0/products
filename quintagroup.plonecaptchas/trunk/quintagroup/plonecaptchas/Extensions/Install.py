from random import randint
import string
from StringIO import StringIO
from os.path import exists as path_exists, join as path_join

from App.Common import package_home

from Products.CMFCore.utils import getToolByName
from Products.CMFCore.DirectoryView import addDirectoryViews
from Products.CMFPlone.migrations.migration_util import safeEditProperty
try:
    from Products.CMFCore.permissions import ManagePortal
except:
    from Products.CMFCore.CMFCorePermissions import ManagePortal

from quintagroup.plonecaptchas.config import *

def install(self):
    out=StringIO()
    portal = getToolByName(self, 'portal_url').getPortalObject()
    # add captchas_tool
    install_tool(self, out)

    safeEditProperty(self, 'captcha_key', generateKey(8))

    # add Property sheet to portal_properies
    pp = getToolByName(self, 'portal_properties')
    if not 'qPloneCaptchas' in pp.objectIds():
        pp.addPropertySheet(id='qPloneCaptchas', title= '%s Properties' % 'qPloneCaptchas')
        out.write("Adding %s property sheet to portal_properies\n" % 'qPloneComments' )
    props_sheet = pp['qPloneCaptchas']
    updateProperties(props_sheet, out, PROPERTIES)

    layers = LAYERS + [LAYER_STATIC_CAPTCHAS]

    out.write('Call setupSkin... \n')
    setupSkin(self, out, layers)

    # Add Configlet. Delete old version before adding, if exist one.
    controlpanel_tool = getToolByName(self, 'portal_controlpanel')
    controlpanel_tool.unregisterConfiglet(CONFIGLET_ID)
    controlpanel_tool.registerConfiglet(id=CONFIGLET_ID, name=CONFIGLET_NAME, category='Products',
                                        action='string:${portal_url}/%s' % CONFIGLET_ID,
                                        appId=PRODUCT_NAME, permission=ManagePortal, imageUrl='group.gif')
    return out.getvalue()

def setupSkin(self, out, layers):
    """Setup skins"""
    skinstool=getToolByName(self, 'portal_skins')
    addDirectoryViews(skinstool, 'skins', GLOBALS)

    for skin in skinstool.getSkinSelections():
        modified = False
        path = skinstool.getSkinPath(skin)
        path = map( string.strip, string.split( path,',' ) )
        for layer in layers:
            if not layer in path:
                try:
                    path.insert(path.index('custom')+1, layer )
                except ValueError:
                    path.append(layer)
                modified = True
                out.write('  Layer %s sucessfully installed into skin %s.\n' % (layer,skin))
            else:
                out.write('  Layer %s was already installed into skin %s.\n' % (layer,skin))
        if modified:
            path = string.join( path, ',' )
            skinstool.addSkinSelection( skin, path )

def uninstall(self):
    skinstool = getToolByName(self, 'portal_skins')
    for skinName in skinstool.getSkinSelections():
        path = skinstool.getSkinPath(skinName)
        path = [i.strip() for i in  path.split(',')]
        pth  = [x for x in path
                    if not ((x in ALL_LAYERS) or
                            filter(lambda y:x.startswith(y), ALL_LAYERS))]
        skinstool.addSkinSelection(skinName, ','.join(pth))

     # Remove configlet
    controlpanel_tool = getToolByName(self, 'portal_controlpanel')
    controlpanel_tool.unregisterConfiglet(CONFIGLET_ID)
    # Remove Product's property sheet from portal_properties
    pp = getToolByName(self, 'portal_properties')
    if 'qPloneCaptchas' in pp.objectIds():
        pp.manage_delObjects(ids=['qPloneCaptchas'])

def updateProperties(pp_ps, out, *args):
    for prop in args:
        for prop_id, prop_value, prop_type in prop:
            if not pp_ps.hasProperty(prop_id):
                pp_ps.manage_addProperty(prop_id, prop_value, prop_type)
                out.write("Adding %s property to %s property sheet\n" % (prop_id, 'qPloneComments'))

def generateKey(length):
    key = ''
    for i in range(length): key += str(randint(0, 9))
    return key

def install_tool(self, out):
    if not hasattr(self, 'portal_captchas'):
        addTool = self.manage_addProduct['quintagroup.plonecaptchas'].manage_addTool
        addTool('CaptchaTool')

def updateProperties(pp_ps, out, *args):
    for prop in args:
        for prop_id, prop_value, prop_type in prop:
            if not pp_ps.hasProperty(prop_id):
                pp_ps.manage_addProperty(prop_id, prop_value, prop_type)
                out.write("Adding %s property to %s property sheet\n" % (prop_id, 'qPloneComments'))
