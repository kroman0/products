from zope import schema
from zope.interface import Interface

from zope.app.container.constraints import contains
from zope.app.container.constraints import containers

from Products.DCWorkflow.interfaces import IAfterTransitionEvent

from quintagroup.plonegooglesitemaps import qPloneGoogleSitemapsMessageFactory as _

# -*- extra stuff goes here -*-

class ISitemap(Interface):
    """Search engine Sitemap content type."""

class INewsSitemapProvider(Interface):
    """Marker interface for News sitemap provider."""
