from zope.interface import implements
from quintagroup.plonegooglesitemaps.interfaces import IBlackoutFilterUtility

class IdBlackoutFilterUtility(object):
    """Filter-out by ID utility."""

    implements(IBlackoutFilterUtility)

    def filterOut(self, fdata, fkey, **kwargs):
        """Filter-out fdata list by id in fkey."""
        return [b for b in fdata if (b.getId or b.id) != fkey]


class PathBlackoutFilterUtility(object):
    """Filter-out by PATH utility."""

    implements(IBlackoutFilterUtility)

    def filterOut(self, fdata, fkey, **kwargs):
        """Filter-out fdata list by path in fkey."""
        if fkey.startswith("/"):
            return [b for b in fdata if b.getPath() != fkey]
        elif fkey.startswith("./"):
            # Add relative path filter
            smpath = kwargs.get("sitemap")
            contpath = '/'.join(smpath.getPhysicalPath()[1:-1])
            resfilter = contpath + fkey[1:]
            return [b for b in fdata if b.getPath() != resfilter]
        return fdata
