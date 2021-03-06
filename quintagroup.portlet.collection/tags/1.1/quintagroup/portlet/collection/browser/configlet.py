from zope.interface import Interface
from zope.component import adapts
from zope.interface import implements
from zope import schema
from zope.app.form import CustomWidgetFactory
from zope.app.form.browser import ObjectWidget
from zope.app.form.browser import ListSequenceWidget
from zope.formlib import form

from Products.CMFCore.utils import getToolByName
from Products.CMFDefault.formlib.schema import SchemaAdapterBase

from Products.CMFPlone.interfaces import IPloneSiteRoot

from plone.app.controlpanel.form import ControlPanelForm

from quintagroup.portlet.collection import MessageFactory as _
from quintagroup.portlet.collection.utils import getStylesVocabulary


class IValueTitlePair(Interface):
    value = schema.TextLine(title=u"value", required=True)
    title = schema.TextLine(title=u"title", required=False)

class ValueTitlePair(object):
    implements(IValueTitlePair)
    def __init__(self, value='', title=''):
        self.value = value
        self.title = title

class IQCollectionPortletPanelSchema(Interface):

    portlet_dropdown = schema.List(
        title=_(u'Dropdown select'),
        description=_(u"These entries are used for generating dropdown select "
                      "for quintagroup collection portlet. Note: pipe (|) "
                      "symbol is not allowed in the value field."),
        value_type=schema.Object(IValueTitlePair, title=u"entry"),
        required=True
    )

class QCollectionPortletControlPanelAdapter(SchemaAdapterBase):
    adapts(IPloneSiteRoot)
    implements(IQCollectionPortletPanelSchema)

    def __init__(self, context):
        super(QCollectionPortletControlPanelAdapter, self).__init__(context)
        self.context = context
        self.pp = getToolByName(context, 'portal_properties', None)

    def get_portlet_dropdown(self):
        return  [ValueTitlePair(v,t) for (v,t) in getStylesVocabulary(self.context)]

    def set_portlet_dropdown(self, value):
        dropdown_list = []
        for vt in value:
            value = vt.value
            title = vt.title or value
            dropdown_list.append('%s|%s' % (value, title))
        self.setValue(dropdown_list)

    portlet_dropdown = property(get_portlet_dropdown, set_portlet_dropdown)

    def setValue(self, value):
        if self.pp is not None:
            if getattr(self.pp, 'qcollectionportlet_properties', None) is None:
                self.pp.addPropertySheet(
                    'qcollectionportlet_properties',
                    'QCollection portlet properties'
                )
            sheet = getattr(self.pp, 'qcollectionportlet_properties', None)
            if not sheet.hasProperty('portlet_dropdown'):
                sheet.manage_addProperty('portlet_dropdown', value, 'lines')
            else:
                sheet.manage_changeProperties(portlet_dropdown=value)

valuetitle_widget = CustomWidgetFactory(ObjectWidget, ValueTitlePair)
combination_widget = CustomWidgetFactory(ListSequenceWidget,
                                         subwidget=valuetitle_widget)

class QCollectionPortletControlPanel(ControlPanelForm):

    form_fields = form.FormFields(IQCollectionPortletPanelSchema)
    form_fields['portlet_dropdown'].custom_widget = combination_widget

    label = _("QCollection portlet settings")
    description = _("This form is for managing QCollection portlet "
                     "classes available on portlet add/edit form.")
    form_name = _("QCollection portlet settings")
