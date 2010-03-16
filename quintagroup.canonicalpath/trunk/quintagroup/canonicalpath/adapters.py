import re
from zope.interface import implements
from zope.component import adapts
from zope.schema.interfaces import InvalidValue

from OFS.interfaces import ITraversable
from Products.CMFCore.utils import getToolByName

from quintagroup.canonicalpath.interfaces import ICanonicalPath

PROPERTY = "canonical_path"

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

    def _validate(self, value):
        value.strip()
        if not _is_canonical(value):
            raise InvalidValue(value)
        return value
        

    def getCanonicalPath(self):
        """ First of all return value from the PROPERTY,
        if PROPERTY not exist - return default value
        """
        if self.context.hasProperty(PROPERTY):
            return self.context.getProperty(PROPERTY)

        purl = getToolByName(self.context,'portal_url')
        return '/'+'/'.join(purl.getRelativeContentPath(self.context))

    def setCanonicalPath(self, value):
        """ First validate value, than add/updater PROPERTY
        """
        value = self._validate(value)

        if self.context.hasProperty(PROPERTY):
            self.context._updateProperty(PROPERTY, value)
        else:
            self.context._setProperty(PROPERTY, value, type="string")

    canonical_path = property(getCanonicalPath, setCanonicalPath)
