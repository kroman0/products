import string
from cStringIO import StringIO

from Products.CMFCore.utils import getToolByName
from Products.CMFCore.DirectoryView import addDirectoryViews

from Products.CMFPlone.migrations.migration_util import safeEditProperty
from Products.CMFCore.Expression import Expression, createExprContext

from Products.qPloneDropDownMenu.config import *

configlets = ({'id':PROJECT_NAME,
    'name':'Drop Down Menu',
    'action':'string:${portal_url}/prefs_dropdownmenu_edit_form',
    'condition':'',
    'category':'Products',
    'visible':1,
    'appId':PROJECT_NAME,
    'permission':VIEW_PERMISSION,
    'imageUrl':'qplonedropdownmenu.gif'},
   {'id':'csshover',
    'name':'CSS Hover',
    'action':'string:${portal_url}/prefs_csshover_edit_form',
    'condition':'',
    'category':'Products',
    'visible':1,
    'appId':'csshover',
    'permission':VIEW_PERMISSION},)

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

def updateMenu(self):
    out = ''

    pu = getToolByName(self, 'plone_utils')

    if hasattr(pu, 'createTopLevelTabs'):
        pactions = getToolByName(self, 'portal_actions').listFilteredActionsFor(self)
        tl_tabs = pu.createTopLevelTabs(pactions)

        for act in tl_tabs:
                out += '<li id="portaltab-%s" class="plain"><a href="%s" accesskey="t">' % \
                    (act['id'], act['url']) + act['name'] + '</a></li>\n'
    else:
        portal = getToolByName(self, 'portal_url').getPortalObject()

        portal_act = getToolByName(self, 'portal_actions')
        actions=portal_act._cloneActions()

        for act in actions:
            if act.category == 'portal_tabs':
                out += '<li id="portaltab-%s" class="plain"><a href="%s" accesskey="t">%s</a></li>\n' % \
                    (act.id, \
                     Expression(act.getActionExpression())(createExprContext(portal, portal, portal)), \
                     act.title)

    portal_props = getToolByName(self, 'portal_properties')
    if not hasattr(portal_props, PROPERTY_SHEET):
        portal_props.addPropertySheet(PROPERTY_SHEET, 'DropDown Menu Properties')
    ap = getattr(portal_props, PROPERTY_SHEET)
    safeEditProperty(ap, 'menu', out, 'text')

def setupSkin(self, out, skinFolder):

    skinstool=getToolByName(self, 'portal_skins')

    addDirectoryViews(skinstool, SKINS_DIR, GLOBALS)

    for skin in skinstool.getSkinSelections():
        path = skinstool.getSkinPath(skin)
        path = map( string.strip, string.split( path,',' ) )

        if not skinFolder in path:
            try:
                path.insert( path.index( 'custom')+1, skinFolder )
            except ValueError:
                path.append(skinFolder)
            path = string.join( path, ', ' )
            skinstool.addSkinSelection( skin, path )
            out.write('  %s layer sucessfully installed into skin %s.\n' % (skinFolder, skin))
        else:
            out.write('  %s layer was already installed into skin %s.\n' % (skinFolder, skin))

def setupTool(self):

    portal_url = getToolByName(self, 'portal_url')
    p = portal_url.getPortalObject()
    x = p.manage_addProduct[PROJECT_NAME].manage_addTool(type='DropDownMenu Tool')

def install(self):
    out = StringIO()

    registerCSS(self, out)

    configTool = getToolByName(self, 'portal_controlpanel', None)
    if configTool:
        for conf in configlets:
            configTool.registerConfiglet(**conf)
            out.write('Added configlet %s\n' % conf['id'])

    if hasattr(self, UNIQUE_ID):
        self.manage_delObjects([UNIQUE_ID])
        out.write('Deleting old %s\n' % (UNIQUE_ID))
    setupTool(self)
    out.write('Added %s to the portal root folder\n' % (UNIQUE_ID))

    portal_props = getToolByName(self, 'portal_properties')
    if not hasattr(portal_props, PROPERTY_SHEET):
        out.write('updateMenu... \n')
        updateMenu(self)
    else:
        out.write('skipping updateMenu... \n')

    out.write('setupSkin... \n')
    setupSkin(self, out, 'qPloneDropDownMenu')

    return out.getvalue()

def uninstall(self):
    out = StringIO()

    unregisterCSS(self, out)

    configTool = getToolByName(self, 'portal_controlpanel', None)
    if configTool:
        for conf in configlets:
            configTool.unregisterConfiglet(conf['id'])
            out.write('Removed configlet %s\n' % conf['id'])

    return out.getvalue()