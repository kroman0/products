import string
from cStringIO import StringIO

from Products.CMFCore.utils import getToolByName
from Products.CMFCore.DirectoryView import addDirectoryViews
from Products.CMFCore.CMFCorePermissions import ManagePortal

from Products.qPloneDropDownMenu.config import *

configlets = ({'id':PROJECTNAME,
    'name':'Drop Down Menu',
    'action':'string:${portal_url}/prefs_dropdownmenu_edit_form',
    'condition':'',
    'category':'Products',
    'visible':1,
    'appId':PROJECTNAME,
    'permission':ManagePortal,
    'imageUrl':'qplonedropdownmenu.gif'},)

def setupConfiglets(self, out):
    configTool = getToolByName(self, 'portal_controlpanel', None)
    if configTool:
        for conf in configlets:
            configTool.registerConfiglet(**conf)
            out.write('Added configlet %s\n' % conf['id'])

def removeConfiglets(self, out):
    configTool = getToolByName(self, 'portal_controlpanel', None)
    if configTool:
        for conf in configlets:
            configTool.unregisterConfiglet(conf['id'])
            out.write('Removed configlet %s\n' % conf['id'])

def registerCSS(self, out):
    qi = getToolByName(self, 'portal_quickinstaller', None)
    if qi is not None:
        try:
            if not qi.isProductInstalled('ResourceRegistries'):
                qi.installProduct('ResourceRegistries', locked=0)
            cssreg = getToolByName(self, 'portal_css', None)
            if cssreg is not None:
                stylesheet_ids = cssreg.getResourceIds()

                if 'drop_down.css' not in stylesheet_ids:
                    cssreg.registerStylesheet('drop_down.css',
                                               expression="python:portal.portal_dropdownmenu")
                    out.write('Register drop_down.css... \n')
                else:
                    out.write('drop_down.css already exists... \n')
        except:
            pass

def unregisterCSS(self, out):
    qi = getToolByName(self, 'portal_quickinstaller', None)
    if qi is not None:
        try:
            if not qi.isProductInstalled('ResourceRegistries'):
                qi.installProduct('ResourceRegistries', locked=0)
            cssreg = getToolByName(self, 'portal_css', None)
            if cssreg is not None:
                stylesheet_ids = cssreg.getResourceIds()

                if 'drop_down.css' in stylesheet_ids:
                    cssreg.unregisterResource('drop_down.css')
                    out.write('Unregister drop_down.css... \n')
        except:
            pass

def setupSkin(self, out, skinFolder):
    skinstool=getToolByName(self, 'portal_skins')
    for skin in skinstool.getSkinSelections():
        path = skinstool.getSkinPath(skin)
        path = map(string.strip, string.split(path,','))
        if not skinFolder in path:
            try:
                path.insert(path.index('custom')+1, skinFolder)
            except ValueError:
                path.append(skinFolder)
            path = string.join(path, ', ')
            skinstool.addSkinSelection(skin, path)
            out.write('  %s layer sucessfully installed into skin %s.\n' % (skinFolder, skin))
        else:
            out.write('  %s layer was already installed into skin %s.\n' % (skinFolder, skin))

def removeSkin(self, skins=[]):
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

def setupTool(self, out):
    if hasattr(self, UNIQUE_ID):
        self.manage_delObjects([UNIQUE_ID])
        out.write('Deleting old %s\n' % (UNIQUE_ID))
    portal_url = getToolByName(self, 'portal_url')
    p = portal_url.getPortalObject()
    x = p.manage_addProduct[PROJECTNAME].manage_addTool(type='DropDownMenu Tool')

def deleteTool(self, out):
    if hasattr(self, UNIQUE_ID):
        self.manage_delObjects([UNIQUE_ID])
        out.write('Deleted %s tool\n' % (UNIQUE_ID))

def install(self):
    out = StringIO()
    registerCSS(self, out)
    out.write('setupSkin... \n')
    skinstool=getToolByName(self, 'portal_skins')
    addDirectoryViews(skinstool, SKINS_DIR, GLOBALS)
    setupSkin(self, out, 'qPloneDropDownMenu')
    mtool = getToolByName(self, 'portal_migration')
    plone_version = mtool.getFileSystemVersion()
    if plone_version == '2.0.5':
         setupSkin(self, out, PROJECTNAME+'/2.0.5')
         out.write('Added %s/2.0.5 Layer to portal_skins\n' % PROJECTNAME)
    setupConfiglets(self, out)
    out.write('Added %s to the portal root folder\n' % (UNIQUE_ID))
    setupTool(self, out)
    return out.getvalue()

def uninstall(self):
    out = StringIO()
    unregisterCSS(self, out)
    removeConfiglets(self, out)
    removeSkin(self, [PROJECTNAME, PROJECTNAME+'/2.0.5'])
    deleteTool(self, out)
    return out.getvalue()