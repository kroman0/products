from zope.interface import implements
from zope.component import adapts, queryUtility

from gdata.spreadsheet.service import SpreadsheetsService
from gdata.spreadsheet.service import DocumentQuery as shDocumentQuery

from quintagroup.gauth.interfaces import IGAuthUtility
from quintagroup.gdocs.spreadsheet import logException, logger
from quintagroup.gdocs.spreadsheet.interfaces import IGSpreadsheet
from quintagroup.gdocs.spreadsheet.interfaces import IGSpreadsheetDataProvider


class GSpreadsheetDataProvider(object):

    adapts(IGSpreadsheet)
    implements(IGSpreadsheetDataProvider)

    def __init__(self, context):
        gauth = queryUtility(IGAuthUtility) or queryUtility(IGAuthUtility, context=context)
        self.context = context
        self.shcl = SpreadsheetsService(gauth.email, gauth.password)
        self.shcl.ProgrammaticLogin()

    def getListFeed(self, query=None):
        """ Get SpreadsheetsListFeed
        """
        return self._safeQuery(self.shcl.GetListFeed,
                              self.context.spreadsheet_id,
                              wksht_id=self.context.worksheet_id,
                              query=query)

    def getWorksheetColumnsInfo(self):
        title_idxs = set()
        query = shDocumentQuery()
        query.max_results = '1'
        feed = self.getListFeed(query=query)
        if len(feed.entry):
            title_idxs.update(feed.entry[0].custom.keys())
        return sorted(title_idxs)

    def _safeQuery(self, meth, *margs, **mkwargs):
        # Make safe method call with logging information about exception
        try:
            return meth(*margs, **mkwargs)
        except Exception:
            logException('%s function call: key=%s, wksht_id=%s' % (
                meth.__name__, self.context.spreadsheet_id,
                self.context.worksheet_id), self.context)
        return None
