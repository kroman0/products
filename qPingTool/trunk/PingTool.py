#from Globals import InitializeClass
import os
from Products.CMFCore.ActionProviderBase import ActionProviderBase
from Products.CMFPlone.PloneFolder import PloneFolder
from config import TOOL_ID, PROJECTNAME
from Products.Archetypes.public import *
from Products.ATContentTypes.content.folder import ATFolder
from Products.ATContentTypes.content.base import updateActions, updateAliases
from Products.CMFPlone.interfaces.OrderedContainer import IOrderedContainer
from Products.CMFCore.ActionInformation import ActionInformation
from Products.CMFCore.Expression import Expression
from Products.CMFCore.CMFCorePermissions import ManageProperties
from Acquisition import aq_base
from Products.CMFCore.utils import _getViewFor
from Products.PageTemplates.PageTemplateFile import PageTemplateFile
from Products.XMLRPCMethod.XMLRPCMethod import RPCThread, XMLRPCMethod
from Products.CMFCore.utils import getToolByName
from util import getCanonicalURL
from zLOG import LOG

_marker = []

def modify_fti(fti):
    fti['title'] = 'Portal Ping Tool'
    fti['allowed_content_types'] = ('PingInfo',)
    fti['filter_content_types'] = 1
    #fti['icon'] = 'tool.gif'
    #fti['immediate_view'] = 'view'
    #fti['default_view'] = 'view'


class PingTool(ATFolder, PloneFolder, ActionProviderBase): #(BaseFolder, PloneFolder, ActionProviderBase):
    """This tool serve for operation with ActionInfo objects
    """

    #schema = BaseSchema
    filter_content_types = 1
    allowed_content_types = ('PingInfo',)
    global_allowed = 0

    meta_type = archetype_name = portal_type = 'PingTool'

    ########
    content_icon   = 'tool.gif'
    immediate_view = 'view'
    default_view   = 'view'

    ########
    __implements__ = (IOrderedContainer,)
    _actions = ( ActionInformation(
                    id='ping'
                  , title='Ping setup'
                  , action=Expression(
                        text='string:${folder_url}/ping_setup')
                  , condition=Expression(
                        text='python: folder is object and portal.portal_syndication.isSyndicationAllowed(object)')
                  , permissions=(ManageProperties,)
                  , category='folder'
                  , visible=1
                  ),
               )

    actions = updateActions(ATFolder,
        ({'id'         : 'view' \
         ,'name'       : 'View' \
         ,'action'     : 'string:folder_contents' \
         ,'permissions': ('Manage portal',) \
         ,'category'   :'object' \
         },
        )
    )
    
    aliases = updateAliases(ATFolder,
        {'(Default)'   : 'folder_listing' \
        ,'view'        : 'folder_contents' \
        },
    )

    manage_options =  (
            {'label' : 'Overview', 'action' : 'manage_overview'},
        ) + ATFolder.manage_options

    manage_overview = PageTemplateFile(os.path.join('www','overview'), globals())
    manage_overview.__name__ = 'manage_overview'
    manage_overview._need__name__ = 0

    def pingFeedReader(self,context):
        """ ping """
        status = 'success'
        message = 'The servers are pinged'
        if context.meta_type == 'BlogFolder':
    	    blog = context.simpleblog_tool.getFrontPage(context)
    	else:
    	    blog = context

        title = blog.Title()
        portal = context.portal_url.getPortalObject()
        canonical_url = getCanonicalURL(context)
        if canonical_url:
            url = context.portal_url.getRelativeContentURL(blog)
            url = canonical_url + url
        else:
            status = 'failed'
            return status, 'Ping is impossible.See portal_pingtool.'

    	ps = getToolByName(context,'portal_syndication')
    	rss_templates = {'Blog':'','RSS1':'/RSS','RSS2':'/RSS2'}
        pingProp = self.getPingProperties(blog)
    	result = 'ok'
    	if not pingProp['enable_ping']:
            status = 'failed'
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
        else:
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

    def om_icons(self):
        """ Checking on ZMI for canonical_url setting."""
        icons = ({'path':'misc_/qPingTool/tool.gif' \
                    ,'alt':self.meta_type \
                    ,'title':self.meta_type \
                },)
        if not getCanonicalURL(self):
            icons = icons + ({'path':'misc_/PageTemplates/exclamation.gif' \
                                ,'alt':'Error' \
                                ,'title':'PingTool needs setting canonical_url' \
                                },)
        return icons

registerType(PingTool)
