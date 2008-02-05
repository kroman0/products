import string
from cStringIO import StringIO
from Products.CMFCore.utils import getToolByName
from Products.CMFCore.DirectoryView import addDirectoryViews
from Products.qPloneGoogleSitemaps import qPGS_globals

try:
    from Products.CMFCore.CMFCorePermissions import ManagePortal
except ImportError:
    from Products.CMFCore.permissions import ManagePortal

from OFS.ObjectManager import BadRequestException

configlets = ({'id':'qPloneGoogleSitemaps',
    'name':'Google Sitemaps',
    'action':'string:${portal_url}/prefs_gsm_overview',
    'condition':'',
    'category':'Products',
    'visible':1,
    'appId':'qPloneGoogleSitemaps',
    'permission':ManagePortal,
    'imageUrl':'qplonegooglesitemaps.gif'},)

def setupSkin(self, out, skinFolder):
    skinstool=getToolByName(self, 'portal_skins')

    addDirectoryViews(skinstool, 'skins', qPGS_globals)

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

def install(self):
    """ Install qPloneGoogleSitemaps """
    out = StringIO()
    if not hasattr(self.portal_properties, 'googlesitemap_properties'):
        self.portal_properties.addPropertySheet('googlesitemap_properties', 'Google SiteMap properties')

    props = self.portal_properties.googlesitemap_properties
    portalTypes = ('Plone Folder', 'ATFolder')
    new_portalTypes = ['Document', ]
    sitemap_properties = (
		('portalTypes', 'lines', new_portalTypes),
		('states', 'lines', ['published', ]),
    		('blackout_list', 'lines',[]),
                ('reg_exp', 'lines',[]),
		('urls', 'lines',[]),
		('verification_filename','string','')
	)
        
    types = self.portal_types.listContentTypes( by_metatype=1 )
    for prop_id, prop_type, prop_value in sitemap_properties:
        if not hasattr(props, prop_id):
            props._setProperty(prop_id, prop_value, prop_type)

    configTool = getToolByName(self, 'portal_controlpanel', None)
    if configTool:
        for conf in configlets:
            configTool.registerConfiglet(**conf)
            out.write('Added configlet %s\n' % conf['id'])

    out.write('Call setupSkin... \n')
    setupSkin(self, out, 'qPloneGoogleSitemaps')

    return out.getvalue()

def uninstall(self):
    """ Uninstall qPloneGoogleSitemaps """
    out = StringIO()

    props = getToolByName(self,'portal_properties')
    try:
        props.manage_delObjects(['googlesitemap_properties',])
    except BadRequestException: pass

    configTool = getToolByName(self, 'portal_controlpanel', None)
    if configTool:
        for conf in configlets:
            try:
                configTool.unregisterConfiglet(conf['id'])
            except BadRequestException,KeyError:
                portal_icons = getToolByName(self,'portal_actionicons')
                portal_icons.manage_removeActionIcon(conf['category'],conf['id'])
            out.write('Removed configlet %s\n' % conf['id'])

    return out.getvalue()
