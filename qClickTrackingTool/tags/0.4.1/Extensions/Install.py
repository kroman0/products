from Products.Archetypes.public import listTypes
from Products.Archetypes.Extensions.utils import installTypes, install_subskin 
from Products.CMFCore.WorkflowTool import addWorkflowFactory
from Products.CMFFormController.FormAction import FormActionKey
from Products.CMFCore import CMFCorePermissions 
from Products.CMFCore.utils import getToolByName
from Products.CMFDefault.Link import Link
from StringIO import StringIO

from Products.qClickTrackingTool.ClickTracker import ClickTracker
from Products.qClickTrackingTool.Workflow import createWorkflow
from Products.qClickTrackingTool.ClickTracker import ClickTracker
from Products.qClickTrackingTool.config import *


def write_object_properties(self, obj, out):
    properties = {}
    pc = getToolByName(self, 'portal_clicktracker')
    if getObjectsType(self, pc, out) == 'Link':
        properties['id'] = obj.id
        properties['title'] = obj.title
        properties['description'] = obj.description
        properties['remote_url'] = obj.getRemoteUrl()
    else:
        properties['id'] = obj.id
        properties['title'] = obj.Title()
        properties['description'] = obj.Description()
        properties['remote_url'] = obj.getRemoteUrl()

    return properties

def update_object(self, obj, properties, out):
    obj.update(title       = properties['title'],
               description = properties['description'],
               url         = properties['remote_url'])

def convert_objects(self, container, new_type, out):
    pt = getToolByName(self, 'portal_types')
    if getObjectsType(self, container, out):
        for o in listFolderItems(container)[:]:
            prop = write_object_properties(self, o, out)
            container._delObject(o.id)
            fti = pt.getTypeInfo('ClickTracker')
            fti.manage_changeProperties(allowed_content_types = (new_type,))
            container.invokeFactory(id = prop['id'], type_name=new_type)
            campaign=getattr(container, prop['id'])
            update_object(self, campaign, prop, out)

def listFolderItems(container):
    res = []
    ids = container.objectIds()
    for ob_id in ids:
        res.append(container._getOb(ob_id))
    return res

def getObjectsType(self, container, out):
    pt = getToolByName(self, 'portal_types')
    ids = container.objectIds()
    if ids:
        obj = container._getOb(ids[0])
        type_obj = obj.meta_type
    else:
        print >> out, "Portal click tracker is empty..."
        type_obj = None

    return type_obj

def setPortalFactoryType(self, out,):
    pf=getToolByName(self, 'portal_factory')
    ftypes=list(pf.getFactoryTypes())
    if TYPE_NAME not in ftypes:
        ftypes.append(TYPE_NAME)
        pf.manage_setPortalFactoryTypes(listOfTypeIds=ftypes)
    else:
        print >>out, " %s type already  in portal_factory..." %TYPE_NAME

    print >> out, "Set %s type to portal_factory" %TYPE_NAME

def install_tool(self, out, tool='ClickTracker'):
    portal=getToolByName(self, 'portal_url').getPortalObject()
    pt = getToolByName(self, 'portal_types')
    if not TOOLID in portal.objectIds():
        addPloneTool=portal.manage_addProduct[PROJECTNAME].manage_addTool(tool)
    else:
        qi=getToolByName(self, 'portal_quickinstaller')
        p=qi._getOb(PROJECTNAME, None)
        oldVersion=p.getInstalledVersion()
        newVersion= qi.getProductVersion(PROJECTNAME)
        pc = getToolByName(self, 'portal_clicktracker')
        if oldVersion<newVersion:
            convert_objects(self, pc, TYPE_NAME, out)

def customizing_FormController(self, out):
    fc = getToolByName(self, 'portal_form_controller')
    fc.addFormAction('validate_integrity',
                     'success',
                     'campaign',
                      None,
                     'redirect_to',
                     'string:portal_url/portal_clicktracker/portal_clicktracker_view')
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
    portal_workflow.setChainForPortalTypes( ('campaign'), C_WORKFLOWID)
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

def remove_FormControllerAction(self, out):
    fc = getToolByName(self, 'portal_form_controller')
    if fc.actions.match('validate_integrity', 'success', TYPE_NAME, None):
        fc.actions.delete(FormActionKey('validate_integrity', 'success', TYPE_NAME, None, fc))

def install(self):

    out=StringIO();

    pt = getToolByName(self, 'portal_types')
    installTypes(self, out, listTypes(PROJECTNAME), PROJECTNAME)
    setPortalFactoryType(self, out)
    install_subskin(self, out, GLOBALS)
    install_workflow(self, out)
    install_tool(self, out)
    install_configlet(self, out)
    fix_permissions(self, out)
    customizing_FormController(self, out)

    print >> out, "Successfully installed %s." % PROJECTNAME
    return out.getvalue()

def uninstall(self):
    out = StringIO()

    remove_configlet(self, out)
    remove_FormControllerAction(self, out)

    print >> out, "Successfully uninstalled %s." % PROJECTNAME
    return out.getvalue()