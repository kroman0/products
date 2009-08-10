from Products.Five import BrowserView
from quintagroup.camefrominfo.interfaces import ICameFromInfoUtility
from zope.component import getUtility

class CameFromInfoView(BrowserView):
    """
    """
    def __call__(self):
        """get info"""
        service = getUtility(ICameFromInfoUtility)
        res = service.getInfo(self.context.REQUEST)
        return res
