from zope.interface import implements

from quills.core.interfaces import IWeblogEntry
from quills.core.interfaces.enabled import IPossibleWeblogEntry
from quills.app.utilities import getArchivePathFor, getArchivePathFor

from Products.CMFCore.utils import getToolByName

class quillsCanonicalPathAdapter(object):
    """Adapts quills entry content to canonical path.
    """
    def __init__(self, context):
        self.context = context

    def canonical_path(self):
        purl = getToolByName(self.context,'portal_url')
        pw = getToolByName(self.context,'portal_workflow')
        if not pw.getInfoFor(self.context, 'review_state') == 'published':
            return '/' + purl.getRelativeContentURL(self.context)
        entry = IWeblogEntry(self.context).__of__(self.context.aq_inner.aq_parent)
        weblog_content = entry.getWeblogContentObject()
        weblog_path = '/' + purl.getRelativeContentURL(weblog_content)
        return '%s/%s' % (weblog_path,'/'.join(getArchivePathFor(entry, weblog_content)))
