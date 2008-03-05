import string
from cStringIO import StringIO

from Products.CMFCore.utils import getToolByName
from Products.CMFCore.DirectoryView import addDirectoryViews

from Products.CMFPlone.migrations.migration_util import safeEditProperty
from Products.qPloneTabs.config import *

configlets = ({'id':PROJECTNAME,
    'name':'Plone Tabs',
    'action':'string:${portal_url}/prefs_tabs_form',
    'condition':'',
    'category':'Products',
    'visible':1,
    'appId':PROJECTNAME,
    'permission':VIEW_PERMISSION,
    'imageUrl':'qplonetabs.gif' },)

def installResources(self, out):
    # register stylesheets
    portal_css = getToolByName(self, 'portal_css', None)
    if portal_css is not None:
        for css in CSSES:
            if css['id'] not in portal_css.getResourceIds():
                portal_css.registerStylesheet(**css)
                out.write("Registered %s stylesheet\n" % css['id'])
            else:
                out.write("Skipped registering %s stylesheet\n" % css['id'])
    
    # register javascripts
    portal_javascripts = getToolByName(self, 'portal_javascripts', None)
    if portal_javascripts is not None:
        for js in JAVASCRIPTS:
            if js['id'] not in portal_javascripts.getResourceIds():
                portal_javascripts.registerScript(**js)
                out.write("Registered %s javascript " % js['id'])
            else:
                out.write("Skipped registering %s javascript\n" % js['id'])
    
    # register kss sheets
    portal_kss = getToolByName(self, 'portal_kss', None)
    if portal_kss is not None:
        for kss in KSSES:
            if kss['id'] not in portal_kss.getResourceIds():
                portal_kss.registerKineticStylesheet(**kss)
                out.write("Registered %s kss " % kss['id'])
            else:
                out.write("Skipped registering %s kss\n" % kss['id'])

def addPropertySheet(self, out):
    """ Add tabs_properties property sheet to portal_properties and some needed field to it """
    portal_props = getToolByName(self, 'portal_properties')
    if not hasattr(portal_props, PROPERTY_SHEET):
        portal_props.addPropertySheet(PROPERTY_SHEET, SHEET_TITLE)
        out.write('Added %s property sheet to portal_properties\n' % PROPERTY_SHEET)
    else:
        out.write('Skipped adding %s property sheet to portal_properties\n' % PROPERTY_SHEET)
    sheet = getattr(portal_props, PROPERTY_SHEET)

    if not hasattr(sheet, FIELD_NAME):
        safeEditProperty(sheet, FIELD_NAME, PROPERTY_FIELD, 'lines')
        out.write('Added %s property field to %s property sheet\n' % (FIELD_NAME, PROPERTY_SHEET))
    else:
        out.write('Skipped adding %s property field to %s property sheet\n' % (FIELD_NAME, PROPERTY_SHEET))

def setupSkin(self, out, skinFolder):
    """ Setup product skin layer """

    skinstool=getToolByName(self, 'portal_skins')
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

    out.write('setupSkin... \n')
    skinstool = getToolByName(self, 'portal_skins')
    addDirectoryViews(skinstool, SKINS_DIR, GLOBALS)
    setupSkin(self, out, PROJECTNAME)

    installResources(self, out)
    out.write("Installed Resources... \n")

    mtool = getToolByName(self, 'portal_migration')
    plone_version = mtool.getFileSystemVersion()
    if plone_version == '2.0.5':
         setupSkin(self, out, PROJECTNAME+'/2.0.5')
         out.write('Added %s/2.0.5 Layer to portal_skins\n' % PROJECTNAME)

    addPropertySheet(self, out)

    addConfiglet(self, out)

    return out.getvalue()

def uninstall(self):
    """ Product uninstallation """

    out = StringIO()

    removeConfiglet(self, out)

    out.write('removeSkin... \n')
    removeSkin(self, [PROJECTNAME, PROJECTNAME+'/2.0.5'])

    return out.getvalue()
