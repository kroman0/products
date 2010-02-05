from zope import schema
from zope.formlib import form
from zope.interface import implements
from zope.component import getMultiAdapter

from plone.app.portlets.portlets import base
from plone.portlets.interfaces import IPortletDataProvider

from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from Products.CMFCore.utils import getToolByName
from plone.memoize.instance import memoize

# Quills imports
from quills.core.interfaces import IBaseContent
from quills.core.interfaces import IWeblogEnhanced
from quills.core.interfaces import IWeblog
from quills.app.utilities import recurseToInterface
from quills.app import QuillsAppMessageFactory as _

# Local imports
from quills.app.portlets.base import BasePortletRenderer



PORTLET_TITLE = _(u"Recent Author")
PORTLET_DESC = _(u"This portlet shows recent author.")


class IRecentAuthorPortlet(IPortletDataProvider):

    blog_path = schema.TextLine(
        title=_(u"Path to Blog"),
        description=_(u"Physical path to blog, from the plone object, 'blog' for ex."),
        required=True)

class Assignment(base.Assignment):

    implements(IRecentAuthorPortlet)

    def __init__(self, blog_path='blog'):
        self.blog_path= blog_path

    @property
    def title(self):
        return PORTLET_TITLE


class Renderer(BasePortletRenderer, base.Renderer):

    _template = ViewPageTemplateFile('recent_author.pt')

    @property
    def title(self):
        return PORTLET_TITLE
    
    @property
    def authors(self):
        weblog = self.getWeblog()
        return weblog.getAuthors()
    
    def getWeblog(self):
        pstate = getMultiAdapter((self.context, self.request), name=u'plone_portal_state')
        portal = pstate.portal()
        weblog = portal.restrictedTraverse(str(self.data.blog_path))
        return IWeblog(weblog)

    @property
    def getEntries(self):
        weblog = self.getWeblog()
        return weblog.getEntries(maximum=1)

    @property
    def getRecentAuthor(self):
        return self.getEntries[0].Creator

    def getPortraitFor(self, author):
        mtool = getToolByName(self.context, 'portal_membership')
        return mtool.getPersonalPortrait(author)

    def getInfoFor(self, author):
        mtool = getToolByName(self.context, 'portal_membership')
        info = mtool.getMemberInfo(author)
        if info is None:
            info = { 'fullname'    : author,
                     'description' : '',
                     'location'    : '',
                     'language'    : '',
                     'home_page'   : '',
                     'username'    : author,
                   }
        if not info['fullname']:
            info['fullname'] = author
        if not info['username']:
            info['username'] = author
        return info
    
    def getAuthorURL(self, author_id):
        weblog = self.getWeblogContentObject()
        return "%s/authors/%s" % (weblog.absolute_url(), author_id)
    
    def getAuthorsURL(self):
        weblog = self.getWeblogContentObject()
        return "%s/authors" % weblog.absolute_url()


class AddForm(base.AddForm):
    form_fields = form.Fields(IRecentAuthorPortlet)
    label = _(u'add-portlet', default=u"Add ${portlet-name} Portlet", mapping={u'portlet-name': PORTLET_TITLE})
    description = PORTLET_DESC

    def create(self, data):
        return Assignment(blog_path = data.get('blog_path', True))

class EditForm(base.EditForm):
    form_fields = form.Fields(IRecentAuthorPortlet)
    label = _(u'edit-portlet', default=u"Edit ${portlet-name} Portlet", mapping={u'portlet-name': PORTLET_TITLE})
    description = PORTLET_DESC
