from zope import schema
from zope.interface import Interface
from zope.interface import Attribute

from zope.app.container.constraints import contains
from zope.app.container.constraints import containers

from quintagroup.gdocs.spreadsheet import spreadsheetMessageFactory as _

class IGSpreadsheet(Interface):
    """Lets you select google spreadsheet and worksheet id"""

    # -*- schema definition goes here -*-

    worksheet_id = Attribute('worksheet_id')
    spreadsheet_id = Attribute('spreadsheet_id')


class IGSpreadsheetDataProvider(Interface):
    """Provide data for pointed google worksheet.
       This data provide data for context, which
       implement IGSpreadsheet interface.
    """

    # -*- schema definition goes here -*-

    def getListFeed(query=None):
        """Return list feed.
           Worksheet get by spreadsheet-id, worksheet-id, got from the context
        """

    def getWorksheetColumnsInfo(maxr='1', minr='1'):
        """Return tuple of tuples with cell-id, cell-title.
        """

