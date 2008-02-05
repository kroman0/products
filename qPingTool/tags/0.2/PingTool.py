# from Globals import InitializeClass
from Products.CMFCore.ActionProviderBase import ActionProviderBase
from Products.CMFPlone.PloneFolder import PloneFolder
from config import TOOL_ID, PROJECTNAME
from Products.Archetypes.public import *
from Products.CMFPlone.interfaces.OrderedContainer import IOrderedContainer
from Products.CMFCore.ActionInformation import ActionInformation
from Products.CMFCore.Expression import Expression
from Products.CMFCore.CMFCorePermissions import ManageProperties
from Acquisition import aq_base

from Products.XMLRPCMethod.XMLRPCMethod import RPCThread, XMLRPCMethod
from Products.CMFCore.utils import getToolByName
from zLOG import LOG

_marker = []
def modify_fti(fti):
    fti['title'] = 'Portal Ping Tool'
    fti['allowed_content_types'] = ('PingInfo',)
    fti['filter_content_types'] = 1
    fti['icon'] = 'tool.gif'
    actions = (
              { 'id': 'view',
                'name': 'View',
                'action': 'string:folder_contents',
                'permissions': ('Manage portal',),
                'category':'object',
              }, )
    fti['actions']=tuple(actions)


class PingTool(BaseFolder, PloneFolder, ActionProviderBase): #, BaseFolder):
    """This tool serve for operation with ActionInfo objects
    """

    schema = BaseSchema
    filter_content_types = 1
    allowed_content_types = ['PingInfo']
    global_allowed = 0

    meta_type = archetype_name = portal_type = 'PingTool'


    __implements__ = (IOrderedContainer,)
    _actions = ( ActionInformation(
                    id='ping'
                  , title='Ping setup'
                  , action=Expression(
                        text='string:${folder_url}/ping_setup')
                  , condition=Expression(
                        text='python: folder==object and portal.portal_syndication.isSyndicationAllowed(object)')
                  , permissions=(ManageProperties,)
                  , category='folder'
                  , visible=1
                  )
               ,
               )                   	


    def pingFeedReader(self,context):
        """ ping """
        status = 'success'
        message = 'The servers are pinged'
        blog = context.simpleblog_tool.getFrontPage(context)
        title = blog.Title()
        portal = context.portal_url.getPortalObject()
        canonical_url = portal.getProperty('canonical_url', None)
        if canonical_url:
            #return "failure", "Please setup 'canonical_url' property for your Plone site"
            url = context.portal_url.getRelativeContentURL(blog)
            url = canonical_url + url          
        else:
            url = blog.absolute_url()  
    	ps = getToolByName(context,'portal_syndication')
    	rss_templates = {'Blog':'','RSS1':'/RSS','RSS2':'/RSS2'}
        pingProp = self.getPingProperties(blog)
    	result = 'ok'
    	if not pingProp['enable_ping']:
    	   message = 'Ping is dissabled'
    	   return status, message
    	if ps.isSyndicationAllowed(blog):
	    sites = pingProp['ping_sites']	
	    if sites:
    	        for site in sites:
    	            site_obj = getattr(self,site)
    	            site_rss_version = rss_templates[site_obj.getRss_version()]
    	            site_method = site_obj.getMethod_name()
    	            site_url = site_obj.getUrl()
    	             
                    PingMethod = XMLRPCMethod('myid',"",site_url,site_method,25)
                    blog_url = url + site_rss_version
                    try: 
                        #LOG('qPing', 0, title, blog_url, site_url)
                        result = PingMethod(title,blog_url)
                    except:
			LOG('qPingTool', 100,"The site "+  site_url+" generated error for "+ blog_url, result)
                    message += '\n'+ str(result)
        return status, message


    def setupPing(self,context,
                  enable_ping=0,
                  ping_sites=(),
                  REQUEST=None):
        """   """	
        obj=aq_base(context)
        status = 'success'
        message = 'Your changes have been saved'

        syInfo = getattr(obj, 'syndication_information', None)

        if syInfo is None:
            message = 'Syndication is Disabled'
            status = 'failed'
        syInfo.ping_sites = list(ping_sites)
        syInfo.enable_ping = enable_ping
        return status, message

    def getPingProperties(self, context):
        """ """
        obj=aq_base(context)

        syInfo = getattr(obj, 'syndication_information', None)
        pingPropeties={}
        pingPropeties['ping_sites'] = getattr(syInfo,'ping_sites',[])
        pingPropeties['enable_ping'] = getattr(syInfo,'enable_ping',0)
        return  pingPropeties

registerType(PingTool)
