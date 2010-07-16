from zope.interface import implements
from zope.component import adapts, queryUtility

from gdata.spreadsheet.text_db import Table
from gdata.spreadsheet.text_db import DatabaseClient
from gdata.spreadsheet.text_db import ConvertStringsToColumnHeaders
from gdata.spreadsheet import SpreadsheetsListFeed
from gdata.spreadsheet import SpreadsheetsCellsFeedFromString
from gdata.spreadsheet.service import SpreadsheetsService
from gdata.spreadsheet.service import CellQuery as shCellQuery
from gdata.spreadsheet.service import DocumentQuery as shDocumentQuery

from quintagroup.gauth.interfaces import IGAuthUtility
from quintagroup.gdocs.spreadsheet import logException, logger
from quintagroup.gdocs.spreadsheet.interfaces import IGSpreadsheet
from quintagroup.gdocs.spreadsheet.interfaces import IGSpreadsheetDataProvider


class GSpreadsheetDataProvider(object):

    adapts(IGSpreadsheet)
    implements(IGSpreadsheetDataProvider)

    def __init__(self, context):
        gauth = queryUtility(IGAuthUtility)
        self.context = context
        self.dbcl = DatabaseClient(gauth.email, gauth.password)
        self.shcl = SpreadsheetsService(gauth.email, gauth.password)
        self.shcl.ProgrammaticLogin()

    def getListFeed(self, query=None):
        """ Get SpreadsheetsListFeed
        """
        if query is None:
            query = shDocumentQuery()
        return self._safeQuery(self.shcl.GetListFeed,
                              self.context.spreadsheet_id,
                              wksht_id=self.context.worksheet_id,
                              query=query)

    def getWorksheetColumnsInfo(self, maxr='1', minr='1'):
        first_row_contents = []
        query = shCellQuery()
        query.max_row = maxr
        query.min_row = minr
        feed = self._safeQuery(
            self.dbcl._GetSpreadsheetsClient().GetCellsFeed,
            self.context.spreadsheet_id,
            wksht_id=self.context.worksheet_id,
            query=query)
        for entry in feed.entry:
            first_row_contents.append(entry.content.text)
        # Get the next set of cells if needed.
        next_link = feed.GetNextLink()
        while next_link:
            feed = self._safeQuery(
                self.dbcl._GetSpreadsheetsClient().Get,
                next_link.href, converter=SpreadsheetsCellsFeedFromString)
            for entry in feed.entry:
                first_row_contents.append(entry.content.text)
            next_link = feed.GetNextLink()
        # Convert the contents of the cells to valid headers.
        return ConvertStringsToColumnHeaders(first_row_contents)

    def _safeQuery(self, meth, *margs, **mkwargs):
        # Make safe method call with logging information about exception
        try:
            return meth(*margs, **mkwargs)
        except Exception:
            logException('%s function call: key=%s, wksht_id=%s' % (
                meth.__name__, self.context.spreadsheet_id,
                self.context.worksheet_id), self.context)
        return None
