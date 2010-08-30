from zope import schema
from zope.component import getMultiAdapter
from zope.formlib import form
from zope.interface import implements

from plone.app.portlets.portlets import base
from plone.memoize.compress import xhtml_compress
from plone.portlets.interfaces import IPortletDataProvider

from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from Products.CMFPlone import PloneMessageFactory as _
from Products.CMFCore.utils import getToolByName

from Products.PloneFormGen.interfaces import  IPloneFormGenForm
from plone.app.vocabularies.catalog import SearchableTextSourceBinder
from plone.app.form.widgets.uberselectionwidget import UberSelectionWidget

class IPFGPortlet(IPortletDataProvider):

    target_form = schema.Choice(
                    title=_(u"Target form"),
                    description=_(u"Find the form which you want to be",
                                   "displayed in portlet."),
                    required=True,
                    source=SearchableTextSourceBinder(
                        {'object_provides':IPloneFormGenForm.__identifier__},
                        default_query='path:'))

class Assignment(base.Assignment):
    implements(IPFGPortlet)

    def __init__(self, target_form=''):
        self.target_form = target_form

    @property
    def title(self):
        return _(u"PFG Portlet")

class Renderer(base.Renderer):

    _template = ViewPageTemplateFile('pfg.pt')

    def __init__(self, *args):
        base.Renderer.__init__(self, *args)
        self.portal_state = getMultiAdapter((self.context, self.request),
                                       name=u'plone_portal_state')
        self.portal = self.portal_state.portal()


    def render(self):
        return xhtml_compress(self._template())

    def pfg_object(self):
        pfg_path = self.data.target_form
        if pfg_path.startswith('/'):
            pfg_path = pfg_path[1:]

        return self.portal.restrictedTraverse(pfg_path, default=None)

    def pfgTitle(self):
	    return self.pfg_object().Title()

    def available(self):
        """By default, portlets are available
        """
        return self.pfg_object() and True or False

    def render_form(self):
        pfg_path = self.pfg_object().absolute_url(True)
        form_view = self.portal.restrictedTraverse('%s/@@embedded' % pfg_path)
        form_view.prefix = 'pfgportlet'
        return form_view()

class AddForm(base.AddForm):

    form_fields = form.Fields(IPFGPortlet)
    form_fields['target_form'].custom_widget = UberSelectionWidget

    label = _(u"Add PFG Portlet")
    description = _(u"This portlet displays pfg content.")

    def create(self, data):
        return Assignment(target_form=data.get('target_form', ''))

class EditForm(base.EditForm):

    form_fields = form.Fields(IPFGPortlet)
    form_fields['target_form'].custom_widget = UberSelectionWidget

    label = _(u"Edit PFG Portlet")
    description = _(u"This portlet displays pfg content.")