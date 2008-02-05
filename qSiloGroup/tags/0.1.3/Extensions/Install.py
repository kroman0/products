import string
from cStringIO import StringIO

from Products.Archetypes import listTypes
from Products.Archetypes.Extensions.utils import installTypes

from Products.CMFCore.utils import getToolByName
from Products.CMFCore.DirectoryView import addDirectoryViews

from Products.qSiloGroup.config import *

def removeSkin(self, layer):
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

def setupActions(self, out):
    out.write("Inspecting portal_types\n")
    types_tool = getToolByName(self, 'portal_types')
    for ptype in types_tool.objectValues():
        if ptype.getId() == 'Folder':
            action = ptype.getActionById( 'edit_silo_navigation', default=None )
            if action is None:
                out.write( '  Added Silo Navigation tab for %s\n' % ptype.getId() )
                ptype.addAction( 'edit_silo_navigation'
                               , 'Silo Navigation'
                               , 'string:${object_url}/silo_navigation_form'
                               , ''
                               , 'Modify portal content'
                               , 'object'
                               , visible=1
                               )
def removeActions(self):
    tool = getToolByName(self, 'portal_types')
    for ptype in tool.objectValues():
        if ptype.getId() == 'Folder':
            action = ptype.getActionById( 'edit_silo_navigation', default=None )
            if action != None:
                acts = list(ptype.listActions())
                ptype.deleteActions([acts.index(a) for a in acts if a.getId()=='edit_silo_navigation'])

def install(self):
    out = StringIO()

    out.write('setupSkin... \n')
    setupSkin(self, out, PROJECTNAME)

    installTypes(self, out, listTypes(PROJECTNAME), PROJECTNAME)
    print >> out, 'Type Installed'

    setupActions(self, out)

    return out.getvalue()

def uninstall(self):
    out = StringIO()

    removeActions(self)

    removeSkin(self, PROJECTNAME)

    return out.getvalue()