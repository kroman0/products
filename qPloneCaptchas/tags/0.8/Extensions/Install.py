from Products.qPloneCaptchas.config import *
from Products.CMFCore.utils import getToolByName
from StringIO import StringIO
from Products.CMFCore.DirectoryView import addDirectoryViews
import string
from App.Common import package_home
from os.path import exists as path_exists, join as path_join


def install(self):
    out=StringIO()
    Layers = LAYERS
    mtool = getToolByName(self, 'portal_migration')
    plone_version = mtool.getFileSystemVersion()
    if plone_version.startswith('2.1'):
        plone_version = '2.1.2'
    elif plone_version.startswith('2.0'):
        plone_version = '2.0.5'
    else:
        raise Exception("Error - Unsupported version. Suported versions: Plone 2.0.5-2.1.2")
    DiscussionLayer = LAYER_DISCUSSION
    try:
        import Products.qPloneComments.config
        DiscussionLayer = LAYER_QCOMMENTS
    except:
        pass
    product_path = package_home(GLOBALS)
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
    # Remove skin
    for skinName in skinstool.getSkinSelections():
        path = skinstool.getSkinPath(skinName)
        path = [i.strip() for i in  path.split(',')]
        for skin in ALL_LAYERS:
            for l in path:
                if (l == skin) or (l.startswith(skin+'/')):
                    path.remove(l)
        skinstool.addSkinSelection(skinName, ','.join(path))
