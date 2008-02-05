## Script (Python) "getPageTitle"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##parameters= category='portal_tabs'
##title=
##

from Products.CMFCore.utils import getToolByName
from Products.qPloneTabs.config import PROPERTY_SHEET, FIELD_NAME

portal_props = getToolByName(context, 'portal_properties')

default_title = 'Plone \'%s\' Configuration' % category

if not hasattr(portal_props, PROPERTY_SHEET):
    return default_title

sheet = getattr(portal_props, PROPERTY_SHEET)

if not hasattr(sheet, FIELD_NAME):
    return default_title

field = sheet.getProperty(FIELD_NAME)
dict = {}

for line in field:
    cat, title = line.split('|', 2)
    dict[cat] = title

return dict.get(category, None) or default_title
