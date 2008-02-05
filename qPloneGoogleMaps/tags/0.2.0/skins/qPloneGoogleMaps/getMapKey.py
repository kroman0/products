## Script (Python) "getMapKey"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##parameters=
##title=
##

from Products.CMFCore.utils import getToolByName
from Products.qPloneGoogleMaps.config import PROPERTY_SHEET, PROPERTY_FIELD, MAP_API_KEYS

s = MAP_API_KEYS[0]

res = {s[:s.index('|')]:s[s.index('|')+1:],}

portal_props = getToolByName(context, 'portal_properties')

if not hasattr(portal_props, PROPERTY_SHEET):
    return res.values()[0]

property_sheet = getattr(portal_props, PROPERTY_SHEET)

if not hasattr(property_sheet, PROPERTY_FIELD):
    return res.values()[0]

map_api_keys = getattr(property_sheet, PROPERTY_FIELD)

for el in map_api_keys:
    res[el[:el.index('|')]] = el[el.index('|')+1:]

try: return res[context.portal_url()]
except: return res.values()[0]
