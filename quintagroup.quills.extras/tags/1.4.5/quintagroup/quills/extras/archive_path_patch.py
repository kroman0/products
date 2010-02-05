from quills.app import utilities
from quills.core.interfaces import IWeblogEntry

def getArchivePathForNoArchive(obj, weblog_content):
    """See IWeblogView.
    """
    weblog_path = weblog_content.getPhysicalPath()

    if IWeblogEntry.providedBy(obj):
        obj = obj.context

    obj_path = getattr(obj, 'getPath', None)
    if obj_path and callable(obj_path):
        obj_path = obj.getPath().split('/')
    else:
        obj_path = obj.getPhysicalPath()

    return obj_path[len(weblog_path):]

utilities.getArchivePathFor =  getArchivePathForNoArchive
