## Controller Script Python "validate_map"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind state=state
##bind subpath=traverse_subpath
##parameters= maplatitude='', maplongitude='', mapzoom='', maptype=''
##title=

from Products.CMFCore.utils import getToolByName
from Products.CMFPlone import PloneMessageFactory as _

plone_utils = getToolByName(context, 'plone_utils')

if (maplatitude and maplongitude):
    try:
        float(maplatitude)
    except:
        state.setError('maplatitude', _('Map Latitude is a decimal number'))
        return state.set(status='failure')
    try:
        float(maplongitude)
    except:
        state.setError('maplongitude', _('Map Longitude is a decimal number'))
        return state.set(status='failure')

    if  not (-90 <= float(maplatitude) <= 90):
        state.setError('maplatitude', _('Map Latitude is not in bounds [-90, 90]'))

    if  not (-180 <= float(maplongitude) <= 180):
        state.setError('maplongitude', _('Map Longitude is not in bounds [-180, 180]'))
elif  not maplatitude and maplongitude:
        state.setError('maplatitude', _('Provide Map Latitude or remove Map Longitude'))
elif  not maplongitude and maplatitude:
        state.setError('maplongitude', _('Provide Map Longitude or remove Map Latitude'))

if state.getErrors():
    plone_utils.addPortalMessage(_(u'Please correct the indicated errors.'))
    return state.set(status='failure')
else:
    return state

