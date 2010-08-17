from zope.component import queryUtility
from zope.component import queryAdapter
from zope.interface import implements, Interface

from Products.Five import BrowserView
from Products.CMFCore.utils import getToolByName

from plone.memoize.view import memoize_contextless

from quintagroup.gauth.interfaces import IGAuthUtility
from gdata.spreadsheet.service import SpreadsheetsService
from gdata.spreadsheet.service import DocumentQuery as shDocumentQuery
from gdata.spreadsheet import SpreadsheetsListFeed

from quintagroup.gdocs.spreadsheet import spreadsheetMessageFactory as _
from quintagroup.gdocs.spreadsheet import logException, logger
from quintagroup.gdocs.spreadsheet.interfaces import IGSpreadsheet
from quintagroup.gdocs.spreadsheet.interfaces import IGSpreadsheetDataProvider


class IWorksheetView(Interface):
    """
    Worksheet view interface
    """

    def renderWorksheet(ssh_id, wsh_idx, startrow_idx):
        """
            ssh_id - Id of the spreadsheet
            wsh_id - Id of the worksheet
            startrow_idx - index of row, from which table should be rendered
        """


class WorksheetView(BrowserView):
    """
    Worksheet browser view
    """
    implements(IWorksheetView)

    def __init__(self, context, request):
        self.context = context
        self.request = request
        self.query = shDocumentQuery()

    @memoize_contextless
    def renderWorksheet(self, ssh_id="", wsh_id='', startrow_idx=0):
        """
        """
        table = ''
        feed = IGSpreadsheetDataProvider(self.context).getListFeed()
        if isinstance(feed, SpreadsheetsListFeed):
            # akc is a list of keys of all columns. The context is GSpreadsheet content type
            akc = self.context.all_keys_columns
            # key_title_columns is list of tuples with two elements (column_key, column_title or column_key)
            key_title_columns = [(e['column_key'], e['column_title'] or e['column_key'])
                for e in self.context.order_columns if e['column_key'] in akc]
            if key_title_columns:
                # Prepare table
                table = "<table id=\"sshwsh\">"
                table += "<tr>"
                table += ''.join(["<th>%s</th>" % el[1] for el in key_title_columns])
                table += "</tr>"
                for i, entry in enumerate(feed.entry):
                    if i >= startrow_idx:
                        td_row = "<tr>"
                        for key in zip(*key_title_columns)[0]:
                            td_row += "<td>%s</td>" \
                                % (not (entry.custom[key].text == 'None') and entry.custom[key].text or '')
                        td_row += "</tr>\n"
                        table += td_row
                table += "</table>"
        return table
