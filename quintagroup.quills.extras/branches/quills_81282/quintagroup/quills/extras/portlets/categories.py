# Zope imports
from zope.formlib import form
from zope.interface import implements
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile

# CMF imports
from Products.CMFCore.utils import getToolByName

# Plone imports
from plone.app.portlets.portlets import base
from plone.app.portlets.browser.formhelper import NullAddForm
from plone.memoize.instance import memoize
from plone.portlets.interfaces import IPortletDataProvider

# Quills imports
from quills.app import QuillsAppMessageFactory as _

# Local imports
from quills.app.portlets.base import BasePortletRenderer


PORTLET_TITLE = _(u"Weblog Categories")
PORTLET_DESC = _(u"This portlet provides list of weblog categories.")


class IWeblogCategoriesPortlet(IPortletDataProvider):
    """A weblog administration portlet.
    """


class Assignment(base.Assignment):
    implements(IWeblogCategoriesPortlet)

    @property
    def title(self):
        return PORTLET_TITLE


class Renderer(BasePortletRenderer, base.Renderer):

    _template = ViewPageTemplateFile('categories.pt')

    @property
    def available(self):
        return self.getCategories() and True or False

    @property
    def title(self):
        return PORTLET_TITLE

    @memoize
    def getCategories(self):
        cats = []
        weblog = self.getWeblogContentObject()
        #import pdb;pdb.set_trace()
        if weblog:
            catalog = getToolByName(self.context, 'portal_catalog')
            bcats = catalog(
                path='/'.join(weblog.getPhysicalPath()),
                portal_type=['Folder','Large Plone Folder'],
                object_provides='quintagroup.quills.extras.browser.interfaces.IWeblogCategory'                
            )
            wbpath = '/'.join(weblog.getPhysicalPath())
            bcats = filter(lambda b:not b.getPath() == wbpath, bcats)
            cats = [{'title':b.Title or b.getId, 'url':b.getURL} for b in bcats]
        return cats


class AddForm(NullAddForm):
    form_fields = form.Fields(IWeblogCategoriesPortlet)
    label = _(u'add-portlet', default=u"Add ${portlet-name} Portlet", 
              mapping={u'portlet-name': PORTLET_TITLE})
    description = PORTLET_DESC

    def create(self):
        return Assignment()


class EditForm(base.EditForm):
    form_fields = form.Fields(IWeblogCategoriesPortlet)
    label = _(u'edit-portlet', default=u"Edit ${portlet-name} Portlet", mapping={u'portlet-name': PORTLET_TITLE})
    description = PORTLET_DESC
