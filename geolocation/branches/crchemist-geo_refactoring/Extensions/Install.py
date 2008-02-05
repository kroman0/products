import string
from cStringIO import StringIO
from Products.CMFCore.utils import getToolByName
from Products.CMFCore.DirectoryView import addDirectoryViews

from Products.geolocation.config import *

PORTAL_TYPES = ['Document', 'News Item', 'Event', 'Link', 'Image']

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

def installGEOLocationAction(self):
    """ add geoLocation edit tab for content types """
    ptypes = getToolByName(self, 'portal_types')
    for tname in PORTAL_TYPES:
        type = ptypes.getTypeInfo(tname)
        type.addAction('edit_location',
                      name='GEO Location',
                      action='string:edit_location',
                      condition='',
                      permission='Modify portal content',
                      category='object')

def uninstallGEOLocationAction(self):
    """ remove geoLocation edit tab for content types """
    ptypes = getToolByName(self, 'portal_types')
    for tname in PORTAL_TYPES:
        type = ptypes.getTypeInfo(tname)
        actions = type._cloneActions()
        actions = [a for a in actions if a.id != 'edit_location']
        type._actions = tuple(actions)

def install(self):
    """ Product installation """
    out = StringIO()
    out.write('setupSkin... \n')
    setupSkin(self, out, PROJECTNAME)
    catalog = getToolByName(self, 'portal_catalog')
    if 'geoLocation' not in catalog.indexes():
        catalog.addIndex('geoLocation','FieldIndex')
    if 'geoLocation' not in catalog.schema():
        catalog.addColumn('geoLocation')
    out.write('geoLocation index created')
    installGEOLocationAction(self)
    out.write('Added geolocation edit for content types')
    return out.getvalue()

def uninstall(self):
    out = StringIO()
    removeSkin(self, [PROJECTNAME,])
    uninstallGEOLocationAction(self)
    out.write('Removed geolocation edit for content types')