from zope.interface import implements
from Products.CMFCore.utils import getToolByName

from quills.core.interfaces import IWeblogLocator

from quintagroup.portlet.cumulus.interfaces import ITagsRetriever
from quintagroup.portlet.cumulus.catalog import GlobalTags

class QuillsBlogTags(GlobalTags):
    implements(ITagsRetriever)

    def __init__(self, context):
        self.context = context

    def getTags(self, number=None):
        """ Get Quills blog's tags.
        """
        weblog = self.getWeblog()
        if weblog == []:
            return super(QuillsBlogTags, self).getTags(number)

        topics = weblog.getTopics()
        tags = []
        for topic in topics:
            tags.append((topic.getTitle(), len(topic), topic.absolute_url()))

        return tags

    def getWeblog(self):
        locator = IWeblogLocator(self.context)
        weblog = locator.find()
        return weblog
