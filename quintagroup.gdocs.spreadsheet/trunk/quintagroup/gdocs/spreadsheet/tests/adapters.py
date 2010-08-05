from quintagroup.gdocs.spreadsheet.adapters import GSpreadsheetDataProvider
from quintagroup.gdocs.spreadsheet.tests.service import SpreadsheetsService

def __init__(self, context):
    self.context = context
    self.shcl = SpreadsheetsService('email','password')

GSpreadsheetDataProvider.__init__ = __init__