import Globals
from Products.CMFCore.DirectoryView import registerDirectory
from AccessControl import allow_module
from Products.CMFCore.utils import getToolByName
from util import SortedDict
from os import path
import config


allow_module('Products.qSEOptimizer.util')
qSEO_globals = globals()
registerDirectory('skins', qSEO_globals)


try:
    # for Plone-2.1 and higher
    from Products.CMFPlone.PloneTool import PloneTool
    _present = hasattr(PloneTool, "listMetaTags")
except ImportError:
    _present = False

if _present:
    old_lmt = PloneTool.listMetaTags

    def listMetaTags(self, context):
        site_props = getToolByName(context, 'portal_properties').site_properties
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
                # no data
                continue
            if ( type(value) == tuple ) or ( type(value) == list ):
                # convert a list to a string
                value = ', '.join(value)
            metaTags[key] = value

        return metaTags

    PloneTool.listMetaTags = listMetaTags
