import string
from cStringIO import StringIO

from Products.CMFCore.utils import getToolByName
from Products.CMFCore.DirectoryView import addDirectoryViews

from Products.qPloneTabs.config import *

configlets = ({'id':PROJECT_NAME,
    'name':'Plone Tabs',
    'action':'string:${portal_url}/prefs_tabs_form',
    'condition':'',
    'category':'Products',
    'visible':1,
    'appId':PROJECT_NAME,
    'permission':VIEW_PERMISSION,
    'imageUrl':'qplonetabs.gif' },)

def setupSkin(self, out, skinFolder):
    """ Setup product skin layer """

    skinstool=getToolByName(self, 'portal_skins')
    addDirectoryViews(skinstool, SKINS_DIR, GLOBALS)
    for skin in skinstool.getSkinSelections():
        path = skinstool.getSkinPath(skin)
        path = map(string.strip, string.split(path,','))
        if not skinFolder in path:
            try:
                path.insert( path.index('custom')+1, skinFolder)
            except ValueError:
                path.append(skinFolder)
            path = string.join(path, ', ')
            skinstool.addSkinSelection(skin, path)
            out.write('  %s layer sucessfully installed into skin %s.\n' % (skinFolder, skin))
        else:
            out.write('  %s layer was already installed into skin %s.\n' % (skinFolder, skin))

def removeSkin(self, skins=[]):
    """ Setup product skin layer """

    if skins:
        skinstool = getToolByName(self, 'portal_skins')
        for skinName in skinstool.getSkinSelections():
            path = skinstool.getSkinPath(skinName)
            path = [i.strip() for i in  path.split(',')]
            for s in skins:
                if s in path:
                    path.remove(s)
                s += '/'
                for layer in path:
                    if layer.startswith(s):
                        path.remove(layer)
            path = ','.join(path)
            skinstool.addSkinSelection(skinName, path)

def addConfiglet(self, out):
    """ Add tabs configlet to portal control panel """

    configTool = getToolByName(self, 'portal_controlpanel', None)
    if configTool:
        for conf in configlets:
            configTool.registerConfiglet(**conf)
            out.write('Added configlet %s\n' % conf['id'])

def removeConfiglet(self, out):
    """ Remove tabs configlet from portal control panel """

    configTool = getToolByName(self, 'portal_controlpanel', None)
    if configTool:
        for conf in configlets:
            configTool.unregisterConfiglet(conf['id'])
            out.write('Removed configlet %s\n' % conf['id'])

def install(self):
    """ Product installation """

    out = StringIO()

    addConfiglet(self, out)

    out.write('setupSkin... \n')
    setupSkin(self, out, PROJECT_NAME)

    return out.getvalue()

def uninstall(self):
    """ Product uninstallation """

    out = StringIO()

    removeConfiglet(self, out)

    out.write('removeSkin... \n')
    removeSkin(self, [PROJECT_NAME,])

    return out.getvalue()
