from Products.qPloneCaptchas.config import *
from Products.CMFCore.utils import getToolByName
from StringIO import StringIO
from Products.CMFCore.DirectoryView import addDirectoryViews
import string
from App.Common import package_home
from os.path import exists as path_exists, join as path_join
from Products.CMFCore.CMFCorePermissions import ManagePortal
from random import randint
from Products.CMFPlone.migrations.migration_util import safeEditProperty
from Products.Transience.Transience import constructTransientObjectContainer

def install(self):
    out=StringIO()
    portal = getToolByName(self, 'portal_url').getPortalObject()
    if not hasattr(portal, TOOL_ID):
        constructTransientObjectContainer(portal, id=TOOL_ID, timeout_mins=60)
    
    safeEditProperty(self, 'captcha_key', generateKey(8))
    Layers = []
    Layers += LAYERS
    qi = getToolByName(self, 'portal_quickinstaller')
    mtool = getToolByName(self, 'portal_migration')
    plone_version = mtool.getFileSystemVersion()
    
    if plone_version.startswith('2.1'):
        plone_version = '2.1.2'
    elif plone_version.startswith('2.0'):
        plone_version = '2.0.5'
    elif plone_version.startswith('2.5'):
        plone_version = '2.5'
    else:
        raise Exception("Error - Unsupported version. Suported versions: Plone 2.0.5-2.5")
    
    DiscussionLayer = LAYER_DISCUSSION
    if qi.isProductInstalled('qPloneComments'):
        DiscussionLayer = LAYER_QCOMMENTS
    if qi.isProductInstalled('PloneFormMailer'):
        formmailer_layer = LAYER_FORMMAILER+'/'+plone_version
        Layers.append(formmailer_layer)
    discussion_layer = DiscussionLayer+'/'+plone_version
    Layers.append(discussion_layer)
    out.write('Call setupSkin... \n')
    setupSkin(self, out, Layers)
    
    
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

def uninstall(self):
    skinstool = getToolByName(self, 'portal_skins')
    for skinName in skinstool.getSkinSelections():
        path = skinstool.getSkinPath(skinName)
        path = [i.strip() for i in  path.split(',')]
        for skin in ALL_LAYERS:
            for l in path:
                if (l == skin) or (l.startswith(skin+'/')):
                    path.remove(l)
        skinstool.addSkinSelection(skinName, ','.join(path))

def generateKey(length):
    key = ''
    for i in range(length): key += str(randint(0, 9))
    return key