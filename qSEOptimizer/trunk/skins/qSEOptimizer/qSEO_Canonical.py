## Script (Python) "qSEO_Canonical"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##parameters=
##title=Get Canonical URL
##

prop_name = 'qSEO_canonical'

if context.hasProperty(prop_name):
    return context.getProperty(prop_name)
else:
    portal = context.portal_url.getPortalObject()
    if portal.hasProperty('canonical_url'):
        rpath = context.portal_url.getRelativeUrl(context)
        if rpath.endswith('index_html'):
            rpath = rpath[:-11]
        return portal.getProperty('canonical_url') + rpath
    else:
        return context.absolute_url()
