from zope.interface import alsoProvides

from quills.app.utilities import recurseToInterface
from quills.core.interfaces import IPossibleWeblog
from quills.core.interfaces.enabled import IPossibleWeblogEntry

def set_layout(sc_info):
    obj = sc_info.object
    weblog = recurseToInterface(obj, IPossibleWeblog)
    if weblog:
        # set default layout
        obj.setLayout('weblogentry_view')
        # add providing of IPossibleWeblogEntry interface
        if not IPossibleWeblogEntry.providedBy(obj):
            alsoProvides(obj, IPossibleWeblogEntry)
