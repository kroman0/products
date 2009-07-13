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
        return portal.getProperty('canonical_url') + context.portal_url.getRelativeUrl(context)
    else:
        return context.absolute_url()
