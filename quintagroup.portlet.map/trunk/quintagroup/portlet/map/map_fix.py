from zope.interface import implements
from Products.Maps.interfaces import IMapView
from Products.Maps.browser.map import BaseMapView

class FolderMapView(BaseMapView):
    implements(IMapView)

    @property
    def enabled(self):
        if self.map is None:
            return False
        return True
