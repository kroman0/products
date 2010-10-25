from zope.interface import implements
from zope.component import queryMultiAdapter
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
        sm = kwargs.get("sitemap", None)
        req = kwargs.get("request", None)
        if fkey.startswith("/"):
            # absolute path filter
            # portal_state = getMultiAdapter((self.context, self.request), name=u'plone_portal_state')
            portal = queryMultiAdapter((sm, req), name=u"plone_portal_state").portal()
            return [b for b in fdata if b.getPath() != '/%s%s' % (portal.getId(), fkey)]
        elif fkey.startswith("./"):
            # relative path filter
            contpath = '/'.join(sm.getPhysicalPath()[:-1])
            return [b for b in fdata if b.getPath() != (contpath + fkey[1:])]
        return fdata
