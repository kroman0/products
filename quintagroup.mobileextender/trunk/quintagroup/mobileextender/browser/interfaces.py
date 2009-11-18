from zope import interface, schema
from zope.schema import vocabulary

from Products.CMFCore.utils import getToolByName
from quintagroup.mobileextender import mobileextenderMessageFactory as _

try:
    from plone.app import vocabularies
except:
    PT_VOCABULARY = "quintagroup.mobileextender.ptypes"
    WF_VOCABULARY = "quintagroup.mobileextender.wfstates"
else:
    PT_VOCABULARY = "plone.app.vocabularies.PortalTypes"
    WF_VOCABULARY = "plone.app.vocabularies.WorkflowStates"
    


class IMobileConfiglet(interface.Interface):
    """A portlet which can render a classic Plone portlet macro
    """

    path = schema.TextLine(
        title=_(u"label_path", default=u"Path"),
        description=_(u"help_path",
            default=u"The Physical path for objects found. "
            "Leave blank to ignore this criterion."),
        default=u"",
        required=False,
    )
    ptypes = schema.List(
        title=_(u'Portal Types'),
        description=_(u"You may search for and choose portal type(s) "
            "of object(s) to find. Leave blank to ignore this criterion."),
        default=[],
        value_type = schema.Choice( title=u"ptypes", source=PT_VOCABULARY ),
        required=False,
    )
    wfstates = schema.List(
        title=_(u'Workflow States'),
        description=_(u"You may search for and choose workflow review state(s) "
            "of object(s) to find. Leave blank to ignore this criterion."),
        default=[],
        value_type = schema.Choice( title=u"review_states", source=WF_VOCABULARY ),
        required=False,
    )
    excludeids = schema.Text(
        title=_(u'Exclude Ids'),
        description=_(u"List ids, for exclude from mobile content marking. Ids must be separated "
            "by new line. Leave blank to ignore this criterion."),
        default=u"",
        #value_type = schema.TextLine(),
        required=False
    )
    excludepaths = schema.Text(
        title=_(u'Exclude by Physical Paths'),
        description=_(u"All objects, which physical path starts with one of specified one - will "
            "be excluded from mobile content marking. Paths must start with portal id "
            "(as in 'Path' field), and seaprated by new line. Leave blank to ignore this criterion."),
        default=u"",
        required=False
    )
    #sorton = schema.Choice(
        #title=_(u'Sort index'),
        #description=_(u"Check sort index."),
        #vocabulary = "quintagroup.mobileextender.sortindices",
        #default='',
        #required=False
    #)

    #@interface.invariant
    #def checkForACriterion(formdata):
        #if not formdata.ptypes \
           #and not formdata.path:
            #raise interface.Invalid("Path of portal type(s) must be entered")
