"""Definition of the GSpreadsheet content type
"""

from zope.interface import implements, directlyProvides

from Products.Archetypes import atapi
from Products.ATContentTypes.content import base
from Products.ATContentTypes.content import schemata

from Products.DataGridField import DataGridField, DataGridWidget
from Products.DataGridField.SelectColumn import SelectColumn

from quintagroup.gdocs.spreadsheet import spreadsheetMessageFactory as _
from quintagroup.gdocs.spreadsheet.interfaces import IGSpreadsheet
from quintagroup.gdocs.spreadsheet.config import PROJECTNAME

GSpreadsheetSchema = schemata.ATContentTypeSchema.copy() + atapi.Schema((

    atapi.StringField(
        name = 'spreadsheet_id',
        default='',
        required = True,
        languageIndependent=True,
        storage=atapi.AnnotationStorage(),
        widget = atapi.StringWidget(
            label = _(
                u'label_spreadsheet_id',
                default=u'Spreadsheet ID'),
            description=_(
                u'help_spreadsheet_id',
                default=u"Please input spreadsheet ID."),
            size = 40,
        ),
    ),

    atapi.StringField(
        name = 'worksheet_id',
        default='',
        required = True,
        languageIndependent=True,
        storage=atapi.AnnotationStorage(),
        widget = atapi.StringWidget(
            label = _(
                u'label_worksheet_id',
                default=u'Worksheet ID'),
            description=_(
                u'help_worksheet_id',
                default=u"Please input worksheet ID."),
            size = 40,
        ),
    ),

    DataGridField(
        name='title_column',
        searchable = True,
        languageIndependent=True,
        storage=atapi.AnnotationStorage(),
        columns=("select_title",),
        widget = DataGridWidget(
            label = _(
                u'label_title_column',
                default=u'Titles of columns'),
            description=_(
                u'help_title_column',
                default=u"Choose titles of columns"),
            columns={
                'select_title' : SelectColumn("Titles of columns", vocabulary="getTitleColumnVocabulary"),
            },
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
    """ Lets you select google spreadsheet worksheet id and choose title of columns """
    implements(IGSpreadsheet)

    meta_type = "GSpreadsheet"
    schema = GSpreadsheetSchema

    order_columns = []
    title = atapi.ATFieldProperty('title')
    description = atapi.ATFieldProperty('description')
    spreadsheet_id = atapi.ATFieldProperty('spreadsheet_id')
    worksheet_id = atapi.ATFieldProperty('worksheet_id')
    title_column = atapi.ATFieldProperty('title_column')

    # -*- Your ATSchema to Python Property Bridges Here ... -*-

    def getTitleColumnVocabulary(self):
        """ Get a list of titles of columns """
        return atapi.DisplayList(
            ([('%s'%i, t) for i,t in enumerate(self.order_columns)])
        )

atapi.registerType(GSpreadsheet, PROJECTNAME)
