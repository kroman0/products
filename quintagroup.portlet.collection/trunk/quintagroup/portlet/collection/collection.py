from zope.interface import implements

from plone.portlet.collection import collection as base

from zope import schema
from zope.formlib import form

from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from zope.schema import ValidationError
from plone.app.form.widgets.uberselectionwidget import UberSelectionWidget

from plone.portlet.collection.collection import ICollectionPortlet

from quintagroup.portlet.collection import MessageFactory as _

MIN_BATCH_SIZE, MAX_BATCHSIZE = 1, 30


class NotValidBatchSizeValue(ValidationError):
    """This is not valid batch size value.

    """


def validate_batch_size(value):
    if MIN_BATCH_SIZE <= value <= MAX_BATCHSIZE:
        return True
    raise NotValidBatchSizeValue(value)


class IQCollectionPortlet(ICollectionPortlet):
    """A portlet which based on plone.portlet.collection and
       adds more functionalities.
    """

    item_attributes = schema.List(
        title=_(u"Attributes to display"),
        description=_(u"description_attributes",
                      default=u"Select attributes to show for collection "
                      "item."),
        required=False,
        default=[u"Title", u"Description"],
        value_type=schema.Choice(vocabulary='quintagroup.portlet.collection.\
                vocabularies.PortletAttributesVocabulary'))

    styling = schema.Choice(
        title=_(u"Portlet style"),
        description=_(u"description_styling",
                      default=u"Choose a css style for the porlet."),
        required=False,
        default=u"",
        vocabulary='quintagroup.portlet.collection.\
                vocabularies.PortletCSSVocabulary')

    show_item_more = schema.Bool(
        title=_(u"Show more... link for collection items"),
        description=_(u"If enabled, a more... link will appear in the bottom "
                      "of the each collection item, linking to the "
                      "corresponding item."),
        required=True,
        default=True)

    link_title = schema.Bool(
        title=_(u"Link title"),
        description=_(u"If enabled, title will be shown as link to "
                      "corresponding object."),
        required=True,
        default=True)

    allow_batching = schema.Bool(
        title=_(u"Allow batching"),
        description=_(u"If enabled, items will be split into pages."),
        required=False,
        default=False)

    batch_size = schema.Int(
        title=_(u"Batch size"),
        description=_("Amount of items per page (if not set 3 items will be "
                      "displayed as default)."),
        required=False,
        default=3,
        constraint=validate_batch_size)


class Assignment(base.Assignment):
    """
    Portlet assignment.
    This is what is actually managed through the portlets UI and associated
    with columns.
    """

    implements(IQCollectionPortlet)

    item_attributes = [u"Title", u"Description"]
    styling = u""
    show_item_more = False
    link_title = True

    def __init__(self, header=u"", target_collection=None, limit=None,
                 random=False, show_more=True, show_dates=False,
                 item_attributes=[], styling=u"", show_item_more=False,
                 link_title=True, allow_batching=False, batch_size=3):

        super(Assignment, self).__init__(header=header, random=random,
                                         target_collection=target_collection,
                                         limit=limit, show_more=show_more,
                                         show_dates=show_dates)

        if len(item_attributes) > 0:
            self.item_attributes = item_attributes
        self.styling = styling
        self.show_item_more = show_item_more
        self.link_title = link_title
        self.allow_batching = allow_batching
        self.batch_size = batch_size

    @property
    def title(self):
        """This property is used to give the title of the portlet in the
        "manage portlets" screen. Here, we use the title that the user gave.
        """
        return self.header


class Renderer(base.Renderer):
    """Portlet renderer.

    This is registered in configure.zcml. The referenced page template is
    rendered, and the implicit variable 'view' will refer to an instance
    of this class. Other methods can be added and referenced in the template.
    """

    render = ViewPageTemplateFile('collection.pt')
    navigation = ViewPageTemplateFile('browser/templates/navigation.pt')
    items_listing = ViewPageTemplateFile('browser/templates/items_listing.pt')

    def showProperty(self, name):
        return name in self.data.item_attributes

    def batches(self):
        items = super(Renderer, self).results()
        delta = self.data.batch_size
        return [items[idx:idx + delta] for idx in range(0, len(items), delta)]

    def batch_navigation(self):
        return self.navigation(batches=self.batches())

    def render_items(self):
        if self.data.allow_batching:
            return ''.join([self.items_listing(portlet_items=batch,
                                               page_number=str(index))
                            for index, batch in enumerate(self.batches())])
        return self.items_listing(portlet_items=self.results())


class AddForm(base.AddForm):
    """Portlet add form.

    This is registered in configure.zcml. The form_fields variable tells
    zope.formlib which fields to display. The create() method actually
    constructs the assignment that is being added.
    """

    form_fields = form.Fields(IQCollectionPortlet)
    form_fields['target_collection'].custom_widget = UberSelectionWidget

    label = _(u"Add Collection Portlet")
    description = _(
        u"This portlet display a listing of items from a Collection.")

    def create(self, data):
        return Assignment(**data)


class EditForm(base.EditForm):
    """Portlet edit form.

    This is registered with configure.zcml. The form_fields variable tells
    zope.formlib which fields to display.
    """

    form_fields = form.Fields(IQCollectionPortlet)
    form_fields['target_collection'].custom_widget = UberSelectionWidget

    label = _(u"Edit Collection Portlet")
    description = _(
        u"This portlet display a listing of items from a Collection.")
