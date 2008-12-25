from string import strip
from time import time

from zope.interface import implements
from zope.component import adapts
from plone.memoize import ram

from Products.CMFCore.utils import getToolByName
from Products.CMFPlone.interfaces import IPloneSiteRoot

from interfaces import IDomainsMapExtractor


def cache_key(*args, **kwargs):
     return time() // (60 * 60)


class DomainsMapExtractor(object):
    implements(IDomainsMapExtractor)
    adapts(IPloneSiteRoot)

    def __init__(self, context):
        self.context = context

    def processData(self, value):
        try:
            pd_maps = map(lambda x: map(strip, x.split('::')), value)
        except:
            pd_maps = ()
        else:
            pd_maps.sort(lambda x,y: len(y[0])-len(x[0]))
        return pd_maps


    @ram.cache(cache_key)
    def getDomainsMap(self):
        """ Return sorted by sybpath length tupple
            of (subpath, domain name) tuple.
        """
        portal = getToolByName(self.context, 'portal_url').getPortalObject()
        pd_maps = portal.getProperty('path_domains_map', ())
        return self.processData(pd_maps)

    def setDomainsMap(self, value):
        """ Set tupple of (subpath, domain name) tuples
        """
        if value:
            prepared_value = self.processData(value)
            portal = getToolByName(self.context, 'portal_url').getPortalObject()

            if not portal.getPropertyType('path_domains_map') == 'lines':
                if not portal.hasPropertyType('path_domains_map'):
                    portal.manage_addProperty('path_domains_map', [], 'lines')
                else:
                    raise Exception("Wrong types of 'path_domains_map' " \
                                    "portal property - should be list type")

            update_value = ['::'.join(l) for l in prepared_value]
            portal._updateProperty('path_domains_map', prepared_value)


