# Author: Melnychuk Taras
# Contact: fenix@quintagroup.com
# Date: $Date: 2006-02-08 12:32:23
# Copyright: quintagroup.com

from Products.Archetypes.public import listTypes
from Products.Archetypes.Extensions.utils import installTypes, install_subskin 
from Products.CMFCore import CMFCorePermissions 
from Products.CMFCore.utils import getToolByName
from StringIO import StringIO

from Products.qPloneEpydoc.PloneEpydoc import PloneEpydoc
from Products.qPloneEpydoc.config import *


def install_tool(self, out, tool='PloneEpydoc'):
    portal=getToolByName(self, 'portal_url').getPortalObject()
    pt = getToolByName(self, 'portal_types')
    if not TOOLID in portal.objectIds():
        addPloneTool=portal.manage_addProduct[PROJECTNAME].manage_addTool(tool)


def install_configlet(self, out):
    control_panel=getToolByName(self,'portal_controlpanel')
    control_panel.registerConfiglet(PROJECTNAME,
                                    'PloneEpydoc',
                                    'string:${portal_url}/prefs_portal_documentation',
                                     permission=MANAGE_TOOL_PERMISSION,
                                     imageUrl='topic_icon.gif',
                                     category='Products',
                                    )
    print >> out, "Installed configlet.,,"



def remove_configlet(self, out):

    control_panel=getToolByName(self,'portal_controlpanel')
    control_panel.unregisterConfiglet(PROJECTNAME) 

def install(self):

    out=StringIO();

    installTypes(self, out, listTypes(PROJECTNAME), PROJECTNAME)
    install_subskin(self, out, GLOBALS)
    install_tool(self, out)
    install_configlet(self, out)

    print >> out, "Successfully installed %s." % PROJECTNAME
    return out.getvalue()

def uninstall(self):
    out = StringIO()

    remove_configlet(self, out)

    print >> out, "Successfully uninstalled %s." % PROJECTNAME
    return out.getvalue()