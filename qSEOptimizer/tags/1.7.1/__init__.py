import Globals
from Products.CMFCore.DirectoryView import registerDirectory
from AccessControl import allow_module
from Products.CMFCore.utils import getToolByName
from util import SortedDict
from os import path

from Products.qSEOptimizer import config

try:
    from Products.qSEOptimizer.interfaces import IKeywords
    zope_interface_available = True
except ImportError:
    zope_interface_available = False

allow_module('Products.qSEOptimizer.util')
qSEO_globals = globals()
registerDirectory('skins', qSEO_globals)

try:
    # for Plone-2.1 and higher
    from Products.CMFPlone.PloneTool import PloneTool
    _present = hasattr(PloneTool, "listMetaTags")
except ImportError:
    _present = False

def propertyItems(context):
    """Return a list of (id,property) tuples.
    """
    return map(lambda i,c=context: (i['id'],getattr(c,i['id'],None)),
                                context._properties)

if _present:
    old_lmt = PloneTool.listMetaTags

    def listMetaTags(self, context):
        portal_props = getToolByName(context, 'portal_properties')
        seo_props = getToolByName(portal_props, 'seo_properties', None)
        if seo_props is None:
            return old_lmt(self, context)

        site_props = getToolByName(portal_props, 'site_properties')
        exposeDCMetaTags = site_props.exposeDCMetaTags

        metaTags = SortedDict()
        metaTags.update(old_lmt(self, context))
        metadataList = [
            ('qSEO_Description', 'description'),
            ('qSEO_Keywords',    'keywords'),
            ('qSEO_Robots',      'robots'),
            ('qSEO_Distribution','distribution')]

        if exposeDCMetaTags:
            metadataList.append(('qSEO_Distribution', 'DC.distribution'))

        for accessor, key in metadataList:
            method = getattr(context, accessor, None)
            if not callable(method):
                # ups
                continue
            # Catch AttributeErrors raised by some AT applications
            try:
                value = method()
            except AttributeError:
                value = None

            if not value:
                continue
            if isinstance(value, (tuple, list)):
                value = ', '.join(value)

            metaTags[key] = value

        # add custom meta tags (added from qseo tab by user) for given context
        property_prefix = 'qSEO_custom_'
        for property, value in propertyItems(context):
            idx = property.find(property_prefix)
            if idx == 0 and len(property) > len(property_prefix):
                metaTags[property[len(property_prefix):]] = value

        # Set the additional matching keywords, if any
        if zope_interface_available:
            adapter = IKeywords(context, None)
            if adapter is not None:
                keywords = adapter.listKeywords()
                if keywords:
                    metaTags['keywords'] = keywords

        return metaTags

    PloneTool.listMetaTags = listMetaTags
