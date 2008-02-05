from StringIO import StringIO
from Products.Archetypes import listTypes
from Products.Archetypes.Extensions.utils import installTypes, install_subskin
from Products.CMFCore.utils import getToolByName

from Products.qTopic.config import *

def install(self):
    out = StringIO()
                         
    installTypes(self, out, listTypes(PROJECTNAME), PROJECTNAME)
    print >> out, 'Types Installed'

    install_subskin(self, out, GLOBALS)
    print >> out, 'Skins Installed'

    out.write('Installation %s successfully completed.\n' % PROJECTNAME)
    return out.getvalue()


def uninstall(self):
    skinstool = getToolByName(self, 'portal_skins')
    for skinName in skinstool.getSkinSelections():
        path = skinstool.getSkinPath(skinName)
        path = [i.strip() for i in  path.split(',')]
        if SKINS_SUBDIR in path:
            path.remove(SKINS_SUBDIR)
            path = ','.join(path)
            skinstool.addSkinSelection(skinName, path)



