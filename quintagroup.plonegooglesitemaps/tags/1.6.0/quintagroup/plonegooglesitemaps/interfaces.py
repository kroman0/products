from zope import schema
from zope.interface import Interface

from zope.app.container.constraints import contains
from zope.app.container.constraints import containers

from Products.DCWorkflow.interfaces import IAfterTransitionEvent
from plone.browserlayer.interfaces import ILocalBrowserLayerType

from quintagroup.plonegooglesitemaps import qPloneGoogleSitemapsMessageFactory as _

# -*- extra stuff goes here -*-

class ISitemap(Interface):
    """Search engine Sitemap content type."""

class INewsSitemapProvider(Interface):
    """Marker interface for News sitemap provider."""


class IGoogleSitemapsLayer(ILocalBrowserLayerType):
    """Marker interface that defines browser layer for the package."""

class IBlackoutFilter(Interface):
    """Base interface for filter adapter."""

    def filterOut(fdata, fargs):
        """Filter out fdata by passed arguments in kwargs.
            * fdata (list/tuple) - data for filtering
              (list of catalog brains).
            * fargs (string) - is key for filtering.
           Return list/tuple like object without filtered out items.
        """

