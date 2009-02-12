from DateTime.DateTime import DateTime

from plone.memoize.view import memoize

from Products.QuillsEnabled.browser.weblogview import WeblogEntryView

class CustomWeblogEntryView(WeblogEntryView):
    #implements(IWeblogEntryView)

    @memoize
    def date(self):
        return self.context.effective()

    @property
    def month(self):
        #import pdb;pdb.set_trace()
        return DateTime(self.date()).strftime('%b').capitalize()

    @property
    def day(self):
        return DateTime(self.date()).day()
