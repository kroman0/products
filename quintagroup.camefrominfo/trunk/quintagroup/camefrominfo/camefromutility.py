from interfaces import ICameFromInfoUtility
from zope.interface import implements

class CameFromInfoUtility(object):
    """
    """
    implements(ICameFromInfoUtility)
    
    def __init__(self):
        pass
    
    def getInfo(self, context):
        """ get info """
        request = context.REQUEST
        ip = request.get('HTTP_X_FORWARDED_FOR', None) or request.getClientAddr()
        ip = ip.split(',')[0]
        browser = request.get('HTTP_USER_AGENT',"")
        came_from = request.get("cmfrm","None")
        return {'ip':ip, 'browser':browser, 'came_from':came_from}
