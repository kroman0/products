from AccessControl import ClassSecurityInfo

from Products.Archetypes.public import Schema

from Products.qSiloGroup.config import PROJECTNAME
from Products.ATContentTypes.content.base import registerATCT
from Products.ATContentTypes.content.base import ATCTContent
from Products.ATContentTypes.content.schemata import ATContentTypeSchema
from Products.ATContentTypes.content.schemata import finalizeATCTSchema
from Products.ATContentTypes.lib.historyaware import HistoryAwareMixin


SiloSiteMapSchema = ATContentTypeSchema.copy()
SiloSiteMapSchema['id'].default = 'sitemap.htm'
SiloSiteMapSchema['id'].default_method = 'getDefaultId'
SiloSiteMapSchema['title'].default_method = 'getDefaultTitle'
SiloSiteMapSchema['allowDiscussion'].schemata = 'metadata'
SiloSiteMapSchema['relatedItems'].schemata = 'metadata'
SiloSiteMapSchema['description'].schemata = 'metadata'


class SiloSiteMap(ATCTContent, HistoryAwareMixin):
    """ Silo Site Map """

    schema         =  SiloSiteMapSchema 

    content_icon   = 'document_icon.gif'
    meta_type      = 'SiloSiteMap'
    portal_type    = 'SiloSiteMap'
    archetype_name = 'Silo Sitemap'
    default_view   = 'silositemap_view'
    immediate_view = 'silositemap_view'
    suppl_views    = ()
    typeDescription= 'Silo Sitemap'
    typeDescMsgId  = 'description_edit_document'

    security       = ClassSecurityInfo()

    def getDefaultTitle(self):
        """  Buid default title """
        return  self.aq_parent.Title() + ' Sitemap'

    def getDefaultId(self):
        """         """
        return 'sitemap.htm'


registerATCT(SiloSiteMap, PROJECTNAME)