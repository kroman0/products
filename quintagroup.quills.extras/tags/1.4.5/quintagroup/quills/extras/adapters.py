from zope.interface import implements

from quills.core.interfaces import IWeblogEntry
from quills.core.interfaces.enabled import IPossibleWeblogEntry
from quills.app.utilities import getArchivePathFor, getArchivePathFor

from Products.CMFCore.utils import getToolByName

from Products.fatsyndication.adapters.feedentry import DocumentFeedEntry as BaseFeedEntry

class quillsCanonicalPathAdapter(object):
    """Adapts quills entry content to canonical path.
    """
    def __init__(self, context):
        self.context = context

    def canonical_path(self):
        purl = getToolByName(self.context,'portal_url')
        pw = getToolByName(self.context,'portal_workflow')
        relpath = '/' + purl.getRelativeContentURL(self.context)
        if pw.getInfoFor(self.context, 'review_state') == 'published':
            entry = IWeblogEntry(self.context).__of__(self.context.aq_inner.aq_parent)
            weblog_content = entry.getWeblogContentObject()
            if weblog_content is not None:
                weblog_path = '/' + purl.getRelativeContentURL(weblog_content)
                relpath = '%s/%s' % (weblog_path,'/'.join(getArchivePathFor(entry, weblog_content)))
        return relpath


class DocumentFeedEntry(BaseFeedEntry):
    """ Fix effective date.
        BaseFeedEntry overwrite return modification date for 
        getEffectiveDate method. This lead to change entries
        order in result feed.
    """

    def getEffectiveDate(self):
        """See IFeedEntry.
        """
        return self.context.effective()
