from Products.DCWorkflow.DCWorkflow import DCWorkflowDefinition
from Products.CMFCore.CMFCorePermissions import ModifyPortalContent
from AccessControl.Permissions import view, access_contents_information
from Products.DCWorkflow.Default import r_anon, r_manager, r_owner, p_access, p_modify, p_view 
from Products.CMFCore import CMFCorePermissions

def setupWorkflow(wf):
    for state in  ('private', 'published',):
        wf.states.addState(state)
    for transition in ('publish', 'hide'):
        wf.transitions.addTransition(transition)
    for permision in (p_access, p_modify, view):
        wf.addManagedPermission(permision)

    # set initial state
    wf.states.setInitialState('published')

    wf_private = wf.states['private']
    wf_private.setProperties(
                             title='Visible and editable only by owner',
                             transitions=('publish',))
    wf_private.setPermission(p_access, 0, (r_manager, r_owner))
    wf_private.setPermission(p_view, 0, (r_manager, r_owner))
    wf_private.setPermission(p_modify, 0, (r_manager, r_owner))

    wf.permissions+=(CMFCorePermissions.ListFolderContents, )
    wf.states.private.permission_roles[CMFCorePermissions.ListFolderContents]=['Authenticated', r_manager]

    wf_published = wf.states['published']
    wf_published.setProperties(
                               title='Public',
                               transitions=('hide',))
    wf_published.setPermission(p_access, 1, (r_manager,))
    wf_published.setPermission(p_view, 1, (r_anon, r_manager))
    wf_published.setPermission(p_modify, 0, (r_manager, ))

    wf.states.published.permission_roles[CMFCorePermissions.ListFolderContents]=[r_anon,]

    tdef = wf.transitions['hide']
    tdef.setProperties(
                       title='Member makes content private',
                       new_state_id='private',
                       actbox_name='Make private',
                       actbox_url='%(content_url)s/content_hide_form',
                       props={'guard_roles':r_owner})

    tdef = wf.transitions['publish']
    tdef.setProperties(
                       title='Reviewer publishes content',
                       new_state_id='published',
                       actbox_name='Publish',
                       actbox_url='%(content_url)s/content_publish_form',
                       props={'guard_permissions':r_anon})
        
    wf.variables.setStateVar('review_state')
     
#create workflow
def createWorkflow(id):
    wf = DCWorkflowDefinition(id)
    setupWorkflow(wf)
    return wf

