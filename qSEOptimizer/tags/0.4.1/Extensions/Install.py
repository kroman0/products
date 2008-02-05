import string
from App.Common import package_home
from os.path import exists as path_exists, join as path_join
from cStringIO import StringIO
from Products.CMFCore.utils import getToolByName
from Products.CMFCore.DirectoryView import addDirectoryViews
from Products.qSEOptimizer import qSEO_globals
from Products.CMFCore.CMFCorePermissions import ManagePortal
from OFS.ObjectManager import BadRequestException

configlets = ({'id':'qSEOptimizer',
    'name':'Search Engine Optimizer',
    'action':'string:${portal_url}/prefs_qseo_setup_form',
    'condition':'',
    'category':'Products',
    'visible':1,
    'appId':'qSEOptimizer',
    'permission':ManagePortal,
    'imageUrl':'search_icon.gif'},)

qSEO_CONTENT = ['File','Document','News Item','BlogEntry']
qSEO_FOLDER  = []
qSEO_TYPES   = qSEO_CONTENT + qSEO_FOLDER
try:
    True
except:
    True = 1
    False = 0

def setupSkin(self, out, layers):
    """Setup skins"""
    skinstool=getToolByName(self, 'portal_skins')
    addDirectoryViews(skinstool, 'skins', qSEO_globals)

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

def removeSkin(self, layer):
    """Remove layers"""
    skinstool = getToolByName(self, 'portal_skins')
    for skinName in skinstool.getSkinSelections():
	original_path = skinstool.getSkinPath(skinName)
	original_path = [l.strip() for l in original_path.split(',')]
	new_path= []
	for l in original_path:
	    if (l == layer) or (l.startswith(layer+'/')):
		continue
	    new_path.append(l)
	skinstool.addSkinSelection(skinName, ','.join(new_path))
	
def setupActions(self, out):
    # And now update the relevant portal_type actions
    out.write("Inspecting portal_types\n")
    tool = getToolByName(self, 'portal_types')
    for ptype in tool.objectValues():
        if ptype.getId() in qSEO_TYPES:
            #add the action for viewing versioning
            action = ptype.getActionById( 'seo_properties', default=None )
            if action is None:
                out.write( '  Added SEO Properties tab for %s\n' % ptype.getId() )
                ptype.addAction( 'seo_properties'
                               , 'SEO Properties'
                               , 'string:${object_url}/qseo_properties_edit_form'
                               , ''
                               , 'Modify portal content'
                               , 'object'
                               , visible=1
                               )
def removeActions(self):
    # And now update the relevant portal_type actions
    tool = getToolByName(self, 'portal_types')
    for ptype in tool.objectValues():
        if ptype.getId() in qSEO_TYPES:
            #delet the action for viewing versioning
            action = ptype.getActionById( 'seo_properties', default=None )
            if action != None:
                acts = list(ptype.listActions())
                ptype.deleteActions([acts.index(a) for a in acts if a.getId()=='seo_properties'])

def install(self):
    """Install product"""
    out = StringIO()
    Layers =[]
    mtool = getToolByName(self, 'portal_migration')
    plone_version = mtool.getFileSystemVersion()
    product_path = package_home(qSEO_globals)
    versioned_skin = path_join(product_path, 'skins','qSEOptimizer', plone_version)
    #add exposeDCMetaTags property to Plone 2.0.x
    props = getToolByName(self, 'portal_properties').site_properties
    if not hasattr(props, 'exposeDCMetaTags'):
            props._setProperty('exposeDCMetaTags', True, 'boolean')

    Layers.append('qSEOptimizer')
    out.write('  Searching for %s... ' % versioned_skin)
    if path_exists(versioned_skin):
        out.write('found.\n')
        Layers.append('qSEOptimizer/%s' % plone_version)
    else:
        out.write("""not found.\nLimited functionality mode. Upgrade qSEOptimizer product or report to support@quintagroup.com if uprade not available.\n\n""") 
    out.write('Call setupSkin... \n')
    setupSkin(self, out, Layers)

    out.write('Call setupActions... \n')
    setupActions(self, out)

    configTool = getToolByName(self, 'portal_controlpanel', None)
    if configTool:
        for conf in configlets:
            configTool.registerConfiglet(**conf)
            out.write('Added configlet %s\n' % conf['id'])

    return out.getvalue()

def uninstall(self):
    """ Uninstall Products """
    out = StringIO()

    removeSkin(self, 'qSEOptimizer')
    removeActions(self)

    configTool = getToolByName(self, 'portal_controlpanel', None)
    if configTool:
        for conf in configlets:
            try:
                configTool.unregisterConfiglet(conf['id'])
            except BadRequestException,KeyError:
                portal_icons = getToolByName(self,'portal_actionicons')
                portal_icons.manage_removeActionIcon(conf['category'],conf['id'])
            out.write('Removed configlet %s\n' % conf['id'])

    return 'qSEOptimizer succesfully removed'
