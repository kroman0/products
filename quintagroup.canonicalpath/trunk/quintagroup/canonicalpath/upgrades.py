import logging
from zope.component import queryAdapter
#from zope.component import queryMultiAdapter
from Acquisition import aq_base, aq_inner
#from Products.CMFCore.utils import getToolByName

#from quintagroup.canonicalpath.adapters import PROPERTY_LINK
#from quintagroup.canonicalpath.adapters import PROPERTY_PATH
from quintagroup.canonicalpath.interfaces  import ICanonicalPath
from quintagroup.canonicalpath.interfaces  import ICanonicalLink

class CanonicalConvertor(object):
    """Convert canonical link to canonical path and vice versa."""

    def __init__(self, portal_url, logger_name="quintagroup.canonicalpath"):
        """Create instanse of convertor.
           - *portal_url* (string), add in the front of canonical path property
             value for get canonical link.
           - *logger_name* - name of the logger
        """
        self.initLogger(logger_name)
        self.portal_url = portal_url

    def initLogger(self, lname):
        self.logger = logging.getLogger(lname)

    def convertLinkToPath(self, obj):
        """Convert canonical link to canonical path"""
        return self._convert(obj, ICanonicalLink, ICanonicalPath,
                             self._convertL2P)

    def convertPathToLink(self, obj):
        """Convert canonical path to canonical link"""
        return self._convert(obj, ICanonicalPath, ICanonicalLink,
                             self._convertP2L)

    def _convert(self, obj, src_iface, dst_iface, converter):
        """Convert canonical from source canonical interface
           to destination canonical interface.

           Return True is successfull, False otherwise.
           Log results in logger.
        """
        src = queryAdapter(obj, src_iface)
        dst = queryAdapter(obj, dst_iface)
        # XXX: Check is this correct work XXX
        obj = aq_base(aq_inner(obj))
        # XXX
        if src is not None \
           and dst is not None:
            msg = "Migrate %s into %s for %s object: " \
                   % (src_iface, dst_iface, obj.absolute_url())
            try:
                converter(src, dst)
            except Exception, e:
                lev = logging.ERROR
                msg += "WITH ERROR: %s" % str(e)
            else:
                lev = logging.INFO
                msg += "SUCCESSFUL"

            self.logger.log(lev, msg)
            
            return lev == logging.INFO and True or False
    
    def _convertP2L(self, src, dst):
        """Convert canonical path to canonical link."""
        cpath = src.canonical_path
        cpath = cpath.startswith('/') and cpath or '/' + cpath
        dst.canonical_link = self.portal_url + cpath
        del dst.canonical_path

    def _convertL2P(self, src, dst):
        """Convert canonical link to canonical path."""
        raise NotImplementedError(
            "Convertion from canonical link to canonical path not implemented")


