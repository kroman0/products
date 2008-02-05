from StringIO import StringIO
from Products.CMFCore.utils import getToolByName
from Products.CMFCore.DirectoryView import addDirectoryViews
from Products.CMFCore.CMFCorePermissions import ManagePortal,ReplyToItem
from App.Common import package_home
from os.path import exists as path_exists, join as path_join

from Products.qPloneComments.config import *

import string
try:
    True
except:
    True = 1
    False = 0

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
            path = string.join( path, ', ' )
            skinstool.addSkinSelection( skin, path )

    
def install(self):
    out=StringIO()

    Layers = []
    mtool = getToolByName(self, 'portal_migration')
    plone_version = mtool.getFileSystemVersion()
    if plone_version.startswith('2.1'):
        plone_version = '2.1'
    elif plone_version.startswith('2.0'):
        plone_version = '2.0.5'
    else:
        raise Exception("Error - Unsupported version. Suported versions: Plone 2.0.5-2.1.2")

    product_path = package_home(GLOBALS)
    versioned_skin = path_join(product_path, 'skins', PROJECTNAME, plone_version)

    Layers.append(SKIN_NAME)
    Layers.append('%s/%s' % (SKIN_NAME, plone_version) )
    out.write('Call setupSkin... \n')
    setupSkin(self, out, Layers)

    # add Property sheet to portal_properies
    pp = getToolByName(self, 'portal_properties')
    if not 'qPloneComments' in pp.objectIds():
        pp.addPropertySheet(id='qPloneComments', title= '%s Properties' % 'qPloneComments')
        out.write("Adding %s property sheet to portal_properies\n" % 'qPloneComments' )
    props_sheet = pp['qPloneComments']
    updateProperty(props_sheet, id="enable_moderation", value="True", property_type='boolean', out=out)
    updateProperty(props_sheet, id="enable_anonymous_commenting", value="True", property_type='boolean', out=out)
    updateProperty(props_sheet, id="enable_published_notification", value="True", property_type='boolean', out=out)
    updateProperty(props_sheet, id="enable_approve_notification", value="True", property_type='boolean', out=out)
    updateProperty(props_sheet, id="email_discussion_manager", value="", property_type='string', out=out)
    updateProperty(props_sheet, id="email_subject_prefix", value="", property_type='string', out=out)
    # Tern on Anonymous commenting
    self.manage_permission(ReplyToItem, ['Anonymous','Manager','Member'], 1)

    out.write("Updating properties of %s property sheet\n" % 'qPloneComments' )

    # Add Configlet. Delete old version before adding, if exist one.
    controlpanel_tool = getToolByName(self, 'portal_controlpanel')
    controlpanel_tool.unregisterConfiglet(CONFIGLET_ID)
    controlpanel_tool.registerConfiglet(id=CONFIGLET_ID, name=CONFIGLET_NAME, category='Products',
                                        action='string:${portal_url}/%s' % CONFIGLET_ID,
                                        appId=PROJECTNAME, permission=ManagePortal, imageUrl='group.gif')

    # Add DiscussionManager role to Portal
    roles = list(self.__ac_roles__)
    if not 'DiscussionManager' in roles:
        roles.append( 'DiscussionManager' )
        roles = tuple(roles)
        self.__ac_roles__ = roles
        out.write("Added DiscussionManager role top portal.\n")

    #  Add 'DiscussionManagers' group
    portal_groups = getToolByName(self, 'portal_groups')
    if not 'DiscussionManager' in portal_groups.listGroupIds():
        portal_groups.addGroup('DiscussionManager', roles=['DiscussionManager'])
        out.write("Added DiscussionManager group to portal_groups with DiscussionManager role.\n")

    # Remove workflow-chain for Discussion Item
    wf_tool = getToolByName(self, 'portal_workflow')
    wf_tool.setChainForPortalTypes( ('Discussion Item',), []) 
    out.write("Removed workflow chain for Discussion Item type.\n")
    
    out.write('Installation successfully completed.\n')
    return out.getvalue()


def updateProperty(pp_ps, id, value, property_type, out):
    if not pp_ps.hasProperty(id):
        pp_ps.manage_addProperty(id, value, property_type)
        out.write("Adding %s property to %s property sheet\n" % (id, 'qPloneComments') )


def uninstall(self) :
    skinstool = getToolByName(self, 'portal_skins')
    # Remove skin
    for skinName in skinstool.getSkinSelections():
        path = skinstool.getSkinPath(skinName)
        path = [i.strip() for i in  path.split(',')]
        if SKIN_NAME in path:
            path.remove(SKIN_NAME)
            path = ','.join(path)
            skinstool.addSkinSelection(skinName, path)
    # Remove configlet
    controlpanel_tool = getToolByName(self, 'portal_controlpanel')
    controlpanel_tool.unregisterConfiglet(CONFIGLET_ID)
    # Remove Product's property sheet from portal_properties
    pp = getToolByName(self, 'portal_properties')
    if 'qPloneComments' in pp.objectIds():
        pp.manage_delObjects(ids=['qPloneComments',])
