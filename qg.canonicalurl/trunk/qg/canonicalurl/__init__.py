#
from ZPublisher.HTTPRequest import HTTPRequest

from ZPublisher.BaseRequest import BaseRequest, quote
def physicalPathToURL(self, path, relative=0):
    """ Convert a physical path into a URL in the current context """
    url = self['SERVER_URL']
    if not type(path) == type(''):
        ps = '/'.join(path)
    else:
        ps = path
    if ps.startswith('/www'):
        url = "http://bipp.quintagroup.com"
        if ps.startswith('/www/programs/energy-forum'):
            url = "http://energy.bipp.quintagroup.com"
            path = ps[len('/www/programs/energy-forum'):]
    path = self._script + map(quote, self.physicalPathToVirtualPath(path))
    if relative:
        path.insert(0, '')
    else:
        path.insert(0, url)
    return '/'.join(path)
HTTPRequest.physicalPathToURL = physicalPathToURL