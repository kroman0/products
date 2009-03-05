from DateTime.DateTime import DateTime

from plone.memoize.view import memoize
from Products.Archetypes.ExtensibleMetadata import FLOOR_DATE
from Products.QuillsEnabled.browser.weblogview import WeblogEntryView

class CustomWeblogEntryView(WeblogEntryView):

    @memoize
    def date(self):
        date = self.context.effective()
        if date == FLOOR_DATE:
            date = self.context.modified()
        if date == FLOOR_DATE:
            date = self.context.created()
        return date

    @property
    def month(self):
        return DateTime(self.date()).strftime('%b').capitalize()

    @property
    def day(self):
        return DateTime(self.date()).day()
