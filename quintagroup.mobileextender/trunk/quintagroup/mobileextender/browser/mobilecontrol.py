#from zope.component import queryMultiAdapter
from zope.interface import implements, alsoProvides, noLongerProvides, Interface
from zope.component import adapts, getMultiAdapter



from zope.formlib import form
from zope.app.form.browser import MultiSelectWidget, TextAreaWidget
try:
    from Products.Five.formlib import formbase
except ImportError:
    from five.formlib import formbase

from Products.Five import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from Products.CMFCore.utils import getToolByName

from quintagroup.mobileextender import mobileextenderMessageFactory as _
from quintagroup.mobileextender.interfaces import IMobile
from interfaces import IMobileConfiglet

def SelectWidgetFactory( field, request ):
    vocabulary = field.value_type.vocabulary
    return MultiSelectWidget( field, vocabulary, request )

def ListTextAreaWidgetFactory( field, request ):
    taw = TextAreaWidget( field, request )
    taw.width = 20
    taw.height = 5
    return taw

class MobileControl(object):
    implements(IMobileConfiglet)
    adapts(Interface)

    ptypes = []
    excludeids = []
    wfstates = []
    excludepaths = []

    def __init__(self, context):
        self.context = context
        self.path = getToolByName(context, 'portal_url').getPortalPath()


class MobileControlView(formbase.FormBase):
    """
    Configlet settings browser view
    """
    template = ViewPageTemplateFile('mobilecontrol.pt')

    form_fields = form.Fields(IMobileConfiglet)

    label = _(u"Define mobile content")
    form_name = _(u"Define mobile content")
    description = _(u"This configlet allows you to define content, " \
                    u"which should be identified as mobile content")

    form_fields["ptypes"].custom_widget = SelectWidgetFactory
    form_fields["wfstates"].custom_widget = SelectWidgetFactory
    form_fields["excludeids"].custom_widget = ListTextAreaWidgetFactory
    form_fields["excludepaths"].custom_widget = ListTextAreaWidgetFactory
    form_fields["path"].render_context = True

    def setUpWidgets(self, ignore_request=False):
        self.adapters = {}
        self.adapters[IMobileConfiglet] = MobileControl(self.context)

        self.widgets = form.setUpWidgets(self.form_fields, self.prefix,
             self.context, self.request, form=self, adapters=self.adapters,
             ignore_request=ignore_request)

    def is_fieldsets(self):
        # We need to be able to test for non-fieldsets in templates.
        return False

    @form.action(_(u"label_mark", default=u"Mark"), name=u'Mark')
    def handle_mark(self, action, data):
        res = self.getFilteredContent(data)
        if res:
            exclids = data.get('excludeids', '')
            if exclids:
                exclids = filter(None, [i.strip() for i in exclids.split('\n')])
                res = filter(lambda b:not b.getId in exclids, res)

            exclpaths = data.get('excludepaths', '')
            if exclpaths:
                exclpaths = filter(None, [i.strip() for i in exclpaths.split('\n')])
                res = filter(lambda b:not [1 for ep in exclpaths if b.getPath().startswith(ep)], res)

            # Mark objects with interface
            marked = 0
            for b in res:
                ob = b.getObject()
                if not IMobile.providedBy(ob):
                    alsoProvides(ob, IMobile)
                    marked += 1

            if marked:
                catalog = getToolByName(self.context, 'portal_catalog')
                catalog.manage_reindexIndex(ids=['object_provides'])

            self.status = "Marked %d objects" % marked
        else:
            self.status = "No objects found for given criterion"

    @form.action(_(u"label_demark", default=u"DeMark"), name=u'DeMark')
    def handle_demark(self, action, data):
        res = self.getFilteredContent(data)
        if res:
            exclids = data.get('excludeids', '')
            if exclids:
                exclids = filter(None, [i.strip() for i in exclids.split('\n')])
                res = filter(lambda b:not b.getId in exclids, res)

            exclpaths = data.get('excludepaths', '')
            if exclpaths:
                exclpaths = filter(None, [i.strip() for i in exclpaths.split('\n')])
                res = filter(lambda b:not [1 for ep in exclpaths if b.getPath().startswith(ep)], res)

            # DeMark objects with interface
            demarked = 0
            for b in res:
                ob = b.getObject()
                if IMobile.providedBy(ob):
                    noLongerProvides(ob, IMobile)
                    demarked += 1

            if demarked:
                catalog = getToolByName(self.context, 'portal_catalog')
                catalog.manage_reindexIndex(ids=['object_provides'])

            self.status = "DeMarked %d objects" % demarked
        else:
            self.status = "No objects found for given criterion"


    def getFilteredContent(self, data):
        purl = getToolByName(self.context, 'portal_url')
        catalog = getToolByName(self.context, 'portal_catalog')

        ptypes = data.get('ptypes',[])
        sorton = data.get('sorton',None)
        wfstates = data.get('wfstates', [])

        query = {'path' : data.get('path', purl.getPortalPath()),}
        if ptypes: query.update({'portal_type':ptypes})
        if wfstates: query.update({'review_state':wfstates})

        return catalog(**query)

    def currentlyMarked(self):
        catalog = getToolByName(self.context, 'portal_catalog')
        return len(catalog(object_provides='quintagroup.mobileextender.interfaces.IMobile'))
