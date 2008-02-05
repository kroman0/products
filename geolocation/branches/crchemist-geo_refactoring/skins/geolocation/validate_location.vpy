## Controller Script Python "validate_location"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind state=state
##bind subpath=traverse_subpath
##parameters= latitude=None, longitude=None
##title=

from Products.CMFCore.utils import getToolByName
from Products.CMFPlone import PloneMessageFactory as _

plone_utils = getToolByName(context, 'plone_utils')

try:
    float(latitude)
    float(longitude)
except:
    state.setError('latitude', _('For saving select your location point on the map'))
    return state.set(status='failure')

if  not (-90 <= float(latitude) <= 90):
    state.setError('latitude', _('Latitude is not in bounds [-90, 90]'))

if  not (-180 <= float(longitude) <= 180):
    state.setError('longitude', _('Longitude is not in bounds [-180, 180]'))

if state.getErrors():
    return state.set(status='failure')
else:
    return state

