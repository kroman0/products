from zope.interface import implements
from plone.memoize.view import memoize_contextless
from plone.app.layout.globals.portal import PortalState
from plone.app.layout.globals.interfaces import IPortalState

from Products.qLocalSkin.interfaces import IShiftPortalUrl

class LocalPortalState(PortalState):
    implements(IPortalState)

    @memoize_contextless
    def portal_url(self):
        """ Return url to container, which provided
	    IShiftPortalUrl marker interface, as portal_url.
	    Use functionality of portal_url's __call__ method
	    patch.
        """
        return self.context.portal_url()
