# Author: Melnychuk Taras
# Contact: fenix@quintagroup.com
# Date: $Date: 2005-12-23 11:42:10
# Copyright: quintagroup.com

"""
This module is created for installing PloneSMSCommunicator tool to Plone site. It has such functions:

     - `install`: this function sets all types in PloneSMSCommunicator tool, also install skin directory and other
     - `install_configlet`: install configlet to portal control panel
     - `remove_configlet`: remove configlet from portal control panel
     - `uninstall`: uninstall all needed things

"""
__docformat__ = 'restructuredtext'


from Products.Archetypes.Extensions.utils import installTypes, install_subskin
from Products.Archetypes.public import listTypes
from Products.CMFCore.utils import getToolByName
from StringIO import StringIO
import os

from Products.PloneSMSCommunicator.PloneSMSCommunicator import PloneSMSCommunicator
from Products.PloneSMSCommunicator.config import *

def install_configlet(self, out):
    """
    install configlet to portal control panel
    """
    control_panel=getToolByName(self,'portal_controlpanel')
    control_panel.registerConfiglet(PROJECTNAME,
                                    'Portal SMS Communicator',
                                    'string:${portal_url}/prefs_smsCommunicator_properties' ,
                                     permission=SMSCOMMUNICATOR_MP,
                                     imageUrl='link_icon.gif',
                                     category='Products',
                                    )
    print >> out, "Installed configlet.,,"


def remove_configlet(self, out):
    """
    remove configlet from portal control panel
    """
    control_panel=getToolByName(self,'portal_controlpanel')
    control_panel.unregisterConfiglet(PROJECTNAME) 
    print >> out, "Removed configlet.,,"

def install(self):
    """
    this function sets all types in PloneSMSCommunicator tool, also install skin directory and other
    """
    out=StringIO();
    installTypes(self, out, listTypes(PROJECTNAME), PROJECTNAME)
    portal=getToolByName(self, 'portal_url').getPortalObject()

    if COMMUNICATORID not in portal.objectIds():
        addPloneTool=portal.manage_addProduct[PROJECTNAME].manage_addTool(PROJECTNAME)

    install_subskin(self, out, GLOBALS)
    install_configlet(self, out)

    print >> out, "Successfully installed %s." % PROJECTNAME
    return out.getvalue()

def uninstall(self):
    """
    uninstall all needed things
    """
    out = StringIO()
    remove_configlet(self, out)
    print >> out, "Successfully uninstalled %s." % PROJECTNAME
    return out.getvalue()