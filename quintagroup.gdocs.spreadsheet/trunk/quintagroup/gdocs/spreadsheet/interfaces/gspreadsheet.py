from zope import schema
from zope.interface import Interface

from zope.app.container.constraints import contains
from zope.app.container.constraints import containers

from quintagroup.gdocs.spreadsheet import spreadsheetMessageFactory as _

class IGSpreadsheet(Interface):
    """Lets you select google spreadsheet and worksheet id"""

    # -*- schema definition goes here -*-
