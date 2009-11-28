from zope import schema
from zope.formlib import form
from zope.interface import implements
from zope.component import getMultiAdapter

from plone.memoize.instance import memoize
from plone.app.portlets.portlets import base
from plone.memoize.compress import xhtml_compress
from plone.portlets.interfaces import IPortletDataProvider

from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile

# Quills imports
from quills.core.interfaces import IWeblog
from quills.core.interfaces import IWeblogLocator
from quills.app.browser.baseview import BaseView
from quills.app.portlets.base import BasePortletRenderer

from quintagroup.quills.extras import quintagroupQuillsMessageFactory as _

PORTLET_TITLE = _(u"Recent Posts")
PORTLET_DESC = _(u"This portlet lists recent posts for specified weblog.")

class IRecentWeblogEntriesPortlet(IPortletDataProvider):

    blog = schema.TextLine(
        title=_(u"Path to Blog"),
        description=_(u"Physical path to blog, from the plone object, 'blog' for ex."),
        required=True)

    max_entries = schema.Int(
        title=_(u'Maximum entries'),
        description=_(u"What's the maximum number of entries to list?"),
        required=True,
        default=5)

class Assignment(base.Assignment):

    implements(IRecentWeblogEntriesPortlet)

    def __init__(self, blog='blog', max_entries=5):
        self.blog = blog
        self.max_entries = max_entries

    @property
    def title(self):
        return PORTLET_TITLE


class Renderer(BasePortletRenderer, base.Renderer, BaseView):

    _template = ViewPageTemplateFile('recententries.pt')

    @property
    def title(self):
        return PORTLET_TITLE

    @memoize
    def getWeblog(self):
        pstate = getMultiAdapter((self.context, self.request), name=u'plone_portal_state')
        portal = pstate.portal()
        weblog = portal.restrictedTraverse(str(self.data.blog))
        return IWeblog(weblog)

    @property
    def getEntries(self):
        weblog = self.getWeblog()
        return weblog.getEntries(maximum=self.data.max_entries)


class AddForm(base.AddForm):
    form_fields = form.Fields(IRecentWeblogEntriesPortlet)
    label = _(u'add-portlet', default=u"Add ${portlet-name} Portlet", mapping={u'portlet-name': PORTLET_TITLE})
    description = PORTLET_DESC

    def create(self, data):
        return Assignment(**data)


class EditForm(base.EditForm):
    form_fields = form.Fields(IRecentWeblogEntriesPortlet)
    label = _(u'edit-portlet', default=u"Edit ${portlet-name} Portlet", mapping={u'portlet-name': PORTLET_TITLE})
    description = PORTLET_DESC
