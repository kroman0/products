from Products.Archetypes.public import listTypes
from Products.Archetypes.Extensions.utils import installTypes, install_subskin 

from Products.CMFCore.utils import getToolByName
from Products.qClickTrackingTool.config import *
from StringIO import StringIO

from Products.qClickTrackingTool.ClickTracker import ClickTracker


def install(self):
    
    out=StringIO();

    installTypes(self, out, listTypes(PROJECTNAME), PROJECTNAME)
   
    install_subskin(self, out, GLOBALS)
    portal=getToolByName(self, 'portal_url').getPortalObject()
    addPloneTool=portal.manage_addProduct['qClickTrackingTool'].manage_addTool('ClickTracker')
    
    control_panel=getToolByName(self,'portal_controlpanel')
    control_panel.registerConfiglet('qClickTrackingTool',
                                    'Click Tracking Tool',
                                    'string:${portal_url}/prefs_clicktrackingtool',
                                     permission='ManagePortal',
                                     imageUrl='link_icon.gif',
                                     category='Products',
                                    )    
   
    
    print >> out, "Successfully installed %s." % PROJECTNAME
    return out.getvalue()

def uninstall(self):
    out = StringIO()

    control_panel=getToolByName(self,'portal_controlpanel')
    control_panel.unregisterConfiglet('qClickTrackingTool')
   
  
    print >> out, "Successfully uninstalled %s." % PROJECTNAME
    return out.getvalue()
