import string
from cStringIO import StringIO
from Products.CMFCore.utils import getToolByName
from Products.CMFCore.DirectoryView import addDirectoryViews
from Products.Plone4ArtistsAudioPatch.config import *

def setupSkin(self, out, skinFolder):
    """ Setup product skin layer """
    skinstool = getToolByName(self, 'portal_skins')
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

def installAction(self):
    ptypes = getToolByName(self, 'portal_types')
    type = ptypes.getTypeInfo('File')
    type.addAction('encode',
                    name='Encode',
                    action='string:${object_url}/audio_encoded_view',
                    condition='python: object.get_content_type() == "audio/mpeg"',
                    permission='Modify portal content',
                    category='object')
                    
def uninstallAction(self):
    ptypes = getToolByName(self, 'portal_types')
    type = ptypes.getTypeInfo('File')
    actions = type._cloneActions()
    actions = [a for a in actions if a.id != 'encode']
    type._actions = tuple(actions)

def install(self):
    """ Product installation """
    out = StringIO()
    out.write('setupSkin... \n')
    setupSkin(self, out, PROJECTNAME)
    installAction(self)
    out.write('Added new action for file content type')
    return out.getvalue()
    
def uninstall(self):
    out = StringIO()
    removeSkin(self, [PROJECTNAME,])
    uninstallAction(self)
    out.write('Removed audio_enc action for file content type')