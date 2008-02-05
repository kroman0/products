from Products.Archetypes.Extensions.utils import installTypes, install_subskin
from Products.Archetypes.public import listTypes
from Products.CMFCore.utils import getToolByName
from StringIO import StringIO
import os

from Products.PloneSMSCommunicator.PloneSMSCommunicator import PloneSMSCommunicator
from Products.PloneSMSCommunicator.config import *

def install_configlet(self, out):
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
    control_panel=getToolByName(self,'portal_controlpanel')
    control_panel.unregisterConfiglet(PROJECTNAME) 
    print >> out, "Removed configlet.,,"

def install(self):

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
    out = StringIO()
    remove_configlet(self, out)
    print >> out, "Successfully uninstalled %s." % PROJECTNAME
    return out.getvalue()