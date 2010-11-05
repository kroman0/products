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
        for b in fdata:
            if (b.getId or b.id) != fargs:
                yield b


class PathBlackoutFilter(object):
    """Filter-out by PATH."""

    implements(IBlackoutFilter)

    def __init__(self, context, request):
        self.context = context
        self.request = request

    def filterOut(self, fdata, fargs):
        """Filter-out fdata list by path in fargs."""
        if not (fargs.startswith("/") or fargs.startswith("./")):
            for b in fdata:
                yield b
            
        if fargs.startswith("/"):
            # absolute path filter
            portal_id = queryMultiAdapter((self.context, self.request),
                         name=u"plone_portal_state").portal().getId()
            test_path = '/' + portal_id + fargs
        else:
            # relative path filter
            container_path = '/'.join(self.context.getPhysicalPath()[:-1])
            test_path = container_path + fargs[1:]

        for b in fdata:
            if b.getPath() != test_path:
                yield b 

