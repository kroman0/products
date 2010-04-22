from zope.interface import implements
from zope.component import queryMultiAdapter, getMultiAdapter

from plone.memoize import ram
from plone.memoize.instance import memoize
from plone.memoize.compress import xhtml_compress

from plone.app.portlets.portlets import base
from plone.app.portlets.cache import render_cachekey
from plone.portlets.interfaces import IPortletDataProvider

from zope import schema
from zope.formlib import form

from Acquisition import aq_inner
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile

from quintagroup.portlet.map import QGMapPortletMessageFactory as _

from logging import getLogger
logger = getLogger("Plone")

class IQGMapPortlet(IPortletDataProvider):
    """A portlet

    It inherits from IPortletDataProvider because for this portlet, the
    data that is being rendered and the portlet assignment itself are the
    same.
    """

    # TODO: Add any zope.schema fields here to capture portlet configuration
    # information. Alternatively, if there are no settings, leave this as an
    # empty interface - see also notes around the add form and edit form
    # below.

    collection_path = schema.TextLine(title=_(u"Path to collection"),
        description=_(u"A plone physical path to collection of locations"),
        required=True)


class Assignment(base.Assignment):
    """Portlet assignment.

    This is what is actually managed through the portlets UI and associated
    with columns.
    """

    implements(IQGMapPortlet)

    # TODO: Set default values for the configurable parameters here

    def __init__(self, collection_path=""):
       self.collection_path = str(collection_path)

    @property
    def title(self):
        """This property is used to give the title of the portlet in the
        "manage portlets" screen.
        """
        return "Quintagroup Google Map portlet"


class Renderer(base.Renderer):
    """Portlet renderer.

    This is registered in configure.zcml. The referenced page template is
    rendered, and the implicit variable 'view' will refer to an instance
    of this class. Other methods can be added and referenced in the template.
    """

    _template = ViewPageTemplateFile('qgmapportlet.pt')

    def __init__(self, *args):
        base.Renderer.__init__(self, *args)
        context = aq_inner(self.context)
        portal_state = getMultiAdapter((context, self.request), name=u'plone_portal_state')
        self.portal = portal_state.portal()
        self.gmapEnView = queryMultiAdapter((self.collection, self.request),
                                          name='maps_googlemaps_enabled_view')
        self.gmapView = queryMultiAdapter((self.collection, self.request),
                                          name='maps_googlemaps_view')

    @ram.cache(render_cachekey)
    def render(self):
        return xhtml_compress(self._template())

    @property
    def available(self):
        return bool(self.gmapEnView and self.gmapView and \
                    self.gmapEnView.enabled and \
                    self._data())

    @property
    def collection(self):
        try:
            return self.portal.restrictedTraverse(self.data.collection_path)
        except:
            return None

    @property
    def footer_url(self):
        collection_url = self.collection and self.collection.absolute_url()
        return collection_url and collection_url + '/maps_map' or ''

    @memoize
    def _data(self):
        if hasattr(self.collection, 'queryCatalog'):
            return self.collection.queryCatalog()
        return []
        


class AddForm(base.AddForm):
    form_fields = form.Fields(IQGMapPortlet)
    label = _(u"Add Quintagroup Map Portlet")
    description = _(u"This portlet displays Locations from the collection on the Google Map.")

    def create(self, data):
        portal_state = getMultiAdapter((self.context, self.request),
                                       name=u'plone_portal_state')
        default_path = '/'.join(portal_state.portal().getPhysicalPath()) + '/events'
        return Assignment(collection_path=data.get('collection_path', default_path))

class EditForm(base.EditForm):
    form_fields = form.Fields(IQGMapPortlet)
    label = _(u"Edit Quintagroup Map Portlet")
    description = _(u"This portlet displays Locations from the collection on the Google Map.")
