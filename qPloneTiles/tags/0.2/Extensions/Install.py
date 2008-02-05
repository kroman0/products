import string
from cStringIO import StringIO

from Products.CMFCore.utils import getToolByName
from Products.CMFCore.DirectoryView import addDirectoryViews

from Products.qPloneTiles.config import *

def registerJS(self, out, js_list=[]):
    """ Register javascripts sources """

    qi = getToolByName(self, 'portal_quickinstaller', None)
    if qi is not None:
        try:
            if not qi.isProductInstalled('ResourceRegistries'):
                qi.installProduct('ResourceRegistries', locked=0)
            jsreg = getToolByName(self, 'portal_javascripts', None)
            if jsreg is not None:
                js_ids = jsreg.getResourceIds()
                for js in js_list:
                    if js not in js_ids:
                        jsreg.manage_addScript(id=js,
                                               expression="",
                                               enabled=True,
                                               cookable=True)
                        out.write('Register %s... \n' % js)
                    else:
                        out.write('%s already exists... \n' % js)
        except:
            pass

def unregisterJS(self, out, js_list=[]):
    """ UnRegister javascripts sources """

    qi = getToolByName(self, 'portal_quickinstaller', None)
    if qi is not None:
        try:
            if not qi.isProductInstalled('ResourceRegistries'):
                qi.installProduct('ResourceRegistries', locked=0)
            jsreg = getToolByName(self, 'portal_javascripts', None)
            if jsreg is not None:
                js_ids = jsreg.getResourceIds()
                for js in js_list:
                    if js in js_ids:
                        jsreg.manage_removeScript(id=js)
                        out.write('Unregister %s... \n' % js)
        except:
            pass

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


def install(self):
    """ Product installation """

    out = StringIO()

    # registering javascript sources
    registerJS(self, out, JS_LIST)

    # setup skin layer
    out.write('setupSkin... \n')
    setupSkin(self, out, PROJECT_NAME)

    return out.getvalue()

def uninstall(self):
    """ Product uninstallation """

    out = StringIO()

    # unregistering javascript sources
    unregisterJS(self, out, JS_LIST)

    # remove skin layer
    removeSkin(self, [PROJECT_NAME,])

    return out.getvalue()