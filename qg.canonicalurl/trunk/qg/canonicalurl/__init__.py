#
from ZPublisher.HTTPRequest import HTTPRequest
from ZPublisher.BaseRequest import quote

def physicalPathToURL(self, path, relative=0):
    """ Convert a physical path into a URL in the current context """
    url = self['SERVER_URL']
    proto = url.split('://')[0]

    if not type(path) == type(''):
        path = '/'.join(path)

    path_domain_map = getattr(self, 'path_domain_map', ())
    for subpath, domain in path_domain_map:
        if len(path) >= len(subpath) \
           and path.startswith(subpath):
            url = "%s://%s" % (proto, domain)
            path = path[len(subpath):]
            break

    path = self._script + map(quote, self.physicalPathToVirtualPath(path))
    if relative:
        path.insert(0, '')
    else:
        path.insert(0, url)
    return '/'.join(path)

HTTPRequest.physicalPathToURL = physicalPathToURL