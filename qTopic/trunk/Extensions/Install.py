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

    pact = getToolByName(self, 'portal_actions')
    pact.addAction( 'export_csv',
                    'Export in CSV',
                    'string:$object_url/export_csv?download=1',
                    'python:(object.meta_type == "qTopic") or (object.meta_type == "ATTopic")',
                    'View',
                    'document_actions')
    pact_icons = getToolByName(self, 'portal_actionicons')
    pact_icons.addActionIcon('plone',
                             'export_csv',
                             'topic_icon.gif',
                             'Export in CSV')

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
        
    pact_icons = getToolByName(self, 'portal_actionicons')
    pact_icons.removeActionIcon('plone', 'export_csv')