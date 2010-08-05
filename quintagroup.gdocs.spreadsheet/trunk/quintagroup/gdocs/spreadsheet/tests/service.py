import os
from gdata.spreadsheet import SpreadsheetsListFeed
from atom import CreateClassFromXMLString


class SpreadsheetsService(object):

    def __init__(self, email=None, password=None, source=None,
                 server='spreadsheets.google.com', additional_headers=None,
                 **kwargs):
        pass

    def GetListFeed(self, key, wksht_id='default', row_id=None, query=None,
                    visibility='private', projection='full'):
        f = open(os.path.join(os.path.dirname(__file__), 'test_sp1.xml'))
        xml_string = f.read()
        f.close()
        feed = CreateClassFromXMLString(SpreadsheetsListFeed, xml_string)
        return feed

    #def ProgrammaticLogin(self, captcha_token=None, captcha_response=None):
    #    pass
