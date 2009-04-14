# Script (Python) "listMetaTags"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##parameters=
##title=List Dublin Core for '<meta>' tags
##
from Products.CMFCore.utils import getToolByName
plone_utils = getToolByName(context, 'plone_utils', None)

site_props = getToolByName(context, 'portal_properties').site_properties
exposeDCMetaTags = site_props.exposeDCMetaTags

if plone_utils:
    metaTags = plone_utils.listMetaTags(context)
    metadataList = [
	 ('qSEO_Description', 'description'),
	 ('qSEO_Keywords',    'keywords'),
	 ('qSEO_Robots',      'robots'),
	 ('qSEO_Distribution','distribution'),
    ]

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
        if same_type(value, ()) or same_type(value, []):
            # convert a list to a string
            value = ', '.join(value)
        metaTags[key] = value
    return metaTags.items()