import os
from zope.component import adapts
from zope.interface import implements

from interfaces import IPublishFeed

try:
    from Products.qPingTool.interfaces import IPingTool
except ImportError:
    IPingTool = None

class PublishFeed(object):
    """ PublishFeed adapter
    """
    if IPingTool:
        adapts(IPingTool)
    implements(IPublishFeed)

    def __init__(self, context):
        """ init
        """
        self.context = context

    def getPublishFeedUrl(self, url):
        return os.path.join('http://feeds.feedburner.com', url)
