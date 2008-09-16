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

from Products.qPingTool import qPingToolMessageFactory as _
from interfaces import IPingTool
from adapter import ICanonicalURL
from config import PROJECTNAME

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
    	    message = _(u'Ping is dissabled.')
    	    return status, message
        canonical_url = ICanonicalURL(self).getCanonicalURL()
        if not canonical_url:
            return status, _(u'Ping is impossible.Setup canonical_url.')
    	ps = getToolByName(context,'portal_syndication')
    	if ps.isSyndicationAllowed(context):
	    sites = pingProp['ping_sites']
            message = _(u'Select servers.')
            for site in sites:
                status = 'success'
                message = _(u'The servers are pinged.')
                site_obj = getattr(self, site)
                site_method = site_obj.getMethod_name()
                site_url = site_obj.getUrl()
                PingMethod = XMLRPCMethod('myid', "", site_url, site_method, 25)
                title = context.Title()
                rss_version = site_obj.getRss_version()
                ping_url = pingProp['ping_'+rss_version]
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
                  ping_Weblog='',
                  ping_RSS1='',
                  ping_RSS2='',
                  REQUEST=None):
        """   """	
        obj=aq_base(context)
        status = 'success'
        message = _(u'Changes saved.')
        syInfo = getattr(obj, 'syndication_information', None)

        if syInfo is None:
            message = _(u'Syndication is Disabled')
            status = 'failed'
        else:
    	    syInfo.ping_sites = list(ping_sites)
    	    syInfo.enable_ping = enable_ping
            syInfo.ping_Weblog = ping_Weblog
            syInfo.ping_RSS1 = ping_RSS1
            syInfo.ping_RSS2 = ping_RSS2
            
        return status, message

    security.declareProtected(ManagePortal, 'getPingProperties')
    def getPingProperties(self, context):
        """ """
        obj=aq_base(context)
        syInfo = getattr(obj, 'syndication_information', None)
        pingProperties={}
        pingProperties['ping_sites'] = getattr(syInfo, 'ping_sites', [])
        pingProperties['enable_ping'] = getattr(syInfo, 'enable_ping', 0)

        pingProperties['ping_Weblog'] = getattr(syInfo, 'ping_Weblog', '')
        if not pingProperties['ping_Weblog']:
            pingProperties['ping_Weblog'] = self.getPingDefaultUrl(context, 'Weblog')

        pingProperties['ping_RSS1'] = getattr(syInfo, 'ping_RSS1', '')
        if not pingProperties['ping_RSS1']:
            pingProperties['ping_RSS1'] = self.getPingDefaultUrl(context, 'RSS1')

        pingProperties['ping_RSS2'] = getattr(syInfo, 'ping_RSS2', '')
        if not pingProperties['ping_RSS2']:
            pingProperties['ping_RSS2'] = self.getPingDefaultUrl(context, 'RSS2')

        return  pingProperties
        
    security.declareProtected(ManagePortal, 'getPingDefaultUrl')
    def getPingDefaultUrl(self, context, rss_version='Weblog'):
        rss_templates = {'Weblog':'','RSS1':'/RSS','RSS2':'/RSS2'}
        url = getToolByName(context, 'portal_url').getRelativeContentURL(context)
        canonical_url = ICanonicalURL(self).getCanonicalURL()
        ping_url = ''
        if canonical_url:
            if not canonical_url[-1] == '/':
                canonical_url += '/'
            url = canonical_url + url
            site_rss_version = rss_templates[rss_version]
            ping_url = url + site_rss_version
        return ping_url

registerType(PingTool, PROJECTNAME)
