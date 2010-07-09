"""Definition of the GSpreadsheet content type
"""

from zope.interface import implements, directlyProvides

from Products.Archetypes import atapi
from Products.ATContentTypes.content import base
from Products.ATContentTypes.content import schemata

from quintagroup.gdocs.spreadsheet import spreadsheetMessageFactory as _
from quintagroup.gdocs.spreadsheet.interfaces import IGSpreadsheet
from quintagroup.gdocs.spreadsheet.config import PROJECTNAME

GSpreadsheetSchema = schemata.ATContentTypeSchema.copy() + atapi.Schema((

    atapi.StringField(
        name = 'spreadsheet_title',
        default='',
        searchable = True,
        required = True,
        languageIndependent=True,
        storage=atapi.AnnotationStorage(),
        widget = atapi.StringWidget(
            label = _(
                u'label_spreadsheet_title',
                default=u'Spreadsheet Title'),
            description=_(
                u'help_spreadsheet_title',
                default=u"Please input title Google Spreadsheet."),
            size = 40,
        ),
    ),

    atapi.IntegerField(
        name = 'worksheet_index',
        default='',
        searchable = True,
        required = True,
        languageIndependent=True,
        storage=atapi.AnnotationStorage(),
        widget = atapi.IntegerWidget(
            label = _(
                u'label_worksheet_index',
                default=u'Worksheet Index'),
            description=_(
                u'help_worksheet_index',
                default=u"Please input worksheet index start from zero."),
            size = 3,
        ),
    ),

    # -*- Your Archetypes field definitions here ... -*-

))

# Set storage on fields copied from ATContentTypeSchema, making sure
# they work well with the python bridge properties.

GSpreadsheetSchema['title'].storage = atapi.AnnotationStorage()
GSpreadsheetSchema['description'].storage = atapi.AnnotationStorage()

schemata.finalizeATCTSchema(GSpreadsheetSchema, moveDiscussion=False)

class GSpreadsheet(base.ATCTContent):
    """Lets you select google spreadsheet and worksheet id"""
    implements(IGSpreadsheet)

    meta_type = "GSpreadsheet"
    schema = GSpreadsheetSchema

    title = atapi.ATFieldProperty('title')
    description = atapi.ATFieldProperty('description')
    spreadsheet_title = atapi.ATFieldProperty('spreadsheet_title')
    worksheet_index = atapi.ATFieldProperty('worksheet_index')

    # -*- Your ATSchema to Python Property Bridges Here ... -*-

atapi.registerType(GSpreadsheet, PROJECTNAME)
