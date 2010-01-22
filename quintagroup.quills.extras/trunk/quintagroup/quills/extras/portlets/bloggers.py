from zope import schema
from zope.formlib import form
from zope.interface import implements
from zope.component.interface import interfaceToName 
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
from quills.core.interfaces import IPossibleWeblogEntry

# Local imports
from quills.app.portlets.base import BasePortletRenderer


PORTLET_TITLE = _(u"Bloggers")
PORTLET_DESC = _(u"This portlet lists weblog authors.")


class IBloggersPortlet(IPortletDataProvider):

    blog_path = schema.TextLine(
        title=_(u"Path to Blog"),
        description=_(u"Physical path to blog, from the plone object, 'blog' for ex."),
        required=True)

class Assignment(base.Assignment):

    implements(IBloggersPortlet)

    def __init__(self, blog_path='/blog'):
        self.blog_path = blog_path

    @property
    def title(self):
        return PORTLET_TITLE


class Renderer(BasePortletRenderer, base.Renderer):

    _template = ViewPageTemplateFile('bloggers.pt')

    @property
    def title(self):
        return PORTLET_TITLE

    def getWeblog(self):
        portal = getToolByName(self.context, 'portal_url').getPortalObject()
        if isinstance(self.data.blog_path, unicode):
            path = self.data.blog_path.encode('utf-8')
        blog = portal.restrictedTraverse(path, None)
        return blog and IWeblog(blog) or []
    
    @property
    def bloggers(self):
        weblog = self.getWeblog()
        return weblog.getAuthors()

    @memoize
    def getBloggerPosts(self, blogger):
        catalog = getMultiAdapter((self.context, self.request), name=u'plone_tools').catalog()
        pstate = getMultiAdapter((self.context, self.request), name=u'plone_portal_state')
        portal = pstate.portal()
        brains = catalog(path='/%s/%s' % (portal.getId(), self.data.blog_path),
                         object_provides=interfaceToName(portal, IPossibleWeblogEntry),
                         review_state='published',
                         Creator=blogger,
                        )
        return brains

    def getBloggersInfo(self ):

        def bcmp(first, second):
            if first['posts_amount'] < second['posts_amount']:
                return -1
            if first['posts_amount'] > second['posts_amount']:
                return 1
            if first['posts_amount'] == second['posts_amount']:
                return 0

        result = []
        mtool = getToolByName(self.context, 'portal_membership')
        for blogger in self.bloggers:
            info = mtool.getMemberInfo(blogger.getId())
            if info is None:
                info = { 'fullname'    : blogger.getId(),
                         'description' : '',
                         'location'    : '',
                         'language'    : '',
                         'home_page'   : '',
                         'username'    : blogger.getId(),
                       }
            if not info['fullname']:
                info['fullname'] = blogger.getId()
            if not info['username']:
                info['username'] = blogger.getId()
            info['posts_amount'] = len(self.getBloggerPosts(blogger.getId()))
            result.append(info)
            result.sort(bcmp)
            result.reverse()
        return result
    
    def getBloggerURL(self, blogger_id):
        weblog = self.getWeblogContentObject()
        return "%s/authors/%s" % (weblog.absolute_url(), blogger_id)
    
    def getBloggersURL(self):
        weblog = self.getWeblogContentObject()
        return "%s/authors" % len(weblog.absolute_url())


class AddForm(base.AddForm):
    form_fields = form.Fields(IBloggersPortlet)
    label = _(u'add-portlet', default=u"Add ${portlet-name} Portlet", mapping={u'portlet-name': PORTLET_TITLE})
    description = PORTLET_DESC

    def create(self, data):
        return Assignment(blog_path=data.get('blog_path', '/blog'))


class EditForm(base.EditForm):
    form_fields = form.Fields(IBloggersPortlet)
    label = _(u'edit-portlet', default=u"Edit ${portlet-name} Portlet", mapping={u'portlet-name': PORTLET_TITLE})
    description = PORTLET_DESC
