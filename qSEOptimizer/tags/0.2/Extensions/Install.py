import string
from App.Common import package_home
from os.path import exists as path_exists, join as path_join
from cStringIO import StringIO
from Products.CMFCore.utils import getToolByName
from Products.CMFCore.DirectoryView import addDirectoryViews

from Products.qSEOptimizer import qSEO_globals

qSEO_CONTENT = ['File','Document','News Item','BlogEntry']
qSEO_FOLDER  = []
qSEO_TYPES   = qSEO_CONTENT + qSEO_FOLDER

def setupSkin(self, out, skinFolder):
    skinstool=getToolByName(self, 'portal_skins')

    addDirectoryViews(skinstool, 'skins', qSEO_globals)

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
            out.write('  Subskin sucessfully installed into skin %s.\n' % skin)
        else:
            out.write('  Subskin was already installed into skin %s.\n' % skin)

def removeSkin(self, skins = []):
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


def install(self):
    out = StringIO()

    out.write('Call setupSkin... \n')

    mtool = getToolByName(self, 'portal_migration')
    plone_version = mtool.getFileSystemVersion()
    product_path = package_home(qSEO_globals)

    skin = 'qSEOptimizer'
    versioned_skin = path_join(product_path, 'skins', skin, plone_version)
    out.write('  Searching for %s... ' % versioned_skin) 

    if path_exists(versioned_skin):
        out.write('found.\n') 
        skin = 'qSEOptimizer/%s' % plone_version
    else:
        out.write("""not found.\n
    Limited functionality mode.
    Upgrade qSEOptimizer product or report to support@quintagroup.com if uprade not available.\n\n""") 
    setupSkin(self, out, skin)

    out.write('Call setupActions... \n')
    setupActions(self, out)

    return out.getvalue()

def uninstall(self):
    removeSkin(self, ('qSEOptimizer',))
    return 'qSEOptimizer uninstalled successfully.'
