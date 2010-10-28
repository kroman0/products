from zope.interface import implements
from zope.component import queryMultiAdapter
from quintagroup.plonegooglesitemaps.interfaces import IBlackoutFilter

class IdBlackoutFilter(object):
    """Filter-out by ID."""

    implements(IBlackoutFilter)

    def __init__(self, context, request):
        self.context = context
        self.request = request

    def filterOut(self, fdata, fargs):
        """Filter-out fdata list by id in fargs."""
        return [b for b in fdata if (b.getId or b.id) != fargs]


class PathBlackoutFilter(object):
    """Filter-out by PATH."""

    implements(IBlackoutFilter)

    def __init__(self, context, request):
        self.context = context
        self.request = request

    def filterOut(self, fdata, fargs):
        """Filter-out fdata list by path in fargs."""
        if fargs.startswith("/"):
            # absolute path filter
            portal = queryMultiAdapter((self.context, self.request),
                         name=u"plone_portal_state").portal()
            return [b for b in fdata if b.getPath() != '/%s%s' % (portal.getId(), fargs)]
        elif fargs.startswith("./"):
            # relative path filter
            contpath = '/'.join(self.context.getPhysicalPath()[:-1])
            return [b for b in fdata if b.getPath() != (contpath + fargs[1:])]
        return fdata
