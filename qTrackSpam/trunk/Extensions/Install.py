from Products.Archetypes.public import listTypes
from Products.Archetypes.Extensions.utils import installTypes, install_subskin 
from Products.CMFCore import CMFCorePermissions 
from Products.CMFCore.utils import getToolByName
from StringIO import StringIO
import sys

from Products.qTrackSpam.config import *

def install(self):
    """ install product """
    out = StringIO();
    portal = getToolByName(self,'portal_url').getPortalObject()
    installTypes(self, out, listTypes(PROJECTNAME), PROJECTNAME)
    install_subskin(self, out, GLOBALS)
    install_configlet(self, out)
    try:
        portal.manage_addProduct[PROJECTNAME].manage_addTool(TOOL_METATYPE)
    except:
        # heuristics for testing if an instance with the same name already exists
        # only this error will be swallowed.
        # Zope raises in an unelegant manner a 'Bad Request' error
        e=sys.exc_info()
        if e[0] != 'Bad Request':
            raise



    print >> out, "Successfully installed %s." % PROJECTNAME
    return out.getvalue()

def uninstall(self):
    """ uninstall product """
    out = StringIO()
    control_panel = getToolByName(self, 'portal_controlpanel', None)
    actions = control_panel._cloneActions()
    res = [a.id for a in actions if a.id == PROJECTNAME]
    for i in res:
        control_panel.unregisterConfiglet(i)
        out.write('Removed configlet %s\n' % i)

    print >> out, "Successfully uninstalled %s." % PROJECTNAME
    return out.getvalue()

def install_configlet(self, out):
    control_panel=getToolByName(self,'portal_controlpanel')
    control_panel.registerConfiglet(PROJECTNAME,
                                    'BlackList Importer',
                                    'string:${portal_url}/prefs_blacklist_importer',
                                     permission = 'Manage Portal',
                                     category   = 'Products',
                                    )
    control_panel.registerConfiglet(PROJECTNAME,
                                    'Clean TrackBacks',
                                    'string:${portal_url}/prefs_clean_trackbacks',
                                     permission = 'Manage Portal',
                                     category   = 'Products',
                                    )
    print >> out, "Installed configlet.,,"
