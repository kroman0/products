from Products.Archetypes.public import listTypes
from Products.Archetypes.Extensions.utils import installTypes, install_subskin
from Products.CMFCore.utils import getToolByName
from StringIO import StringIO
from Products.CMFCore.CMFCorePermissions import setDefaultRoles
from Products.CMFDynamicViewFTI.migrate import migrateFTIs
from Products.SimpleBlog.config import *

portlets=['here/portlet_simpleblog/macros/portletBlogFull_local', 
          'here/portlet_simpleblog/macros/portletBlogFull_global',
          'here/portlet_simpleblog/macros/portletBlogRecent_local',
          'here/portlet_simpleblog/macros/portletBlogRecent_global']

def install(self):

    out = StringIO()

    installTypes(self, out,
                 listTypes(PROJECTNAME),
                 PROJECTNAME)

    install_subskin(self, out, GLOBALS)

    # Migrate FTI, to make sure we get the necessary infrastructure for the
    # 'display' menu to work.
    migrated = migrateFTIs(self, product=PROJECTNAME)
    print >>out, "Switched to DynamicViewFTI: %s" % ', '.join(migrated)

    # Enable portal_factory
    factory = getToolByName(self, 'portal_factory')
    types = factory.getFactoryTypes().keys()
    if 'TrackBack' not in types:
        types.append('TrackBack')
        factory.manage_setPortalFactoryTypes(listOfTypeIds = types)
    if 'BlogEntry' not in types:
        types.append('BlogEntry')
        factory.manage_setPortalFactoryTypes(listOfTypeIds = types)
    if 'BlogFolder' not in types:
        types.append('BlogFolder')
        factory.manage_setPortalFactoryTypes(listOfTypeIds = types)
    if 'Blog' not in types:
        types.append('Blog')
        factory.manage_setPortalFactoryTypes(listOfTypeIds = types)

    portal = getToolByName(self,'portal_url').getPortalObject()

    if not hasattr(self, 'simpleblog_tool'):
        addTool = portal.manage_addProduct['SimpleBlog'].manage_addTool
        addTool(type='SimpleBlog manager')    
    
    # register the css
    # Install stylesheet
    # Make it work for the entire portal because the portlets can
    # be used everywhere
    portal_css = getToolByName(self, 'portal_css')
    portal_css.manage_addStylesheet(id = 'SimpleBlogCSS.css',
                                    expression = '',
                                    media = 'all',
                                    title = 'SimpleBlog styles',
                                    enabled = True)    
    
    #register the folderish items in portal_properties/site_properties for folder-contents views etc
    site_props = getToolByName(self, 'portal_properties').site_properties
    
    use_folder_tabs = site_props.getProperty('use_folder_tabs')
    if not 'Blog' in use_folder_tabs:
        site_props._updateProperty('use_folder_tabs', tuple(use_folder_tabs) + ('Blog','BlogFolder'))

    use_folder_contents = site_props.getProperty('use_folder_contents')
    if not 'Blog' in use_folder_contents:
        site_props._updateProperty('use_folder_contents', tuple(use_folder_contents) + ('Blog','BlogFolder'))

    if ENTRY_IS_FOLDERISH:
        if not 'BlogEntry' in use_folder_tabs:
            site_props._updateProperty('use_folder_tabs', tuple(use_folder_tabs) + ('BlogEntry',))
        if not 'BlogEntry' in use_folder_contents:
            site_props._updateProperty('use_folder_contents', tuple(use_folder_contents) + ('BlogEntry',))
        

    #Make sure blog entries aren't shown in the navtree by default
    nav_props = getToolByName(self, 'portal_properties').navtree_properties
    metaTypesNotToList = nav_props.getProperty('metaTypesNotToList')
    if not 'BlogEntry' in metaTypesNotToList:
        nav_props._updateProperty('metaTypesNotToList', tuple(metaTypesNotToList) + ('BlogEntry',))
        
    # Add to default_page_types
    # Allow people to have a Blog as the default page
    propsTool = getToolByName(self, 'portal_properties')
    siteProperties = getattr(propsTool, 'site_properties')    
    defaultPageTypes = list(siteProperties.getProperty('default_page_types'))
    if 'Blog' not in defaultPageTypes:
        defaultPageTypes.append('Blog')
    siteProperties.manage_changeProperties(default_page_types = defaultPageTypes)

    if not portal.hasProperty('trackback_notification_email'):
        portal.manage_addProperty('trackback_notification_email', '', 'string')

    # discussion enabled by default for BlogEntries
    getToolByName(self, 'portal_types').BlogEntry.allow_discussion=1

    # register 2.0 control panel
    try:
        cp=self.portal_controlpanel
        cp.addAction(id='SimpleBlogSetup',
                     name='SimpleBlog Setup',
                     action='string:${portal_url}/prefs_simpleblog_form',
                     permission='Manage portal',
                     category='Products',
                     appId='SimpleBlog',
                     imageUrl='simpleblog_icon.gif',
                     description='Configure SimpleBlog global settings')
    except:
        pass

    # install the workflow
    from Products.SimpleBlog import SimpleBlogWorkflow, TrackbackWorkflow
    reload(SimpleBlogWorkflow)
    reload(TrackbackWorkflow)


    # Remove workflows for BlogEntry and BlogFolder
    wf_tool = getToolByName(self, 'portal_workflow')
    wf_tool.setChainForPortalTypes( ('Blog', 'BlogEntry','BlogFolder'), []) 
    
    add_workflow(self, 'simpleblog_workflow', 'simpleblog_workflow (Workflow for Blog Entries)', ('BlogEntry',), out)
    add_workflow(self, 'trackback_workflow', 'trackback_workflow (TrackBack Workflow)', ('TrackBack',), out)

    wf_tool.setChainForPortalTypes(('Blog','BlogFolder'), 'folder_workflow')        

    print >> out, "Successfully installed %s." % PROJECTNAME
    return out.getvalue()

def add_workflow(self, wf_id, wf_factory_id, types, out):
    """ add a workflow definition to the portal_workflow tool """
    wf_tool = self.portal_workflow
    try:
        wf_tool.manage_delObjects([wf_id])
        out.write('Removed existant workflow "%s"\n'%wf_id)
    except:
        pass
    wf_tool.manage_addWorkflow(wf_factory_id, wf_id)
    if types:
        wf_tool.setChainForPortalTypes(types, wf_id)
    out.write('Added workflow "%s"\n'%wf_id)


def uninstall(self):
    # remove the references in each folder to our portlet:
    
    # this gotta be effective some time
    # someone's gotta test if this works like it should
    # commented out for the time being:
    
    #portal = getToolByName(self,'portal_url').getPortalObject()
    #processPortletOld(portal)
    #processPortletNew(portal)
    #removeReferences(portal)
    
    #remove configlet
    try:
        self.portal_controlpanel.unregisterApplication('SimpleBlog')
    except:
        pass
                     
def removeReferences(obj):
    for o in obj.contentValues():
        if o.isPrincipiaFolderish:
            processPortletOld(o)
            processPortletNew(o)
            removeReferences(o)

def processPortletOld(o):
    if not o.portal_type in ['Blog', 'BlogFolder', 'BlogEntry']:
        if hasattr(o.aq_base, 'left_slots') or hasattr(o.aq_base, 'right_slots'):
            new=[]
            if hasattr(o.aq_base,'left_slots'):
                for l in o.aq_base.left_slots:
                    if not l in portlets:
                        new.append(l)
                o.left_slots=new
            new=[]
            if hasattr(o.aq_base, 'right_slots'):
                for l in o.aq_base.right_slots:
                    if not l in portlets:
                        new.append(l)
                o.right_slots=new

def processPortletNew(o):
    if not o.portal_type in ['Blog', 'BlogFolder', 'BlogEntry']:    
        if hasattr(o.aq_base, 'column_one_portlets') or hasattr(o.aq_base, 'column_two_portlets'):
            new=[]
            if hasattr(o.aq_base,'column_one_portlets'):
                for l in o.aq_base.column_one_portlets:
                    if not l in portlets:
                        new.append(l)
                o.column_one_portlets=new
            new=[]
            if hasattr(o.aq_base, 'column_two_portlets'):
                for l in o.aq_base.column_two_portlets:
                    if not l in portlets:
                        new.append(l)
                o.column_two_portlets=new
        
            