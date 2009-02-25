from Products.AutocompleteWidget.AutocompleteWidget import AutocompleteWidget
from Products.Archetypes import PloneMessageFactory as _
from Products.CMFCore.utils import getToolByName
from Products.Archetypes.utils import DisplayList
from Products.ATContentTypes.content import schemata
from Products.ATContentTypes.content.schemata import marshall_register
from Products.ATContentTypes.content.schemata import ATContentTypeSchema
from Products.ATContentTypes.content.base import ATCTMixin
from Products.ATContentTypes.content.document import ATDocument
from Products.ATContentTypes.content.folder import ATFolder, ATBTreeFolder
from Products.ATContentTypes.content.image import ATImage
from Products.ATContentTypes.content.event import ATEvent
from Products.ATContentTypes.content.file import ATFile
from Products.ATContentTypes.content.newsitem import ATNewsItem

new_subject_widget = AutocompleteWidget(
    label=_(u'label_categories', default=u'Categories'),
    description=_(u'help_categories',
                  default=u'Also known as keywords, tags or labels, '
                           'these help you categorize your content.'),
    actb_expand_onfocus=0,
    maxlength='1024'
 	)

def getKeywords(self):
    portal_catalog = getToolByName(self, 'portal_catalog')
    res = portal_catalog.uniqueValuesFor('Subject')
    return DisplayList(zip(res,res))

ATCTMixin.getKeywords = getKeywords 	

for content_type in [ATFolder, ATDocument, ATBTreeFolder, ATImage, ATEvent, ATFile, ATNewsItem]:
    content_type.schema['subject'].widget = new_subject_widget
    content_type.schema['subject'].vocabulary = 'getKeywords'
    