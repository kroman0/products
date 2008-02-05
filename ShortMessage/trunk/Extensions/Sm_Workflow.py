# Author: Melnychuk Taras
# Contact: fenix@quintagroup.com
# Date: $Date: 2005-11-23 13:33:15 +0200 (Thu, 23 Nov 2005) $
# Copyright: quintagroup.com

"""
This is workflow for ShortMessage type that sends SMS upon object publishing.
This module define the following functions:

    - `createWorkflow`: create new workflow.
    - `fillWorkflow`: takes created workflow and add to it state, transitions, permissions and etc.
    - `addWorkflowScripts`: add ExternalMethod named send_publishedMessage to the workflow
    - `setupWorkflow`: setup created workflow to portal and set it to ShortMessage type
    - `send_publishedMessage`: Send message if it is published
"""
__docformat__ = 'restructuredtext'

from Products.DCWorkflow.DCWorkflow import DCWorkflowDefinition
from Products.CMFCore.CMFCorePermissions import ModifyPortalContent
from AccessControl.Permissions import view, access_contents_information
from Products.DCWorkflow.Default import r_anon, r_manager, r_owner, r_reviewer, \
                                        p_access, p_modify, p_view, p_request , p_review 
from Products.CMFCore.WorkflowTool import addWorkflowFactory
from Products.CMFCore import CMFCorePermissions
from Products.ShortMessage.config import *
from Products import ShortMessage

def addWorkflowScripts(wf):
    """add ExternalMethod named send_publishedMessage to the workflow"""
    if 'send_publishedMessage' not in wf.scripts.objectIds():
        wf.scripts.manage_addProduct['ExternalMethod'].manage_addExternalMethod('send_publishedMessage', 'Send Message', 'ShortMessage.Sm_Workflow', 'send_publishedMessage')

def fillWorkflow(wf):
    """takes created workflow and add to it state, transitions, permissions and etc"""
    for state in  ('pending', 'visible', 'published',):
        wf.states.addState(state)
    for transition in ('publish', 'submit', 'retract'):
        wf.transitions.addTransition(transition)
    for permision in (p_access, p_modify, view):
        wf.addManagedPermission(permision)
    for l in ('reviewer_queue',):
        wf.worklists.addWorklist(l)

    # set initial state
    wf.states.setInitialState('visible')

    wf_visible = wf.states['visible']
    wf_visible.setProperties(
                             title='Visible but not published',
                             transitions=('publish','submit'))
    wf_visible.setPermission(p_access, 1, (r_anon, r_manager, r_reviewer))
    wf_visible.setPermission(p_view, 1, (r_anon, r_manager, r_reviewer))
    wf_visible.setPermission(p_modify, 0, (r_manager, r_owner))


    wf_visible = wf.states['pending']
    wf_visible.setProperties(
                             title='Waiting for reviewer',
                             transitions=('retract', 'publish',))
    wf_visible.setPermission(p_access, 1, (r_manager, r_owner,  r_reviewer))
    wf_visible.setPermission(p_view, 1, (r_manager, r_owner,  r_reviewer))
    wf_visible.setPermission(p_modify, 0, (r_manager, r_reviewer))

    wf_published = wf.states['published']
    wf_published.setProperties(
                               title='Public',
                               transitions=())
    wf_published.setPermission(p_access, 1, (r_anon, r_manager,))
    wf_published.setPermission(p_view, 1, (r_anon, r_manager))
    wf_published.setPermission(p_modify, 0, (r_manager, ))


    tdef = wf.transitions['submit']
    tdef.setProperties(
                       title='Member requests publishing',
                       new_state_id='pending',
                       actbox_name='Submit',
                       actbox_url='%(content_url)s/content_submit_form',
                       props={'guard_permissions':p_request})

    tdef = wf.transitions['retract']
    tdef.setProperties(
                       title='Member retracts submission',
                       new_state_id='visible',
                       actbox_name='Retract',
                       actbox_url='%(content_url)s/content_retract_form',
                       props={'guard_permissions':p_request})

    tdef = wf.transitions['publish']
    tdef.setProperties(
                       title='Reviewer publishes content',
                       new_state_id='published',
		       script_name = 'send_publishedMessage',
                       actbox_name='Publish',
                       actbox_url='%(content_url)s/content_publish_form',
                       props={'guard_permissions':r_anon})

    wf.variables.setStateVar('review_state')

    ldef = wf.worklists['reviewer_queue']
    ldef.setProperties(description='Reviewer tasks',
                       actbox_name='Pending (%(count)d)',
                       actbox_url='%(portal_url)s/search?review_state=pending',
                       props={'var_match_review_state':'pending',
                              'guard_permissions':p_review})


def setupWorkflow(portal):
    portal_workflow = portal.portal_workflow
    addWorkflowFactory(createWorkflow,
                   id=Sm_WORKFLOWID,
                   title='ShortMessage Workflow')
    portal_workflow.manage_addWorkflow(id=Sm_WORKFLOWID, workflow_type=Sm_WORKFLOWID +' (ShortMessage Workflow)')
    addWorkflowScripts(portal_workflow[Sm_WORKFLOWID])
    #set workflow for SMS
    portal_workflow.setChainForPortalTypes( ('ShortMessage'), Sm_WORKFLOWID)

def send_publishedMessage(self, state_change):
    """Send message if it is published"""
    message_obj = state_change.object
    #send message to user(s)
    state_change.getPortal().portal_smsCommunicator.send_Request(message_obj.getSender(), message_obj.getRecipient(), message_obj.getBody())

def createWorkflow(id):
    """create new workflow"""
    wf = DCWorkflowDefinition(id)
    fillWorkflow(wf)
    return wf
