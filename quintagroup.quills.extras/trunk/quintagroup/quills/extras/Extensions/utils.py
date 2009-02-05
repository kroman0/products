from quills.app.utilities import recurseToInterface
from quills.core.interfaces import IPossibleWeblog

def set_layout(sc_info):
    weblog = recurseToInterface(sc_info.object, IPossibleWeblog)
    if weblog:
        sc_info.object.setLayout('weblogentry_view')

