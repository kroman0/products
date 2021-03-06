# 
#
# Generated by dumpDCWorkflow.py written by Sebastien Bigaret
# Original workflow id/title: trackback_workflow/TrackBack Workflow
# Date: 2005/09/30 17:29:38.476 GMT+3
#
# WARNING: this dumps does NOT contain any scripts you might have added to
# the workflow, IT IS YOUR RESPONSABILITY TO MAKE BACKUPS FOR THESE SCRIPTS.
#
# The following scripts have been detected and should be backed up:
# - notifyTrackBack (Script (Python))
# - sbPublishEntry (Script (Python))
# - notifyTB (External Method)
# 
"""
Programmatically creates a workflow type
"""
__version__ = "$Revision: 1.1.1.1 $"[11:-2]

from Products.CMFCore.WorkflowTool import addWorkflowFactory

from Products.DCWorkflow.DCWorkflow import DCWorkflowDefinition

script_notifyTrackBack = """## Script (Python) "notifyTrackBack"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##parameters=change_state=None
##title=notify about TrackBack creating
##
from zLOG import LOG
LOG('SimpleBlog.TrackbackWorkflow',203,'debug','notifyTrackBack sript JUST CALLED')
if not change_state:
    return None
obj = change_state.object
# get to- and from- emails
member = context.portal_membership.getAuthenticatedMember()
blog = context.simpleblog_tool.getFrontPage(obj)
to_email = blog.getAdminEmail()
from_email = context.portal_url.getPortalObject().getProperty("email_from_address", "andrijm@neonet.if.ua")
if to_email:
    # get additional data for mail-template
    post_title = obj.aq_parent.Title()
    obj_url = obj.absolute_url()
    charset = context.portal_properties.site_properties.getProperty('default_charset','utf-8')
    body = obj.notifyTBtemplate(from_email=from_email, to_email=to_email, charset=charset, post_title=post_title, obj_url=obj_url)
    try:
        mh = context.MailHost
        mh.send(body)
    except:
        pass
LOG('SimpleBlog.TrackbackWorkflow',203,'debug','notifyTrackBack sript SUCCESSFULLY COMPLETED')
"""


def setupTrackback_workflow(wf):
    "..."
    wf.setProperties(title='TrackBack Workflow')

    for s in ['new', 'pending', 'published']:
        wf.states.addState(s)
    for t in ['retract', 'publish', 'make_pending']:
        wf.transitions.addTransition(t)
    for v in ['action', 'review_history', 'comments', 'actor', 'time']:
        wf.variables.addVariable(v)
    for l in []:
        wf.worklists.addWorklist(l)
    for p in ('Access contents information', 'Modify portal content', 'View'):
        wf.addManagedPermission(p)


    #from Products.PythonScripts.PythonScript import manage_addPythonScript
    #for p in ['notifyTrackBack']:
    #    manage_addPythonScript(wf.scripts, p)
    #    srcdef = wf.scripts['notifyTrackBack']
    #    srcdef.ZPythonScript_edit('', script_notifyTrackBack)
    #    srcdef._proxy_roles = ( "Manager", )
    #    #roles = ("Manager",)
    #    #srcdef.manage_proxy(roles)

    from Products.ExternalMethod.ExternalMethod import manage_addExternalMethod
    manage_addExternalMethod(wf.scripts, 
                             id='notifyTrackBack', 
                             title='',
                             module='SimpleBlog.utils',
                             function='notifyTrackBack')

    ## Initial State
    wf.states.setInitialState('new')

    ## States initialization
    sdef = wf.states['new']
    sdef.setProperties(title="""""",
                       transitions=('make_pending',))
    sdef.setPermission('Access contents information', 1, [])
    sdef.setPermission('Modify portal content', 1, [])
    sdef.setPermission('View', 1, [])

    sdef = wf.states['pending']
    sdef.setProperties(title="""""",
                       transitions=('publish',))
    sdef.setPermission('Access contents information', 0, ['Manager', 'Owner'])
    sdef.setPermission('Modify portal content', 0, ['Manager', 'Owner'])
    sdef.setPermission('View', 0, ['Manager', 'Owner'])

    sdef = wf.states['published']
    sdef.setProperties(title="""Public""",
                       transitions=('retract',))
    sdef.setPermission('Access contents information', 1, ['Anonymous', 'Manager'])
    sdef.setPermission('Modify portal content', 0, ['Manager', 'Owner'])
    sdef.setPermission('View', 0, ['Anonymous', 'Authenticated', 'Manager'])


    ## Transitions initialization
    tdef = wf.transitions['retract']
    tdef.setProperties(title="""Member retracts published item""",
                       new_state_id="""draft""",
                       trigger_type=1,
                       script_name="""""",
                       after_script_name="""""",
                       actbox_name="""Retract""",
                       actbox_url="""%(content_url)s/content_retract_form""",
                       actbox_category="""workflow""",
                       props={'guard_roles': 'Owner; Manager'},
                       )

    tdef = wf.transitions['publish']
    tdef.setProperties(title="""Reviewer publishes content""",
                       new_state_id="""published""",
                       trigger_type=1,
                       script_name="""""",
                       after_script_name="""""",
                       actbox_name="""Publish""",
                       actbox_url="""%(content_url)s/content_publish_form""",
                       actbox_category="""workflow""",
                       props={'guard_roles': 'Manager; Owner'},
                       )

    tdef = wf.transitions['make_pending']
    tdef.setProperties(title="""Make pending""",
                       new_state_id="""pending""",
                       trigger_type=0,
                       script_name="""notifyTrackBack""",
                       after_script_name="""""",
                       actbox_name="""""",
                       actbox_url="""""",
                       actbox_category="""workflow""",
                       props=None,
                       )

    ## State Variable
    wf.variables.setStateVar('review_state')

    ## Variables initialization
    vdef = wf.variables['action']
    vdef.setProperties(description="""The last transition""",
                       default_value="""""",
                       default_expr="""transition/getId|nothing""",
                       for_catalog=0,
                       for_status=1,
                       update_always=1,
                       props=None)

    vdef = wf.variables['review_history']
    vdef.setProperties(description="""Provides access to workflow history""",
                       default_value="""""",
                       default_expr="""state_change/getHistory""",
                       for_catalog=0,
                       for_status=0,
                       update_always=0,
                       props={'guard_permissions': 'Request review; Review portal content'})

    vdef = wf.variables['comments']
    vdef.setProperties(description="""Comments about the last transition""",
                       default_value="""""",
                       default_expr="""python:state_change.kwargs.get('comment', '')""",
                       for_catalog=0,
                       for_status=1,
                       update_always=1,
                       props=None)

    vdef = wf.variables['actor']
    vdef.setProperties(description="""The ID of the user who performed the last transition""",
                       default_value="""""",
                       default_expr="""user/getId""",
                       for_catalog=0,
                       for_status=1,
                       update_always=1,
                       props=None)

    vdef = wf.variables['time']
    vdef.setProperties(description="""Time of the last transition""",
                       default_value="""""",
                       default_expr="""state_change/getDateTime""",
                       for_catalog=0,
                       for_status=1,
                       update_always=1,
                       props=None)

    ## Worklists Initialization

def createTrackback_workflow(id):
    "..."
    ob = DCWorkflowDefinition(id)
    setupTrackback_workflow(ob)
    return ob

addWorkflowFactory(createTrackback_workflow,
                   id='trackback_workflow',
                   title='TrackBack Workflow')

    