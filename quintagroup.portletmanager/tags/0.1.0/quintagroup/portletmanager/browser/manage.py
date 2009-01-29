from zope.interface import implements
from zope.component import getMultiAdapter, getUtility
from zope.publisher.interfaces.browser import IDefaultBrowserLayer

from AccessControl import Unauthorized
from Acquisition import aq_inner
from Acquisition import aq_base
from Products.Five import BrowserView

from Products.CMFCore.utils import getToolByName
from Products.CMFCore.interfaces import ISiteRoot

from plone.portlets.interfaces import IPortletManager
from plone.portlets.interfaces import IPortletAssignmentMapping
from plone.portlets.interfaces import ILocalPortletAssignmentManager

from plone.portlets.constants import USER_CATEGORY
from plone.portlets.constants import GROUP_CATEGORY
from plone.portlets.constants import CONTENT_TYPE_CATEGORY
from plone.portlets.constants import CONTEXT_CATEGORY

from plone.app.portlets.storage import PortletAssignmentMapping
from plone.app.portlets.storage import UserPortletAssignmentMapping

from plone.app.portlets.interfaces import IPortletPermissionChecker

from plone.app.portlets.browser.interfaces import IManagePortletsView
from plone.app.portlets.browser.interfaces import IManageContextualPortletsView
from plone.app.portlets.browser.interfaces import IManageDashboardPortletsView
from plone.app.portlets.browser.interfaces import IManageGroupPortletsView
from plone.app.portlets.browser.interfaces import IManageContentTypePortletsView

from plone.app.portlets import utils
from plone.memoize.view import memoize

class ManageContextualPortlets(BrowserView):
    implements(IManageContextualPortletsView)
    
    def __init__(self, context, request):
        super(ManageContextualPortlets, self).__init__(context, request)
        self.request.set('disable_border', True)
        
    # IManagePortletsView implementation
    
    @property
    def category(self):
        return CONTEXT_CATEGORY
        
    @property
    def key(self):
        return '/'.join(self.context.getPhysicalPath())
    
    def getAssignmentMappingUrl(self, manager):
        baseUrl = str(getMultiAdapter((self.context, self.request), name='absolute_url'))
        return '%s/++contextportlets++%s' % (baseUrl, manager.__name__)
    
    def getAssignmentsForManager(self, manager):
        assignments = getMultiAdapter((self.context, manager), IPortletAssignmentMapping)
        return assignments.values()
    
    # view @@manage-portlets
    
    def has_legacy_portlets(self):
        left_slots = getattr(aq_base(self.context), 'left_slots', [])
        right_slots = getattr(aq_base(self.context), 'right_slots', [])
        
        return (left_slots or right_slots)

    # view @@set-portlet-blacklist-status
    def set_blacklist_status(self, manager, group_status, content_type_status, context_status):
        portletManager = getUtility(IPortletManager, name=manager)
        assignable = getMultiAdapter((self.context, portletManager,), ILocalPortletAssignmentManager)
        assignments = getMultiAdapter((self.context, portletManager), IPortletAssignmentMapping)
        
        IPortletPermissionChecker(assignments.__of__(aq_inner(self.context)))()
        
        def int2status(status):
            if status == 0:
                return None
            elif status > 0:
                return True
            else:
                return False
        
        assignable.setBlacklistStatus(GROUP_CATEGORY, int2status(group_status))
        assignable.setBlacklistStatus(CONTENT_TYPE_CATEGORY, int2status(content_type_status))
        assignable.setBlacklistStatus(CONTEXT_CATEGORY, int2status(context_status))
        
        baseUrl = str(getMultiAdapter((self.context, self.request), name='absolute_url'))
        self.request.response.redirect(baseUrl + '/@@manage-portlets')
        return ''
    
    # view @@convert-legacy-portlets
    
    def convert_legacy_portlets(self):
        utils.convert_legacy_portlets(self.context)
        self.context.request.response.redirect(self.context.absolute_url() + '/@@manage-portlets')
    
    def is_portal_root(self):
        context = aq_inner(self.context)
        portal = getUtility(ISiteRoot)
        return aq_base(context) is aq_base(portal)
