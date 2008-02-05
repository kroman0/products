import string
from cStringIO import StringIO

from Products.CMFCore.utils import getToolByName
from Products.CMFCore.DirectoryView import addDirectoryViews

try:
    from Products.CMFCore.permissions import ManagePortal
except ImportError:
    from Products.CMFCore.CMFCorePermissions import ManagePortal

from Products.CMFPlone.migrations.migration_util import safeEditProperty

from Products.Archetypes.Extensions.utils import installTypes
from Products.Archetypes.public import listTypes

from Products.qPloneGoogleMaps.config import *

configlets = \
({'id':PROJECTNAME,
  'name':'Google Map Api Keys',
  'action':'string:${portal_url}/prefs_mapkeys_form',
  'condition':'',
  'category':'Products',
  'visible':1,
  'appId':PROJECTNAME,
  'permission':ManagePortal},)
  #'imageUrl':'niimportablefooter.gif'},)

def addProperty(self, out):
    """ Add property sheet to portal_properties """

    portal_props = getToolByName(self, 'portal_properties')
    if not hasattr(portal_props, PROPERTY_SHEET):
        portal_props.addPropertySheet(PROPERTY_SHEET, 'Maps Properties')
        out.write('Added %s property sheet...\n' % PROPERTY_SHEET)
    ap = getattr(portal_props, PROPERTY_SHEET)
    if not hasattr(ap, PROPERTY_FIELD):
        safeEditProperty(ap, PROPERTY_FIELD, MAP_API_KEYS, 'lines')
        out.write('Added %s property field to %s property sheet...\n' % (PROPERTY_FIELD, PROPERTY_SHEET))
    else: out.write('Skipped adding property...\n')

def removeProperty(self, out):
    """ Remove property sheet from portal_properties """

    portal_props = getToolByName(self, 'portal_properties')
    if hasattr(portal_props, PROPERTY_SHEET):
        portal_props.manage_delObjects(PROPERTY_SHEET)
        out.write('Deleted %s property sheet...\n' % PROPERTY_SHEET)

def addConfiglets(self, out):
    """ Add configlets to portal control panel """

    configTool = getToolByName(self, 'portal_controlpanel', None)
    if configTool:
        for conf in configlets:
            out.write('Added configlet %s\n' % conf['id'])
            configTool.registerConfiglet(**conf)

def removeConfiglets(self, out):
    """ Remove the configlet from the portal control panel """

    configTool = getToolByName(self, 'portal_controlpanel', None)
    if configTool:
        for conf in configlets:
            out.write('Removed configlet %s\n' % conf['id'])
            configTool.unregisterConfiglet('%s' % conf['id'])

def addCatalogIndex(self, name, out):
    """ Add to portal catalog given index """

    portal_catalog = getToolByName(self, 'portal_catalog')
    if name not in portal_catalog.indexes():
        portal_catalog.addIndex(name=name, type="FieldIndex")
        out.write('Added %s index to portal_catalog...\n' % name)

def removeCatalogIndex(self, name, out):
    """ Remove from portal catalog given index """

    portal_catalog = getToolByName(self, 'portal_catalog')
    if name in portal_catalog.indexes():
        portal_catalog.delIndex(name=name)
        out.write('Removed %s index from portal_catalog...\n' % name)

def addCatalogColumn(self, name, out):
    """ Add to portal catalog given metadata column """

    portal_catalog = getToolByName(self, 'portal_catalog')
    if name not in portal_catalog.schema():
        portal_catalog.addColumn(name=name)
        out.write('Added %s column metadata to portal_catalog...\n' % name)


def removeCatalogColumn(self, name, out):
    """ Remove from portal catalog given metadata column """

    portal_catalog = getToolByName(self, 'portal_catalog')
    if name in portal_catalog.schema():
        portal_catalog.delColumn(name=name)
        out.write('Removed %s column metadata from portal_catalog...\n' % name)

def installContentTypes(self, out):
    """ Install new portal types and add to the portal_factory """

    typesInfo = listTypes(PROJECTNAME)
    installTypes(self, out, typesInfo, PROJECTNAME)
    out.write("Installed types\n")
    factory_tool = getToolByName(self, 'portal_factory')
    types = factory_tool.getFactoryTypes().keys()
    for item in NEW_PORTAL_TYPES:
        if item not in types:
            types.append(item)
            factory_tool.manage_setPortalFactoryTypes(listOfTypeIds = types)
            out.write('Added %s portal type to portal_factory\n' % item)

def addTopicMapView(self, out, view):
    """ Add map view template to the topic type """

    portal_types = getToolByName(self, 'portal_types', None)
    if portal_types is not None:
        for tp in ['Folder', 'Large Plone Folder', 'Topic']:
            fti = getattr(portal_types, tp, None)
            if fti is not None:
                views = list(getattr(fti, 'view_methods'))
                if view not in views:
                    views.append(view)
                    fti.manage_changeProperties(view_methods = tuple(views))
                    out.write("Added new view template to '%s' FTI.\n" % tp)

def removeTopicMapView(self, out, view):
    """ Remove map view template from the topic type """

    portal_types = getToolByName(self, 'portal_types', None)
    if portal_types is not None:
        for tp in ['Folder', 'Large Plone Folder', 'Topic']:
            fti = getattr(portal_types, tp, None)
            if fti is not None:
                views = list(getattr(fti, 'view_methods'))
                if view in views:
                    views.remove(view)
                    fti.manage_changeProperties(view_methods = tuple(views))
                    out.write("Removed maps view template from '%s' FTI.\n" % tp)

def addPortlets(self, out, slots=[]):
    """ Add portlet to right slot """

    right_slots = getattr(self, 'right_slots', None)
    if right_slots != None:
        for slot in slots:
            if slot not in right_slots:
                right_slots = list(right_slots) + [slot,]
                self.right_slots = right_slots
                out.write('Added %s portlet to right_slots property.\n' % slot)

def removePortlets(self, out, slots=[]):
    """ Remove portlet from right slot """

    right_slots = list(getattr(self, 'right_slots', ()))
    for slot in slots:
        if slot in right_slots:
            right_slots.remove(slot)
            self.right_slots = right_slots
            out.write('Removed %s portlet from right slots property.\n' % slot)

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

    # add property field to 'maps_properties' sheet
    addProperty(self, out)

    # installing configlet
    addConfiglets(self, out)

    # adding indexes and metadata columns to portal_catalog
    addCatalogIndex(self, GEO_INDEX, out)
    addCatalogColumn(self, GEO_INDEX, out)

    out.write('Update catalog...\n')
    getToolByName(self, 'portal_catalog').refreshCatalog()

    # installin content types
    installContentTypes(self, out)

    # add portlets to right slot
    addPortlets(self, out, MAP_PORTLETS)

    # add map view template to the topic portal type
    addTopicMapView(self, out, 'topic_maps_view')

    # setup skin layer
    out.write('setupSkin... \n')
    setupSkin(self, out, PROJECTNAME)

    return out.getvalue()

def uninstall(self):
    """ Product uninstallation """

    out = StringIO()

    # remove property sheet 'maps_properties' from portal_properties
    removeProperty(self, out)

    # removing configlet
    removeConfiglets(self, out)

    # removing indexes and metadata columns from portal_catalog
    removeCatalogIndex(self, GEO_INDEX, out)
    removeCatalogColumn(self, GEO_INDEX, out)

    # remove portlets from right slot
    removePortlets(self, out, MAP_PORTLETS)

    # remove map view template from the topic portal type
    removeTopicMapView(self, out, 'topic_maps_view')

    # remove skin layer
    removeSkin(self, [PROJECTNAME,])

    return out.getvalue()