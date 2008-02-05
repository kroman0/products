## Script (Python) "searchForGoogleSitemapObjects"
##bind container=
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##parameters=path=None
##
from Products.CMFCore.utils import getToolByName
from Products.qPloneGoogleSitemaps.utils import applyOperations
from string import find

if not path:
    path = '/'.join(context.getPhysicalPath())

catalog = getToolByName(context, 'portal_catalog')
try:
    props = getToolByName(context, 'portal_properties').googlesitemap_properties
    objects = catalog(path = path,
                portal_type = props.portalTypes,
                review_state = props.states,
                )
except AttributeError:
    # We are run without being properly installed, do default processing
    return applyOperations(catalog(path = path,
                                   review_state = ['published'],
                                  ),[])

blackout_list = props.blackout_list
return applyOperations([ob for ob in objects if not(ob.getId in blackout_list)],
                    props.getProperty('reg_exp'))