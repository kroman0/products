import re
from zope.component import queryAdapter
from zope.component import queryMultiAdapter
from Products.Five.browser import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile

from quintagroup.gauth.interfaces import IGAuthUtility

REBODY = re.compile("<body\s[^\>]*>(.*)</body>", re.I|re.S)

class TestView( BrowserView ):

    def __init__(self, *args, **kwargs):
        super(TestView, self).__init__(*args, **kwargs)
        self.gauth = queryAdapter(self.context, IGAuthUtility)

    @property
    def sh_title(self):
        return self.request.get("title", "mylan test")

    @property
    def base_download_url(self):
        return "%s/gauth-download?title=%s" % (
            self.context.absolute_url(), self.sh_title)

    def files(self):
        return [{"title": fn, "html": self.getWSheetHTML(f)} \
                for fn, f in self.gauth.downloadSpreadSheetByTitle(self.sh_title)]

    def getWSheetHTML(self, fpath):
        fulltext = self.getHTML(fpath)
        body = REBODY.search(fulltext)
        return body and body.groups()[0] or ""

    def getHTML(self, fpath):
        res = ""
        try:
            f = file(fpath, 'rb')
            res = f.read()
        except:
            pass
        if "f" in locals().keys():
            f.close()
        return res
        
    def download(self):
        index = int(self.request.get("i", -1))
        if index < 0:
            return
        
        files = self.gauth.downloadSpreadSheetByTitle(self.sh_title)
        data = self.getHTML(files[index][1])
        if not data:
            return ""
        response = self.request.RESPONSE
        response.setHeader('Content-Type', "text/html")
        response.setHeader('Content-Length', len(data))
        response.setHeader('Accept-Ranges', 'bytes')

        response.setBase(None)
        return data
