from zope.interface import Interface
from zope.interface import implements
from zope.component import getMultiAdapter

from plone.app.portlets.portlets import base
from plone.portlets.interfaces import IPortletDataProvider

from zope import schema
from zope.formlib import form
from plone.memoize.instance import memoize
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from DateTime.DateTime import DateTime

from quintagroup.quills.extras import quintagroupQuillsMessageFactory as _

class IMostCommented(IPortletDataProvider):
    """A portlet

    It inherits from IPortletDataProvider because for this portlet, the
    data that is being rendered and the portlet assignment itself are the
    same.
    """

    # TODO: Add any zope.schema fields here to capture portlet configuration
    # information. Alternatively, if there are no settings, leave this as an
    # empty interface - see also notes around the add form and edit form
    # below.

    blog = schema.TextLine(
        title=_(u"Path to Blog"),
        description=_(u"Physical path to blog, from the plone object, 'blog' for ex."),
        required=True)

    period = schema.Int(
        title=_(u"Actual Period"),
        description=_(u"Actual period in days"),
        default = 30,
        required=True)

    limit = schema.Int(
        title=_(u"Maximum entries"),
        default = 5,
        description=_(u"What's the maximum number of entries to list?"),
        required=True)


class Assignment(base.Assignment):
    """Portlet assignment.

    This is what is actually managed through the portlets UI and associated
    with columns.
    """

    implements(IMostCommented)

    # TODO: Set default values for the configurable parameters here

    # some_field = u""

    # TODO: Add keyword parameters for configurable parameters here
    # def __init__(self, some_field=u"):
    #    self.some_field = some_field

    def __init__(self, blog='/www/blog', period=30, limit=5):
        self.blog = blog
        self.period = period
        self.limit = limit

    @property
    def title(self):
        """This property is used to give the title of the portlet in the
        "manage portlets" screen.
        """
        return "Most Commented"

class Renderer(base.Renderer):
    """Portlet renderer.

    This is registered in configure.zcml. The referenced page template is
    rendered, and the implicit variable 'view' will refer to an instance
    of this class. Other methods can be added and referenced in the template.
    """

    render = ViewPageTemplateFile('mostcommented.pt')

    @property
    def days(self):
        return self.data.period

    @property
    @memoize
    def mostCommented(self):
        catalog = getMultiAdapter((self.context, self.request), name=u'plone_tools').catalog()
        pstate = getMultiAdapter((self.context, self.request), name=u'plone_portal_state')
        portal_id = pstate.portal().getId()
        brains = catalog(path='/%s/%s' % (portal_id, self.data.blog),
                         portal_type='Discussion Item',
                         review_state='published',
                         created={'query':DateTime() - self.data.period, 
                                  'range':'min'}
                        )
        # count comments per blogpost
        comments = {}
        for b in brains:
            bep = '/'.join(b.getPath().split('/')[:-2])
            comments.setdefault(bep, 0)
            comments[bep] = comments[bep] + 1
        # sort blogpost_pathes by comment number
        sorted_dict = list(comments.iteritems())
        sorted_dict.sort(lambda i1, i2: cmp(i1[1], i2[1]))
        sorted_dict.reverse()
        mcpathes = [k for k,v in sorted_dict[:self.data.limit]]
        # get mostcommented blogpost brains
        mostcommented = catalog(path={'query':mcpathes, 'depth':0})
        mcomm_dict = dict([(b.getPath(),b) for b in mostcommented])
        # associate comment number with appropriate blogpost brain
        res = [(n,mcomm_dict[p]) for p,n in sorted_dict if p in mcomm_dict.keys()]
        return res

# NOTE: If this portlet does not have any configurable parameters, you can
# inherit from NullAddForm and remove the form_fields variable.

class AddForm(base.AddForm):
    """Portlet add form.

    This is registered in configure.zcml. The form_fields variable tells
    zope.formlib which fields to display. The create() method actually
    constructs the assignment that is being added.
    """
    form_fields = form.Fields(IMostCommented)

    def create(self, data):
        return Assignment(**data)


# NOTE: IF this portlet does not have any configurable parameters, you can
# remove this class definition and delete the editview attribute from the
# <plone:portlet /> registration in configure.zcml

class EditForm(base.EditForm):
    """Portlet edit form.

    This is registered with configure.zcml. The form_fields variable tells
    zope.formlib which fields to display.
    """
    form_fields = form.Fields(IMostCommented)
