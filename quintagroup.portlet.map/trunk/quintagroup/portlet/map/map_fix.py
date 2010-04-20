from zope.component import adapts
from zope.interface import implements
from zope.component import getMultiAdapter

from Acquisition import aq_inner, aq_parent

from Products.ATContentTypes import interface
from Products.Maps.adapters import FolderMap
from Products.Maps.interfaces import IMapView
from Products.Maps.browser.map import BaseMapView

class DefaultPageMapView(BaseMapView):
    implements(IMapView)

    @property
    def enabled(self):
        if self.map is None:
            return False
        elif not self.isDefaultPage():
            return False
        return True

    def isDefaultPage(self):
        context = aq_inner(self.context)
        container = aq_parent(context)
        if not container:
            return False
        view = getMultiAdapter((container, self.request), name='default_page')
        return view.isDefaultPage(context)


class DefaultPageMap(FolderMap):
    adapts(interface.IATDocument)

    def __init__(self, context):
        context = aq_inner(context)
        container = aq_parent(context)
        self.context = container


class FolderMapView(BaseMapView):
    implements(IMapView)

    @property
    def enabled(self):
        if self.map is None:
            return False
        return True
