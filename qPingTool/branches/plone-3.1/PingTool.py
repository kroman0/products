import os
from Acquisition import aq_base
from zLOG import LOG
from zope.interface import implements
from AccessControl import ClassSecurityInfo
from Products.PageTemplates.PageTemplateFile import PageTemplateFile
from Products.Archetypes.public import *
from Products.CMFCore.ActionProviderBase import ActionProviderBase
from Products.CMFCore.permissions import ManagePortal
from Products.CMFCore.utils import getToolByName
from Products.ATContentTypes.content.folder import ATFolder
from Products.CMFPlone.interfaces.OrderedContainer import IOrderedContainer
from Products.CMFPlone.PloneFolder import PloneFolder
from Products.XMLRPCMethod.XMLRPCMethod import RPCThread, XMLRPCMethod

from interfaces import IPingTool
from adapter import ICanonicalURL
from config import PROJECTNAME

try:
    from Products.qRSS2Syndication.interfaces import IPublishFeed
except ImportError:
    IPublishFeed = None

_marker = []

def modify_fti(fti):
    fti['title'] = 'Portal Ping Tool'
    fti['allowed_content_types'] = ('PingInfo',)
    fti['filter_content_types'] = 1
    #fti['icon'] = 'tool.gif'
    #fti['immediate_view'] = 'view'
    #fti['default_view'] = 'view'


class PingTool(ATFolder, PloneFolder):
    """

    >>> IPingTool.implementedBy(PingTool)
    True
    """
    security = ClassSecurityInfo()

    implements(IPingTool)
    __implements__ = (IOrderedContainer,)

    archetype_name = portal_type = 'PingTool'
    manage_options =  (
            {'label' : 'Overview', 'action' : 'manage_overview'},
        ) + ATFolder.manage_options

    manage_overview = PageTemplateFile(os.path.join('www', 'overview'), globals(), __name__='manage_overview')

    def om_icons(self):
        """ Checking on ZMI for canonical_url setting."""
        icons = ({'path':'misc_/qPingTool/tool.gif' \
                    ,'alt':self.meta_type \
                    ,'title':self.meta_type \
                },)
        if not ICanonicalURL(self).getCanonicalURL():
            icons = icons + ({'path':'misc_/PageTemplates/exclamation.gif' \
                                ,'alt':'Error' \
                                ,'title':'PingTool needs setting canonical_url' \
                                },)
        return icons

    security.declareProtected(ManagePortal, 'pingFeedReader')
    def pingFeedReader(self,context):
        """ ping """
        
        status = 'failed'
        pingProp = self.getPingProperties(context)
    	if not pingProp['enable_ping']:
    	    message = 'Ping is dissabled.'
    	    return status, message
        self.c_url = ICanonicalURL(self).getCanonicalURL()
        if not self.c_url:
            return status, 'Ping is impossible.Setup canonical_url.'
    	ps = getToolByName(context,'portal_syndication')
    	if ps.isSyndicationAllowed(context):
	    sites = pingProp['ping_sites']
            message = 'Select servers.'
            for site in sites:
                status = 'success'
                message = 'The servers are pinged.'
                self.site_obj = getattr(self, site)
                site_method = self.site_obj.getMethod_name()
                site_url = self.site_obj.getUrl()
                PingMethod = XMLRPCMethod('myid', "", site_url, site_method, 25)
                title = context.Title()
                ping_url = self.getPingUrl(context)
                try: 
                    result_ping = PingMethod(title, ping_url)
                    result = result_ping['message']
                except:
                    result = 'The site %s generated error for %s.' % (site_url, ping_url)
		LOG('qPingTool', 100, result)
                message += '\nReturned message from %s: %s' % (site_url, str(result))
        else:
            message = 'The %s is not syndication allowed' % url 
        return status, message

    security.declareProtected(ManagePortal, 'setupPing')
    def setupPing(self,context,
                  enable_ping=0,
                  ping_sites=(),
                  REQUEST=None):
        """   """	
        obj=aq_base(context)
        status = 'success'
        message = "Changes saved."
        syInfo = getattr(obj, 'syndication_information', None)

        if syInfo is None:
            message = 'Syndication is Disabled'
            status = 'failed'
        else:
    	    syInfo.ping_sites = list(ping_sites)
    	    syInfo.enable_ping = enable_ping

        return status, message

    security.declareProtected(ManagePortal, 'getPingProperties')
    def getPingProperties(self, context):
        """ """
        obj=aq_base(context)

        syInfo = getattr(obj, 'syndication_information', None)
        pingPropeties={}
        pingPropeties['ping_sites'] = getattr(syInfo,'ping_sites',[])
        pingPropeties['enable_ping'] = getattr(syInfo,'enable_ping',0)
        return  pingPropeties

    security.declareProtected(ManagePortal, 'getPingUrl')
    def getPingUrl(self, context):
        rss_templates = {'Weblog':'','RSS1':'/RSS','RSS2':'/RSS2'}
        url = getToolByName(context, 'portal_url').getRelativeContentURL(context)
        if not self.c_url[-1] == os.path.sep:
            self.c_url += os.path.sep
        url = self.c_url + url
        site_rss_version = rss_templates[self.site_obj.getRss_version()]
        ping_url = ''
        if IPublishFeed:
            ping_url = IPublishFeed(self).getPublishFeedUrl(url)
        if not ping_url:
            ping_url = url + site_rss_version
        return ping_url

registerType(PingTool, PROJECTNAME)
