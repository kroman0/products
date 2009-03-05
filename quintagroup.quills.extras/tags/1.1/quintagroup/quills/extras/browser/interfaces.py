from zope.viewlet.interfaces import IViewletManager
from quills.core.interfaces.enabled import IPossibleWeblog

class IActionsBox(IViewletManager):
    """A viewlet manager for collect actions
    """

class IWeblogCategory(IPossibleWeblog):
    """Marker interface for Blog' category folder
    """
