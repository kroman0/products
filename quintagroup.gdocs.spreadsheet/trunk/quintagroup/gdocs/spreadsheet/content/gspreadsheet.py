"""Definition of the GSpreadsheet content type
"""

from zope.interface import implements, directlyProvides

from Products.Archetypes import atapi
from Products.ATContentTypes.content import base
from Products.ATContentTypes.content import schemata

from Products.DataGridField import DataGridField, DataGridWidget
from Products.DataGridField.SelectColumn import SelectColumn
from Products.DataGridField.Column import Column

from quintagroup.gdocs.spreadsheet import spreadsheetMessageFactory as _
from quintagroup.gdocs.spreadsheet.interfaces import IGSpreadsheet
from quintagroup.gdocs.spreadsheet.interfaces import IGSpreadsheetDataProvider
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
        name='order_columns',
        searchable = True,
        languageIndependent=True,
        storage=atapi.AnnotationStorage(),
        columns=("column_key", "column_title"),
        widget = DataGridWidget(
            label = _(
                u'label_order_column',
                default=u'Ordering columns'),
            description=_(
                u'help_order_column',
                default=u"Choose keys of columns and enter them titles"),
            columns={
                'column_key' : SelectColumn("Key of column", vocabulary="getKeyColumnVocabulary"),
                'column_title' : Column("Title of column"),
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
    """Lets you select google spreadsheet id, worksheet id,
    choose keys of columns and define them title
    """
    implements(IGSpreadsheet)

    meta_type = "GSpreadsheet"
    schema = GSpreadsheetSchema

    title = atapi.ATFieldProperty('title')
    description = atapi.ATFieldProperty('description')
    spreadsheet_id = atapi.ATFieldProperty('spreadsheet_id')
    worksheet_id = atapi.ATFieldProperty('worksheet_id')
    order_columns = atapi.ATFieldProperty('order_columns')

    # -*- Your ATSchema to Python Property Bridges Here ... -*-

    def getKeyColumnVocabulary(self):
        """ Get a list of keys of columns """
        return atapi.DisplayList(
            ([(t, t) for t in self.all_keys_columns])
        )

    @property
    def all_keys_columns(self):
        if self.spreadsheet_id and self.worksheet_id:
            return IGSpreadsheetDataProvider(self).getWorksheetColumnsInfo()
        return []

atapi.registerType(GSpreadsheet, PROJECTNAME)
