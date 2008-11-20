"""Definition of the Sitemap content type
"""

from zope.interface import implements, directlyProvides

from Products.Archetypes import atapi
from Products.ATContentTypes.content import base
from Products.ATContentTypes.content import schemata
from Products.CMFCore.utils import getToolByName

from Products.qPloneGoogleSitemaps import qPloneGoogleSitemapsMessageFactory as _
from Products.qPloneGoogleSitemaps.interfaces import ISitemap
from Products.qPloneGoogleSitemaps.config import PROJECTNAME

SitemapSchema = schemata.ATContentTypeSchema.copy() + atapi.Schema((

    # -*- Your Archetypes field definitions here ... -*-
    atapi.LinesField(
        name='portalTypes',
        storage = atapi.AnnotationStorage(),
        required=False,
        default=['Document',],
        vocabulary="availablePortalTypes",
        #schemata ='default',
        widget=atapi.MultiSelectionWidget(
            label=_(u"Define the types"),
            description=_(u"Define the types to be included in sitemap."),
        ),
    ),
    atapi.LinesField(
        name='states',
        storage = atapi.AnnotationStorage(),
        required=False,
        default=['published',],
        vocabulary="getWorkflowStates",
        #schemata ='default',
        widget=atapi.MultiSelectionWidget(
            label=_(u"Review status"),
            description=_(u"You may include items in sitemap depend of their " \
                          u"review state."),
        ),
    ),
    atapi.LinesField(
        name='blackout_list',
        storage = atapi.AnnotationStorage(),
        required=False,
        #default='',
        #schemata ='default',
        widget=atapi.LinesWidget(
            label=_(u"Blackout entries"),
            description=_(u"The objects with the given ids will not be " \
                          u"included in sitemap."),
        ),
    ),
    atapi.LinesField(
        name='reg_exp',
        storage = atapi.AnnotationStorage(),
        required=False,
        #default='',
        #schemata ='default',
        widget=atapi.LinesWidget(
            label=_(u"URL processing Regular Expressions"),
            description=_(u"Provide regular expressions (in Perl syntax), " \
                          u"one per line to be applied to URLs before " \
                          u"including them into Sitemap. For instance, " \
                          u"\"s/\/index_html//\" will remove /index_html " \
                          u"from URLs representing default documents."),
        ),
    ),
    atapi.LinesField(
        name='urls',
        storage = atapi.AnnotationStorage(),
        required=False,
        #default='',
        #schemata ='default',
        widget=atapi.LinesWidget(
            label=_(u"Additional URLs"),
            description=_(u"Define additional URLs that are not objects and " \
                          u"that should be included in sitemap."),
        ),
    ),
    atapi.StringField(
        name='verificationFilename',
        storage = atapi.AnnotationStorage(),
        required=False,
        #default='',
        #schemata ='default',
        widget=atapi.StringWidget(
            label=_(u"Provide verification file name"),
            description=_(u"Default verification file name for this sitemaps"),
        ),
    ),

))

# Set storage on fields copied from ATContentTypeSchema, making sure
# they work well with the python bridge properties.

SitemapSchema['title'].storage = atapi.AnnotationStorage()
SitemapSchema['description'].storage = atapi.AnnotationStorage()

schemata.finalizeATCTSchema(SitemapSchema, moveDiscussion=False)
SitemapSchema['relatedItems'].schemata='metadata'
SitemapSchema['relatedItems'].widget.visible = {'edit':'invisible', 'view':'invisible'}


class Sitemap(base.ATCTContent):
    """Search engine Sitemap content type"""
    implements(ISitemap)

    portal_type = "Sitemap"
    schema = SitemapSchema

    #title = atapi.ATFieldProperty('title')
    #description = atapi.ATFieldProperty('description')
    def availablePortalTypes(self):
        pt = getToolByName(self, 'portal_types')
        types = pt.listContentTypes()
        return atapi.DisplayList(zip(types,types))

    def getWorkflowStates(self):
        pw = getToolByName(self,'portal_workflow')
        states = list(set([v for k,v in pw.listWFStatesByTitle()]))
        states.sort()
        return atapi.DisplayList(zip(states, states))


atapi.registerType(Sitemap, PROJECTNAME)
