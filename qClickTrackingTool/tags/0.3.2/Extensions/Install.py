from Products.Archetypes.public import listTypes
from Products.Archetypes.Extensions.utils import installTypes, install_subskin 
from Products.CMFCore.WorkflowTool import addWorkflowFactory
from Products.CMFCore import CMFCorePermissions 
from Products.CMFCore.utils import getToolByName
from Products.CMFDefault.Link import Link
from StringIO import StringIO

from Products.qClickTrackingTool.ClickTracker import ClickTracker
from Products.qClickTrackingTool.Workflow import createWorkflow
from Products.qClickTrackingTool.Campaign import Campaign
from Products.qClickTrackingTool.ClickTracker import ClickTracker
from Products.qClickTrackingTool.config import *


def tool_migration(self, out, oldVersion, newVersion):
    #get tools
    pc=getToolByName(self, 'portal_clicktracker')

    for o in pc.listFolderContents()[:]:
        #create temp link object
        temp_link=Link(id=o.getId(), title=o.Title(), remote_url=o.getRemoteUrl(), description=o.Description())
        #remove old link
        pc._delObject(o.getId())
        #create new Campaign
        pc.invokeFactory(id=temp_link.id, type_name='Campaign')
        campaign=getattr(pc, temp_link.id)
        campaign.update(title=temp_link.title, description=temp_link.description, remoteUrl=temp_link.remote_url)

    print >> out, "migration complete..."


def install_tool(self, out, tool='ClickTracker'):
    portal=getToolByName(self, 'portal_url').getPortalObject()
    if TOOLID  not in portal.objectIds():
        addPloneTool=portal.manage_addProduct[PROJECTNAME].manage_addTool(tool)
    else:
        qi=getToolByName(self, 'portal_quickinstaller')

        p=qi._getOb(PROJECTNAME, None)
        oldVersion=p.getInstalledVersion()
        newVersion= qi.getProductVersion(PROJECTNAME)
                            	
        if oldVersion < newVersion:
            tool_migration(self, out, oldVersion, newVersion)    

    print >> out, "Installed %s tool..." % tool
    
def install_configlet(self, out):
    control_panel=getToolByName(self,'portal_controlpanel')
    control_panel.registerConfiglet(PROJECTNAME,
                                    'Click Tracking Tool',
                                    'string:${portal_url}/%s/portal_clicktracker_view' % TOOLID,
                                     permission=MANAGE_CLICKTRACKINGTOOL_PERMISSION, 
                                     imageUrl='link_icon.gif',
                                     category='Products',
                                    )
    print >> out, "Installed configlet.,,"

def install_workflow(self, out):
    portal_workflow=getToolByName(self, 'portal_workflow')

    #register the workflow in the system
    addWorkflowFactory(createWorkflow,
                   id=C_WORKFLOWID,
                   title='Campaign Workflow')

    portal_workflow.manage_addWorkflow(id=C_WORKFLOWID, workflow_type=C_WORKFLOWID +' (Campaign Workflow)') 
    #set workflow for Campaign
    portal_workflow.setChainForPortalTypes( ('Campaign'), C_WORKFLOWID)           
    print >> out, "Installed workflow..."
    
def fix_permissions(self, out):
    portal_workflow=getToolByName(self, 'portal_workflow')
    #remove worklow from tool
    portal_workflow.setChainForPortalTypes( ('ClickTracker (qClickTrackingTool)'), '')    
    #set permission for portal_clicktracker
    pc=getToolByName(self, 'portal_clicktracker')
    pc.manage_permission(CMFCorePermissions.ListFolderContents, ('Manager', 'Owner', 'Anonymous'), 1)

    print >> out, "Click Tracking Tool Permissions fixed..."

def remove_configlet(self, out):
    # unregister Configlet
    control_panel=getToolByName(self,'portal_controlpanel')
    control_panel.unregisterConfiglet(PROJECTNAME) 

def install(self):
    
    out=StringIO();

    installTypes(self, out, listTypes(PROJECTNAME), PROJECTNAME)
    install_subskin(self, out, GLOBALS)
    install_workflow(self, out)
    install_tool(self, out)
    install_configlet(self, out)
    fix_permissions(self, out)

    print >> out, "Successfully installed %s." % PROJECTNAME
    return out.getvalue()

def uninstall(self):
    out = StringIO()

    remove_configlet(self, out)
      
    print >> out, "Successfully uninstalled %s." % PROJECTNAME
    return out.getvalue()
