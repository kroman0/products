import re
from zope.interface import implements
from zope.component import adapts
from zope.schema.interfaces import InvalidValue

from OFS.interfaces import ITraversable
from Products.CMFCore.utils import getToolByName

from quintagroup.canonicalpath.interfaces import ICanonicalPath
from quintagroup.canonicalpath.interfaces import ICanonicalLink

PROPERTY_PATH = "canonical_path"
PROPERTY_LINK = "canonical_link"

_is_canonical = re.compile(
    r"\S*$"               # non space and no new line(should be pickier)
    ).match


class DefaultCanonicalPathAdapter(object):
    """Adapts base content to canonical path.
    """
    adapts(ITraversable)
    implements(ICanonicalPath)

    def __init__(self, context):
        self.context = context
        self.purl = getToolByName(self.context,'portal_url')

    def _validate_path(self, value):
        value.strip()
        if not _is_canonical(value):
            raise InvalidValue(value)
        return value

    def getCanonicalPath(self):
        """ First of all return value from the PROPERTY_PATH,
        if PROPERTY_PATH not exist - return default value
        """
        if self.context.hasProperty(PROPERTY_PATH):
            return self.context.getProperty(PROPERTY_PATH)

        return '/'+'/'.join(self.purl.getRelativeContentPath(self.context))

    def setCanonicalPath(self, value):
        """ First validate value, than add/updater PROPERTY_PATH
        """
        value = self._validate_path(value)

        if self.context.hasProperty(PROPERTY_PATH):
            self.context._updateProperty(PROPERTY_PATH, value)
        else:
            self.context._setProperty(PROPERTY_PATH, value, type="string")

    canonical_path = property(getCanonicalPath, setCanonicalPath)


class DefaultCanonicalLinkAdapter(object):
    """Adapts base content to canonical link.
    """
    adapts(ITraversable)
    implements(ICanonicalLink)

    def __init__(self, context):
        self.context = context
        self.purl = getToolByName(self.context,'portal_url')

    def _validate_link(self, value):
        value.strip()
        if not _is_canonical(value):
            raise InvalidValue(value)
        return value
        
    def getCanonicalLink(self):
        """ First of all return value from the PROPERTY_LINK,
        if PROPERTY_LINK not exist - return default value
        """
        if self.context.hasProperty(PROPERTY_LINK):
            return self.context.getProperty(PROPERTY_LINK)

        return self.context.absolute_url()

    def setCanonicalLink(self, value):
        """ First validate value, than add/updater PROPERTY_LINK
        """
        value = self._validate_link(value)

        if self.context.hasProperty(PROPERTY_LINK):
            self.context._updateProperty(PROPERTY_LINK, value)
        else:
            self.context._setProperty(PROPERTY_LINK, value, type="string")

    canonical_link = property(getCanonicalLink, setCanonicalLink)

