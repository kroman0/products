from zope import schema
from zope.formlib import form
from zope.interface import implements
from zope.component import getMultiAdapter

from plone.memoize.compress import xhtml_compress
from plone.portlets.interfaces import IPortletDataProvider

from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile

# Quills imports
from quills.core.interfaces import IBaseContent
from quills.core.interfaces import IWeblogEnhanced
from quills.core.interfaces import IWeblog
from quills.app.utilities import recurseToInterface
from quills.app.utilities import talkbackURL
from quills.app.utilities import getArchiveURLFor
from quills.app.browser.baseview import BaseView
from quills.app import QuillsAppMessageFactory as _

# Local imports
from quills.app.portlets import recentcomments as base
from quills.app.portlets.base import BasePortletRenderer


PORTLET_TITLE = _(u"Recent Comments")
PORTLET_DESC = _(u"This portlet lists recent weblog comments.")


class IRecentCommentsPortlet(base.IRecentWeblogCommentsPortlet):

    blog_path = schema.TextLine(
        title=_(u"Path to Blog"),
        description=_(u"Physical path to blog, from the plone object, 'blog' for ex."),
        required=True)


class Assignment(base.Assignment):

    implements(IRecentCommentsPortlet)

    def __init__(self, max_comments=5, blog_path='blog'):
        super(Assignment, self).__init__(max_comments = max_comments)
        self.blog_path = blog_path

    @property
    def title(self):
        return PORTLET_TITLE


class Renderer(BasePortletRenderer, base.Renderer, BaseView):

    _template = ViewPageTemplateFile('recentcomments.pt')

    @property
    def available(self):
        return len(self.getComments) > 0

    @property
    def title(self):
        return PORTLET_TITLE

    def getWeblog(self):
        pstate = getMultiAdapter((self.context, self.request), name=u'plone_portal_state')
        portal = pstate.portal()
        weblog = portal.restrictedTraverse(str(self.data.blog_path))
        return IWeblog(weblog)
        
class AddForm(base.AddForm):
    form_fields = form.Fields(IRecentCommentsPortlet)
    label = _(u'add-portlet', default=u"Add ${portlet-name} Portlet", mapping={u'portlet-name': PORTLET_TITLE})
    description = PORTLET_DESC

    def create(self, data):
        return Assignment(max_comments=5, blog_path='blog')


class EditForm(base.EditForm):
    form_fields = form.Fields(IRecentCommentsPortlet)
    label = _(u'edit-portlet', default=u"Edit ${portlet-name} Portlet", mapping={u'portlet-name': PORTLET_TITLE})
    description = PORTLET_DESC
