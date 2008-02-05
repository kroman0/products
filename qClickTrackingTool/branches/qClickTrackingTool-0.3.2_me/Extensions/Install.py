from Products.Archetypes.public import listTypes
from Products.Archetypes.Extensions.utils import installTypes, install_subskin 
from Products.CMFCore.WorkflowTool import addWorkflowFactory
from Products.CMFCore import CMFCorePermissions 
from Products.CMFCore.utils import getToolByName
from Products.CMFDefault.Link import Link
from StringIO import StringIO

from Products.qClickTrackingTool.ClickTracker import ClickTracker
from Products.qClickTrackingTool.Workflow import createWorkflow
from Products.qClickTrackingTool.ClickTracker import ClickTracker
from Products.qClickTrackingTool.config import *


def isSwitchedToATCT(self):
    pt = getToolByName(self, 'portal_types')
    doc_fti = pt.getTypeInfo('Document')
    if doc_fti.Metatype() == 'ATDocument':
        return 1
    else:
        return 0

def write_object_properties(self, obj):
    properties = {}
    if not isSwitchedToATCT(self):
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

def update_object(self, obj, properties):
    if isSwitchedToATCT(self):
        obj.update(title       = properties['title'],
                   description = properties['description'],
                   remoteUrl   = properties['remote_url'])
    else:
        setattr(obj, 'title',       properties['title'])
        setattr(obj, 'description', properties['description'])
        setattr(obj, 'remote_url',  properties['remote_url'])

def convert_objects(self, container, new_type, out):
    pt = getToolByName(self, 'portal_types')
    if getObjectsType(self, container, out):
        for o in listFolderItems(container)[:]:
            prop = write_object_properties(self, o)
            container._delObject(o.id)
            fti = pt.getTypeInfo('ClickTracker')
            fti.manage_changeProperties(allowed_content_types = (new_type,))
            container.invokeFactory(id = prop['id'], type_name=new_type)
            campaign=getattr(container, prop['id'])
            update_object(self, campaign, prop)
    else:
        create_repType(self, out)

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

def install_tool(self, out, tool='ClickTracker'):
    portal=getToolByName(self, 'portal_url').getPortalObject()
    pt = getToolByName(self, 'portal_types')
    create_repType(self, out)
    if not TOOLID in portal.objectIds():
        addPloneTool=portal.manage_addProduct[PROJECTNAME].manage_addTool(tool)
    else:
        qi=getToolByName(self, 'portal_quickinstaller')

        p=qi._getOb(PROJECTNAME, None)
        oldVersion=p.getInstalledVersion()
        newVersion= qi.getProductVersion(PROJECTNAME)
        is_migrated = isSwitchedToATCT(self)
        pc = getToolByName(self, 'portal_clicktracker')
        if oldVersion<newVersion:
            convert_objects(self, pc, REP_TYPE, out)

        if is_migrated:
            if getObjectsType(self, pc, out) != 'ATLink':
                convert_objects(self, pc, REP_TYPE, out)

            else:
                print >> out, "Repurpouse type already migrated to ATCT..."
        else:
            if getObjectsType(self, pc, out) == 'ATLink':
                convert_objects(self, pc, 'Link', out)

            else:
                print >> out, "Repurpouse type already migrated to CMF..."

    print >> out, "Installed %s tool..." % tool

def repurpose_content_type(self, old_type, new_type):
    pt = getToolByName(self, 'portal_types')
    copy = pt.manage_copyObjects(old_type)
    pt.manage_pasteObjects(cb_copy_data=copy)
    copy_name = 'copy_of_%s' %old_type
    copy_obj = pt._getOb(copy_name)
    copy_obj.manage_renameObject(copy_name, new_type)
    setattr(copy_obj, 'title', new_type)

def create_repType(self, out):
    pt = getToolByName(self, 'portal_types')
    if REP_TYPE in pt.objectIds():
        print >> out, "%s already installed ..." %REP_TYPE
        pt._delObject(REP_TYPE)
    repurpose_content_type(self, 'Link', 'Campaign')
    print >> out, "Repurpose content successfully"

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

    pt = getToolByName(self, 'portal_types')
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