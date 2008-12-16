import sys
from ZODB.POSException import ConflictError

from zope.interface import Interface
from zope.component import adapts, getMultiAdapter

from zope.publisher.interfaces.browser import IBrowserView
from zope.publisher.interfaces.browser import IDefaultBrowserLayer

from Acquisition import  aq_inner,  aq_acquire
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from Products.CMFCore.utils import getToolByName

from plone.portlets.interfaces import  ILocalPortletAssignable

from plone.app.portlets.interfaces import IColumn
from plone.app.portlets.interfaces import IDashboard
from plone.app.portlets.manager import PortletManagerRenderer

import logging
logger = logging.getLogger('portlets')

class ColumnPortletManagerRenderer(PortletManagerRenderer):
    """A renderer for the column portlets
    """
    adapts(Interface, IDefaultBrowserLayer, IBrowserView, IColumn)
    template = ViewPageTemplateFile('browser/templates/column.pt')
    error_message = ViewPageTemplateFile('browser/templates/error_message.pt')

    def _context(self):
        context = aq_inner(self.context)
        return context

    def base_url(self):
        """If context is a default-page, return URL of folder, else
        return URL of context.
        """
        return str(getMultiAdapter((self._context(), self.request,), name=u'absolute_url'))

    def can_manage_portlets(self):
        context = self._context()
        if not ILocalPortletAssignable.providedBy(context):
            return False
        mtool = getToolByName(context, 'portal_membership')
        return mtool.checkPermission("Portlets: Manage portlets", context)

    def safe_render(self, portlet_renderer):
        try:
            return portlet_renderer.render()
        except ConflictError:
            raise
        except Exception:
            logger.exception('Error while rendering %r' % (self,))
            aq_acquire(self, 'error_log').raising(sys.exc_info())
            return self.error_message()
